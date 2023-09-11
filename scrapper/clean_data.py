import pandas as pd

def cleandata(data):
    def remove_newlines(cell_value):
        if isinstance(cell_value, str):
            return cell_value.replace('\n', ' ')
        return cell_value


    columns_to_clean = ['Will_write', 'Will_write_down']

    # Creating a dictionary with column-specific functions
    column_converters = {col: remove_newlines for col in columns_to_clean}

    # Loading the CSV file into a DataFrame with column-specific conversions
    df = pd.read_csv('scrapped_table.csv', converters=column_converters)
    df.drop(df.columns[[0]], axis=1, inplace=True)

    df["Year"] = pd.to_datetime(df["Year"])

    df['Will_write_down'].fillna('Unknown', inplace=True)

    df['Will_write'] = df['Will_write'].str.replace(' . ,', '')
    df['Will_write_down'] = df['Will_write_down'].str.replace(' . ,', '')
