import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import re

web_page = requests.get("https://www.worldometers.info/coronavirus", auth=("user", "pass"))
soup = BeautifulSoup(web_page.text, "html.parser")

# print(soup.prettify())

covid_data = soup.find_all("div", class_="maincounter-number")

print("COVID-19 cases:", covid_data[0].text.strip())
print("COVID-19 deaths:", covid_data[1].text.strip())
print("COVID-19 recoveries:", covid_data[2].text.strip())
print("\n\n")

data = soup.find_all("script", {"type": "text/javascript"})

# for content in data:
#    print(content)

results = soup.find(id="main_table_countries_today")
content = results.find_all("td")
# print(content)

clean_data = ""

for data in content:
    clean_data += data.text.strip() + "|"
    clean_data = clean_data.replace("+", "")
    clean_data = clean_data.replace("N/A", "0")

# print(clean_data)

countries = [
    'usa', 'spain', 'italy', 'france', 'germany', 'uk', 'turkey', 'iran',
    'russia', 'brazil', 'canada', 'belgium', 'netherlands', 'switzerland',
    'india', 'peru', 'portugal', 'ecuador', 'ireland', 'sweden', 'saudi-arabia',
    'israel', 'austria', 'mexico', 'singapore', 'japan', 'chile', 'pakistan',
    'poland', 'romania', 'belarus', 'qatar', 'south-korea', 'united-arab-emirates',
    'indonesia', 'ukraine', 'denmark', 'serbia', 'philippines', 'norway',
    'czech-republic', 'australia', 'dominican-republic', 'bangladesh', 'malaysia',
    'panama', 'colombia', 'finland', 'south-africa', 'egypt', 'morocco', 'argentina',
    'luxembourg', 'moldova', 'algeria', 'kuwait', 'thailand', 'kazakhstan',
    'bahrain', 'hungary', 'greece', 'oman', 'croatia', 'uzbekistan', 'iraq',
    'armenia', 'iceland', 'afghanistan', 'estonia', 'azerbaijan', 'cameroon',
    'bosnia-and-herzegovina', 'ghana', 'new-zealand', 'lithuania', 'slovenia',
    'macedonia', 'slovakia', 'cuba', 'bulgaria', 'nigeria', 'cote-d-ivoire',
    'china-hong-kong-sar', 'djibouti', 'guinea', 'bolivia', 'tunisia', 'latvia',
    'cyprus', 'andorra', 'albania', 'lebanon', 'niger', 'kyrgyzstan', 'costa-rica',
    'senegal', 'honduras', 'burkina-faso', 'uruguay', 'sri-lanka', 'san-marino',
    'channel-islands', 'guatemala', 'georgia', 'democratic-republic-of-the-congo',
    'malta', 'jordan', 'somalia', 'taiwan', 'reunion', 'mayotte', 'mali', 'kenya',
    'jamaica', 'state-of-palestine', 'mauritius', 'venezuela', 'el-salvador',
    'montenegro', 'isle-of-man', 'tanzania', 'viet-nam', 'equatorial-guinea',
    'sudan', 'paraguay', 'maldives', 'congo', 'rwanda', 'faeroe-islands', 'gabon',
    'martinique', 'guadeloupe', 'myanmar', 'gibraltar', 'brunei-darussalam',
    'liberia', 'ethiopia', 'madagascar', 'cambodia', 'trinidad-and-tobago',
    'french-guiana', 'bermuda', 'cabo-verde', 'aruba', 'togo', 'monaco',
    'sierra-leone', 'zambia', 'liechtenstein', 'bahamas', 'barbados', 'uganda',
    'mozambique', 'sint-maarten', 'guyana', 'haiti', 'cayman-islands', 'benin',
    'libya', 'swaziland', 'french-polynesia', 'guinea-bissau', 'nepal', 'chad',
    'china-macao-sar', 'syria', 'eritrea', 'saint-martin', 'mongolia', 'malawi',
    'zimbabwe', 'angola', 'antigua-and-barbuda', 'timor-leste', 'botswana',
    'central-african-republic', 'laos', 'belize', 'fiji', 'grenada', 'new-caledonia',
    'curacao', 'dominica', 'namibia', 'saint-kitts-and-nevis', 'saint-lucia',
    'saint-vincent-and-the-grenadines', 'nicaragua', 'falkland-islands-malvinas',
    'burundi', 'montserrat', 'turks-and-caicos-islands', 'greenland', 'seychelles',
    'gambia', 'suriname', 'holy-see', 'papua-new-guinea', 'mauritania', 'bhutan',
    'british-virgin-islands', 'saint-barthelemy', 'south-sudan', 'western-sahara',
    'caribbean-netherlands', 'sao-tome-and-principe', 'anguilla', 'saint-pierre-and-miquelon',
    'yemen', 'china'
]

