import pandas as pd
import re
import matplotlib.pyplot as plt
import os

keywords = [
    'техподдержка',
    'тех поддержка',
    'technical support engineer',
    'поддержка',
    'support',
    'підтримки',
]

currency_to_rub = {
    "AZN": 54.08,
    "BYR": 28.7,
    "EUR": 101.29,
    "GEL": 34.2,
    "KGS": 1.03,
    "KZT": 0.20,
    "RUR": 1,
    "UAH": 2.45,
    "USD": 91.94,
    "UZS": 0.0074,
}
filename = 'vacancies.csv'

def make_revelance(file_name, keywords):
    output_folder = keywords[0]
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(file_name, low_memory=False)
    df = df.query("salary_currency in @currency_to_rub.keys()") \
        .assign(salary_currency=lambda x: x["salary_currency"].replace(currency_to_rub))
    df['Средняя зарплата'] = (df.salary_from + df.salary_to) * df.salary_currency / 2
    df = df.dropna(subset='Средняя зарплата')
    df['Год'] = df['published_at'].str.partition('-')[0].astype(int)
    df['Город'] = df['area_name']
    df_this_job = df.loc[df['name'].str.contains(keywords[0], flags=re.IGNORECASE, regex=True)]
    for i in range(len(keywords) - 1):
        df_t = df.loc[df['name'].str.contains(keywords[i + 1], flags=re.IGNORECASE, regex=True)]
        df_this_job = pd.concat([df_this_job, df_t])