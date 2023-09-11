import pandas as  pd
def cleandata(data):
    def remove_newlines(cell_value):
        if isinstance(cell_value, str):
            return cell_value.replace('\n', ' ')
        return cell_value

    # Convert the list of lists to a DataFrame
    columns_to_clean = ['Will_write', 'Will_write_down']
    df = pd.DataFrame(data, columns = ['S_N', 'Document_no', 'Document_type', 'Document Office', 'Year', 'Will_write', 'Will_write_down', 'Other_Information', 'Link']) 

    # Apply the remove_newlines function to the specified columns
    # for col in columns_to_clean:
    #     df[col] = df[col].apply(remove_newlines)

    # Convert the "Year" column to datetime
    df['Year'] = pd.to_datetime(df['Year'])

    # Fill missing values in 'Will_write_down' column with 'Unknown'
    df['Will_write_down'].fillna('Unknown', inplace=True)

    # Replace specific characters in 'Will_write' and 'Will_write_down' columns
    df['Will_write'] = df['Will_write'].str.replace(' . ,', '')
    df['Will_write_down'] = df['Will_write_down'].str.replace(' . ,', '')
    print("Data cleaning done")
    return df

# data=cleandata(data)
# import pandas as pd

# def cleandata(data):
#     def remove_newlines(cell_value):
#         if isinstance(cell_value, str):
#             return cell_value.replace('\n', ' ')
#         return cell_value


#     columns_to_clean = ['Will_write', 'Will_write_down']

#     # Creating a dictionary with column-specific functions
#     column_converters = {col: remove_newlines for col in columns_to_clean}

#     # Loading the CSV file into a DataFrame with column-specific conversions
#     df = pd.read_csv('scrapped_table.csv', converters=column_converters)
#     df.drop(df.columns[[0]], axis=1, inplace=True)

#     df["Year"] = pd.to_datetime(df["Year"])

#     df['Will_write_down'].fillna('Unknown', inplace=True)

#     df['Will_write'] = df['Will_write'].str.replace(' . ,', '')
#     df['Will_write_down'] = df['Will_write_down'].str.replace(' . ,', '')
