from io import StringIO

import pandas as pd

from workshop.possible_data_contract import(
    get_failed_data_expectations, get_compound_non_uniques
)

def test_enforce_data_expectations():

    data = '''customer_id,agg_claim_amount,year
0,10.26,2022
0,0.0,2022
'''
    df = pd.read_csv(StringIO(data))
    expectation_name = 'ClaimData'
    expected_n_failures = 1

    failures = get_failed_data_expectations(df, expectation_name)
    assert len(failures) == expected_n_failures


def test_get_compound_non_uniques():
    data = '''customer_id,agg_claim_amount,year
0,10.26,2022
0,0.0,2022
1,42.,2022
'''
    compound_unique_cols = ['customer_id', 'year']
    expected_data = '''customer_id,agg_claim_amount,year
0,10.26,2022
0,0.0,2022
'''
    df = pd.read_csv(StringIO(data))
    expected_df = pd.read_csv(StringIO(expected_data))

    res = get_compound_non_uniques(df, compound_unique_cols=compound_unique_cols)

    pd.testing.assert_frame_equal(res, expected_df)
