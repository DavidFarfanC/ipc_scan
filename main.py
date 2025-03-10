import os
import csv
import platform
import multiprocessing
from tqdm import tqdm
from scripts.extract_text import extract_text
from scripts.scan_cards import detect_credit_cards
from scripts.scan_curp import detect_curp

# 🔍 Lista de palabras clave para filtrado
KEYWORDS = [
    "#DE REGISTRO CTA", "# DE REGISTRO RECHAZADO", "ACEPTADA", "ADF", "afiliacion", "BANCO", "BUC",
    "CANAL", "Card", "CC", "CLAVE OFICIAL", "CLIENTE", "COBRADA", "Código de cliente",
    "Comercio Nombre", "CON_DISPERSIÖN", "CONTAR POR SUCURSAL", "Contrato", "CREDITO",
    "CUENTA", "CVV", "DESC_MOTIVO_RECHAZO", "DIAS DE ATRASO", "Divisa", "DOCUMENTADA",
    "EFECTIVA", "EFEC", "EJECUTIVO", "ESTATUS", "ESTATUS EXP", "ESTATUS REP", "EXPEDIENTE",
    "FECHA", "FECHA DE EMISIÓN", "FECHA DE ENVIO", "FECHA_1RA_DISP", "fecha_de_transaccion1",
    "FECHA_SOLICITUD", "FOLIO_CANCELACION", "FORMA DE PAGO", "Grupo", "ID_CUENTA_ORDENANTE",
    "ID_EJECUTIVO", "ID_SUCURSAL", "ID_ZONA", "importe", "INTERVENTOR", "mcc", "medio_de_acceso",
    "MODELO", "modo_de_entrada", "MOTIVO DE RECHAZO", "No. DE TARJETA", "Nombre", "NOMBRE EJECUTIVO",
    "NOMBRE SUC", "NUM DE CUENTA", "Number", "Numero", "numero_autorizacion", "numero_de_tarjeta",
    "numero_tarjeta", "POLIZA", "POLIZA X EJECUTIVO", "PRIMA", "RAMO", "Razón social",
    "REGION CON CENTRO PYME", "SUC", "SUCURSAL", "Tarjeta", "TDC", "terminal_del_commercio",
    "Tipo", "Tipos de cuenta", "ZONA", "VALIDACION ADF", "SEG REGIONAL", "American Express",
    "MasterCard", "Visa", "Discover", "PIN", "PAN", "CVC", "CAV", "CSC", "CID", "CAV2", "CVC2", "CVV2"
]

def get_matching_keywords(text):
    """
    Encuentra las palabras clave que están en el texto.
    """
    found_keywords = [kw for kw in KEYWORDS if kw.lower() in text.lower()]
    return found_keywords if len(found_keywords) >= 2 else None

def process_file(args):
    """
    Procesa un solo archivo: extrae texto, filtra por palabras clave y detecta IPC.
    """
    root, file, doc_number = args
    file_path = os.path.join(root, file)
    ext = os.path.splitext(file)[-1].lower()

    # Saltar archivos temporales de Microsoft Office (~$archivo.docx)
    if file.startswith("~$"):
        return None

    # Extraer texto del archivo solo si es un tipo soportado
    text = extract_text(file_path)
    if text is None:
        return None

    # 🚀 **Filtro: solo analizar archivos con al menos 2 palabras clave**
    matched_keywords = get_matching_keywords(text)
    if not matched_keywords:
        return None  # Ignorar archivo

    # Análisis de datos IPC
    found_cards = detect_credit_cards(text)
    found_curps = detect_curp(text)

    # Determinar el tipo de dato encontrado y el número detectado
    sensitive_data_type = []
    sensitive_data_numbers = []

    if found_cards:
        sensitive_data_type.append("Tarjeta")
        sensitive_data_numbers.extend(found_cards)
    
    if found_curps:
        sensitive_data_type.append("CURP")
        sensitive_data_numbers.extend(found_curps)

    # 🚀 **Filtro: Solo incluir archivos que tengan al menos 2 datos sensibles**
    if len(sensitive_data_numbers) < 2:
        return None  # Ignorar archivo si tiene menos de 2 datos expuestos

    return [
        doc_number, root, file, ext, "Sí",  # Solo llega aquí si cumple la condición
        ", ".join(matched_keywords),  # Palabras clave encontradas
        ", ".join(sensitive_data_type),  # Tipo de dato (Tarjeta o CURP)
        ", ".join(sensitive_data_numbers)  # Números detectados
    ]

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
        writer.writerow([
            "Número de Documento", "Ruta", "Nombre", "Formato", "Datos IPC Expuestos",
            "Palabras Clave Encontradas", "Tipo de Dato Sensible", "Número Detectado"
        ])
        writer.writerows(results)

    print(f"\n✅ Análisis completado. Resultados guardados en: {output_file}")

# 🔹 Bloque principal
if __name__ == "__main__":
    multiprocessing.freeze_support()  # ✅ NECESARIO para PyInstaller en Windows y Mac

    # Configurar multiprocessing en Windows
    if platform.system() == "Windows":
        multiprocessing.set_start_method("spawn", force=True)  # ✅ Obligatorio en Windows con PyInstaller

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

    # Detectar la cantidad de procesos óptima (CPU - 1, mínimo 1)
    NUM_PROCESOS = max(1, multiprocessing.cpu_count() - 1)

    # Ejecutar escaneo
    scan_files(BASE_DIR)
