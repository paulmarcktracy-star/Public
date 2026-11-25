import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { ThreeCanvas } from "@remotion/three";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { z } from "zod";
import type { Brain3D as Brain3DSchema } from "../schema";
import { COLORS, TYPE } from "../design/tokens";
import { easeStd, lerp, prog, rng } from "../components/anim";

type Props = z.infer<typeof Brain3DSchema> & { durationInFrames: number };
type Region = "prefrontal" | "reward" | "amygdala" | "hippocampus";

// Anatomical anchor points in brain space (+z = front, +y = up). Stylised, not to scale.
const REGION_CENTER: Record<Region, [number, number, number]> = {
  prefrontal: [0, 0.18, 0.78],
  reward: [0, -0.12, 0.22], // ventral striatum / nucleus accumbens area
  amygdala: [0.3, -0.32, 0.12],
  hippocampus: [0.3, -0.26, -0.18],
};

const regionOf = (x: number, y: number, z: number): Region | null => {
  if (z > 0.48 && y > -0.2) return "prefrontal";
  if (Math.abs(x) < 0.3 && y > -0.28 && y < 0.04 && z > 0.05 && z < 0.4) return "reward";
  if (Math.abs(Math.abs(x) - 0.3) < 0.1 && y < -0.24 && y > -0.42 && z > 0.02 && z < 0.24) return "amygdala";
  if (Math.abs(Math.abs(x) - 0.3) < 0.09 && y < -0.16 && y > -0.36 && z > -0.4 && z < 0.0) return "hippocampus";
  return null;
};

type Cloud = { positions: Float32Array; region: (Region | null)[]; base: Float32Array };

const buildBrain = (): Cloud => {
  const r = rng(42);
  const pts: number[] = [];
  const reg: (Region | null)[] = [];
  const base: number[] = [];
  const push = (x: number, y: number, z: number, b: number) => {
    pts.push(x, y, z);
    reg.push(regionOf(x, y, z));
    base.push(b);
  };
  // Cortex: two hemispheres with gyri-like folds on the surface.
  for (let i = 0; i < 7600; i++) {
    const side = i % 2 === 0 ? 1 : -1;
    const u = r() * Math.PI * 2;
    const v = Math.acos(2 * r() - 1);
    let x = Math.sin(v) * Math.cos(u);
    let y = Math.cos(v);
    let z = Math.sin(v) * Math.sin(u);
    if (x * side < -0.35) x *= 0.3; // flatten the medial wall
    const folds = 1 + 0.055 * Math.sin(11 * z + 4 * Math.sin(6 * y)) * Math.cos(9 * y + 3 * x);
    x = side * 0.3 + x * 0.36 * folds;
    y = y * 0.62 * folds;
    z = z * 0.92 * folds;
    if (y < -0.2) y = -0.2 + (y + 0.2) * 0.6; // flatter base
    if (z > 0.3 && y < -0.1) y = -0.1 + (y + 0.1) * 0.5; // frontal lobe sits higher
    push(x, y, z, 0.55 + r() * 0.45);
  }
  // Cerebellum
  for (let i = 0; i < 900; i++) {
    const u = r() * Math.PI * 2;
    const v = Math.acos(2 * r() - 1);
    const stripes = 1 + 0.06 * Math.sin(40 * Math.cos(v));
    push(Math.sin(v) * Math.cos(u) * 0.42 * stripes, -0.36 + Math.cos(v) * 0.16, -0.62 + Math.sin(v) * Math.sin(u) * 0.22, 0.35 + r() * 0.3);
  }
  // Deep structures (dense clusters that light up when highlighted)
  (Object.keys(REGION_CENTER) as Region[]).filter((k) => k !== "prefrontal").forEach((k) => {
    const [cx, cy, cz] = REGION_CENTER[k];
    for (const side of k === "reward" ? [0] : [1, -1]) {
      for (let i = 0; i < 260; i++) {
        const rad = 0.09 * Math.cbrt(r());
        const u = r() * Math.PI * 2;
        const v = Math.acos(2 * r() - 1);
        const sx = k === "reward" ? (r() - 0.5) * 0.36 : side * cx;
        push(sx + rad * Math.sin(v) * Math.cos(u), cy + rad * Math.cos(v), cz + rad * Math.sin(v) * Math.sin(u) * (k === "hippocampus" ? 2.2 : 1), 0.18);
      }
    }
  });
  return { positions: new Float32Array(pts), region: reg, base: new Float32Array(base) };
};

