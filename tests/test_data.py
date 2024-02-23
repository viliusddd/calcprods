import pytest

from pathlib import Path

from utils.data import Data, Ingredient, Macros, UnitOfMeasurement


def test_tight_dict():
    ing = Ingredient(
        name='carrot',
        quantity=10,
        unit=UnitOfMeasurement.kg,
    )
    assert ing.tight_dict() == {
        'name': 'carrot',
        'quantity': 10.0,
        'unit': 'kg',
    }


def test_get_days():
    data = Data(path='tests/io_data')
    assert data.get_days('tests/io_data/') == {
        'day0': [
            Ingredient('carrots', 0.07, UnitOfMeasurement.kg),
            Ingredient('sunflower oil', 0.0, UnitOfMeasurement.ml),
        ],
        'day1.1': [
            Ingredient('water', 250.0, UnitOfMeasurement.ml),
            Ingredient('macaroni', 0.07, UnitOfMeasurement.kg),
        ],
        'day1.main': [
            Ingredient('water', 35.0, UnitOfMeasurement.ml),
        ],
        'day1.2': [
            Ingredient('soy sauce', 0.02, UnitOfMeasurement.cup),
            Ingredient('water', 35.0, UnitOfMeasurement.ml),
        ],
    }


def test_read_csv():
    data = Data(path='tests/io_data')
    STOCK_IN_PATH = Path('tests/io_data/day1.main.csv')
    assert data.read_csv(STOCK_IN_PATH) == [
        Ingredient('water', 35.0, UnitOfMeasurement('ml'))
    ]


def test_read_csv_value_error():
    data = Data(path='tests/io_data')
    STOCK_IN_PATH = Path('tests/nonexist/day1.main.csv')

    with pytest.raises(ValueError) as exc_info:
        data.read_csv(STOCK_IN_PATH)

    assert exc_info.value.args[0] == \
        "tests/nonexist/day1.main.csv doesn't exist. Create new " \
        "empty tests/nonexist/day1.main.csv, fill it out and add " \
        "it to data/."


def test_obj_to_dict_for_csv_with_Ingredient_obj():
    data = Data(path='tests/io_data')
    ingr = Ingredient('water', 35.0, UnitOfMeasurement('ml'))
    assert data.obj_to_dict_for_csv([ingr]) == [
        {'name': 'water', 'quantity': 35.0, 'unit': 'ml'}
    ]


def test_obj_to_dict_for_csv_with_Macros_obj():
    data = Data(path='tests/io_data')
    ingr = Macros('carrots', 35, 8, 1, 2, '87/9/5')
    assert data.obj_to_dict_for_csv([ingr]) == [{
        'calories_kcal': 35,
        'carbs_g': 8,
        'fat_g': 2,
        'macros': '87/9/5',
        'name': 'carrots',
        'protein_g': 1,
    }]
