from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def extract(url, table_attribs):
    row_dfs_list = []

    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    tables = soup.find_all("tbody")[2]
    rows = tables.find_all("tr")
    for row in rows[3:]:
        # create a data dict with keys=table_attribs and values=''
        data = {key: "" for key in table_attribs}

        cells = row.find_all("td")
        data_idx = 0

        # loop for setting data dict with their content
        for cell in cells:
            # get content
            content = cell.text.strip()
            if content == "—":
                content = ""

            # save content to data dict
            data_key = table_attribs[data_idx]
            data[data_key] = content

            # skip index if a cell takes more than one column
            if cell.has_attr("colspan"):
                data_idx += int(cell["colspan"])
            else:
                data_idx += 1

        row_df = pd.DataFrame(data, index=[0])
        row_dfs_list.append(row_df)

    df = pd.DataFrame(columns=table_attribs)
    df = pd.concat(row_dfs_list, ignore_index=True)
    return df


def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)


def log_progress(message):
    timestamp_format = "%Y-%b-%d-%H:%M:%S"  # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()  # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("./etl_project_log.txt", "a") as f:
        f.write(timestamp + " : " + message + "\n")


if __name__ == "__main__":
    # Define variables
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    table_attribs = [
        "Country",
        "IMF_forecast",
        "IMF_year",
        "WB_forecast",
        "WB_year",
        "UN_forecast",
        "UN_year",
    ]
    db_name = "World_Economies.db"
    table_name = "Countries_by_GDP"
    csv_path = "./Countries_by_GDP.csv"

    # Start the ETL process
    log_progress("Preliminaries complete. Initiating ETL process.")

    # Extract data
    df = extract(url, table_attribs)
    log_progress("Data extraction complete. Initiating saving CSV process.")

    # Load data to CSV
    load_to_csv(df, csv_path)
    log_progress("Data saved to CSV file.")
