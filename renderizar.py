import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Genera el video de puentes.")
    parser.add_argument("--preview", action="store_true", help="Vista previa 960x540 a 30 fps")
    args = parser.parse_args()
    raiz = Path(__file__).resolve().parent
    ancho, alto = (960, 540) if args.preview else (2560, 1440)
    carpeta = f"{alto}p30"
    subprocess.run([
        sys.executable, "-m", "manim", "--resolution", f"{ancho},{alto}",
        "--fps", "30", "--save_sections", "bridges_lesson.py", "BridgesLesson",
    ], cwd=raiz / "animaciones", check=True)
    generado = raiz / "animaciones" / "media" / "videos" / "bridges_lesson" / carpeta
    destino = raiz / "resultados"
    destino.mkdir(exist_ok=True)
    nombre = "BridgesLesson_preview.mp4" if args.preview else "BridgesLesson_fondo.mp4"
    shutil.copy2(generado / "BridgesLesson.mp4", destino / nombre)
    clips = destino / ("escenas_preview" if args.preview else "escenas")
    clips.mkdir(exist_ok=True)
    for archivo in (generado / "sections").iterdir():
        if archivo.suffix in (".mp4", ".json"):
            shutil.copy2(archivo, clips / archivo.name)
    print(f"Video listo: {destino / nombre}")
    print(f"Clips por escena: {clips}")


if __name__ == "__main__":
    main()
