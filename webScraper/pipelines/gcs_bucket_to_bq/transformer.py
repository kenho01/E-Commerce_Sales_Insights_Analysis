import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    current_date = datetime.now().strftime('%Y-%m-%d')
    data['brand'] = data['brand'].astype('string')
    data['sku'] = data['sku'].astype('string')
    data['name'] = data['name'].astype('string')
    data['actual_price'] = data['actual_price'].str.replace('S$ ', '', regex=False).astype('float')
    data['discounted_price'] = data['discounted_price'].str.replace('S$ ', '', regex=False) \
                                .str.strip() \
                                .replace('', np.nan) \
                                .astype('float')
    data['discounted_price'] = data['discounted_price'].fillna(data['actual_price'])
    data['discount'] = data['actual_price'] - data['discounted_price']
    data['discount_percentage'] = (data['discount'] / data['actual_price']) * 100
    data['date'] = current_date
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    # display(data)
    return data


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
