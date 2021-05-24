from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import datetime
import time

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
    counties_dataframe['State'] = counties_dataframe['State'].apply(lambda x: 'Hawaii' if x.startswith('Hawai') else x)
    return counties_dataframe

# --------------------------------------------------------------------------------------------------------------------------------
def US_States_Scrape():
    target_url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population'
    page = requests.get(target_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_data = soup.find(class_="wikitable sortable")
    rows = table_data.find_all('tr')

    Us_States = {
    'Rank_2020':[],
    'Rank_2010':[],
    'State':[],
    '2020 Pop.':[],
    '2010 Pop.':[],
    'Pop_Change_%':[],
    'Pop_Change_#':[],
    'House Rep. Seats':[],
    '% of Total Seats':[],
    'Pop. Per Electoral Vote':[],
    'Census_Pop_Per_Seat_2020':[],
    'Census_Pop_Per_Seat_2010':[],
    '% of Total Pop. 2020': [],
    '% of Total Pop. 2010': [],
    '% of Total Pop. Change': [],
    '% of Electoral College': []
    }

    for i in rows[2:]:
        row_data = i.find_all('td')
        data_list = [x.text.strip('\n') for x in row_data]
        
        Us_States['Rank_2020'].append(data_list[0])
        Us_States['Rank_2010'].append(data_list[0])
        Us_States['State'].append(data_list[2])
        Us_States['2020 Pop.'].append(data_list[3])
        Us_States['2010 Pop.'].append(data_list[4])
        Us_States['Pop_Change_%'].append(data_list[5])
        Us_States['Pop_Change_#'].append(data_list[6])
        Us_States['House Rep. Seats'].append(data_list[7])
        Us_States['% of Total Seats'].append(data_list[8])
        Us_States['Pop. Per Electoral Vote'].append(data_list[9])
        Us_States['Census_Pop_Per_Seat_2020'].append(data_list[10])
        Us_States['Census_Pop_Per_Seat_2010'].append(data_list[11])
        Us_States['% of Total Pop. 2020'].append(data_list[12])
        Us_States['% of Total Pop. 2010'].append(data_list[13])
        Us_States['% of Total Pop. Change'].append(data_list[14])
        Us_States['% of Electoral College'].append(data_list[15])
    
    #creating the dataframe
    US_States_DF = pd.DataFrame(Us_States)

    for i in ['Pop_Change_%','Pop_Change_#','% of Total Seats','% of Total Pop. Change']:
        US_States_DF[i] = US_States_DF[i].str.replace('–‍','-').apply(lambda x: x.replace('–','-'))

    #cleaning string characters - adding 0's and eliminating en dashes
    US_States_DF['Pop. Per Electoral Vote'] = US_States_DF['Pop. Per Electoral Vote'].str.replace('—','0')
    US_States_DF['% of Total Seats'] = US_States_DF['% of Total Seats'].str.replace('—','0.0%')
    US_States_DF['% of Electoral College'] = US_States_DF['% of Electoral College'].str.replace('—','0.0%')
    US_States_DF['% of Total Pop. 2020'] = US_States_DF['% of Total Pop. 2020'].str.replace('—','0.0%')
    US_States_DF['% of Total Pop. 2010'] = US_States_DF['% of Total Pop. 2010'].str.replace('—','0.0%')
    US_States_DF['% of Total Seats'] = ['0.0%' if len(i)==0 else i for i in US_States_DF['% of Total Seats']]
    US_States_DF['State'] = US_States_DF['State'].str.replace('\xa0','')
        
    #handling superscripts
    US_States_DF['2020 Pop.'] = US_States_DF['2020 Pop.'].str.replace('\[.+\]','',regex=True).apply(lambda x: x.replace(',',''))
    US_States_DF['2010 Pop.'] = US_States_DF['2010 Pop.'].str.replace('\[.+\]','',regex=True).apply(lambda x: x.replace(',',''))

    US_States_DF['Pop. Per Electoral Vote'] = US_States_DF['Pop. Per Electoral Vote'].str.replace(',','')

    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].apply(lambda x: x.replace('*','')).apply(lambda x: x.replace(' ',''))
    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].apply(lambda x: x.replace('(','')).apply(lambda x: x.replace(')',''))

    US_States_DF['House Rep. Seats'] = US_States_DF['House Rep. Seats'].apply(lambda x: eval(x))
    
    return US_States_DF

