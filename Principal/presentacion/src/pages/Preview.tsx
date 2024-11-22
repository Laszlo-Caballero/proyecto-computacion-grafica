import { Canvas } from "@react-three/fiber";
import Planet from "../components/Three/Planet";
import { OrbitControls } from "@react-three/drei";
import { Suspense } from "react";
import Saturno from "../components/Three/Saturno";
// import Saturno from "../components/Three/Saturno";
export default function Preview() {
  return (
    <Suspense fallback={<h1>Cargando</h1>}>
      <Canvas>
        {/* <Saturno /> */}
        <Planet intensity={1} planet="Sol" radiusCenter={0} speed={0} />
        <Planet planet="Mercurio" radiusCenter={4.5} speed={0.1} />
        <Planet planet="Venus" radiusCenter={7.2} speed={0.05} />
        <Planet planet="Tierra" radiusCenter={12} speed={0.01} />
        <Planet planet="Marte" radiusCenter={18} speed={0.009} />
        <Planet planet="Jupiter2" radiusCenter={24} speed={0.003} />
        <Planet planet="Urano" radiusCenter={32} speed={0.0009} />
        <Saturno intensity={0.2} radiusCenter={36} speed={0.0005} />
        <Planet radiusCenter={40} speed={0.0001} planet="Urano" />
        <Planet planet="Neptuno" radiusCenter={46} speed={0.00009} />
        <OrbitControls />
      </Canvas>
    </Suspense>
  );
}
