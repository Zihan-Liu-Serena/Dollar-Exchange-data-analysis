"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""

import pandas as pd
import numpy as np
from my_module.functions import *

def test_read_data():
  data = read_data('Dollar-Exchange.csv')
  df = pd.DataFrame(data)
  assert df.shape == (4956,38)


# Test for fill_na function
def test_fill_na():
    data = {
        'A': [1, np.nan, 3, 4, 5],
        'B': [np.nan, 2, 3, np.nan, 5]
    }
    expected_result = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 2, 3, 4, 5]
    })
    df = pd.DataFrame(data)
    assert fill_na(df).equals(expected_result)


# Test for calculate_yearly_average function
def test_calculate_yearly_average():
    data = {
        'date': ['2020-01-01', '2020-05-15', '2021-02-20', '2021-07-30', '2022-03-10'],
        'value': [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)
    expected_result = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'value': [15.0, 35.0, 50.0]
    })
    assert calculate_yearly_average(df, 'date', 'value').equals(expected_result)

# Test for compare_currency function
def test_compare_currency():
    data = {
        'currency1': [100, 200, 150, 300, 250],
        'currency2': [150, 180, 150, 250, 260]
    }
    df = pd.DataFrame(data)
    expected_result = pd.Series([  
        'currency1 is more expensive',  
        'currency2 is more expensive',  
        'they are the same',  
        'currency2 is more expensive',  
        'currency1 is more expensive'  
    ], index=df.index) 
    assert compare_currency(df, 'currency1', 'currency2').equals(expected_result)
