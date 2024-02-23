import csv
import glob
import os
import re

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from utils.consts import DATA_DIR


@dataclass
class Macros:
    name: str
    calories_kcal: int
    carbs_g: int
    protein_g: int
    fat_g: int
    macros: str


class UnitOfMeasurement(Enum):
    '''
    More units and conversions at
    https://en.wikipedia.org/wiki/Cooking_weights_and_measures
    '''
    L = 'L'
    ml = 'ml'
    g = 'g'
    kg = 'kg'
    cup = 'cup'
    tsp = 'tsp'
    tbsp = 'tbsp'
    pcs = 'pcs'


@dataclass(order=True)
class Ingredient:
    name: str
    quantity: float
    unit: UnitOfMeasurement

    def tight_dict(self) -> dict[str, str | float]:
        """
        Returns "cleaned-up" version of dictionary, that
        Question.__dict__ usually returns. Without classes names
        in it or unnecessary double qotes or brackets.
        """
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit.value
        }

    def __post_init__(self):
        if self.unit == UnitOfMeasurement.g:
            self.unit = UnitOfMeasurement.kg
            self.quantity /= 1000

        if self.unit == UnitOfMeasurement.L:
            self.unit = UnitOfMeasurement.ml
            self.quantity *= 1000

        if self.unit == UnitOfMeasurement.tbsp:
            self.unit = UnitOfMeasurement.ml
            self.quantity *= 14.7868


class Data:
    '''
    Read and write operations to main questions database CSV file.
    '''
    def __init__(self, path: str) -> None:
        self.menu: dict[str, list[Ingredient]] = self.get_days(path)
        if not self.menu:
            raise ValueError(f'No Ingredients were found in files at `{path}`')

    def get_days(self, csv_dir: str) -> dict[str, list[Ingredient]]:
        '''
        Get directory with CSV files and return dict of days, where
        each day have list with multiple Ingredient objects.

        Args:
            csv_dir (str): path to directory where CSVs reside.

        Returns:
            dict[str, list[Ingredient]]: example:
                {
                    'day0': [Ingredient(
                        name='carrots',
                        unit=UnitOfMeasurement('kg'),
                        quantity=0.07'), ...],
                    'day1.lunch': [...],
                    'day1.cake': [...]
                }
        '''
        if not Path(csv_dir).is_dir():
            raise ValueError(f'Expected `{csv_dir}` directory doesn\'t exist.')

        if not any(Path(csv_dir).iterdir()):
            raise ValueError(f'There are no files to process in `{csv_dir}`.')

        filepaths = glob.glob(f'{csv_dir}/day*.csv')
        if not filepaths:
            raise ValueError(f'There are no matching files in `{csv_dir}` to process.')

        pattern = re.compile(r'^((day\d)\.?(\d|\w+)?)\.csv$', re.IGNORECASE)

        days: dict[str, list[Ingredient]] = {}

        for filepath in filepaths:
            _, filename = os.path.split(filepath)

            if match := re.match(pattern, filename):
                day_name = match.group(1)
                if self.read_csv(Path(filepath)):
                    days[day_name] = self.read_csv(Path(filepath))

        return days

    def read_csv(self, filepath: Path) -> list[Ingredient]:
        '''Read CSV file and return list of dataclass objects from it.

        Args:
            filepath (str): path to CSV file.

        Returns:
            list[Ingredient]: list of Ingredient objects
        '''
        day: list[Ingredient] = []

        if not Path(filepath).exists():
            raise ValueError(
                f"{filepath} doesn't exist. Create new empty {filepath},"
                f' fill it out and add it to {DATA_DIR}/.'
            )

        with open(filepath) as file:
            for row in csv.DictReader(file):
                day.append(Ingredient(
                    name=row['name'],
                    unit=UnitOfMeasurement(row['unit']),
                    quantity=float(row['quantity'] or 0),
                ))
        return day

    def write_csv(self, filepath: Path, data: list[Ingredient] | list[Macros]) -> None:
        '''
        Write data to CSV file. Data can be either list of Ingredient
        object or list of dicts.

        Args:
            filepath (Path): filepath of CSV file.
            data (list[Ingredient] | list[Macros]): either list of Macros
                or Ingredient objs.
        '''
        clean_data = self.obj_to_dict_for_csv(data)

        Path(filepath).resolve().parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as file:
            writer = csv.DictWriter(file, [item for item in clean_data[0]])
            writer.writeheader()
            writer.writerows(clean_data)

    @staticmethod
    def obj_to_dict_for_csv(data: list[Ingredient] | list[Macros]) -> list[dict]:
        '''
        Convert list of obj to list of dictionaries.
        '''
        dict_data: list[dict[str, str | float]] = []

        if isinstance(data[0], Ingredient):
            dict_data = [i.tight_dict() for i in data]  # type: ignore

        elif isinstance(data[0], Macros):
            dict_data = [i.__dict__ for i in data]

        return dict_data
