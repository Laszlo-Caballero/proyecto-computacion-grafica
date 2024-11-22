import { useTexture } from "@react-three/drei";
import { useFrame, useLoader } from "@react-three/fiber";
import { useLayoutEffect, useMemo, useRef, useState } from "react";
import { Group, Mesh } from "three";
import { MTLLoader, OBJLoader } from "three/examples/jsm/Addons.js";

interface Props {
  intensity?: number;
  speed: number;
  radiusCenter: number;
}

export default function Tierra({ intensity, radiusCenter, speed }: Props) {
  const planetRef = useRef<Group>(null);
  const [angle, setAngle] = useState(0);

  const material = useLoader(MTLLoader, `Tierra.mtl`);

  const position = useMemo(() => {
    return [0, 0, 0];
  }, []);

  const obj = useLoader(OBJLoader, `Tierra.obj`, (loader) => {
    material.preload();
    loader.setMaterials(material);
  });

  const coloMap = useTexture(`Tierra.jpg`);

  useLayoutEffect(() => {
    obj.traverse((child) => {
      if ((child as Mesh).isMesh) {
        (child as Mesh).material.map = coloMap;
      }
    });
  }, [obj, coloMap]);

  useFrame(() => {
    if (planetRef.current) {
      const x = position[0] + radiusCenter * Math.cos(angle);
      const z = position[2] + radiusCenter * Math.sin(angle);
      planetRef.current.position.set(x, position[1], z);
      setAngle((prevAngel) => prevAngel + speed);
    }
  });

  return (
    <group ref={planetRef}>
      <ambientLight intensity={intensity ?? 0.2} />
      <directionalLight />
      <primitive object={obj} />
    </group>
  );
}
