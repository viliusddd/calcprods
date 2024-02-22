import requests

from tabulate import tabulate

from utils.data import Data, Ingredient, Macros


def tabulate_data(rows: list[Ingredient] | list[Macros]) -> str:
    rows_dict = Data.obj_to_dict_for_csv(rows)

    colalign = ('right', 'left', 'right', 'right')
    if isinstance(rows[0], Macros):
        colalign = ('right', 'left', 'right', 'right', 'right', 'right', 'right')

    return tabulate(
        rows_dict,
        headers='keys',
        tablefmt='rounded_grid',
        showindex=True,
        colalign=colalign,
    )


def print_list(ingredients: list[Ingredient] | list[Macros]) -> None:
    print(tabulate_data(ingredients))


def split_str_to_ints(digits: str) -> list[int]:
    '''Convert string of numbers to list of numbers.

    Args:
        digits (str): incoming numbers str can be in '1' or '1-5' or
                      '1,2,5' form.

    Raises:
        ValueError: if value is not number(s) and/or can't be split.

    Returns:
        list[int]: of question ids, e.g.: [3] or [1,3,5,6]
    '''
    if digits.isdigit():
        nums: list[int] = [int(digits)]
    elif ',' in digits:
        nums = [int(num) for num in digits.split(',')]
    elif '-' in digits:
        num1, num2 = digits.split('-')
        nums = list(range(int(num1), int(num2) + 1))
    else:
        raise ValueError('Wrong digit or digits range.')

    return nums


def get_api_response(url: str, headers=None) \
        -> dict[str, list[dict[str, str | float]]] | None:
    """
    Connect to chosen api and return json response.

    Args:
        url (str): api url address.
        headers (str | None): headers.

    Returns:
        dict[str, str] | None: response from api.
    """

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f'FAILED: {exc}')
    else:
        return response.json()

    return None
