# Wikipedia World / US State / US County Population Scraper

### Purpose
To pull table data from Wikipedia, transform the results, and save them locally to .csv with MAXIMUM effort.</br>
This script takes no user inputs, run either python script in terminal and it will complete in a few seconds.</br>

There are two .py files in this repository:
* Wikipedia_Population_Scraper_Soup.py
* Wikipedia_Population_Scraper_Pandas.py

This project was designed with two purposes in mind:
1. To create a light and reliable script for obtaining population data
2. To investigate performance differences between webscraping with BeautifulSoup and Pandas.read_html

![Capture](https://user-images.githubusercontent.com/14188580/116706393-35a19280-a993-11eb-86ba-a1eb83a57edb.PNG)
<br></br>
### Dependencies
Library | Install
--------|--------
BeautifulSoup| pip install bs4
Pandas| pip install pandas
Requests| pip install requests

</br>
### Results
The following webpages contain population data for the US by State, US by County, and World by Country. By running this script, you will receive filtered and modified copies of the wikitables available below:</br>
[US State Population/Government Data](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population)
![3](https://user-images.githubusercontent.com/14188580/115887729-d6360680-a417-11eb-967d-c5605ac6954f.PNG)
</br>
[US County Population Data](https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents)
![4](https://user-images.githubusercontent.com/14188580/115887739-d8986080-a417-11eb-9d50-5d4aad3bfe49.PNG)
</br>
[World Population Data](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)
![5](https://user-images.githubusercontent.com/14188580/115922069-072b3100-a442-11eb-8e38-d0d1f20da88b.PNG)
</br>
</br>
Output files will be saved in an automatically created directory named /Wikipedia_Data/ <br></br>
#### Samples of .csv Outputs:
![1](https://user-images.githubusercontent.com/14188580/115888845-003bf880-a419-11eb-9fb6-1b5ddbd4eb8a.PNG)

![2](https://user-images.githubusercontent.com/14188580/115885177-4abb7600-a415-11eb-889f-075f251a6370.PNG)

![0](https://user-images.githubusercontent.com/14188580/115922081-0db9a880-a442-11eb-97b5-19e45da7d2b6.PNG)

</br>

## Significance of Current Data - Warning of Future Issues
The most surprising result of writing these scripts is the the speed differences between them.</br>
As seen in the image above, the script based around BeautifulSoup takes ~2sec to complete while Pandas nears 3sec.</br>
The lengths of these scripts is not even close.
* Wikipedia_Population_Scraper_Soup.py ---> 212 Lines of Code
* Wikipedia_Population_Scraper_Pandas.py ---> 73 Lines of Code

While the practical use of each script is not greatly inhibited by an extra half second of processing time, I am surprised that pandas.read_html() takes longer to parse than manually creating a dictionary based on BeautifulSoup.find_all()</br>

## Compatibility - Useability of Data
Looking at US_County Data, I ran all 3245 rows of results through geopy to retrieve Latitude and Longitude coordinates with the goal of determining the useability of data.</br>
</br>
To achieve a complete county coordinate dataset for the lower-48 States, only minor adjustments need to be made.</br>


![plot counties](https://user-images.githubusercontent.com/14188580/119355256-aa05e380-bc6a-11eb-9282-e5286501813f.PNG)
</br>

## Lastly
While Wikipedia may not be the most academically reliable source for data, this script will give anyone a good jumping-off point for State/County based code or analyses.<br>
High traffic Wikipedia pages such as the ones being scraped here are meticulously moderated as well as frequently trolled: [See Wiki History](https://en.wikipedia.org/w/index.php?title=List_of_states_and_territories_of_the_United_States_by_population&action=history)<br></br>

It will be interesting to see if there are significant changes in population data from this source on a day-to-day basis.<br>
Since this script saves each .csv by adding the date it is run, it will be easy to locate data discrepancies.<br></br>

Due to the nature of HTML scraping, this script will not work as intended for BeautifulSoup should a column be added to either WikiTable.<br>
As of 4.29.2021, there are no issues. I will be exploring possible routes for future-proofing that may require the use of every table header.<br></br>


