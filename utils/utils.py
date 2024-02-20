from tabulate import tabulate

from utils.io import Ingredient


def tabulate_data(rows: list[Ingredient]) -> str:
    for row in rows:
        row.unit = row.unit.value

    return tabulate(rows, headers='keys', tablefmt='rounded_grid', showindex=True)


def print_list(input: list[Ingredient]) -> None:
    print(tabulate_data(input))


def print_out(input: dict) -> None:
    for day, products in input.items():
        print(f'{day.capitalize()}:')
        print(tabulate_data(products))


def split_str_to_ints(digits: str) -> list[int]:
    '''Convert string of numbers to list of numbers.

    Args:
        digits (str): incoming numbers str can be in '1' or '1-5' or '1,2,5' form.

    Raises:
        ValueError: if value is not number(s) and/or can't be split.

    Returns:
        list[int]: of question ids, e.g.: [3] or [1,3,5,6]
    '''
    if digits.isdigit():
        nums = [int(digits)]
    elif ',' in digits:
        nums = digits.split(',')
        nums = [int(num) for num in nums]
    elif '-' in digits:
        num1, num2 = digits.split('-')
        nums = list(range(int(num1), int(num2) + 1))
    else:
        raise ValueError('Wrong digit or digits range.')

    return nums