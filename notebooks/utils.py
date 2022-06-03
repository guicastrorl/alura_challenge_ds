import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# função para devolver alguns detalhes de cada coluna
def column_analysis(data, column, dataframe = True):
    if dataframe == False:
        print('-' * 25)
        print(f'Nome:          {column}')
        print(f'Cardinalidade: {data[column].nunique()}')
        print(f'Dados únicos:  {data[column].unique()}')
        print(f'Tipo:          {data[column].dtypes}')
    else:
        return (column, data[column].nunique(), str(data[column].unique()), data[column].isna().sum(), data[column].dtypes)

def show_values(axs, orient = "v", space = 0.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height() * 0.01)
                value = '{:.1f}'.format(p.get_height())
                ax.text(_x, _y, value, ha = "center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.1f}'.format(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

def plot_bar(data, column):
    if column == 'genero':
        x_values = data[column].replace({0: 'Masculino', 1: 'Feminino'}).value_counts().sort_index().index
    else:
        x_values = data[column].replace({0: 'Não', 1: 'Sim'}).value_counts().sort_index().index
    y_values = data[column].value_counts(normalize = True).sort_index().values * 100
    p = sns.barplot(x = x_values, y = y_values, label = f'{column}')
    show_values(p)
    plt.title(f'Análise univariada - {column}', loc = 'left', fontsize = 14)
    plt.ylim(0, 100)
    plt.ylabel('Porcentagem (%)')

def plot_pie(data, column):
    plt.pie(data[column].value_counts(normalize = True).values, labels = data[column].replace(0, 'Nenhuma').value_counts().index, autopct = '%.2f' + '%%')
    plt.title(f'Análise univariada - {column}', loc = 'left', fontsize = 14)

def plot_hist(data, column):
    plt.hist(data[column], bins = 20)
    plt.title(f'Análise univariada - {column}', loc = 'left', fontsize = 14)
    plt.xlabel(f'{column}')
    plt.ylabel('Volumetria')

# def plot_catplot(data, column):
#     g = sns.catplot(x = column, hue = 'churn', kind = 'count', data = data, height = 8, aspect = 0.9)
#     g.fig.suptitle(f'Churn por {column}', fontsize = 14)
#     g.set_ylabels('Quantidade de churn')
#     g.set_xlabels(column)
#     g.despine(left = True)

def plot_catplot(data, column):
    x = column
    y = 'churn'
    data = data.groupby(x)[y].value_counts(normalize=True).mul(100).rename('percent').reset_index()
    

    g = sns.catplot(x = x, y = 'percent', hue = y, kind = 'bar', data = data, height = 8, aspect = 0.9)
    g.fig.suptitle(f'Churn por {column}', fontsize = 14)
    g.set_ylabels('Porcentagem (%)')
    g.set_xlabels(column)
    g.set(ylim = (0, 100))

# fucntion to extract dict from columns
def extract_dict(data):
    data = data.copy()
    x = 0
    while x == 0:
        for i in data.columns:
            if type(data[i].loc[0]) == dict:
                x = 0
                for j in data[i].loc[0].keys():
                    data[j] = data[i].apply(lambda x: x[j])
                data.drop(i, axis = 1, inplace = True)
            else: x = 1

    return data

# função para devolver alguns detalhes de cada coluna
def column_analysis(data, column, dataframe = False):
    # print('-' * 25)
    # print(f'Nome:          {column}')
    # print(f'Cardinalidade: {data[column].nunique()}')
    # print(f'Dados únicos:  {data[column].unique()}')
    # print(f'Tipo:          {data[column].dtypes}')
    
    return (column, data[column].nunique(), str(data[column].unique()), data[column].isna().sum(), data[column].dtypes)