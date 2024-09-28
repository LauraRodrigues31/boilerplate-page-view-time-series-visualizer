import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Registra conversores de data para o matplotlib
register_matplotlib_converters()

# Importa os dados e define a coluna 'date' como índice, convertendo-a para o formato de data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpa os dados: remove valores fora dos percentis 2.5% e 97.5% para eliminar outliers
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# Garante que a coluna 'value' seja do tipo float para evitar possíveis erros
df['value'] = df['value'].astype(float)


def draw_line_plot():
    # Desenha o gráfico de linha
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salva a imagem e retorna a figura
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copia e modifica os dados para o gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year  # Extrai o ano
    df_bar['month'] = df_bar.index.month  # Extrai o mês

    # Cria uma tabela pivotada para obter a média das visualizações mensais por ano
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Desenha o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(15, 8), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(
        title='Months',
        labels=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    )

    # Salva a imagem e retorna a figura
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepara os dados para os gráficos de caixa
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]  # Extrai o ano
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Extrai o mês como abreviação

    # Garante que a coluna 'value' seja do tipo float para evitar possíveis erros
    df_box['value'] = df_box['value'].astype(float)

    # Desenha os gráficos de caixa (usando Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico de caixa por ano (tendência)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Gráfico de caixa por mês (sazonalidade)
    sns.boxplot(
        x='month', y='value', data=df_box,
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ax=ax2
    )
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Salva a imagem e retorna a figura
    fig.savefig('box_plot.png')
    return fig
