"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

const PARTICLE_COUNT = 260;
const CONNECTION_DISTANCE = 2.6;
const FIELD_RADIUS = 9;

function generateField() {
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  for (let i = 0; i < PARTICLE_COUNT; i += 1) {
    const radius = FIELD_RADIUS * Math.cbrt(Math.random());
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta) * 0.55;
    positions[i * 3 + 2] = radius * Math.cos(phi) * 0.6 - 2;
  }
  return positions;
}

function buildConnections(positions: Float32Array) {
  const lineVertices: number[] = [];
  for (let i = 0; i < PARTICLE_COUNT; i += 1) {
    const ax = positions[i * 3];
    const ay = positions[i * 3 + 1];
    const az = positions[i * 3 + 2];
    for (let j = i + 1; j < PARTICLE_COUNT; j += 1) {
      const bx = positions[j * 3];
      const by = positions[j * 3 + 1];
      const bz = positions[j * 3 + 2];
      const dist = Math.hypot(ax - bx, ay - by, az - bz);
      if (dist < CONNECTION_DISTANCE) {
        lineVertices.push(ax, ay, az, bx, by, bz);
      }
    }
  }
  return new Float32Array(lineVertices);
}

function NeuralField() {
  const groupRef = useRef<THREE.Group>(null);
  const pointer = useThree((state) => state.pointer);
  const targetRotation = useRef({ x: 0, y: 0 });

  const positions = useMemo(() => generateField(), []);
  const linePositions = useMemo(() => buildConnections(positions), [positions]);

  useFrame((state, delta) => {
    const group = groupRef.current;
    if (!group) return;

    targetRotation.current.y = pointer.x * 0.35;
    targetRotation.current.x = -pointer.y * 0.2;

    group.rotation.y +=
      (targetRotation.current.y - group.rotation.y) * 0.6 * delta * 4;
    group.rotation.x +=
      (targetRotation.current.x - group.rotation.x) * 0.6 * delta * 4;

    group.rotation.y += delta * 0.02;
    group.position.y = Math.sin(state.clock.elapsedTime * 0.15) * 0.15;
  });

  return (
    <group ref={groupRef}>
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[positions, 3]}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.045}
          color="#2dd4e8"
          transparent
          opacity={0.85}
          sizeAttenuation
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </points>
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[linePositions, 3]}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="#3b82f6"
          transparent
          opacity={0.16}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
    </group>
  );
}

function useCanRenderWebgl() {
  const [canRender, setCanRender] = useState(false);

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    const isSmallViewport = window.innerWidth < 640;
    const hasLimitedCores =
      typeof navigator !== "undefined" &&
      typeof navigator.hardwareConcurrency === "number" &&
      navigator.hardwareConcurrency > 0 &&
      navigator.hardwareConcurrency <= 4;

    let hasWebgl = false;
    try {
      const testCanvas = document.createElement("canvas");
      hasWebgl = Boolean(
        testCanvas.getContext("webgl") || testCanvas.getContext("experimental-webgl")
      );
    } catch {
      hasWebgl = false;
    }

    const frame = requestAnimationFrame(() => {
      setCanRender(
        hasWebgl && !prefersReducedMotion && !(isSmallViewport && hasLimitedCores)
      );
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  return canRender;
}

function StaticGlowFallback() {
  return (
    <div
      aria-hidden="true"
      className="absolute inset-0"
      style={{
        background:
          "radial-gradient(60% 50% at 50% 35%, rgba(45,212,232,0.16) 0%, rgba(59,130,246,0.10) 40%, rgba(10,14,23,0) 75%)",
      }}
    />
  );
}

export default function HeroBackground3D() {
  const canRender = useCanRenderWebgl();

  return (
    <div className="absolute inset-0 overflow-hidden">
      <StaticGlowFallback />
      {canRender && (
        <Canvas
          className="!absolute !inset-0"
          camera={{ position: [0, 0, 6], fov: 55 }}
          dpr={[1, 1.5]}
          gl={{ antialias: true, alpha: true }}
        >
          <NeuralField />
        </Canvas>
      )}
    </div>
  );
}
