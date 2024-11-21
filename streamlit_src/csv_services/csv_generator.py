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
    items = json_data["data"].pop("Item") if "Item" in json_data["data"] else None
    flattened_data = flatten_json(json_data)
    basic_info = prepare_basic_info(flattened_data)
    if items:
        prepare_items_and_save_as_csv(items, basic_info.get("invoice_id", None))

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
    new_fieldnames = list(set(existing_fieldnames).union(basic_info.keys()))

    # Update existing data with new data
    updated_data = existing_data
    updated_data.append(basic_info)

    # Write updated data to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=new_fieldnames)
        writer.writeheader()
        for row in updated_data:
            writer.writerow(row)


def prepare_basic_info(flattened_data: dict):
    # Extract basic info
    basic_info = {
        "invoice_id": flattened_data.get("data Invoice Id", ""),
        "customer_name": flattened_data.get("data Customer Name", ""),
        "vendor_name": flattened_data.get("data Vendor Name", ""),
        "sub_total": flattened_data.get("data Subtotal amount", ""),
        "total_amount": flattened_data.get("data Invoice Total amount", ""),
        "invoice_date": flattened_data.get("data Invoice Date", ""),
        "due_date": flattened_data.get("data Due Date", "")
    }

    return basic_info


def prepare_items_and_save_as_csv(items, invoice_id):
    print("PREPARE ITEMS CALLED")
    # Prepare items data
    items_data = []
    if items:
        for item_key, item_value in items.items():
            item_data = {
                "invoice_id": invoice_id,
                "item_name": item_value.get("Description", ""),
                "quantity": item_value.get("Quantity", ""),
                "unit_price": item_value.get("Unit Price")["amount"] if item_value.get("Unit Price") else None,
                "amount": item_value.get("Amount")["amount"] if item_value.get("Amount") else None
            }
            items_data.append(item_data)
    print("Items:", items_data)
    # Write items data to CSV
    if items_data:
        items_csv_filename = "items.csv"
        file_exists = os.path.isfile(items_csv_filename)

        with open(items_csv_filename, mode='a', newline='', encoding='utf-8') as items_csv_file:
            items_fieldnames = ["invoice_id", "item_name", "quantity", "unit_price", "amount"]
            items_writer = csv.DictWriter(items_csv_file, fieldnames=items_fieldnames)

            # Only write the header if the file didn't exist or was empty
            if not file_exists or os.stat(items_csv_filename).st_size == 0:
                items_writer.writeheader()

            for item in items_data:
                items_writer.writerow(item)
            # def prepare_items_and_save_as_csv(items, invoice_id):

#     # Prepare items data
#     items_data = []
#     if items:
#         for item_key, item_value in items.items():
#             item_data = {
#                 "invoice_id": invoice_id,
#                 "item_name": item_value.get("Description", ""),
#                 "quantity": item_value.get("Quantity", ""),
#                 "unit_price": item_value.get("Unit Price")["amount"] if item_value.get("Unit Price") else None,
#                 "amount": item_value.get("Amount")["amount"] if item_value.get("Amount") else None
#             }
#             items_data.append(item_data)
#
#     # Write items data to CSV
#     if items_data:
#         items_csv_filename = f"items.csv"
#         with open(items_csv_filename, mode='w', newline='', encoding='utf-8') as items_csv_file:
#             items_fieldnames = ["invoice_id", "item_name", "quantity", "unit_price", "amount"]
#             items_writer = csv.DictWriter(items_csv_file, fieldnames=items_fieldnames)
#             items_writer.writeheader()
#             for item in items_data:
#                 items_writer.writerow(item)


if __name__ == "__main__":
    # Example JSON Data
    DATA = {
        "data": {
            "Amount Due": {
                "amount": 1102.95,
                "code": "USD"
            },
            "Customer Address": {
                "city": "Pittsburgh",
                "city_district": None,
                "country_region": "United States",
                "house": None,
                "house_number": "1121",
                "level": None,
                "po_box": None,
                "postal_code": "45682",
                "road": "Manhatten Blvd",
                "state": "PA",
                "state_district": None,
                "street_address": "1121 Manhatten Blvd",
                "suburb": None,
                "unit": None
            },
            "Customer Address Recipient": "Michael Auto Depot",
            "Customer Name": "Michael Auto Depot",
            "Due Date": "Thu, 18 Sep 2014 00:00:00 GMT",
            "Invoice Date": "Sat, 06 Sep 2014 00:00:00 GMT",
            "Invoice Id": "208027",
            "Invoice Total": {
                "amount": 1102.95,
                "code": "USD"
            },
            "Item": {
                "Item #1": {
                    "Amount": {
                        "amount": 350,
                        "code": "GBP"
                    },
                    "Description": "Exhaust repair",
                    "Quantity": 1,
                    "Unit Price": {
                        "amount": 350,
                        "code": "GBP"
                    }
                },
                "Item #2": {
                    "Amount": {
                        "amount": 280,
                        "code": "GBP"
                    },
                    "Description": "Front left window glass replaced",
                    "Product Code": "Repair",
                    "Quantity": 1,
                    "Unit Price": {
                        "amount": 280,
                        "code": "GBP"
                    }
                },
                "Item #3": {
                    "Amount": {
                        "amount": 96,
                        "code": "GBP"
                    },
                    "Description": "Front tires changed",
                    "Quantity": 2,
                    "Unit Price": {
                        "amount": 48,
                        "code": "GBP"
                    }
                },
                "Item #4": {
                    "Amount": {
                        "amount": 35,
                        "code": "GBP"
                    },
                    "Description": "Bumper paint touch up",
                    "Product Code": "Repair",
                    "Quantity": 1,
                    "Unit Price": {
                        "amount": 35,
                        "code": "GBP"
                    }
                },
                "Item #5": {
                    "Amount": {
                        "amount": 400,
                        "code": "GBP"
                    },
                    "Description": "New sound system installed",
                    "Product Code": "Detail",
                    "Quantity": 1,
                    "Unit Price": {
                        "amount": 400,
                        "code": "GBP"
                    }
                }
            },
            "Subtotal": {
                "amount": 1161,
                "code": "GBP"
            },
            "Vendor Address": {
                "city": None,
                "city_district": None,
                "country_region": "United States",
                "house": None,
                "house_number": "123",
                "level": None,
                "po_box": None,
                "postal_code": "97315",
                "road": "Ninja Blvd.\nNinjaLand",
                "state": None,
                "state_district": None,
                "street_address": "123 Ninja Blvd.\nNinjaLand",
                "suburb": None,
                "unit": None
            },
            "Vendor Address Recipient": "Ninja Sample",
            "Vendor Name": "ULL\nUPLOAD YOUR LOGO"
        },
        "message": "Image received, processing done"
    }
    # Generate the CSV
    csv_file_name = "output.csv"
    json_to_csv(DATA, csv_file_name)
    print(f"CSV file '{csv_file_name}' has been updated.")
