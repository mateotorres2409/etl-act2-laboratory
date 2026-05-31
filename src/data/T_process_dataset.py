import pandas as pd
import unicodedata
import re
import logging
from pathlib import Path

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

logger = setup_logger("processing.log")

def normalizar_texto(valor):
    """Función de tu compañero para limpiar textos y tildes"""
    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).lower()

def transform_and_merge():
    try:
        logger.info("1. Leyendo datos Globales y Taxonomía OMS...")
        df_raw = pd.read_csv("data/raw/causeofdeath.csv", sep=';', decimal=',')
        df_ext = pd.read_csv("data/external/who_disease_taxonomy.csv")
        df_map_dane = pd.read_csv("data/external/dane_mapping.csv")
        
        # --- PROCESAMIENTO DANE ---
        logger.info("2. Procesando datos de mortalidad del DANE (Colombia)...")
        # Leemos el archivo 00 ignorando el encabezado del reporte
        df_dane = pd.read_csv("data/raw/dane/CUADRO5-NOFETALES-2017-definitivas - 00.csv", skiprows=10)
        df_dane = df_dane.iloc[:, :2] # Solo nos interesa la causa y el total
        
        # CORRECCIÓN: Usamos 'cause_dane' idéntico al mapping
        df_dane.columns = ["cause_dane", "total_muertes_dane"] 
        
        # Limpieza de comas/puntos en los miles y conversión a numérico
        df_dane['total_muertes_dane'] = df_dane['total_muertes_dane'].astype(str).str.replace('.', '', regex=False)
        df_dane['total_muertes_dane'] = pd.to_numeric(df_dane['total_muertes_dane'], errors='coerce')
        
        # Obtenemos el total nacional de manera segura
        filtro_total = df_dane['cause_dane'].astype(str).str.contains('TOTAL NACIONAL', case=False, na=False)
        total_nacional = df_dane[filtro_total]['total_muertes_dane'].values[0]
        
        df_dane = df_dane.dropna(subset=['cause_dane'])
        df_dane['pct_deaths_colombia'] = df_dane['total_muertes_dane'] / total_nacional
        # ------------------------------------------------------

        # --- PROCESAMIENTO GLOBAL ---
        logger.info("3. Aplicando Pivot a causas globales...")
        df_pivot = df_raw.pivot_table(index='Cause of death or injury', columns='Measure', values='Value', aggfunc='first').reset_index()
        df_pivot.rename(columns={
            'Percent of total deaths 2017': 'pct_deaths_global',
            'Deaths annual % change 2010-2017': 'annual_change_global',
            'Cause of death or injury': 'cause'
        }, inplace=True)
        df_pivot.columns.name = None
        
        # --- EL GRAN CRUCE (JOIN MÚLTIPLE) ---
        logger.info("4. Unificando: Global + OMS + Mapeo DANE + Datos Colombia...")
        df_final = pd.merge(df_pivot, df_ext, on='cause', how='left')
        
        # Unimos con el mapeo para traer la llave 'cause_dane' al dataset global
        df_final = pd.merge(df_final, df_map_dane, left_on='cause', right_on='cause_global', how='left')
        
        # Unimos con las métricas de Colombia (AHORA SÍ coinciden los nombres)
        df_final = pd.merge(df_final, df_dane[['cause_dane', 'pct_deaths_colombia']], on='cause_dane', how='left')
        
        # Limpiamos columnas redundantes para dejar el dataset pulcro
        df_final.drop(columns=['cause_global', 'cause_dane'], inplace=True)
        
        output_path = Path("data/processed/analytical_dataset.csv")
        df_final.to_csv(output_path, index=False)
        logger.info(f"¡Éxito! Dataset analítico súper-enriquecido guardado en {output_path}")

    except Exception as e:
        logger.critical(f"Fallo en el pipeline de procesamiento: {str(e)}")

if __name__ == '__main__':
    logger.info("--- INICIANDO TRANSFORMACIÓN Y AUDITORÍA ---")
    transform_and_merge()