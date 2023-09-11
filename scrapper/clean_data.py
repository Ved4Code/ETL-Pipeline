import re
def cleandata(data):
    for row in data:
        for i in range(len(row)):
            if isinstance(row[i], str):
                row[i] = row[i].replace('\n', ' ')
    

    for row in data:
        for i, item in enumerate(row):
            if item is None or str(item).strip().lower() == 'none':
                row[i] = 'Unknown'

    
    # Defining a regular expression pattern to match '.' and ',' before the name
    pattern = r'[.,]+\s*([\w]+)'

    # Iterate through the list and remove '.' and ',' before the name
    for row in data:
        for i in range(len(row)):
            if isinstance(row[i], str):
                row[i] = re.sub(pattern, r' \1', row[i])

    
   
    print("Data cleaning done")
    return data
