# These are some universal functionalities for pandas dataframe objects.

# Imports

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Functions

def show_basic_info(df, head = 5, numerical_cols = None, categorical_cols = None,
    bins = 1000, rel_freq = True):
    
    # Given dataframe object 'df', display basic summary statistics and plots. 

    # numerical_cols should either be None, in which case all columns deemed numerical
    # will be summarized, or a list of strings specifiying the column names for numerical
    # variables that are to be summarized.
    # Likewise for categorical_cols.
    
    print(f"Sample size: {len(df)}")

    print('Column names and data types:')
    col_table = df.dtypes.to_frame()
    col_table.rename(columns={0 : 'Data Type'}, inplace=True)
    display(col_table)
    
    print(f'First {head} rows:')
    display(df.head(head))

    # Provide info for numerical data
    
    print('==========')
    print('Numerical data summary: \n')
    
    # Filter for numerical columns only
    if numerical_cols == None:
        numerical_cols = [df.columns[i] for i in range(0, len(df.columns)) 
                        if df.dtypes[i].type in (np.int64, np.float64)]
    
    if numerical_cols == []:
        print('No numerical column to display.\n')
    else:
        display(df[numerical_cols].describe())

    # Plot the histogram without 'inf' or 'NaN' values.

    print('Plots \n')

    for each in numerical_cols:
        print(each + ": \n")
        df[[each]][~np.isinf(df[each]) & ~np.isnan(df[each])].plot.hist(bins = bins)
        plt.show()	

    # Provide info for categorical data

    if categorical_cols == None:
        categorical_cols = [df.columns[i] for i in range(0, len(df.columns)) 
                            if df.dtypes[i].type == np.object_]
        
    print('==========')
    print('Categorical data summary:')    
    display(df[categorical_cols].describe())
    print('-----')

    for each in categorical_cols:
        print(each + '\n')
        print('Frequency table')
        
        if len(df[each].value_counts()) <= 10:
            display(df[each].value_counts().head(10).to_frame())
        else:
            # Shorten the frequency table a bit for simplicity.
            print('\nMost frequent categories:')
            display(df[each].value_counts().head(5).to_frame())
            print('\nLeast frequent categories:')
            display(df[each].value_counts().tail(5).to_frame())
        
        print(f'Number of unique categories: {len(df[each].value_counts())}')
        print(f'Number of observations: {len(df[each])}')
        print(f'Number of missing observations: {df[each].isnull().values.sum()}')
        
        # Plot the relative frequency pie chart
        plot_top_pie(df, each, rel_freq = rel_freq)
        
        print('-----')

    # Missing values
    print(f'Number of entries missing values: {df.isnull().values.sum()} \n')
    
    
def plot_top_pie(df, col_name, top = 5, rel_freq = True, fontsize = 20, figsize = (6, 6)):

    # Create a pie chart displaying the most frequent occurences
    # (determined by argument 'top') while conglomerating all other categorical
    # counts as 'Others'. Returns a regular pie chart if the number of categories
    # is fewer than 'top'.
    # rel_freq: True returns a relative-frequency (ie. percentage) pie chart, 
    # and False returns a frequency (ie. count) pie chart.
    # The rest of the arguments are for adjusting the pie chart's appearance.
    
    pass
    
    # Create frequency data
    freq_data = pd.DataFrame(df[col_name].value_counts(), columns = [col_name])
    total_count = int(freq_data.sum())
    
    # Pick the most frequent occurences for viewing.
    if len(freq_data) > top:
        rest_count = int(freq_data[top:].sum())
        rest_len = len(freq_data[top:])
        others_row = pd.DataFrame([rest_count], columns = [col_name], 
                                  index = [f'Others ({rest_len} categories)'])
        freq_data = freq_data.head(top).append(others_row)

    # Finalize relative frequency data
    if rel_freq:
        title_suffix = ' Relative Frequency'
        scale = total_count / 100
        num_format = '%.2f%%'
    else:
        title_suffix = ' Frequency'
        scale = 1
        num_format = '%d'
    
    freq_data = freq_data[col_name] / scale

    # Create and display the plot.
    freq_data.plot.pie(autopct=num_format, fontsize = fontsize, figsize = figsize)
    plt.axis('off')
    plt.title(col_name + title_suffix, fontsize = fontsize)
    plt.show()