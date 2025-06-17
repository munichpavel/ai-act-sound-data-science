"""Simple, DIY implementation of data expectation enforcement,
consciously imitating frameworks like GreatExpectations and dbt.
"""
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
import pandas as pd


PROJECT_ROOT = Path(__file__).parents[2]

def get_failed_data_expectations(df: pd.DataFrame, expectation_suite_name: str) -> list[dict]:
    data_conf = load_data_conf(root_dir=PROJECT_ROOT)
    expectations = data_conf.expectations[expectation_suite_name]
    res = []
    for expectation_name, expectation_val in expectations.items():
        failed_df = _get_failed_data_expectation(df, name=expectation_name, args=expectation_val)
        if failed_df.shape[0] > 0:
            res.append({'expectation_name': expectation_name, 'failures': failed_df})
    return res


def load_data_conf(root_dir: Path) -> OmegaConf:
    data_conf = OmegaConf.load(root_dir / 'config' / 'data.yaml')
    return data_conf


def _get_failed_data_expectation(df: pd.DataFrame, name: str, args: Any) -> pd.DataFrame:
    if name == 'expect_compound_unique_fields':
        compound_unique_values = list(args)
        res = get_compound_non_uniques(df, compound_unique_cols=compound_unique_values)
    return res


def get_compound_non_uniques(df: pd.DataFrame, compound_unique_cols: list[str]) -> pd.DataFrame:
    duplicate_mask = df.duplicated(subset=compound_unique_cols, keep=False)
    res = df.loc[duplicate_mask, :]
    # order
    res = res.sort_values(by=compound_unique_cols)

    return res
