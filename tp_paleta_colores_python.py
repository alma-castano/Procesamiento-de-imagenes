from PIL import Image
from IPython.display import display, HTML
import colorsys


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def get_dominant_colors(image_path, n_colors):
    img = Image.open(image_path)

    # Reducir tamaño para acelerar el análisis
    img = img.resize((150, 150))

    # Reducir la imagen a n colores
    img = img.convert("P", palette=Image.ADAPTIVE, colors=n_colors)
    img = img.convert("RGB")

    # Obtener colores y ordenarlos por frecuencia
    colors = img.getcolors(150 * 150)
    colors.sort(reverse=True)

    # Devolver los colores dominantes
    dominant_colors = [color[1] for color in colors[:n_colors]]

    return dominant_colors


def mostrar_paleta(colors, titulo="Paleta"):
    html = f"""
    <h2>{titulo}</h2>
    <div style="
        display:flex;
        gap:15px;
        margin-bottom:20px;
        flex-wrap:wrap;
    ">
    """

    for color in colors:
        hex_code = rgb_to_hex(color)

        html += f"""
        <div style="text-align:center; font-family:monospace;">
            <div style="
                width:100px;
                height:100px;
                background:{hex_code};
                border:1px solid #000;
            "></div>
            <div>{hex_code}</div>
        </div>
        """

    html += "</div>"

    display(HTML(html))


def cambiar_tono(color, delta):
    r, g, b = [x / 255 for x in color]

    # Convertir RGB a HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Pasar h a grados
    h = h * 360

    # Cambiar el tono
    nuevo_h = (h + delta) % 360

    # Volver a escala 0-1
    nuevo_h = nuevo_h / 360

    # Convertir nuevamente a RGB
    r2, g2, b2 = colorsys.hsv_to_rgb(nuevo_h, s, v)

    return (
        int(r2 * 255),
        int(g2 * 255),
        int(b2 * 255)
    )


def generar_complementaria(colores):
    return [cambiar_tono(color, 180) for color in colores]


def generar_analogos(colores):
    return [cambiar_tono(color, delta)
            for color in colores
            for delta in (-30, 30)]


def generar_triadicos(colores):
    return [cambiar_tono(color, delta)
            for color in colores
            for delta in (120, 240)]


# Programa principal
image_path = input("Ingrese la ruta de la imagen: ")
n_colors = int(input("¿Cuántos colores desea extraer?: "))

# Obtener colores dominantes
colors = get_dominant_colors(image_path, n_colors)

# Mostrar colores dominantes
print("\nColores dominantes:")
for i, color in enumerate(colors, start=1):
    print(f"{i}. {rgb_to_hex(color)}")

mostrar_paleta(colors, "Colores dominantes")

# Generar paletas armónicas
paleta_complementaria = generar_complementaria(colors)
paleta_analogos = generar_analogos(colors)
paleta_triadicos = generar_triadicos(colors)

# Mostrar paletas generadas
mostrar_paleta(paleta_complementaria, "Paleta complementaria")
mostrar_paleta(paleta_analogos, "Paleta análoga")
mostrar_paleta(paleta_triadicos, "Paleta triádica")
print("\nPaleta complementaria:")
for color in paleta_complementaria:
    print(rgb_to_hex(color))

print("\nPaleta análoga:")
for color in paleta_analogos:
    print(rgb_to_hex(color))

print("\nPaleta triádica:")
for color in paleta_triadicos:
    print(rgb_to_hex(color))