# --------------------------------------------------------------------------------------------------------------------------------

def world_population_scrape():
    target_url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
    
    page = requests.get(target_url)
    soup = BeautifulSoup(page.content, 'html5lib')
    
    whole_table = soup.find(class_="wikitable sortable plainrowheaders")
    columns = whole_table.find_all('th')

# Dict comprehension for dictionary output
    col = [v.text.strip('\n') for v in columns[:6]]
    table_to_df = {v.text.strip('\n'):[] for k,v in enumerate(columns[:6])}

    rows = whole_table.find_all('tr')
    for i in rows[1:]:
        result = i.text.split('\n')
        if len(result)==10:
            result.pop(6)
        if result[2]=='\xa0World':
            break
        
        table_to_df[col[0]].append(result[1])
        table_to_df[col[1]].append(result[3].strip('\xa0'))
        table_to_df[col[2]].append(result[4])
        table_to_df[col[3]].append(result[5])
        table_to_df[col[4]].append(result[6])
        table_to_df[col[5]].append(result[7])
    
    #make dataframe
    world_pop_df = pd.DataFrame(table_to_df)

    #remove superscript
    world_pop_df['Country(or dependent territory)'] = [i.split('[')[0] if '[' in i else i for i in world_pop_df['Country(or dependent territory)']]
    world_pop_df['Source(official or United Nations)'] = [i.split('[')[0] if '[' in i else i for i in world_pop_df['Source(official or United Nations)']]
    world_pop_df['Population'] = world_pop_df['Population'].apply(lambda x: x.replace(',','')).apply(pd.to_numeric)
    world_pop_df['% of world'] = world_pop_df['% of world'].apply(lambda x: x.replace('%','')).apply(pd.to_numeric)
    
    world_pop_df['Rank'] = world_pop_df['Rank'].apply(lambda x: x.replace('–','None'))
    return world_pop_df


# --------------------------------------------------------------------------------------------------------------------------------

# Pulling Data from Wikipedia
print()
start_time = time.time()
counties_df = US_Counties_Scrape()

states_df = US_States_Scrape()

world_df = world_population_scrape()
today = datetime.datetime.strftime(datetime.datetime.now(),'%m-%d-%Y')

counties_output_name = f'US_County_Population_WikiScrape_(BS4)_{today}.csv'
states_output_name = f'US_State_Population_Gov_WikiScrape_(BS4)_{today}.csv'
world_output_name = f'World_Population_WikiScrape_(BS4)_{today}.csv'

if 'Wikipedia_Data' not in os.listdir():
    os.mkdir('Wikipedia_Data')
try:
    world_df.to_csv(f'Wikipedia_Data/{world_output_name}', index=False)
    print('Successfully Wrote World Population Data to /Wikipedia_Data')
except:
    print('*****Failed to Write World Population Data*****')

try:
    counties_df.to_csv(f'Wikipedia_Data/{counties_output_name}', index=False)
    print('Successfully Wrote US County Population Data to /Wikipedia_Data')
except:
    print('*****Failed to Write US County Population Data*****')
    pass

try:
    states_df.to_csv(f'Wikipedia_Data/{states_output_name}', index=False)
    print('Successfully Wrote US State Population Data to /Wikipedia_Data')
except Exception as exc:
    print('*****Failed to Write World Population Data*****')
    print(exc)
    
end_time = time.time()
print(f'Elapsed Time: {round(end_time - start_time,2)} Seconds.\n')