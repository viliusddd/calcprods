#! .venv/bin/python3
'''
Generate list of ingredients with the quantity for particular number of
days and people. This app is can be used in multiple day retreat kitchens,
but it is optimized for Dhamma.org meditation center kitchen, where
courses happen multiple times a year.

Usage: calcprods [-os] [-p PEOPLE] [-d DAYS] [--nomenu]

Try:
  python calcprods.py -p 25 -d 2-6
  python calcprods.py -p 60 -d 1,2,7 --nomenu -s

Options:
  -s --instock-list         Generate empty instock list.
  -o --order-list           Generate order list.
  -p --people NUMBER        Number of peaople. [default: 70]
  -d --days NUMBER          Number of days. In 1 or 1-3 or 1,2,5 form.
                            [default: 0-10]
  --nomenu                  Skip menu selection and use switches instead.
'''
import copy

from docopt import docopt
from simple_term_menu import TerminalMenu

from utils.consts import *
from utils.io import Data
from utils.io import Ingredient
from utils.utils import print_out, print_list, split_str_to_ints


type IngredientDict = dict[str, list[Ingredient]]


class Calcprods:
    def __init__(self, data: Data, people: int, days: list[int]) -> None:
        self._data = data
        self._people = people
        self._days = days

    @property
    def data(self) -> Data:
        return self._data

    @property
    def people(self) -> int:
        return self._people

    @property
    def days(self) -> list[int]:
        return self._days

    def _compare_ingredients(self, ingr_a: Ingredient, ingr_b: Ingredient) -> Ingredient | None:
        '''
        Merge same name Ingredient objs.
        '''
        if ingr_b.name == ingr_a.name:
            return Ingredient(
                name=ingr_b.name,
                quantity=round(ingr_b.quantity - ingr_a.quantity, 2),
                unit=ingr_b.unit
            )

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

                if ingredients[j + 1] == None:
                    break

                if new_ingr := self._compare_ingredients(ingredients[j], ingredients[j + 1]):
                    ingredients[j], ingredients[j + 1] = None, new_ingr

                    swapped = True

        return [ing for ing in ingredients if ing != None]

    def filter_by_days(self) -> IngredientDict:
        '''Filter current menu by days: only show days that are requested.

        Args:
            data (IngredientDict): all available days of menu ingredients.

        Returns:
            IngredientDict: only the requested days.
        '''
        new_data = {}
        for day_name, day_val in self.data.menu.items():
            if int(day_name[3]) in self.days:
                new_data[day_name] = day_val
        return new_data

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
        stock: list[Ingredient] = copy.deepcopy(self.list_ingredients())
        for i in stock:
            i.quantity = ''

        return stock

    def get_order_list(self) -> list[Ingredient]:
        ''' Calculate how much of the ingredients to order.

        Gets stock, days, people and calculate how much of produce to order.
        This funcion also looks for "instock" CSV file. It checks it to
        see if there are already any leftover ingredients in pantry. If
        it finds any: it takes them out from the main order list.

        Returns:
            list[Ingredient]: of what and how much to order.
        '''
        required_ingredients: list[Ingredient] = self.list_ingredients()
        instock_ingredients = self.data.read_csv(STOCK_IN_PATH)

        processed_ingredients: list[Ingredient] = []

        for ingr in required_ingredients:
            ingr.quantity *= self.people
            for stock_ingr in instock_ingredients:
                if new_ingr := self._compare_ingredients(stock_ingr, ingr):
                    processed_ingredients.append(new_ingr)

        return processed_ingredients


def main() -> None:
    args = docopt(__doc__, version='0.01')

    days: list[int] = split_str_to_ints(args['--days'])
    people: int = int(args['--people'])

    data = Data(path=DATA_DIR)
    cp = Calcprods(data, people, days)

    if not args['--nomenu']:
        options: list[str] = ['[1] Generate stock list with empty values',
                   '[2] Calculate ePromo order list']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            data.write_csv(STOCK_OUT_PATH, cp.get_empty_instock_list())
        elif menu_entry_index == 1:
            data.write_csv(PREP_OUT_PATH, cp.get_order_list())

    if args['--order-list']:
        data.write_csv(PREP_OUT_PATH, cp.get_order_list())
        # print_list(cp.get_order_list())
    elif args['--instock-list']:
        data.write_csv(STOCK_OUT_PATH, cp.get_empty_instock_list())


if __name__ == '__main__':
    main()
