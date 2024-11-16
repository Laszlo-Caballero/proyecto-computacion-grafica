import { Canvas } from "@react-three/fiber";
import Planet from "../components/Three/Planet";
export default function Preview() {
  return (
    <Canvas className="bg-white">
      <Planet />
    </Canvas>
  );
}
