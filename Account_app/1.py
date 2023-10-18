list_1 = [
    {
        'unique_id': '001',
        'key1': 'AAA',
        'key2': 'BBB',
        'key3': 'EEE'
    },
    {
        'unique_id': '002',
        'key1': 'AAA',
        'key2': 'CCC',
        'key3': 'FFF'
    }
]

list_2 = [
    {
        'unique_id': '001',
        'key1': 'AAA',
        'key3': 'EEE',
    },
    {
        'unique_id': '003',
        'key1': 'AAB',
        'key2': 'EEW',
    },
    {
        'unique_id': '002',
        'key1': 'AAA',
    }
]

# Create a set of unique_id values from each list
unique_ids_1 = {item['unique_id'] for item in list_1}
unique_ids_2 = {item['unique_id'] for item in list_2}

# Find the common unique_ids
common_unique_ids = unique_ids_1.intersection(unique_ids_2)

# Iterate through the dictionaries in both lists for common unique_ids and compare 'key1' values
for unique_id in common_unique_ids:
    dict1 = next(item for item in list_1 if item['unique_id'] == unique_id)
    dict2 = next(item for item in list_2 if item['unique_id'] == unique_id)
    if dict1.get('key1') == dict2.get('key1'):
        print(f"'key1' values match for unique_id {unique_id}")
    else:
        print(f"'key1' values do not match for unique_id {unique_id}")

    

