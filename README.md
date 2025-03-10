
# 📂 IPC Scan - Detección de Datos Sensibles en Archivos

**IPC Scan** es un sistema de escaneo para identificar datos sensibles en archivos dentro de un directorio específico. 
Se centra en la detección de **números de tarjetas de crédito/débito** y **CURP** utilizando expresiones regulares 
y validación con el **Algoritmo de Luhn**.

---

## 🚀 Características
✅ **Escaneo automático** en archivos **PDF, DOCX, XLSX, TXT y CSV**.  
✅ **Detección de información sensible** (Números de tarjeta, CURP).  
✅ **Validación de tarjetas con el Algoritmo de Luhn**.  
✅ **Generación de un reporte CSV** con los resultados.  
✅ **Soporte para Windows y Mac/Linux**.  
✅ **Ignora archivos temporales de Microsoft Office (`~$archivo.docx`)**.  
✅ **Interfaz en la terminal con barra de progreso (`tqdm`)**.  

---

## 📁 Estructura del Proyecto

```plaintext
ipc_scan/
│── scripts/
│   │── scan_cards.py        # Detección de números de tarjeta
│   │── scan_curp.py         # Detección de CURP
│   │── extract_text.py      # Extracción de texto desde archivos (PDF, DOCX, XLSX, TXT, CSV)
│   │── utils.py             # Funciones auxiliares (como validaciones)
│── main.py                  # Script principal que ejecuta todo
│── results/
│   │── ipc_report.csv        # Archivo CSV con los resultados
│── config.py                 # Configuración de rutas y parámetros
│── README.md                 # Documentación del proyecto
```

---

## 🛠️ Instalación y Uso

### 1️⃣ **Instalar dependencias**
Asegúrate de tener **Python 3.8+** instalado y ejecuta:
```bash
pip install -r requirements.txt
```

### 2️⃣ **Ejecutar el escaneo**
Corre el script principal:
```bash
python3 main.py
```
📌 **Cuando el script te pida la carpeta a escanear, ingrésala en formato correcto:**
- **Mac/Linux:** `/Users/usuario/Downloads/`
- **Windows:** `C:\Users\usuario\Documents\`

### 3️⃣ **Revisar los resultados**
Una vez finalizado el escaneo, el reporte se guardará en:
```
results/ipc_report.csv
```

---

## 🏗️ Cómo Funciona

1. **Escanea todos los archivos** en la carpeta seleccionada y sus subcarpetas.
2. **Extrae texto** de cada archivo usando librerías como `pdfminer.six`, `python-docx`, y `pandas`.
3. **Aplica expresiones regulares** para encontrar CURPs y números de tarjeta.
4. **Valida los números de tarjeta** con el **Algoritmo de Luhn** para filtrar falsos positivos.
5. **Muestra una barra de progreso (`tqdm`)** y **omite archivos temporales** (`~$archivo.docx`).
6. **Guarda los resultados en un CSV** con los archivos analizados.

---

## ⚡ Ejemplo de Salida en `ipc_report.csv`
| Número de Documento | Ruta | Nombre | Formato | Datos IPC Expuestos |
|---------------------|------|--------|---------|----------------------|
| 1 | /Users/david/Downloads/ | test1.pdf | PDF | Sí |
| 2 | /Users/david/Downloads/ | test2.docx | DOCX | No |
| 3 | /Users/david/Downloads/ | test3.xlsx | XLSX | Sí |

---

## 📌 Notas Importantes
- El script **ignora archivos temporales de Word** (`~$archivo.docx`).
- Si ingresas una ruta incorrecta en Mac con formato de Windows (`C:\`), el script lo detecta.
- Para escanear directorios grandes, asegúrate de tener suficiente RAM disponible.

---

## 👨‍💻 Autor
**David Farfán**  
📍 Proyecto desarrollado para detección de IPC en archivos.  

🚀 ¡Contribuciones y mejoras son bienvenidas!
```

---
