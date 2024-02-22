# CalcProds App

## Setup Development Environment

Requires python 3.12
1. Create virtual environment and install requirements:
    ```bash
    python3.12 -m venv .venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```
2. Get free `API` key from `calorieninjas.com` and set it to `FOOD_API_KEY` env var:
    ```bash
    echo 'export FOOD_API_KEY="<your_api_key_goes_here>"' >> ~/.zshrc
    ```
3. Copy files from `example/` to `data/`:
    ```bash
    mkdir data/ && cp -r example/* data/
    ```

## Command Line Interface Help
Generate list of ingredients with the quantity for particular number of days and people. Get the nutrition values of ingredients.
This app is can be used in multiple day retreat kitchens, but it is optimized for Dhamma.org meditation center kitchen, where courses happen multiple times a year.
```
Usage: calcprods [-s|-o|-n] [-p PEOPLE] [-d DAYS] [-vmh]

Try:
  python calcprods.py -p25 -d2-6
  python calcprods.py -p 60 -d 1,2,7 -s --nomenu
  python calcprods.py -nm -v

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
```

> Link to original project repo: `https://github.com/viliusddd/calcprods`