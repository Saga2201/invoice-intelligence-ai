# import csv
#
#
# def flatten_json(nested_json, parent_key='', separator=' '):
#     """
#     Flattens a nested JSON object.
#
#     :param nested_json: The JSON object to flatten
#     :param parent_key: The base key string (for recursion)
#     :param separator: The string used to separate key levels
#     :return: A flattened dictionary
#     """
#     items = []
#     for k, v in nested_json.items():
#         new_key = f"{parent_key}{separator}{k}" if parent_key else k
#         if isinstance(v, dict):
#             items.extend(flatten_json(v, new_key, separator).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)
#
#
# def json_to_csv(json_data: dict, csv_filename) -> None:
#     """
#     Converts JSON data to a CSV file.
#
#     :param json_data: The JSON data to convert
#     :param csv_filename: The output CSV filename
#     """
#     # Flatten the JSON data
#     flattened_data = flatten_json(json_data)
#
#     # Write to CSV
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=flattened_data.keys())
#         writer.writeheader()
#         writer.writerow(flattened_data)
#
#
# if __name__ == "__main__":
#     # Example JSON Data
#     DATA = {
#         "Name": {
#             "first": "John",
#             "last": "Doe"
#         },
#         "Address": {
#             "first": {
#                 "street": "123 Main St",
#                 "city": "Anytown"
#             },
#             "second": {
#                 "street": "456 Oak Ave",
#                 "city": "Othertown"
#             }
#         },
#         "Phone": "000000000000"
#     }
#
#     # Generate the CSV
#     csv_file_name = "../CSV_service/output.csv"
#     json_to_csv(DATA, csv_file_name)
#     print(f"CSV file '{csv_file_name}' has been created.")


import csv
import os


def flatten_json(nested_json, parent_key='', separator=' '):
    """
    Flattens a nested JSON object.
    :param nested_json: The JSON object to flatten
    :param parent_key: The base key string (for recursion)
    :param separator: The string used to separate key levels
    :return: A flattened dictionary
    """
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, separator).items())
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_csv(json_data: dict, csv_filename) -> None:
    """
    Converts JSON data to a CSV file, updating an existing file if it exists.
    :param json_data: The JSON data to convert
    :param csv_filename: The output CSV filename
    """
    # Flatten the JSON data
    flattened_data = flatten_json(json_data)

    # Read existing data from CSV if file exists
    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            existing_data = list(reader)
            if existing_data:
                # Get the existing header
                existing_fieldnames = reader.fieldnames
            else:
                existing_fieldnames = []
    else:
        existing_data = []
        existing_fieldnames = []

        # Combine existing fieldnames with new fieldnames
    new_fieldnames = list(set(existing_fieldnames).union(flattened_data.keys()))

    # Update existing data with new data
    updated_data = existing_data
    updated_data.append(flattened_data)

    # Write updated data to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=new_fieldnames)
        writer.writeheader()
        for row in updated_data:
            writer.writerow(row)


if __name__ == "__main__":
    # Example JSON Data
    DATA = {
        "Name": {
            "first": "John",
            "last": "Doe"
        },
        "Address": {
            "first": {
                "street": "123 Main St",
                "city": "Anytown"
            },
            "second": {
                "street": "456 Oak Ave",
                "city": "Othertown"
            }
        },
        "Phone": "000000000000"
    }
    # Generate the CSV
    csv_file_name = "../CSV_service/output.csv"
    json_to_csv(DATA, csv_file_name)
    print(f"CSV file '{csv_file_name}' has been updated.")