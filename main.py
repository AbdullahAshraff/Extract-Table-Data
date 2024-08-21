from html_to_df import Page

def extract(url):
    return Page(url).get_tables()[2].toDataFrame()


def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)



if __name__ == "__main__":
    # Define variables
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    table_name = "Countries_by_GDP"
    csv_path = "./Countries_by_GDP.csv"

    # Extract data
    df = extract(url)

    # Load data to CSV
    load_to_csv(df, csv_path)
