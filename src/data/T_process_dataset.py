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

logger = setup_logger("processing.log")

# ==========================================
# 2. LÓGICA DE TRANSFORMACIÓN Y JOIN
# ==========================================
def transform_and_merge():
    """
    (Transformación) Pivota el dataset base y lo cruza con la taxonomía externa de la OMS.
    """
    try:
        logger.info("1. Leyendo datos desde capas raw y external...")
        df_raw = pd.read_csv("data/raw/causeofdeath.csv", sep=';', decimal=',')
        df_ext = pd.read_csv("data/external/who_disease_taxonomy.csv")
        
        logger.info("2. Aplicando Pivot a causas de muerte (Formato Ancho)...")
        # En este camino, nuestro índice es la causa, ya no la ubicación geográfica
        df_pivot = df_raw.pivot_table(
            index='Cause of death or injury',
            columns='Measure',
            values='Value',
            aggfunc='first'
        ).reset_index()
        
        # Limpieza y estandarización de columnas
        df_pivot.rename(columns={
            'Percent of total deaths 2017': 'pct_deaths_2017',
            'Deaths annual % change 2010-2017': 'annual_change_2010_2017',
            'Cause of death or injury': 'cause'
        }, inplace=True)
        df_pivot.columns.name = None
        
        logger.info("3. Ejecutando Left Join con la taxonomía externa (Llave: cause)...")
        df_final = pd.merge(df_pivot, df_ext, on='cause', how='left')
        
        # Guardado en la capa procesada
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        output_path = Path("data/processed/analytical_dataset.csv")
        df_final.to_csv(output_path, index=False)
        
        logger.info(f"Dataset analítico listo y guardado en {output_path}")
        logger.info(f"Total de causas de muerte procesadas: {len(df_final)}")
        
        # Pequeña auditoría de calidad de datos
        nulos_cat = df_final['who_category'].isnull().sum()
        if nulos_cat > 0:
            logger.warning(f"Se detectaron {nulos_cat} causas sin categoría asignada.")
            
    except Exception as e:
        logger.critical(f"Fallo en el pipeline de procesamiento: {str(e)}")

# ==========================================
# 3. EJECUCIÓN MAIN
# ==========================================
if __name__ == '__main__':
    logger.info("--- INICIANDO TRANSFORMACIÓN (HITO 2) - CAMINO 2 ---")
    transform_and_merge()
    logger.info("--- TRANSFORMACIÓN FINALIZADA ---")