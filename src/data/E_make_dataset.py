import pandas as pd
import wbgapi as wb
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_world_bank_data(indicator: str, output_path: str, year: int):
    """
    (Extracción) Descarga datos del Banco Mundial de forma idempotente.
    """
    path = Path(output_path)
    if path.exists():
        logger.info(f"Los datos externos ya existen en {path}. Omitiendo descarga.")
        return
        
    logger.info(f"Conectando a API del Banco Mundial. Indicador: {indicator}...")
    try:
        # Extraemos datos crudos del BM
        df_wb = wb.data.DataFrame(indicator, time=year, labels=True).reset_index()
        df_wb.to_csv(path, index=False)
        logger.info(f"Extracción exitosa. Guardado en {path}")
    except Exception as e:
        logger.error(f"Error en la extracción: {str(e)}")

if __name__ == '__main__':
    logger.info("--- INICIANDO EXTRACCIÓN (HITO 1) ---")
    
    # 1. Validar que el archivo local crudo exista
    if not Path("data/raw/causeofdeath.csv").exists():
        logger.warning("Falta causeofdeath.csv en data/raw/")
        
    # 2. Extraer fuente adicional: Gasto en salud (% del PIB)
    fetch_world_bank_data(
        indicator='SH.XPD.CHEX.GD.ZS', 
        output_path="data/external/health_expenditure_2017.csv", 
        year=2017
    )
    logger.info("--- EXTRACCIÓN FINALIZADA ---")