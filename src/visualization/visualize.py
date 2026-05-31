import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_visuals():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    Path("reports/figures").mkdir(parents=True, exist_ok=True)

def generate_plots():
    logger.info("Leyendo dataset analítico...")
    df = pd.read_csv("data/processed/analytical_dataset.csv")
    
    # NUEVOS NOMBRES DE COLUMNAS
    df_clean = df.dropna(subset=['pct_deaths_global', 'annual_change_global'])
    
    # ---------------------------------------------------------
    # Gráfico 1: Top 10 Causas (Global)
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 1: Top 10 Causas Globales...")
    top_10 = df_clean.nlargest(10, 'pct_deaths_global')
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_10, x='pct_deaths_global', y='cause', hue='who_category', dodge=False, palette='viridis')
    plt.title('Top 10 Causas de Mortalidad Global (2017)', fontsize=16, pad=20)
    plt.xlabel('Porcentaje Total de Muertes', fontsize=12)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('reports/figures/01_top_10_causas.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Gráfico 2: Matriz de Riesgo
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 2: Matriz de Riesgo...")
    plt.figure(figsize=(14, 9))
    sns.scatterplot(
        data=df_clean, x='annual_change_global', y='pct_deaths_global',
        hue='who_category', size='pct_deaths_global', sizes=(50, 800), alpha=0.7, palette='Set2'
    )
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    plt.title('Matriz de Riesgo: Crecimiento Anual vs Volumen de Mortalidad', fontsize=16, pad=20)
    plt.xlabel('Tasa de Cambio Anual (2010-2017) -> Positivo indica crecimiento', fontsize=12)
    plt.ylabel('Porcentaje Total de Muertes (Global)', fontsize=12)
    plt.tight_layout()
    plt.savefig('reports/figures/02_matriz_riesgo.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Gráfico 3: Taxonomía OMS
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 3: Impacto por Categoría OMS...")
    category_group = df_clean.groupby('who_category')['pct_deaths_global'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_group.sort_values('pct_deaths_global', ascending=False), x='who_category', y='pct_deaths_global', palette='pastel')
    plt.title('Carga Global de Mortalidad por Taxonomía OMS', fontsize=16, pad=20)
    plt.xlabel('Categoría Epidemiológica', fontsize=12)
    plt.ylabel('Suma Acumulada de Porcentaje de Muertes', fontsize=12)
    plt.tight_layout()
    plt.savefig('reports/figures/03_taxonomia_oms.png', dpi=300)
    plt.close()
    
    # ---------------------------------------------------------
    #