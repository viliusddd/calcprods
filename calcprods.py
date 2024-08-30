#! .venv/bin/python3
'''
Generate list of ingredients with the quantity for particular number of
days and people. Get the nutrition values of ingredients.
This app iscan be used in multiple day retreat kitchens, but it is
optimized for Dhamma.org meditation center kitchen, where courses happen
multiple times a year.

Usage: calcprods [-s|-o|-n] [-p PEOPLE] [-d DAYS] [-vmh]

Try:
  ./calcprods.py -p25 -d2-6
  ./calcprods.py -p 60 -d 1,2,7 -s --nomenu
  ./calcprods.py -nm -v

Options:
  -h --help           Show this screen and exit.
  -s --instock        Generate empty instock list.
  -o --order          Generate order list.
  -n --nutrition      It requires calorieninjas.com api key as
                      FOOD_API_KEY environment variable.
  -p --people NUMBER  Number of peaople. [default: 70]
  -d --days NUMBER    Number of days. In 1 or 1-3 or 1,2,5 form.
                      [default: 0-10]
  -m --nomenu         Skip menu selection and use switches instead.
  -v                  Print output table to the terminal.
'''
import copy

from docopt import docopt
from pathlib import Path
from simple_term_menu import TerminalMenu  # type: ignore

from utils.consts import (STOCK_OUT_PATH, PREP_OUT_PATH, NUTRITION_OUT_PATH,
                          STOCK_IN_PATH, DATA_DIR)
from utils.data import Data, Ingredient
from utils.nutrition import Nutrition
from utils.utils import split_str_to_ints, print_list


type IngredientDict = dict[str, list[Ingredient]]  # type: ignore


class Calcprods:
    def __init__(self, data: Data, people: int, days: list[int]) -> None:
        self._data = data
        self._people = people
        self._days = days
        self._ingredients_processed: list[Ingredient] = self.list_ingredients()
        self._ingredient_names: list[str] = [i.name for i in self._ingredients_processed]

    @property
    def data(self) -> Data:
        return self._data

    @property
    def people(self) -> int:
        return self._people

    @property
    def days(self) -> list[int]:
        return self._days

    @property
    def ingredient_names(self) -> list[str]:
        return self._ingredient_names

    def _compare_ingredients(self, ingr_a: Ingredient, ingr_b: Ingredient,
                             subtract=False) -> Ingredient | None:
        '''
        Merge same name Ingredient objs.
        '''
        if ingr_a.name == ingr_b.name:

            if subtract:
                quantity = ingr_a.quantity - ingr_b.quantity
            else:
                quantity = ingr_a.quantity + ingr_b.quantity

            return Ingredient(
                name=ingr_a.name,
                quantity=round(quantity, 2),
                unit=ingr_a.unit
            )
        return None

    def _merge_duplicates(self, ingredients: list[Ingredient]) -> list[Ingredient]:
        '''Merge duplicate Ingredient objs in the list.

        Finding duplicates method works by examining each set of adjacent
        objects in the list, from left to right, merging them if they
        share the same name. Similar to bubble sort algorithm.

        Args:
            ingredients (list[Ingredient]): list of Ingredient objs.

        Returns:
            list[Ingredient]: sorted and w/o duplicates list of Ingredient objs.
        '''
        n: int = len(ingredients)
        ingredients = sorted(ingredients)
        swapped: bool = False

        for i in range(n-1):
            for j in range(0, n-i-1):

                if ingredients[j + 1] is None:
                    break

                if new_ingr := self._compare_ingredients(
                    ingredients[j], ingredients[j + 1]
                ):
                    ingredients[j], ingredients[j + 1] = None, new_ingr

                    swapped = True

        return [ing for ing in ingredients if ing is not None]

    def list_ingredients(self) -> list[Ingredient]:
        '''
        List all ingredients filtered by requested days. Merge duplicates,
        align alphabetically.

        Returns:
            list[Ingredient]: example:[Ingredient(...), ...]
        '''
        filtered_ingredients = {}

        for k, v in self.data.menu.items():
            day_num = int(k[3])

            if day_num in self.days:
                filtered_ingredients[k] = v

        ingredients: list[Ingredient] = [
            ing for _, ings in filtered_ingredients.items() for ing in ings
        ]
        return self._merge_duplicates(ingredients)

    def get_empty_instock_list(self) -> list[Ingredient]:
        '''Return Ingredient obj list with no quantity values.

        This empty ingredient list is used to be filled out manually
        when counting what's in stock in pantry. After it is filled-out
        it is used in calculating final order of ingredients.

        Returns:
            list: list of Ingredient objs without quantity values.
        '''
        stock: list[Ingredient] = copy.deepcopy(self._ingredients_processed)

        for i in stock:
            i.quantity = ''  # type: ignore

        return stock

    def get_order_list(self, stock_in_path: Path) -> list[Ingredient]:
        ''' Calculate how much of the ingredients to order.

        Gets stock, days, people and calculate how much of produce to order.
        This funcion also looks for "instock" CSV file. It checks it to
        see if there are already any leftover ingredients in pantry. If
        it finds any: it takes them out from the main order list.

        Returns:
            list[Ingredient]: of what and how much to order.
        '''
        required_ingredients: list[Ingredient] = self._ingredients_processed
        instock_ingredients = self.data.read_csv(stock_in_path)

        if len(required_ingredients) != len(instock_ingredients):
            raise ValueError(
                f'Length of `{stock_in_path}` and current order doesn\'t '
                f'match. Make sure that `{stock_in_path}` was generated using'
                'same days nd people values as is used now.')

        processed_ingredients: list[Ingredient] = []

        for ingr in required_ingredients:
            ingr.quantity *= self.people
            for stock_ingr in instock_ingredients:
                if new_ingr := self._compare_ingredients(
                    ingr, stock_ingr, subtract=True
                ):
                    processed_ingredients.append(new_ingr)

        for i in processed_ingredients:
            i.quantity = round(i.quantity, 2)

        return processed_ingredients


def main() -> None:
    args = docopt(__doc__, version='0.01')

    days: list[int] = split_str_to_ints(args['--days'])
    people: int = int(args['--people'])

    data = Data(path=DATA_DIR)
    cp = Calcprods(data, people, days)

    choice: str = ''

    if not args['--nomenu']:
        options: list[str] = ['[1] Generate stock list with empty values',
                              '[2] Calculate ePromo order list',
                              '[3] Get nutritional values']

        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            choice = 'instock'
        elif menu_entry_index == 1:
            choice = 'order'
        elif menu_entry_index == 2:
            choice = 'nutrition'

    if args['--instock']:
        choice = 'instock'
    elif args['--order']:
        choice = 'order'
    elif args['--nutrition']:
        choice = 'nutrition'

    match choice:
        case 'instock':
            instock = cp.get_empty_instock_list()
            data.write_csv(STOCK_OUT_PATH, instock)
            print_list(instock) if args['-v'] >= 1 else ...
        case 'order':
            order = cp.get_order_list(STOCK_IN_PATH)
            data.write_csv(PREP_OUT_PATH, order)
            print_list(order) if args['-v'] >= 1 else ...
        case 'nutrition':
            nu = Nutrition(cp.ingredient_names)
            data.write_csv(NUTRITION_OUT_PATH, nu.nutrition)
            print_list(nu.nutrition) if args['-v'] >= 1 else ...


if __name__ == '__main__':
    main()
