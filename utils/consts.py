import os

from pathlib import Path


DATA_DIR = 'data'
OUTPUT_DIR = 'out'
STOCK_FILENAME = 'instock.csv'
PREP_FILENAME = 'order.csv'

STOCK_IN_PATH = Path(DATA_DIR, STOCK_FILENAME)
PREP_IN_PATH = Path(DATA_DIR, PREP_FILENAME)

STOCK_OUT_PATH = Path(OUTPUT_DIR, STOCK_FILENAME)
PREP_OUT_PATH = Path(OUTPUT_DIR, PREP_FILENAME)

NUTRITION_OUT_PATH = Path(OUTPUT_DIR, 'nutrition.csv')
FOOD_API_KEY = os.getenv('FOOD_API_KEY')