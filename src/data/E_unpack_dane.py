import pandas as pd
import logging
from pathlib import Path

# ==========================================
# 1. FUNCIÓN DE OBSERVABILIDAD
# ==========================================
def setup_logger(log_filename: str) -> logging.Logger:
    Path("logs").mkdir(parents=True, exist_ok=True)
    log_path = f"logs/{log_filename}"
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger("ingestion_dane.log")

# ==========================================
# 2. LÓGICA DE DESEMPAQUETADO (FLATTENING)
# ==========================================
def unpack_excel_to_csv(excel_path: str, output_folder: str, name_sheet: str):
    """
    Lee un archivo Excel multipestaña y exporta cada hoja 
    como un archivo CSV independiente en la capa raw.
    """
    file_path = Path(excel_path)
    out_dir = Path(output_folder)
    
    if not file_path.exists():
        logger.error(f"No se encontró el archivo original en {file_path}")
        return

    # Creamos el directorio de salida si no existe
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        logger.info(f"Leyendo el archivo Excel: {file_path.name} (Esto puede tomar un minuto...)")
        
        # Al usar sheet_name=None, Pandas lee TODAS las pestañas y devuelve un diccionario
        # donde la llave es el nombre de la hoja y el valor es el DataFrame
        diccionario_hojas = pd.read_excel(file_path, sheet_name=None)
        
        total_hojas = len(diccionario_hojas)
        logger.info(f"Se detectaron {total_hojas} hojas en el libro de Excel.")
        
        # Si se especifica un nombre de hoja, solo procesamos esa hoja
        if name_sheet:
            if name_sheet in diccionario_hojas:
                diccionario_hojas = {name_sheet: diccionario_hojas[name_sheet]}
            else:
                logger.warning(f"La hoja '{name_sheet}' no se encontró en el archivo Excel.")
                return

        # Iteramos sobre el diccionario para guardar cada hoja
        for nombre_hoja, df in diccionario_hojas.items():
            # Construimos el nombre del CSV: "NombreOriginal - NombreHoja.csv"
            # Ejemplo: CUADRO5-NOFETALES-2017-definitivas - 00.csv
            nombre_csv = f"{file_path.stem} - {nombre_hoja}.csv"
            ruta_csv = out_dir / nombre_csv
            
            # Guardamos el CSV respetando la estructura cruda
            df.to_csv(ruta_csv, index=False, encoding='utf-8')
            logger.info(f"Exportado: {nombre_csv}")
            
        logger.info(f"¡Desempaquetado exitoso! Todos los CSVs están en {out_dir}")
        
    except Exception as e:
        logger.critical(f"Fallo durante el desempaquetado del Excel: {str(e)}")

# ==========================================
# 3. EJECUCIÓN MAIN
# ==========================================
if __name__ == '__main__':
    logger.info("--- INICIANDO EXTRACCIÓN Y APLANAMIENTO DANE ---")
    
    # Ruta donde debes colocar tu Excel original del DANE
    ruta_excel_origen = "data/raw/CUADRO5-NOFETALES-2017-definitivas.xls"
    
    # Carpeta donde aterrizarán todos los CSVs sueltos
    carpeta_destino = "data/raw/dane"
    
    unpack_excel_to_csv(ruta_excel_origen, carpeta_destino, name_sheet="00")  # name_sheet=None para procesar todas las hojas
    
    logger.info("--- EXTRACCIÓN DANE FINALIZADA ---")