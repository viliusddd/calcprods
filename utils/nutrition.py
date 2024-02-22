from utils.consts import FOOD_API_KEY
from utils.data import Macros
from utils.utils import get_api_response


class Nutrition:
    def __init__(self, names: list[str]) -> None:
        self.names = names
        self.nutrition: list[Macros] = self.get_nutrition()

    def get_nutrition(self) -> list[Macros]:
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

        ingr_with_macros: list[Macros] = []

        for query in self.names:
            if response := get_api_response(url + query, headers):
                if macro := self.assign_macros_to_ingr(response):
                    ingr_with_macros.append(macro)

        return ingr_with_macros

    def assign_macros_to_ingr(self, response: dict[str, list[dict]]) -> Macros | None:
        '''
        Create dict with ingredient and it's macro values, add macros in
        percentages.

        Args:
            response (dict[str, str]): api response from food api.

        Returns:
            dict[str, str] | None: dict with reassgned values, added macros %.
        '''
        for item in response['items']:
            if macroprc := self.count_macros(item):
                macros: str = f'{macroprc[0]:.0f}/{macroprc[1]:.0f}/{macroprc[2]:.0f}'
            else:
                macros = ''

            return Macros(
                name=item['name'],
                calories_kcal=item['calories'],
                carbs_g=item['carbohydrates_total_g'],
                protein_g=item['protein_g'],
                fat_g=item['fat_total_g'],
                macros=macros,
            )
        return None

    def count_macros(self, item: dict[str, str | float]) -> list[float] | None:
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
        return None