const cameraAt = (camera: Props["camera"], t: number) => {
  // t: 0..1 across the scene
  if (camera === "topDown") {
    return { pos: new THREE.Vector3(Math.sin(t * 0.6) * 0.6, 5.8 - t * 0.6, 1.6), fov: 32 };
  }
  if (camera === "pushIn") {
    const d = lerp(7.6, 5.8, easeStd(t));
    const a = 1.3 - t * 0.5;
    return { pos: new THREE.Vector3(Math.sin(a) * d, 0.9, Math.cos(a) * d), fov: 32 };
  }
  const a = 1.45 - t * 0.75; // from the side (sagittal) toward three-quarter front
  return { pos: new THREE.Vector3(Math.sin(a) * 6.9, 0.9 + Math.sin(t * Math.PI) * 0.3, Math.cos(a) * 6.9), fov: 32 };
};

let SPRITE: THREE.Texture | null = null;
const sprite = () => {
  if (SPRITE) return SPRITE;
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const g = c.getContext("2d")!;
  const grd = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)");
  grd.addColorStop(0.35, "rgba(255,255,255,0.6)");
  grd.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = grd;
  g.fillRect(0, 0, 64, 64);
  SPRITE = new THREE.CanvasTexture(c);
  return SPRITE;
};

const CameraRig: React.FC<{ pos: THREE.Vector3; fov: number }> = ({ pos, fov }) => {
  const cam = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  cam.position.copy(pos);
  cam.fov = fov;
  cam.lookAt(0, -0.05, 0.05);
  cam.updateProjectionMatrix();
  return null;
};

const gold = new THREE.Color(COLORS.goldBright);
const ivory = new THREE.Color("#CFC6B4");
const dimGold = new THREE.Color(COLORS.goldDeep);

