from pathlib import Path

from calcprods import Calcprods
from utils.data import Data, Ingredient, UnitOfMeasurement
from utils.consts import DATA_DIR


def test_calcprods_var_data():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0])

    assert cp.data == data


def test_calcprods_var_people():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0])

    assert cp.people == 60


def test_calcprods_var_days():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0, 1, 3])

    assert cp.days == [0, 1, 3]


def test_compare_ingredients():
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [1])

    ing_a = Ingredient('carrots', 10, UnitOfMeasurement.kg)
    ing_b = Ingredient('carrots', 10, UnitOfMeasurement.kg)
    ing_c = Ingredient('apples', 15, UnitOfMeasurement.kg)

    assert cp._compare_ingredients(ing_a, ing_c) is None
    assert cp._compare_ingredients(ing_a, ing_b) == \
        Ingredient('carrots', 20, UnitOfMeasurement.kg)


def test_merge_duplicates():
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [1])
    ings = [
        Ingredient('carrots', 10, UnitOfMeasurement.kg),
        Ingredient('water', 3000, UnitOfMeasurement.ml),
        Ingredient('water', 304, UnitOfMeasurement.ml),
        Ingredient('water', 2304, UnitOfMeasurement.ml),
        Ingredient('apples', 15, UnitOfMeasurement.kg),
    ]
    assert cp._merge_duplicates(ings) == [
        Ingredient('apples', 15, UnitOfMeasurement.kg),
        Ingredient('carrots', 10, UnitOfMeasurement.kg),
        Ingredient('water', 5608, UnitOfMeasurement.ml),
    ]


def test_list_ingredients():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0])

    assert cp.list_ingredients() == [
        Ingredient('carrots', 0.07, UnitOfMeasurement.kg),
        Ingredient('sunflower oil', 0.0, UnitOfMeasurement.ml),
    ]


def test_get_empty_instock_list():
    DATA_DIR = 'tests/io_data'
    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0])

    assert cp.get_empty_instock_list() == [
        Ingredient('carrots', '', UnitOfMeasurement.kg),
        Ingredient('sunflower oil', '', UnitOfMeasurement.ml),
    ]


def test_get_order_list():
    DATA_DIR = 'tests/io_data'
    STOCK_IN_PATH = Path('tests/io_data/instock.csv')

    data = Data(path=DATA_DIR)
    cp = Calcprods(data, 60, [0, 1])

    assert cp.get_order_list(STOCK_IN_PATH) == [
        Ingredient('carrots', 4.13, UnitOfMeasurement.kg),
        Ingredient('macaroni', 4.13, UnitOfMeasurement.kg),
        Ingredient('soy sauce', 1.18, UnitOfMeasurement.cup),
        Ingredient('sunflower oil', 0.0, UnitOfMeasurement.ml),
        Ingredient('water', 18880.0, UnitOfMeasurement.ml),
    ]
