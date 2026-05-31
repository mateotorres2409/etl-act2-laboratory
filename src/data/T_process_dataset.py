import pandas as pd
import pycountry
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_iso_code(country_name: str) -> str:
    """Convierte nombre de país a código ISO-3 para garantizar el cruce."""
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        try:
            return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
        except Exception:
            return 'UNKNOWN'

def run_transformation_pipeline():
    """
    (Transformación) Lee, estructura (Pivot), estandariza llaves y unifica (Merge).
    """
    logger.info("1. Leyendo datos desde capas raw y external...")
    df_causes = pd.read_csv("data/raw/causeofdeath.csv", sep=';', decimal=',')
    df_health = pd.read_csv("data/external/health_expenditure_2017.csv")
    
    # Excluimos la fila 'Global' porque ahora el análisis es por países
    df_countries = df_causes[df_causes['Location'] != 'Global'].copy()
    
    logger.info("2. Aplicando Pivot a causas de muerte...")
    df_pivot = df_countries.pivot_table(
        index=['Location', 'Cause of death or injury'],
        columns='Measure',
        values='Value',
        aggfunc='first'
    ).reset_index()
    
    # Limpieza de columnas
    df_pivot.columns.name = None
    df_pivot.rename(columns={
        'Percent of total deaths 2017': 'pct_deaths_2017',
        'Deaths annual % change 2010-2017': 'annual_change_2010_2017',
        'Cause of death or injury': 'cause'
    }, inplace=True)
    
    logger.info("3. Generando llaves geográficas (ISO-3) para Merge...")
    df_pivot['iso_code'] = df_pivot['Location'].apply(get_iso_code)
    
    # El Banco Mundial ya trae el código de 3 letras en su primera columna (economy)
    wb_code_col = df_health.columns[0]
    wb_val_col = df_health.columns[2] # Usualmente la métrica está en la 3ra columna
    df_health_clean = df_health.rename(columns={
        wb_code_col: 'iso_code', 
        wb_val_col: 'health_exp_pct_gdp'
    })[['iso_code', 'health_exp_pct_gdp']]
    
    logger.info("4. Ejecutando Inner Join...")
    df_final = pd.merge(df_pivot, df_health_clean, on='iso_code', how='inner')
    
    # Guardamos en la capa de modelo analítico
    output_path = Path("data/processed/analytical_dataset.csv")
    df_final.to_csv(output_path, index=False)
    
    logger.info(f"Dataset analítico listo en {output_path}")
    logger.info(f"Total de registros procesados: {len(df_final)}")
    
    # Un pequeño log para verificar que Colombia sobrevivió al cruce
    colombia_data = df_final[df_final['iso_code'] == 'COL']
    logger.info(f"Registros de Colombia ('COL') encontrados en el dataset final: {len(colombia_data)}")

if __name__ == '__main__':
    logger.info("--- INICIANDO TRANSFORMACIÓN (HITO 2) ---")
    run_transformation_pipeline()
    logger.info("--- TRANSFORMACIÓN FINALIZADA ---")