export const Brain3D: React.FC<Props> = ({ highlight, labels, camera, pulses, note, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const cloud = useMemo(buildBrain, []);
  const t = frame / Math.max(1, durationInFrames);
  const cam = cameraAt(camera, t);
  const active = highlight.filter((h): h is Region => h !== "none");
  const lightUp = prog(frame, 18, 30); // regions ignite after the scene settles
  const build = prog(frame, 0, 28); // points assemble at scene start

  const colors = useMemo(() => new Float32Array(cloud.positions.length), [cloud]);
  const positions = useMemo(() => new Float32Array(cloud.positions.length), [cloud]);
  const n = cloud.base.length;
  const c = new THREE.Color();
  for (let i = 0; i < n; i++) {
    const reg = cloud.region[i];
    const on = reg !== null && active.includes(reg);
    const shimmer = 0.85 + 0.15 * Math.sin(frame / 7 + i * 0.37);
    if (on) {
      c.copy(dimGold).lerp(gold, lightUp);
      c.multiplyScalar(Math.min(1, (cloud.base[i] + 0.5 * lightUp) * shimmer));
    } else {
      const fade = active.length ? 1 - 0.5 * lightUp : 1; // quiet the rest when something is highlighted
      c.copy(ivory).multiplyScalar(cloud.base[i] * 0.7 * fade * shimmer);
    }
    colors[i * 3] = c.r;
    colors[i * 3 + 1] = c.g;
    colors[i * 3 + 2] = c.b;
    // assemble from a slightly expanded cloud
    const k = lerp(1.35 + (i % 7) * 0.05, 1, build);
    positions[i * 3] = cloud.positions[i * 3] * k;
    positions[i * 3 + 1] = cloud.positions[i * 3 + 1] * k;
    positions[i * 3 + 2] = cloud.positions[i * 3 + 2] * k;
  }

  const halo = useMemo(() => {
    const arr: number[] = [];
    for (let i = 0; i < n; i++) {
      const reg = cloud.region[i];
      if (reg !== null && active.includes(reg) && i % 2 === 0) arr.push(cloud.positions[i * 3], cloud.positions[i * 3 + 1], cloud.positions[i * 3 + 2]);
    }
    return new Float32Array(arr);
  }, [cloud, active.join(",")]);

  // Signal pulses travel along arcs between highlighted regions (or around the cortex).
  const pairs: [Region, Region][] =
    active.length >= 2 ? [[active[0], active[1]], [active[1], active[0]]] : active.length === 1 ? [[active[0], "prefrontal"]] : [];
  const pulseObjs = pulses
    ? pairs.flatMap(([a, b], pi) =>
        [0, 1, 2].map((j) => {
          const p = ((frame + j * 22 + pi * 11) % 66) / 66;
          const A = new THREE.Vector3(...REGION_CENTER[a]);
          const B = new THREE.Vector3(...REGION_CENTER[b]);
          const mid = A.clone().add(B).multiplyScalar(0.5).add(new THREE.Vector3(0, 0.45, 0));
          const curve = new THREE.QuadraticBezierCurve3(A, mid, B);
          return { pos: curve.getPoint(p), alpha: Math.sin(p * Math.PI) * lightUp, key: `${pi}-${j}` };
        }),
      )
    : [];

  // Project region centers to screen for the HTML labels.
  const projCam = new THREE.PerspectiveCamera(cam.fov, width / height, 0.1, 100);
  projCam.position.copy(cam.pos);
  projCam.lookAt(0, -0.05, 0.05);
  projCam.updateMatrixWorld();
  projCam.updateProjectionMatrix();

  return (
    <AbsoluteFill>
      <ThreeCanvas width={width} height={height} camera={{ fov: cam.fov, position: cam.pos.toArray() }}>
        <CameraRig pos={cam.pos} fov={cam.fov} />
        <ambientLight intensity={0.5} />
        <group position={[0, 0.05, 0]} rotation={[0, 0, 0]}>
          <points>
            <bufferGeometry>
              <bufferAttribute attach="attributes-position" args={[positions, 3]} />
              <bufferAttribute attach="attributes-color" args={[colors, 3]} />
            </bufferGeometry>
            <pointsMaterial
              size={0.042}
              map={sprite()}
              vertexColors
              transparent
              depthWrite={false}
              blending={THREE.AdditiveBlending}
              sizeAttenuation
            />
          </points>
          {halo.length ? (
            <points>
              <bufferGeometry>
                <bufferAttribute attach="attributes-position" args={[halo, 3]} />
              </bufferGeometry>
              <pointsMaterial size={0.16} map={sprite()} color={COLORS.gold} transparent opacity={0.16 * lightUp * (0.85 + 0.15 * Math.sin(frame / 9))} depthWrite={false} blending={THREE.AdditiveBlending} sizeAttenuation />
            </points>
          ) : null}
          {pulseObjs.map((p) => (
            <sprite key={p.key} position={p.pos} scale={[0.22, 0.22, 0.22]}>
              <spriteMaterial map={sprite()} color={COLORS.goldBright} transparent opacity={p.alpha} depthWrite={false} blending={THREE.AdditiveBlending} />
            </sprite>
          ))}
        </group>
      </ThreeCanvas>
      {labels
        .map((l) => {
          const v = new THREE.Vector3(...REGION_CENTER[l.region]).add(new THREE.Vector3(0, 0.05, 0)).project(projCam);
          return { l, sx: (v.x * 0.5 + 0.5) * width, sy: (-v.y * 0.5 + 0.5) * height };
        })
        .sort((a, b) => a.sx - b.sx)
        .map(({ l, sx, sy }, i, all) => {
        const appear = prog(frame, 30 + i * 10, 18);
        const leftSide = all.length === 1 ? sx < width / 2 : i === 0;
        const ly = 330 + (i % 2) * 70;
        const lx = leftSide ? 90 : width - 90 - 420;
        const anchorX = leftSide ? lx + 12 : lx + 408;
        return (
          <React.Fragment key={i}>
            <svg width={width} height={height} style={{ position: "absolute", opacity: appear }}>
              <circle cx={sx} cy={sy} r={12} fill="none" stroke={COLORS.goldBright} strokeWidth={3} />
              <circle cx={sx} cy={sy} r={4} fill={COLORS.goldBright} />
              <polyline
                points={`${anchorX},${ly + 62} ${anchorX},${ly + 90} ${sx},${sy - 14}`}
                fill="none"
                stroke={COLORS.gold}
                strokeWidth={2}
                strokeDasharray={1400}
                strokeDashoffset={1400 * (1 - appear)}
              />
            </svg>
            <div
              style={{
                position: "absolute",
                left: lx,
                top: ly,
                width: 420,
                textAlign: leftSide ? "left" : "right",
                fontFamily: TYPE.sans,
                fontWeight: 600,
                fontSize: 40,
                color: COLORS.goldBright,
                opacity: appear,
                translate: `0 ${(1 - appear) * 16}px`,
                textShadow: "0 2px 18px rgba(0,0,0,0.9)",
              }}
            >
              {l.text}
            </div>
          </React.Fragment>
        );
      })}
      {note ? (
        <div style={{ position: "absolute", top: 1440, left: 90, right: 170, textAlign: "center", fontFamily: TYPE.sans, fontSize: 26, color: COLORS.inkMuted, opacity: prog(frame, 20, 14) }}>
          {note}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
