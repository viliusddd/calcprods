# CalcProds 👨🏼‍🍳

Need to feed a small army of meditators? This app calculates everything from carrots to calories, ensuring you have just the right amount of zen in your kitchen!

- [CalcProds 👨🏼‍🍳](#calcprods-)
  - [Features](#features)
  - [TL;DR Setup](#tldr-setup)
  - [File naming convention](#file-naming-convention)
  - [Examples](#examples)
  - [CLI Help](#cli-help)

## Features

- Calculates ingredient quantities based on the number of people and days.
- Fetches nutritional data for ingredients using the CalorieNinjas API.
- Generates order lists and in-stock/inventory lists.
- Accepts flexible day inputs, including single days, ranges, or custom lists.
- Pre-configured for 70 people and 0-10 days by default, with easy customisation.
- Command Line Interface.

## TL;DR Setup

> [!IMPORTANT]
> Requires at least Python 3.12

1. Execute the following:

    ```sh
    git clone git@github.com:viliusddd/calcprods.git && \
    cd calcprods && \
    cp .env.example .env && \
    cp -r example/* data/ && \
    python3.12 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt
    ```
2. Replace the dummy value in `.env`

## File naming convention

- `data/` items should be named in `day<number>.<anysimbol(s)>.csv` or `day<number>.csv` way.
- `<number>` indicates which day ingredients they are and user can choose days with `-d --days` switch.

## Examples

```sh
  ./calcprods.py -p25 -d2-6
  ./calcprods.py -p 60 -d 1,2,7 -s --nomenu
  ./calcprods.py -nm -v
```

## CLI Help

Run the following to get detailed command descriptions and examples:

```sh
./calcprods.py --help
```

<details>
  <summary><b>--help</b> output:</summary>

  <pre>
Generate list of ingredients with the quantity for particular number of days and people. Get the nutrition values of ingredients.
This app is can be used in multiple day retreat kitchens, but it is optimized for Dhamma.org meditation center kitchen, where courses happen multiple times a year.

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
  -v                  Print output table to the terminal.</pre>
