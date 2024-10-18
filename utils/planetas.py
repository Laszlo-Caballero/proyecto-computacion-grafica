class PlanetaDescripcion:
    def __init__(self, nombre, descripcion, diametro, distanciaSol, canSatelites, tiempoRotacion, tiempoTraslacion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.diametro = diametro  
        self.distanciaSol = distanciaSol  
        self.canSatelites = canSatelites  
        self.tiempoRotacion = tiempoRotacion  
        self.tiempoTraslacion = tiempoTraslacion


planetas = [
    PlanetaDescripcion("Mercurio", "Planeta más cercano al Sol y el más pequeño", "4.879,4 km", "57.910.000 km", "0", "59 días", "88 días"),
    PlanetaDescripcion("Venus", "Segundo objeto más brillante de la noche terrestre", "12.104 km", "108.200.000 km", "0", "243 días", "225 días"),
    PlanetaDescripcion("Tierra", "Único planeta que tiene agua en estado líquido", "12.742 km", "149.600.000 km", "1", "24 horas", "365 días"),
    PlanetaDescripcion("Marte", "El planeta rojo, famoso por su Gran Mancha Roja", "6.779 km", "227.940.000 km", "2", "25 horas", "687 días"),
    PlanetaDescripcion("Júpiter", "El más grande del sistema solar, famoso por su Gran Mancha Roja", "139.820 km", "778.330.000 km", "79", "10 horas", "12 años"),
    PlanetaDescripcion("Saturno", "Rodeado de anillos formados por hielo y rocas", "116.460 km", "1.429.400.000 km", "82", "10 horas", "29 años"),
    PlanetaDescripcion("Urano", "Gigante helado con un eje de rotación inclinado", "50.724 km", "2.870.990.000 km", "27", "18 horas", "84 años"),
    PlanetaDescripcion("Neptuno", "Tiene los vientos más rápidos del sistema solar", "49.244 km", "4.504.300.000 km", "14", "16 horas", "165 años")
]
