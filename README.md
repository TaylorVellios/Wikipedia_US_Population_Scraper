# Wikipedia US Population Scraper
To pull table data from Wikipedia, transform the results, and save them locally to .csv<br>
This script takes no user inputs, run Wikipedia_US_Population_Scraper.py in terminal and it will complete in a second or two.
<br></br>
### Dependencies
* BeautifulSoup
* Pandas
* Requests
* os

<br></br>
### Purpose
The following webpages contain population data for the United States by State, and by County. By running this script, you will receive filtered and modified copies of the wikitables available below:<br></br>
[US State Population/Government Data](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population)<br></br>
![3](https://user-images.githubusercontent.com/14188580/115887729-d6360680-a417-11eb-967d-c5605ac6954f.PNG)

[US County Population Data](https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents)
![4](https://user-images.githubusercontent.com/14188580/115887739-d8986080-a417-11eb-9d50-5d4aad3bfe49.PNG)

<br></br>
Some columns for US_State_Data on Wikipedia are being ignored for the .csv output. Data reached by simple calculations or sorting can be done by the user.<br>
Output files will be saved in an automatically created directory named /Wikipedia_Data/ <br></br>
#### Samples of .csv Outputs:
![1](https://user-images.githubusercontent.com/14188580/115885169-498a4900-a415-11eb-9748-89a169350743.PNG)
![2](https://user-images.githubusercontent.com/14188580/115885177-4abb7600-a415-11eb-889f-075f251a6370.PNG)
<br></br>

#### Significance of Current Data - Warning of Future Issues
While Wikipedia may not be the most academically reliable source for data, this script will give anyone a good jumping-off point for State/County based code or analyses.<br>
High traffic Wikipedia pages such as the ones being scraped here are meticulously moderated as well as frequently trolled: [See Wiki History](https://en.wikipedia.org/w/index.php?title=List_of_states_and_territories_of_the_United_States_by_population&action=history)<br></br>

Due to the nature of HTML scraping, this script will not work as intended should a column be added to either WikiTable.<br>
As of 4.23.2021, there are no issues. I will be exploring possible routes that may require the use of every table header.
