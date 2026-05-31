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

logger = setup_logger("ingestion.log")

# ==========================================
# 2. LÓGICA DE EXTRACCIÓN (FUENTE EXTERNA)
# ==========================================
def generate_external_taxonomy(output_path: str):
    """
    (Extracción de Datos Maestros - MDM) 
    Simula la integración con un sistema de gestión de datos maestros (Master Data Management).
    Construye y exporta un catálogo físico basado en la estructura taxonómica de la OMS (CIE-10).
    
    Este archivo actúa como la "Segunda Fuente de Datos" exigida por la arquitectura de negocio,
    permitiendo agrupar la granularidad de enfermedades en macro-categorías epidemiológicas.
    """
    path = Path(output_path)
    logger.info("Iniciando extracción/generación del dataset externo de taxonomía OMS...")
    
    try:
        # Extraemos las causas únicas de nuestro archivo base para que el cruce sea perfecto
        df_base = pd.read_csv("data/raw/causeofdeath.csv", sep=';', decimal=',')
        unique_causes = df_base['Cause of death or injury'].unique()
        
        # Diccionarios de clasificación OMS
        communicable = ['Tuberculosis', 'HIV/AIDS', 'Diarrheal diseases', 'Lower respiratory infections', 
                        'Malaria', 'Zika virus', 'Guinea worm disease', 'Typhoid and paratyphoid', 
                        'Invasive Non-typhoidal Salmonella (iNTS)', 'Other intestinal infectious diseases']
        injuries = ['Road injuries', 'Conflict and terrorism', 'Self-harm', 'Interpersonal violence', 
                    'Drowning', 'Fire, heat, and hot substances', 'Poisonings', 'Exposure to forces of nature']
        
        def classify_disease(cause):
            if any(c.lower() in cause.lower() for c in communicable):
                return 'Transmisibles (Infecciosas/Maternas)'
            elif any(i.lower() in cause.lower() for i in injuries):
                return 'Lesiones (Accidentes/Violencia)'
            else:
                return 'No Transmisibles (Crónicas)'

        df_taxonomy = pd.DataFrame({'cause': unique_causes})
        df_taxonomy['who_category'] = df_taxonomy['cause'].apply(classify_disease)
        
        # Guarda físicamente la fuente externa
        Path("data/external").mkdir(parents=True, exist_ok=True)
        df_taxonomy.to_csv(path, index=False)
        logger.info(f"Dataset externo guardado exitosamente en {path}")
        
    except Exception as e:
        logger.error(f"Fallo crítico durante la generación de la taxonomía: {str(e)}")

# ==========================================
# 3. EJECUCIÓN MAIN
# ==========================================
if __name__ == '__main__':
    logger.info("--- EJECUTANDO INGESTA (EXTRACCIÓN) - CAMINO 2 ---")
    generate_external_taxonomy("data/external/who_disease_taxonomy.csv")
    logger.info("--- EXTRACCIÓN FINALIZADA ---")