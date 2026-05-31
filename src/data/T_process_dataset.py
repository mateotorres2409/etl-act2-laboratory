import pandas as pd
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

def transform_and_merge():
    try:
        logger.info("1. Leyendo datos desde capas raw y external...")
        df_raw = pd.read_csv("data/raw/causeofdeath.csv", sep=';', decimal=',')
        df_ext = pd.read_csv("data/external/who_disease_taxonomy.csv")
        
        # --- AUDITORÍA DE CALIDAD DE DATOS (DATA PROFILING) ---
        medidas_unicas = df_raw['Measure'].unique()
        logger.info(f"Auditoría de métricas disponibles: {medidas_unicas}")
        
        if 'Deaths annual % change 2010-2017' in medidas_unicas:
            logger.warning("ALERTA DE NEGOCIO: La guía solicita variación 2005-2010, pero la metadata real contiene 2010-2017.")
            logger.warning("ACCIÓN: Se mantendrá la fidelidad de la fuente original (2010-2017) para garantizar la integridad analítica.")
        # ------------------------------------------------------

        logger.info("2. Aplicando Pivot a causas de muerte (Formato Ancho)...")
        df_pivot = df_raw.pivot_table(
            index='Cause of death or injury',
            columns='Measure',
            values='Value',
            aggfunc='first'
        ).reset_index()
        
        df_pivot.rename(columns={
            'Percent of total deaths 2017': 'pct_deaths_2017',
            'Deaths annual % change 2010-2017': 'annual_change_2010_2017',
            'Cause of death or injury': 'cause'
        }, inplace=True)
        df_pivot.columns.name = None
        
        logger.info("3. Ejecutando Left Join con la taxonomía externa de la OMS...")
        df_final = pd.merge(df_pivot, df_ext, on='cause', how='left')
        
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        output_path = Path("data/processed/analytical_dataset.csv")
        df_final.to_csv(output_path, index=False)
        
        logger.info(f"Dataset analítico consolidado en {output_path} ({len(df_final)} filas).")
            
    except Exception as e:
        logger.critical(f"Fallo en el pipeline de procesamiento: {str(e)}")

if __name__ == '__main__':
    logger.info("--- INICIANDO TRANSFORMACIÓN Y AUDITORÍA ---")
    transform_and_merge()