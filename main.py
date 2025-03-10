import os
import csv
from scripts.extract_text import extract_text
from scripts.scan_cards import detect_credit_cards
from scripts.scan_curp import detect_curp

# Configuración del directorio base
BASE_DIR = "/Users/davidfarfan/Documents/PY/SANTANDER/ipc_scan/test_data"
OUTPUT_FILE = "results/ipc_report.csv"

def scan_files():
    """
    Escanea los archivos en BASE_DIR en busca de datos sensibles y genera un reporte CSV.
    """
    results = []
    doc_number = 0

    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[-1].lower()

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

    # Guardar resultados en CSV
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Número de Documento", "Ruta", "Nombre", "Formato", "Datos IPC Expuestos"])
        writer.writerows(results)

    print(f"Análisis completado. Resultados guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_files()
