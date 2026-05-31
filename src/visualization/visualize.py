import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Configuración básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_visuals():
    """Configura el estilo estético global de las gráficas."""
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    Path("reports/figures").mkdir(parents=True, exist_ok=True)

def generate_plots():
    logger.info("Leyendo dataset analítico...")
    df = pd.read_csv("data/processed/analytical_dataset.csv")
    
    # Limpiar posibles datos nulos o ruidos antes de graficar
    df = df.dropna(subset=['pct_deaths_2017', 'annual_change_2010_2017'])
    
    # ---------------------------------------------------------
    # Gráfico 1: Top 10 Causas de Muerte (El "Qué")
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 1: Top 10 Causas...")
    top_10 = df.nlargest(10, 'pct_deaths_2017')
    
    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=top_10, 
        x='pct_deaths_2017', 
        y='cause', 
        hue='who_category',
        dodge=False,
        palette='viridis'
    )
    plt.title('Top 10 Causas de Mortalidad Global (2017)', fontsize=16, pad=20)
    plt.xlabel('Porcentaje Total de Muertes', fontsize=12)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('reports/figures/01_top_10_causas.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Gráfico 2: Matriz de Evolución vs Impacto (El "Hacia Dónde")
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 2: Evolución vs Impacto...")
    plt.figure(figsize=(14, 9))
    
    # Creamos un Scatter Plot. X = Crecimiento Anual, Y = % Muertes.
    scatter = sns.scatterplot(
        data=df,
        x='annual_change_2010_2017',
        y='pct_deaths_2017',
        hue='who_category',
        size='pct_deaths_2017',
        sizes=(50, 800),
        alpha=0.7,
        palette='Set2'
    )
    
    # Líneas divisorias para crear "Cuadrantes" (Cero crecimiento)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    
    plt.title('Matriz de Riesgo: Crecimiento Anual vs Volumen de Mortalidad', fontsize=16, pad=20)
    plt.xlabel('Tasa de Cambio Anual (2010-2017) -> Positivo significa que la causa está creciendo', fontsize=12)
    plt.ylabel('Porcentaje Total de Muertes (2017)', fontsize=12)
    
    # Anotamos los outliers más peligrosos (alto volumen y alto crecimiento)
    for i in range(len(df)):
        if df['pct_deaths_2017'].iloc[i] > 0.05 or df['annual_change_2010_2017'].iloc[i] > 0.02:
            plt.text(df['annual_change_2010_2017'].iloc[i] + 0.001, 
                     df['pct_deaths_2017'].iloc[i], 
                     df['cause'].iloc[i], 
                     fontsize=9)
            
    plt.tight_layout()
    plt.savefig('reports/figures/02_matriz_riesgo.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Gráfico 3: Análisis por Taxonomía OMS (El "Por Qué")
    # ---------------------------------------------------------
    logger.info("Generando Gráfico 3: Impacto por Categoría OMS...")
    category_group = df.groupby('who_category')['pct_deaths_2017'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=category_group.sort_values('pct_deaths_2017', ascending=False),
        x='who_category',
        y='pct_deaths_2017',
        palette='pastel'
    )
    plt.title('Carga Global de Mortalidad por Taxonomía OMS', fontsize=16, pad=20)
    plt.xlabel('Categoría de la Enfermedad (Fuente Externa)', fontsize=12)
    plt.ylabel('Suma Acumulada de Porcentaje de Muertes', fontsize=12)
    plt.tight_layout()
    plt.savefig('reports/figures/03_taxonomia_oms.png', dpi=300)
    plt.close()
    
    logger.info("¡Todas las gráficas han sido generadas en reports/figures/!")

if __name__ == '__main__':
    setup_visuals()
    generate_plots()