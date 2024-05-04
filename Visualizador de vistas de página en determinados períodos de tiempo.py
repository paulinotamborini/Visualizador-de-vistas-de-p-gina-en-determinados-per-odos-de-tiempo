import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Importar los datos y establecer el índice
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Limpieza de datos
df_clean = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Copia de los datos
    df_copy = df_clean.copy()
    
    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_copy.index, df_copy['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Guardar y devolver la figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copia de los datos y extracción de año y mes
    df_copy = df_clean.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month_name()
    
    # Agrupar por año y mes
    df_grouped = df_copy.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Crear el gráfico de barras
    fig = df_grouped.plot(kind='bar', figsize=(10, 6)).get_figure()
    plt.legend(title='Months')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.title('Average daily page views per month')
    plt.xticks(rotation=45)
    
    # Guardar y devolver la figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Copia de los datos y extracción de año y mes
    df_copy = df_clean.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month_name()
    
    # Preparar los datos para el gráfico de cajas
    df_copy['month_num'] = df_copy['date'].dt.month
    df_copy = df_copy.sort_values('month_num')
    df_copy['month'] = pd.Categorical(df_copy['month'], categories=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
    
    # Crear los gráficos de cajas
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))
    
    sns.boxplot(x='year', y='value', data=df_copy, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    sns.boxplot(x='month', y='value', data=df_copy, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    plt.xticks(rotation=45)
    
    # Guardar y devolver la figura
    fig.savefig('box_plot.png')
    return fig
