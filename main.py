import os
import csv
import platform
import multiprocessing
from tqdm import tqdm
from scripts.extract_text import extract_text
from scripts.scan_cards import detect_credit_cards
from scripts.scan_curp import detect_curp

# Detectar la cantidad de procesos óptima (CPU - 1, mínimo 1)
NUM_PROCESOS = max(1, multiprocessing.cpu_count() - 1)

def process_file(args):
    """
    Procesa un solo archivo: extrae texto y detecta IPC.
    """
    root, file, doc_number = args
    file_path = os.path.join(root, file)
    ext = os.path.splitext(file)[-1].lower()

    # Saltar archivos temporales de Microsoft Office (~$archivo.docx)
    if file.startswith("~$"):
        return None

    # Extraer texto del archivo
    text = extract_text(file_path)
    if not text:
        return None

    # Análisis de datos IPC
    found_cards = detect_credit_cards(text)
    found_curps = detect_curp(text)
    has_sensitive_data = "Sí" if found_cards or found_curps else "No"

    return [doc_number, root, file, ext, has_sensitive_data]

def scan_files(base_dir):
    """
    Escanea los archivos en la carpeta especificada en busca de datos sensibles y genera un reporte CSV con multiprocessing.
    """
    results = []
    file_list = []

    # Obtener la lista total de archivos antes de iniciar el escaneo
    doc_number = 0
    for root, _, files in os.walk(base_dir):
        for file in files:
            doc_number += 1
            file_list.append((root, file, doc_number))

    total_files = len(file_list)

    # Si no hay archivos, detener ejecución
    if total_files == 0:
        print("⚠️ No se encontraron archivos en la carpeta seleccionada.")
        exit(1)

    print(f"🔍 Iniciando análisis de {total_files} archivos usando {NUM_PROCESOS} procesos...\n")

    # Usamos multiprocessing para procesar archivos en paralelo
    with multiprocessing.Pool(NUM_PROCESOS) as pool:
        for result in tqdm(pool.imap_unordered(process_file, file_list), total=total_files, desc="Escaneando archivos", unit="archivo"):
            if result:
                results.append(result)

    # Crear carpeta de resultados si no existe
    output_file = os.path.join(base_dir, "results", "ipc_report.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Guardar resultados en CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Número de Documento", "Ruta", "Nombre", "Formato", "Datos IPC Expuestos"])
        writer.writerows(results)

    print(f"\n✅ Análisis completado. Resultados guardados en: {output_file}")

if __name__ == "__main__":
    # Pedir ruta al usuario solo una vez
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

    # Ejecutar escaneo
    scan_files(BASE_DIR)