for c in countries:
    pattern = c + "[,|\d]*"
    data = re.search(pattern, clean_data, re.IGNORECASE)

    if data is not None:
        print(data.group())

print("\n\n")

# OWID - OurWorldInData.org COVID-19 Cases
owid_df = pd.read_csv("owid-covid-data.csv")

print(owid_df.columns)
print("\n\n")

country_df = owid_df.location.unique()

print(country_df)
print("\n\n")

print(country_df.size)
print("\n\n")

indexer = owid_df[owid_df["location"] == "Kazakhstan"].index

# kaz_tc - Kazakhstan total cases
kaz_tc = owid_df.loc[indexer, "date":"total_cases"]
kaz_tc = kaz_tc.dropna()
kaz_tc.set_index("date", inplace=True)
kaz_tc.plot(figsize=(12, 6))

# moving average - all previous growth in the past through 30 days
kaz_tc.rolling(window=30).mean()["total_cases"].plot()

plt.show()

print(kaz_tc)
print("\n\n")


def plot_covid_data(country, col, plot_ma=False, y_max=200):
    indexer1 = owid_df[owid_df["location"] == country].index
    country_tc = owid_df.loc[indexer1, "date":col]
    country_tc = country_tc.dropna()
    country_tc.set_index("date", inplace=True)
    country_tc.drop(country_tc.columns.difference([col]), 1, inplace=True)
    country_tc.plot(figsize=(12, 6), ylim=[0, y_max])

    if plot_ma:
        country_tc.rolling(window=30).mean()[col].plot()


# Do lockdowns work?
plot_covid_data("Sweden", "new_cases_per_million", True)  # Sweden didn't lockdown
plot_covid_data("Kazakhstan", "new_cases_per_million", True)  # Kazakhstan did lockdown

plt.show()

# How does median age affect death rate?
plot_covid_data("Serbia", "new_deaths_per_million", True, 2.5)  # Serbia has low median age
plot_covid_data("Japan", "new_deaths_per_million", True, 2.5)  # Japan has high median age

plt.show()

# How does obesity affect death rate?
plot_covid_data("United States", "new_deaths_per_million", True, 15)  # United States has high obesity rate
plot_covid_data("Canada", "new_deaths_per_million", True, 15)  # Canada has relatively high obesity rate
plot_covid_data("India", "new_deaths_per_million", True, 15)  # India has low obesity rate
plot_covid_data("Japan", "new_deaths_per_million", True, 15)  # Japan has low obesity rate

plt.show()

# How does diabetes prevalence affect death?
plot_covid_data("United States", "new_deaths_per_million", True, 15)  # United States has high diabetes rate
plot_covid_data("Ireland", "new_deaths_per_million", True, 15)  # Ireland has low diabetes rate

plt.show()

# Does more testing slow death rate?
plot_covid_data("Denmark", "new_deaths_per_million", True, 15)  # Denmark has a lot of testing
plot_covid_data("Mexico", "new_deaths_per_million", True, 15)  # Mexico has a low amount of testing

plt.show()


def scatter_plot(date, col1, col2):
    tot_df = pd.DataFrame(columns=["date", "location", col1, col2])

    for c in country_df:
        temp_df = owid_df[(owid_df["location"] == c) &
                          (owid_df["date"] == date)][["date", "location", col1, col2]]
        tot_df = tot_df.append(temp_df, ignore_index=True).fillna(0)

    tot_df.set_index("date", inplace=True)

    fig = px.scatter(data_frame=tot_df, x=col2,
                     y=col1, color="location", trendline="ols",
                     hover_data=["location"])
    
    fig.show()
    return tot_df


scatter_plot("2021-02-09", "total_deaths_per_million", "aged_70_older")
