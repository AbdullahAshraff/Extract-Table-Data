from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime

def extract(url, table_attribs):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = soup.find_all('tbody')[2]
    rows = tables.find_all('tr')
    for row in rows[3:]:
        cells = row.find_all('td')
        country = cells[0].text
        gdp_usd_millions = cells[1].text
        if cells[1].has_attr('colspan'):
            print(cells[1]['colspan'])
        # if gdp_usd_millions != '—':    
        #     data_dict = {
        #         "Country": country,
        #         "GDP_USD_millions": gdp_usd_millions
        #     }
        #     df1 = pd.DataFrame(data_dict, index=[0])
        #     df = pd.concat([df,df1], ignore_index=True)
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)

def log_progress(message):
    timestamp_format = '%Y-%b-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./etl_project_log.txt", "a") as f: 
        f.write(timestamp + ' : ' + message + '\n')



if __name__ == '__main__':
    # Define variables
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    table_attribs = ["Country", "IMF_Forcast", "IMF_year", "WB_Forecast", "WB_year", "UN_forecast", "UN_year"]
    db_name = 'World_Economies.db'
    table_name = 'Countries_by_GDP'
    csv_path = './Countries_by_GDP.csv'

    # Start the ETL process
    log_progress('Preliminaries complete. Initiating ETL process.')

    # Extract data
    df = extract(url, table_attribs)
    log_progress('Data extraction complete. Initiating saving CSV process.')

    # Load data to CSV
    load_to_csv(df, csv_path)
    log_progress('Data saved to CSV file.')
