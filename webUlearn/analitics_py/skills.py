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

def make_skills(file_name, vacancy):
    output_folder = vacancy[0]

    df = pd.read_csv(file_name, low_memory=False)
    df = df.dropna(subset='key_skills')
    df['Год'] = df['published_at'].str.partition('-')[0].astype(int)

    df_this_job = df.loc[df['name'].str.contains(vacancy[0], flags=re.IGNORECASE, regex=True)]
    for i in range(len(vacancy) - 1):
        df_t = df.loc[df['name'].str.contains(vacancy[i + 1], flags=re.IGNORECASE, regex=True)]
        df_this_job = pd.concat([df_this_job, df_t])

    key_skills = df_this_job['key_skills'].tolist()
    for i in range(len(key_skills)):
        key_skills[i] = key_skills[i].split('\n')

    skills_dict = dict()

    for skills in key_skills:
        for skill in skills:
            if skill in skills_dict:
                skills_dict[skill] = skills_dict[skill] + 1
            else:
                skills_dict[skill] = 1

    skills_df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['Кол-во'])
    skills_df.index.rename('Навык', inplace=True)
    skills_df = skills_df.sort_values(by=['Кол-во'], ascending=False).head(20)
    top20 = skills_df.index.values.tolist()
    print(top20)
    key_skillses = []
    for i in range(2015, 2024):
        df = df_this_job.loc[df_this_job['Год'] == i]
        key_skills = df['key_skills'].tolist()
        key_skillses.append(key_skills)

    table = pd.DataFrame()
    for key_skills in key_skillses:
        for i in range(len(key_skills)):
            key_skills[i] = key_skills[i].split('\n')

        skills_dict = dict()

        for skills in key_skills:
            for skill in skills:
                if skill in skills_dict and skill in top20:
                    skills_dict[skill] = skills_dict[skill] + 1
                else:
                    skills_dict[skill] = 1

        df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['Кол-во'])
        df.index.rename('Навык', inplace=True)
        df = df.reset_index()
        df = df.sort_values(by=['Кол-во'], ascending=False).head(20)
        res = (df
               .assign(n=df.groupby("Навык").cumcount())
               .pivot_table(index="n", columns="Навык", values="Кол-во")
               .rename_axis(None))
        table = pd.concat([table, res])

    table.reset_index()
    table['Год'] = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    max_label_length = 10
    short_top20 = [label[:max_label_length] for label in top20]

    ax = table.plot(x='Год', y=top20)
    ax.legend(short_top20, loc='upper left', fontsize=7)
    fig = ax.get_figure()
    fig.savefig(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\static\images', 'tech-sup.png'), dpi=300)

    # Таблица - навыки
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py', 'skills_by_year.html'), "w")
    html_content = "<table border='1'>\n<tr><th>Год</th>"
    for skill in top20:
        html_content += f"<th>{skill}</th>"
    html_content += "</tr>\n"
    table[top20] = table[top20].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    for index, row in table.iterrows():
        print(row, index)
        html_content += "<tr>"
        html_content += f"<td>{row['Год']}</td>"
        for skill in top20:
            html_content += f"<td>{row[skill]}</td>"
        html_content += "</tr>\n"

    html_content += "</table>"

    text_file.write(html_content)
    text_file.close()

def make_geography_demand(file_name, keywords):
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

    sal_year = df.groupby('Год').aggregate({'Средняя зарплата': "mean"})
    sal_year['Средняя зарплата'] = sal_year['Средняя зарплата'].astype(int)
    sal_count = df.groupby('Год').aggregate({'name': "count"}) \
        .rename(columns={"name": "Количество вакансий"})

    sal_year_job = df_this_job.groupby('Год').aggregate({'Средняя зарплата': "mean"})
    sal_year_job['Средняя зарплата'] = sal_year_job['Средняя зарплата'].astype(int)
    sal_year_job = sal_year_job.rename(columns={"Средняя зарплата": f"Средняя зарплата - {keywords[0]} "})

    sal_count_job = df_this_job.groupby('Год').aggregate({'name': "count"}) \
        .rename(columns={"name": f"Количество вакансий - {keywords[0]} "})

    sal_rate_city = df.groupby('Город').aggregate({'Средняя зарплата': "mean", 'name': 'count'}) \
        .rename(columns={'name': 'Доля вакансий'}) \
        .sort_values('Доля вакансий', ascending=False)
    sal_rate_city['Доля вакансий'] = (sal_rate_city['Доля вакансий'] / (df['salary_currency'].count())).round(4)

    vacancy_rate_city = sal_rate_city.loc[sal_rate_city['Доля вакансий'] > 0.01] \
        .drop(['Средняя зарплата'], axis=1)

    sal_rate_city = sal_rate_city.dropna(subset='Средняя зарплата')
    sal_rate_city['Средняя зарплата'] = sal_rate_city['Средняя зарплата'].astype(int)

    sal_city = sal_rate_city.loc[sal_rate_city['Доля вакансий'] > 0.01] \
        .drop(['Доля вакансий'], axis=1).rename(columns={'Средняя зарплата': 'Уровень зарплат'}) \
        .sort_values('Уровень зарплат', ascending=False)

    sal_city_to_plot = sal_city.head(10)
    sal_city_to_plot.reset_index(inplace=True)

    vac_rate_to_plot = vacancy_rate_city.head(10)
    vac_rate_to_plot.reset_index(inplace=True)
    another_fraction = 1 - vac_rate_to_plot['Доля вакансий'].sum()
    vac_rate_to_plot.loc[len(vac_rate_to_plot.index)] = ['Другие', another_fraction]
    vac_rate_to_plot.reset_index()

    plt.rcParams.update({'font.size': 8})
    plt.rc('legend', fontsize=8)
    ax = sal_year.join(sal_year_job).plot.bar(title='Уровень зарплат по годам')
    ax.figure.savefig(os.path.join(output_folder, 'demend1.png'), dpi=300)

    fig, axes = plt.subplots(nrows=2)
    sal_count.join(sal_count_job).plot.bar(title='Количество вакансий по годам', ax=axes[0])
    axes[0].grid(axis='y')
    sal_count_job.plot.bar(title='Количество вакансий по годам', color=(1, 0.49609375, 0.0546875), ax=axes[1])
    axes[1].grid(axis='y')

    plt.tight_layout()
    fig.savefig(os.path.join(output_folder, 'demend2.png'), dpi=300)
    plt.show()
    fig, ax1 = plt.subplots()
    ax1.barh(sal_city_to_plot['Город'][::-1], sal_city_to_plot['Уровень зарплат'][::-1], color='#FF5733')
    ax1.set_title('Уровень зарплат по городам')
    ax1.tick_params(axis='y', labelsize=6)
    ax1.grid(axis='x')
    plt.tight_layout()
    plt.savefig(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\static\images', 'geography_salary_levels.png'), dpi=300)

    fig, ax2 = plt.subplots()
    colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33C7', '#33C7FF', '#C7FF33', '#FF3362', '#3362FF', '#FFD700',
              '#8B4513', '#00FFFF']
    ax2.pie(x=vac_rate_to_plot['Доля вакансий'], colors=colors, labels=vac_rate_to_plot['Город'],
            textprops={'fontsize': 6})
    ax2.set_title('Доля вакансий по городам')
    plt.tight_layout()
    plt.savefig(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\static\images', 'geography_dolya_vac.png'), dpi=300)
    plt.close()

    # Таблицы
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"geography1_salary_level_general.html"), "w")
    text_file.write(sal_city.to_html())
    text_file.close()
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"geography2_vac_fraction_general.html"), "w")
    text_file.write(vacancy_rate_city.to_html())
    text_file.close()
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"revelance_salary_general.html"), "w")
    text_file.write(sal_year.to_html())
    text_file.close()
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"revelance_salary_by_vac.html"), "w")
    text_file.write(sal_year_job.to_html())
    text_file.close()
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"revelance_num_of_vac_general.html"), "w")
    text_file.write(sal_count.to_html())
    text_file.close()
    text_file = open(os.path.join(r'C:\Users\kosty\PycharmProjects\web\webUlearn\analitics_py',"revelance_num_of_vac.html"), "w")
    text_file.write(sal_count_job.to_html())
    text_file.close()




make_geography_demand(filename, keywords)
make_skills(filename, keywords)