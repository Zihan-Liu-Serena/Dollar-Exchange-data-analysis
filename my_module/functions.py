"""A collection of functions for doing my project."""

import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_name):
    """
    Reads a csv and convert it to a dataframe. 

    Parameters
    ----------
    file_name: string
        Name of the file containing the data.
        
    Returns
    -------
    data: dataframe
       The dataframe of all the information in the file. 
    
    """ 

    data = pd.read_csv(file_name) # Uses pandas' read_csv function to open the file and have it as dataframe

    return data 


def fill_na(df):
    """
    Fill NaN values in the DataFrame with the average of the previous and next row values.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be processed, which may contain NaN values.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with NaN values filled.
    
    """ 

    for i in range(len(df)):
        for j in range(len(df.columns)):
            if pd.isna(df.iat[i, j]):
                if i == 0:
                    # The first row uses only the values of the next row
                    df.iat[i, j] = df.iat[i+1, j] if i+1 < len(df) else df.iat[i, j]
                elif i == len(df) - 1:
                    # The last row uses only the values of the previous row
                    df.iat[i, j] = df.iat[i-1, j] if i-1 >= 0 else df.iat[i, j]
                else:
                    # The average of the previous row and the next row on the middle row
                    df.iat[i, j] = (df.iat[i-1, j] + df.iat[i+1, j]) / 2
    return df


def calculate_yearly_average(df, date_col, value_col):
    """
    Convert the date column to datetime format, extract the year, 
    and calculate the yearly average of the specified value column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    date_col : str
        The name of the column containing date information.
    value_col : str
        The name of the column for which to calculate the yearly average.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with years and their corresponding average values.
    """
    # Convert the date_col column to datetime format
    df[date_col] = pd.to_datetime(df[date_col])

    # Extract the year and add it as a new column
    df['year'] = df[date_col].dt.year

    # Group value_col column by year and calculate the average value for each year
    yearly_avg = df.groupby('year')[value_col].mean().reset_index()

    # Plot a line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(yearly_avg['year'], yearly_avg[value_col], marker='o', linestyle='-', color='b')
    ax.set_xlabel('Year')
    ax.set_ylabel(value_col)
    ax.set_title(f'Line chart of {value_col} exchange rate from {yearly_avg["year"].min()} to {yearly_avg["year"].max()}')
    ax.grid(True)
    plt.show()

    return yearly_avg, fig



def compare_currency(df, col1, col2):
    """
    Compare the values of two currencies in a DataFrame and return a new column with results.
    Also, plot the exchange rates of the two currencies and the difference.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    col1 : str
        The name of the first currency.
    col2 : str
        The name of the second currency.

    Returns
    -------
    tuple
        A tuple containing a Series with the comparison results, 
        and the matplotlib figure objects for the exchange rates plot and the difference plot.
    """
    # Plot the exchange rates of the two currencies
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df[col1], label=col1, color='red')
    ax1.plot(df[col2], label=col2, color='blue')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Exchange Rate')
    ax1.set_title(f'Exchange rates for {col1} and {col2}')
    ax1.legend()
    ax1.grid(True)

    # Calculate the difference between the two columns
    diff = df[col1] - df[col2]

    # Plot the difference
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.bar(df.index, diff, color='purple')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Difference')
    ax2.set_title(f'Difference between {col1} and {col2} exchange rates')
    ax2.grid(True)

    # Return the comparison results based on the difference
    result = diff.apply(lambda x: f"{col1} is more expensive" if x < 0 else f"{col2} is more expensive" if x > 0 else "they are the same")

    return result, fig1, fig2

