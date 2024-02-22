import pytest

from pathlib import Path

from utils.data import Data
from calcprods import Calcprods
from utils.utils import (
    tabulate_data, split_str_to_ints
)


def test_tabulate_data():
    DATA_DIR = 'tests/io_data'
    STOCK_IN_PATH = Path('tests/io_data/instock.csv')
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0, 1])

    order = cp.get_order_list(STOCK_IN_PATH)
    assert tabulate_data(order) == \
        '╭────┬───────────────┬────────────┬────────╮\n' \
        '│    │ name          │   quantity │   unit │\n' \
        '├────┼───────────────┼────────────┼────────┤\n' \
        '│  0 │ carrots       │       4.13 │     kg │\n' \
        '├────┼───────────────┼────────────┼────────┤\n' \
        '│  1 │ macaroni      │       4.13 │     kg │\n' \
        '├────┼───────────────┼────────────┼────────┤\n' \
        '│  2 │ soy sauce     │       1.18 │    cup │\n' \
        '├────┼───────────────┼────────────┼────────┤\n' \
        '│  3 │ sunflower oil │          0 │     ml │\n' \
        '├────┼───────────────┼────────────┼────────┤\n' \
        '│  4 │ water         │      18880 │     ml │\n' \
        '╰────┴───────────────┴────────────┴────────╯'


def test_split_str_to_ints():
    assert split_str_to_ints('1') == [1]
    assert split_str_to_ints('1-5') == [1, 2, 3, 4, 5]
    assert split_str_to_ints('1, 2, 8') == [1, 2, 8]
    assert split_str_to_ints('1,2,8') == [1, 2, 8]

    with pytest.raises(ValueError) as excinfo:
        split_str_to_ints('foo')
    assert 'Wrong digit or digits range.' in str(excinfo.value)
