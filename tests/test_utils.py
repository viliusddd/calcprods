import pytest

from utils.io import Data
from calcprods import Calcprods
from utils.utils import (
    tabulate_data, print_dict, print_list, split_str_to_ints
)

def test_tabulate_data():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0])

    order = cp.get_order_list()
    assert tabulate_data(order) == \
        '╭────┬─────────┬────────────┬────────╮\n' \
        '│    │ name    │   quantity │ unit   │\n' \
        '├────┼─────────┼────────────┼────────┤\n' \
        '│  0 │ carrots │       14.2 │ kg     │\n' \
        '╰────┴─────────┴────────────┴────────╯'

def test_split_str_to_ints():
    assert split_str_to_ints('1') == [1]
    assert split_str_to_ints('1-5') == [1, 2, 3, 4, 5]
    assert split_str_to_ints('1, 2, 8') == [1, 2, 8]
    assert split_str_to_ints('1,2,8') == [1, 2, 8]

    with pytest.raises(ValueError) as excinfo:
        split_str_to_ints('foo')
    assert 'Wrong digit or digits range.' in str(excinfo.value)
