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

import pandas as pd
import statsmodels.api as sm


def forward_regression(X, y, threshold_in, verbose=True):
    included = []

    while True:
        changed = False

        excluded = list(set(X.columns) - set(included))
        new_pval = pd.Series(index = excluded)

        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included + [new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]

        best_pval = new_pval.min()

        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed = True

            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))
        
        if not changed:
            break

    return included

def backward_regression(X, y, threshold_out, verbose=True):
    included = list(X.columns)

    while True:
        changed = False

        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty

        if worst_pval > threshold_out:
            changed = True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)

            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        
        if not changed:
            break

    return included

def stepwise_regression(X, y, threshold_in = 0.01, threshold_out = 0.05, verbose=True):
    """ 
    Perform a forward-backward feature selection 
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features 
    Always set threshold_in < threshold_out to avoid infinite looping.
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    initial_list = X.columns.tolist()
    best_features = list(initial_list)

    while True:
        changed = False
        # forward step
        remaining_features = list(set(X.columns) - set(best_features))
        new_pval = pd.Series(index = remaining_features)

        for new_column in remaining_features:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[best_features + [new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]

        best_pval = new_pval.min()

        if best_pval < threshold_in:
            best_feature = new_pval.idxmin() #.argmin()
            best_features.append(best_feature)
            changed = True

            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[best_features]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty

        if worst_pval >= threshold_out:
            changed = True
            worst_feature = pvalues.idxmax() #argmax()
            best_features.remove(worst_feature)

            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        
        if not changed:
            break
        
    return best_features

def stepwise_regression_1(X, y, threshold_in = 0.05, threshold_out = 0.05, verbose = True):
    initial_list = X.columns.tolist()
    best_features = []

    while (len(initial_list) > 0):
        remaining_features = list(set(initial_list) - set(best_features))
        new_pval = pd.Series(index = remaining_features)

        for new_column in remaining_features:
            model = sm.OLS(y, sm.add_constant(X[best_features + [new_column]])).fit()
            new_pval[new_column] = model.pvalues[new_column]

        min_p_value = new_pval.min()

        if(min_p_value < threshold_in):
            best_feature = new_pval.idxmin()
            best_features.append(best_feature)
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, min_p_value))

            while(len(best_features) > 0):
                best_features_with_constant = sm.add_constant(X[best_features])
                p_values = sm.OLS(y, best_features_with_constant).fit().pvalues[1:]
                max_p_value = p_values.max()
                
                if(max_p_value >= threshold_out):
                    excluded_feature = p_values.idxmax()
                    best_features.remove(excluded_feature)
                    if verbose:
                        print('Drop {:30} with p-value {:.6}'.format(excluded_feature, max_p_value))

                else:
                    break 
        else:
            break
    return best_features

