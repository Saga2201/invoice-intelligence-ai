from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generate_invoice(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Basic setup
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, height - 50, "Invoice")

    # Vendor and Customer Info
    c.setFont("Helvetica-Bold", 10)
    vendor_info = f"""From:  
{data['Vendor Address Recipient']}  
{data['Vendor Name']}  
{data['Vendor Address']['street_address']}  
"""

    customer_info = f"""To:  
{data['Customer Address Recipient']}  
{data['Customer Name']}  
{data['Customer Address']['street_address']}  
{data['Customer Address']['city']}, {data['Customer Address']['state']} {data['Customer Address']['postal_code']}  
{data['Customer Address']['country_region']}  
"""

    c.drawString(50, height - 100, vendor_info)
    c.drawString(300, height - 100, customer_info)

    # Invoice details
    details = f"""Invoice ID: {data['Invoice Id']}  
Invoice Date: {data['Invoice Date']}  
Due Date: {data['Due Date']}  
Amount Due: {data['Amount Due']['amount']} {data['Amount Due']['code']}  
"""

    c.drawString(50, height - 200, details)

    # Items table headers
    c.setFont("Helvetica-Bold", 10)
    table_headers = ['Item', 'Description', 'Quantity', 'Unit Price', 'Amount']
    x_positions = [50, 150, 350, 400, 460]
    y_position = height - 240
    for x_pos, header in zip(x_positions, table_headers):
        c.drawString(x_pos, y_position, header)

        # Items
    c.setFont("Helvetica", 9)
    y_position -= 20
    for item_name, item in data['Item'].items():
        c.drawString(x_positions[0], y_position, item_name)
        c.drawString(x_positions[1], y_position, item['Description'])
        c.drawString(x_positions[2], y_position, str(item['Quantity']))
        c.drawString(x_positions[3], y_position, f"{item['Unit Price']['amount']} {item['Unit Price']['code']}")
        c.drawString(x_positions[4], y_position, f"{item['Amount']['amount']} {item['Amount']['code']}")
        y_position -= 20

        # Subtotal and Amount Due
    y_position -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_positions[0], y_position, "Subtotal:")
    c.drawString(x_positions[4], y_position, f"{data['Subtotal']['amount']} {data['Subtotal']['code']}")

    y_position -= 20
    c.drawString(x_positions[0], y_position, "Amount Due:")
    c.drawString(x_positions[4], y_position, f"{data['Amount Due']['amount']} {data['Amount Due']['code']}")

    # Footer
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 50, "Thank you for your business!")

    c.save()


# Assuming the provided data is stored in the `invoice_data` variable
if __name__ == "__main__":
    invoice_data = {
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
    filename = "invoice.pdf"
    generate_invoice(invoice_data['data'], filename)
