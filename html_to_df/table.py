import pandas as pd


class Table:
    def __init__(self, tableHTML) -> None:
        self.table = tableHTML

    def init_head_body(self):
        self.thead = self.table.find("thead")
        self.tbody = self.table.find("tbody")

    def extractTableHeaders(self):
        table_attribs = [
            "Country",
            "IMF_forecast",
            "IMF_year",
            "WB_forecast",
            "WB_year",
            "UN_forecast",
            "UN_year",
        ]
        self.table_attribs = table_attribs
        return self.table_attribs

    def extractBodyData(self) -> pd.DataFrame:
        table_attribs = self.table_attribs
        row_dfs_list = []
        rows = self.tbody.find_all("tr")
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
        self.df = df
        return df

    def toDataFrame(self):
        self.init_head_body()
        self.extractTableHeaders()
        self.extractBodyData()
        return self.df
