from utils.consts import FOOD_API_KEY
from utils.data import Ingredient
from utils.utils import get_api_response


def get_nutrition(ingredient_list: list[Ingredient]) -> list[dict[str, str]]:
    '''
    Get nutritional values and percentages for ingredients from
    calorieninjas.com api.

    Returns:
        list[dict[str, str]]: example: [{
            'Name': 'basil',
            'Calories kcal': 24.4,
            'Carbs g': 2.0,
            'Protein g': 4.0,
            'Fat g': 0.0,
            'Macros %': '33/67/0'}, {...}
        ]
    '''
    url = 'https://api.calorieninjas.com/v1/nutrition?query='
    headers = {'X-Api-Key': FOOD_API_KEY}

    queries: list[str] = [i.name for i in ingredient_list]
    ingr_with_macros: list[dict[str, str]] = []

    for query in queries:
        if response := get_api_response(url + query, headers):
            if macros := assign_macros_to_ingr(response):
                ingr_with_macros.append(macros)

    return ingr_with_macros


def assign_macros_to_ingr(response: dict[str, str]) -> dict[str, str] | None:
    '''
    Create dict with ingredient and it's macro values, add macros in
    percentages.

    Args:
        response (dict[str, str]): api response from food api.

    Returns:
        dict[str, str] | None: dict with reassgned values, added macros %.
    '''
    for item in response['items']:
        if macro_perc := count_macros(item):
            macros = f'{macro_perc[0]:.0f}/{macro_perc[1]:.0f}/{macro_perc[2]:.0f}'
        else:
            macros = '0%'

        return {
            'Name': item['name'],
            'Calories kcal': item['calories'],
            'Carbs g': item['carbohydrates_total_g'],
            'Protein g': item['protein_g'],
            'Fat g': item['fat_total_g'],
            'Macros %': macros,
        }

def count_macros(item: dict[str, str]) -> list[float] | None:
    '''Calculate carbs, protein and fat percentages.

    Each gram of carbohydrates provides 4 calories, protein 4 and
    fat 9 calories.

    Args:
        item (dict[str, str]): food item and its values.

    Returns:
        list[float] | None: list of macro values in %, e.g. [60, 90, 10].
    '''
    if item['calories']:

        carbs = 4 * float(item['carbohydrates_total_g'])
        protein = 4 * float(item['protein_g'])
        fat = 9 * float(item['fat_total_g'])

        total = carbs + protein + fat

        return [macro * 100 / total for macro in (carbs, protein, fat)]
