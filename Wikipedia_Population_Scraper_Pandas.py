import pandas as pd
from datetime import datetime as dt
import os
import time

def world_pop_scrape():
    target_url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
    world_pop = pd.read_html(target_url, flavor='bs4')[0]
    world_pop['Rank'] = world_pop['Rank'].str.replace('–','-')
    world_pop['% of world'] = world_pop['% of world'].str.replace('%','')
    world_pop['Country(or dependent territory)'] = world_pop['Country(or dependent territory)'].str.replace('\[.+\]','', regex=True)
    world_pop['Date'] = world_pop['Date'].apply(lambda x: dt.strptime(x,'%d %b %Y'))
    world_pop = world_pop.fillna('0')
    return world_pop

def us_counties():
    target_url = 'https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents'
    counties = pd.read_html(target_url)[0]

    counties['County or equivalent'] = counties['County or equivalent'].str.replace('\[.+\]','', regex=True)
    return counties

def us_states():
    target_url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population'
    columns = ['Current Rank','2010 Rank','State/Territory','2020 Pop.','2010 Pop.','% Change - Population','Absolute Change','Seats in House of Reps.',
           '% of Total House Seats','Pop. Per Electoral Vote','2020 Census Pop. Per Seat','2010 Census Pop. Per Seat',
           'Est. % of Pop - 2020','Est. % of Pop - 2010','% Change - Population Percent','% of Electoral College']

    states = pd.read_html(target_url,flavor='bs4')[0]
    states.columns=columns

    for i in states.columns:
        states[i] = states[i].str.replace('—','-')
    for i in ['2020 Pop.','2010 Pop.']:
        states[i] = states[i].str.replace('\[.+\]','' ,regex=True)
    
    states['Seats in House of Reps.'] = states['Seats in House of Reps.'].str.replace('\(|\*|\)','', regex=True)
    states['Seats in House of Reps.'] = states['Seats in House of Reps.'].apply(lambda x: eval(x))

    return states

print()
start_time = time.time()
today = dt.strftime(dt.now(),'%m-%d-%Y')
world = world_pop_scrape()
counties = us_counties()
states = us_states()

if 'Wikipedia_Data' not in os.listdir():
    os.mkdir('Wikipedia_Data')

try:
    world.to_csv(f"Wikipedia_Data/World_Population_WikiScrape_{today}.csv")
    print('Successfully Wrote World Population Data to /Wikipedia_Data')
except:
    print('*****Failed to Write World Population Data*****')
    pass

try:
    counties.to_csv(f"Wikipedia_Data/US_Counties_Population_WikiScrape_{today}.csv")
    print('Successfully Wrote US County Population Data to /Wikipedia_Data')
except:
    print('*****Failed to Write US County Population Data*****')
    pass

try:
    states.to_csv(f"Wikipedia_Data/US_States_Population_WikiScrape_{today}.csv")
    print('Successfully Wrote US State Population Data to /Wikipedia_Data')
except:
    print('*****Failed to Write World Population Data*****')
end_time = time.time()
print(f"Elapsed Time: {round(end_time - start_time, 2)} Seconds.\n")