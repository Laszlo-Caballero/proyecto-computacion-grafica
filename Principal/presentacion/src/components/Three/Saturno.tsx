import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef, useState } from "react";
import { Group, Mesh, MeshStandardMaterial } from "three";

type nodeType = {
  Scene: Group;
  Círculo: Mesh;
  Esfera001: Mesh;
};

type materialsType = {
  MaterialRing: MeshStandardMaterial;
  Material_Planeta: MeshStandardMaterial;
};

interface Props {
  intensity: number;
  speed: number;
  radiusCenter: number;
}

export default function Saturno({ intensity, radiusCenter, speed }: Props) {
  const groupRef = useRef<Group>(null);
  const [angle, setAngle] = useState(0);
  const position = useMemo(() => {
    return [0, 0, 0];
  }, []);

  const { nodes, materials } = useGLTF("saturno.glb");
  useFrame(() => {
    if (groupRef.current) {
      const x = position[0] + radiusCenter * Math.cos(angle);
      const z = position[2] + radiusCenter * Math.sin(angle);
      groupRef.current.position.set(x, position[1], z);
      setAngle((prevAngel) => prevAngel + speed);
    }
  });
  return (
    <>
      <ambientLight intensity={intensity} />

      <group ref={groupRef} dispose={null}>
        <mesh
          castShadow
          receiveShadow
          geometry={(nodes as nodeType).Círculo.geometry}
          material={(materials as materialsType).MaterialRing}
        />
        <mesh
          castShadow
          receiveShadow
          geometry={(nodes as nodeType).Esfera001.geometry}
          material={(materials as materialsType).Material_Planeta}
        />
      </group>
    </>
  );
}

useGLTF.preload("saturno.glb");
