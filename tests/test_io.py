from pathlib import Path

from utils.data import Data, Ingredient, UnitOfMeasurement


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
    data = Data(path='io_data')
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
    data = Data(path='io_data')
    STOCK_IN_PATH = Path('tests/io_data/day1.main.csv')
    assert data.read_csv(STOCK_IN_PATH) == [
        Ingredient('water', 35.0, UnitOfMeasurement('ml'))
    ]
