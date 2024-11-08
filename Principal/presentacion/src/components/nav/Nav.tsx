import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";

export default function Nav() {
  return (
    <nav className="w-full p-6">
      <ul className="flex w-full justify-center items-center gap-48">
        <Link to="/">
          <img src={logo} className="h-28" />
        </Link>
        <Link to="/descargar">Descargar</Link>
        <Link to="/preview">Preview</Link>
      </ul>
    </nav>
  );
}
