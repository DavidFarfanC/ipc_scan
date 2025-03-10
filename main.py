import os
import csv
import platform
from tqdm import tqdm
from scripts.extract_text import extract_text
from scripts.scan_cards import detect_credit_cards
from scripts.scan_curp import detect_curp

# Pedir ruta al usuario y limpiar espacios
BASE_DIR = input("📂 Ingrese la carpeta donde quiere buscar datos sensibles: ").strip()

# Si el usuario ingresa una ruta de Windows en Mac, la corregimos
if platform.system() == "Darwin" and BASE_DIR.startswith("C:\\"):
    print("⚠️ Parece que ingresaste una ruta de Windows en Mac. Conviértela a formato Mac.")
    exit(1)

# Convertir a ruta absoluta
BASE_DIR = os.path.abspath(BASE_DIR)

# Validar si la ruta existe
if not os.path.isdir(BASE_DIR):
    print(f"❌ La ruta ingresada no es válida o no existe: {BASE_DIR}")
    exit(1)

OUTPUT_FILE = os.path.join(BASE_DIR, "results", "ipc_report.csv")

def scan_files():
    """
    Escanea los archivos en la carpeta especificada en busca de datos sensibles y genera un reporte CSV con barra de progreso.
    """
    results = []
    doc_number = 0

    # Obtener la lista total de archivos antes de iniciar el escaneo
    file_list = []
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            file_list.append((root, file))  # Guardamos ruta y nombre

    total_files = len(file_list)  # Número total de archivos a analizar

    # Si no hay archivos, detener ejecución
    if total_files == 0:
        print("⚠️ No se encontraron archivos en la carpeta seleccionada.")
        exit(1)

    print(f"🔍 Iniciando análisis de {total_files} archivos...\n")

    # Usamos tqdm para mostrar el progreso
    for root, file in tqdm(file_list, desc="Escaneando archivos", unit="archivo"):
        file_path = os.path.join(root, file)
        ext = os.path.splitext(file)[-1].lower()

        # Saltar archivos temporales de Microsoft Office (~$archivo.docx)
        if file.startswith("~$"):
            print(f"⚠️ Archivo temporal omitido: {file_path}")
            continue

        # Extraer texto del archivo
        text = extract_text(file_path)
        if not text:
            continue

        # Análisis de datos IPC
        found_cards = detect_credit_cards(text)
        found_curps = detect_curp(text)
        has_sensitive_data = "Sí" if found_cards or found_curps else "No"

        # Agregar resultado a la lista
        doc_number += 1
        results.append([doc_number, root, file, ext, has_sensitive_data])

    # Crear carpeta de resultados si no existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Guardar resultados en CSV
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Número de Documento", "Ruta", "Nombre", "Formato", "Datos IPC Expuestos"])
        writer.writerows(results)

    print(f"\n✅ Análisis completado. Resultados guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_files()
