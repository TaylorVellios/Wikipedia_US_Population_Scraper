from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import datetime

def terminal_sep(string):
    dashes = 50 - (len(string)//2)
    x = '-'
    return f"{x*dashes}{string}{x*dashes}"

def date_out():
    x = datetime.datetime.now()
    y = str(x).split()[0].split('-')
    return '_'.join([y[1],y[2],y[0]])

# --------------------------------------------------------------------------------------------------------------------------------
# Scrapes Wikipedia for County Population Data by State - Returns a Dictionary to be Made into a DataFrame
def US_Counties_Scrape():
    target_url = 'https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents'
    page = requests.get(target_url)

    soup = BeautifulSoup(page.content, 'html.parser')


    entire_wikitable = soup.find(class_="wikitable sortable")
    #wikitable_columns = entire_wikitable.find_all('th')
    wikitable_rows = entire_wikitable.find_all('tr')


    counties_in_us = {
        'County':[],
        'Population':[],
        'State':[]
    }

    current_state = ''
    for i in wikitable_rows[1:]:
        objects = [x.text.strip('\n') for x in i.find_all('td')]

        if objects[1].startswith('\xa0') or objects[1].startswith(' '):
            current_state = objects[1].replace('\xa0',' ')
            counties_in_us['County'].append(objects[0])
            counties_in_us['Population'].append(objects[2])
            counties_in_us['State'].append(current_state)
        else:
            counties_in_us['County'].append(objects[0])
            counties_in_us['Population'].append(objects[1])
            counties_in_us['State'].append(current_state)

    counties_dataframe = pd.DataFrame(counties_in_us)

    #removing superscript from some results
    counties_dataframe['County'] = counties_dataframe['County'].str.replace(r'(\[[\d+|\D+]\])', '', regex=True)
    #removing leading whitespace from some <td> values
    counties_dataframe['State'] = [i[1:] if i.startswith(' ') else i for i in counties_dataframe['State']]

    counties_dataframe['Population'] = counties_dataframe['Population'].str.replace(',','')
    counties_dataframe['Population'] = counties_dataframe['Population'].apply(pd.to_numeric)

    return counties_dataframe

# --------------------------------------------------------------------------------------------------------------------------------
def US_States_Scrape():
    target_url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population'
    page = requests.get(target_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_data = soup.find(class_="wikitable sortable")
    rows = table_data.find_all('tr')

    Us_States = {
    'State':[],
    '2020 Pop.':[],
    '2010 Pop.':[],
    'Pop. Change':[],
    'House Rep. Seats':[],
    '% of Total Seats':[],
    'Pop. Per Electoral Vote':[],
    '% of Total Pop. 2020': [],
    '% of Total Pop. 2010': [],
    '% of Electoral College': []
    }

    for i in rows[2:]:
        row_data = i.find_all('td')
        data_list = [x.text.strip('\n') for x in row_data]
        
        Us_States['State'].append(data_list[2])
        Us_States['2020 Pop.'].append(data_list[3])
        Us_States['2010 Pop.'].append(data_list[4])
        Us_States['Pop. Change'].append(data_list[5])
        Us_States['House Rep. Seats'].append(data_list[7])
        Us_States['% of Total Seats'].append(data_list[8])
        Us_States['Pop. Per Electoral Vote'].append(data_list[9])
        Us_States['% of Total Pop. 2020'].append(data_list[12])
        Us_States['% of Total Pop. 2010'].append(data_list[13])
        Us_States['% of Electoral College'].append(data_list[15])
    
    #creating the dataframe
    US_States_DF = pd.DataFrame(Us_States)

    #cleaning string characters - adding 0's and eliminating en dashes
    US_States_DF['Pop. Per Electoral Vote'] = US_States_DF['Pop. Per Electoral Vote'].str.replace('—','0')
    US_States_DF['% of Total Seats'] = US_States_DF['% of Total Seats'].str.replace('—','0.0%')
    US_States_DF['% of Electoral College'] = US_States_DF['% of Electoral College'].str.replace('—','0.0%')
    US_States_DF['% of Total Pop. 2020'] = US_States_DF['% of Total Pop. 2020'].str.replace('—','0.0%')
    US_States_DF['% of Total Pop. 2010'] = US_States_DF['% of Total Pop. 2010'].str.replace('—','0.0%')
    US_States_DF['% of Total Seats'] = ['0.0%' if len(i)==0 else i for i in US_States_DF['% of Total Seats']]
    US_States_DF['State'] = US_States_DF['State'].str.replace('\xa0','')


    #converting all % based columns to floats
    percentage_columns = [i for h,i in enumerate(US_States_DF.columns) if '%' in str(US_States_DF.iloc[2,h])]
    for i in percentage_columns:
        US_States_DF[i] = US_States_DF[i].str.replace('%','').str.replace('–','-').str.replace('\u200d','').apply(pd.to_numeric)

        
    #handling superscripts
    US_States_DF['2020 Pop.'] = [i[:-4] if '[' in i else i for i in US_States_DF['2020 Pop.']]
    US_States_DF['2010 Pop.'] = [i[:-4] if '[' in i else i for i in US_States_DF['2010 Pop.']]

    #converting to numeric values
    US_States_DF['2020 Pop.'] = US_States_DF['2020 Pop.'].str.replace(',','').apply(pd.to_numeric)
    US_States_DF['2010 Pop.'] = US_States_DF['2010 Pop.'].str.replace(',','').apply(pd.to_numeric)
    US_States_DF['Pop. Per Electoral Vote'] = US_States_DF['Pop. Per Electoral Vote'].str.replace(',','').apply(pd.to_numeric)

    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].str.replace('*','').str.replace(' ','')
    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].str.replace('(','').str.replace(')','')

    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].apply(lambda x: eval(x)).apply(pd.to_numeric)

    
    return US_States_DF

# --------------------------------------------------------------------------------------------------------------------------------
# Pulling Data from Wikipedia
counties_df = US_Counties_Scrape()
states_df = US_States_Scrape()

print()
print(terminal_sep('Checking for NaN Values - US Counties'))
print(f'\n{counties_df.isna().sum()}\n\n')


print(terminal_sep('Checking for NaN Values - US States'))
print(f'\n{states_df.isna().sum()}\n\n')


print(terminal_sep('Saving as .csv to /Wikipedia_Data/'))
print()
counties_output_name = f'US_County_Population_WikiScrape_{date_out()}.csv'
states_output_name = f'US_State_Population_Gov_WikiScrape_{date_out()}.csv'


try:
    counties_df.to_csv(f'Wikipedia_Data/{counties_output_name}', index=False)
except:
    os.mkdir('Wikipedia_Data')
    counties_df.to_csv(f'Wikipedia_Data/{counties_output_name}', index=False)

print(f'\nUS_Counties Saved to /Wikipedia_Data/{counties_output_name}\n')

try:
    states_df.to_csv(f'Wikipedia_Data/{states_output_name}', index=False)
except:
    os.mkdir('Wikipedia_Data')
    states_df.to_csv(f'Wikipedia_Data/{states_output_name}', index=False)

print(f'\nUS_States Saved to /Wikipedia_Data/{states_output_name}\n')
