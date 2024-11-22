import { Link } from "react-router-dom";
import video from "../assets/video.webm";
import "./index.css";

export default function Landing() {
  return (
    <section className="w-full h-screen relative">
      <div className="absolute w-full h-2/3">
        <video autoPlay muted loop className="w-full h-full object-cover -z-10">
          <source src={video} type="video/mp4" />
        </video>
      </div>
      <div className="w-full h-1/2 flex items-center px-12 z-10 relative">
        <div className="w-1/2 flex flex-col gap-y-4 text-white">
          <h1 className="text-4xl font-bold">Simulador de Sistema Solar</h1>
          <p className="text-lg">
            Explora el sistema solar en un simulador interactivo donde puedes
            observar el movimiento de planetas, lunas, y otros cuerpos celestes
            en tiempo real, experimentando sus órbitas, tamaños y distancias en
            un entorno educativo y visualmente atractivo.
          </p>
        </div>

        <div className="w-1/2 flex justify-center">
          <Link
            to="/preview"
            className="bg-black px-6 py-3 rounded-xl text-white bg-gray-700"
          >
            Ir a la preview
          </Link>
        </div>
      </div>
    </section>
  );
}
