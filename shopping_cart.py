# shopping_cart.py

#from pprint import pprint
import datetime
import os
import pandas
import pprint

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

#import csv

def to_usd(x):
    price_usd = "${0:,.2f}".format(x)
    return price_usd

if __name__ == "__main__":

    # INPUT AND READ CSV FILE TO CREATE PRODUCTS DICTIONARY
    products_filepath = os.path.join(os.path.dirname(__file__), "products.csv")
    df = pandas.read_csv(products_filepath)
    products = df.to_dict("records")
    
    #with open(products_filepath, "r") as products_list: # "r" means "open the file for reading"
    #    products = csv.DictReader(products_list) # assuming your CSV has headers

 #products - hard coded 
    #products = [
    #{"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    #{"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    #{"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    #{"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    #{"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    #{"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    #{"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    #{"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    #{"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    #{"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    #{"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    #{"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    #{"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    #{"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    #{"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    #{"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    #{"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    #{"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    #{"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    #{"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
    #] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017
#

    # TODO: write some Python code here to produce the desired output

    # Capturing User Inputs

    # DEFINE USER INPUTS
    subtotal = 0
    tax = 0
    total = 0
    selected_items = [] # CREATE LIST OF INPUTS
    valid_ids = [str(p["id"]) for p in products]
    # VALIDATE INPUTS 
    while True:
        selected_item = input("Please input a product identifier, or DONE if there are no more items: ")
        if selected_item == "DONE":
            break
        elif str(selected_item) in valid_ids:
            selected_items.append(selected_item)
        else:
            print()
            print("OOPS, this item does not exist. Please enter a new identifier.")
            print()
            next
    # Info Display/Output#
    # PRINT RECEIPT
    print("---------------------------------")
    print("PYTHON MARKET")
    print("WWW.PYTHONMARKET.COM")
    print("---------------------------------")
    checkout = datetime.datetime.now()
    print("CHECKOUT AT: " + str(checkout.strftime("%Y-%m-%d %I:%M %p"))) # https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/ date time format
    print("---------------------------------")
    print("SELECTED PRODUCTS:")
    # CALCULATE LIST OF PRODUCTS SELECTED AND TOTALS
        
    for selected_item in selected_items:
        matching_products = [p for p in products if str(p["id"]) == str(selected_item)]
        matching_product = matching_products[0]
        subtotal = subtotal + matching_product["price"]
        tax = subtotal * 0.0875 
        total = subtotal + tax
        print("... " + matching_product["name"] + " " + "(" + to_usd((matching_product["price"])) + ")")

    print("---------------------------------")
    print("SUBTOTAL: " + to_usd((subtotal)))
    print("TAX: " + to_usd((tax)))
    print("TOTAL: " + to_usd((total)))
    print("---------------------------------")
    print("THANK YOU, SEE YOU AGAIN SOON!")
    print("---------------------------------")
    print_receipt = input("Would you like an email receipt? y/n: ")
    # SEND RECEIPT
    if print_receipt == "y":
        template_data = {
            "total": str(to_usd(total)),
            "checkout": str(checkout.strftime("%Y-%m-%d %I:%M %p")),
            "products":[
                {"id":1, "name": "Product 1"},
                {"id":2, "name": "Product 2"},
                {"id":3, "name": "Product 3"},
                {"id":2, "name": "Product 2"},
                {"id":1, "name": "Product 1"}
            ]          
}
        client = SendGridAPIClient(SENDGRID_API_KEY)
        print("CLIENT:", type(client))
        recipient = input("Enter an email address. ")
        message = Mail(from_email=MY_ADDRESS, to_emails=recipient)
        print("MESSAGE:", type(message))

        message.template_id = SENDGRID_TEMPLATE_ID

        message.dynamic_template_data = template_data

#       EMAIL TEMPLATE HARD CODED 
        #client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
        #print("CLIENT:", type(client))
        #subject = "Your Receipt from the Green Grocery Store"
        #recepient = input("Enter an email address. ")
        #html_content = "You're the bomb :)"
        #print("HTML:", html_content)
        #message = Mail(from_email=MY_ADDRESS, to_emails=recepient, subject=subject, html_content=html_content)
#
        try:
            response = client.send(message)
            print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
            print(response.status_code) #> 202 indicates SUCCESS
            print(response.body)
            print(response.headers)
            print("Email successfully sent.")

        except Exception as e:
            print("OOPS", e.message)
    else:
        print("THANK YOU")
        exit





# Write a program that asks the user to input one or more product identifiers, then looks up the prices for each, then prints an itemized customer receipt including the total amount owed. - DONE
# The program should use one of the provided datastores (see "Data Setup") to represent the store owner's inventory of products and prices. - DONE
# The program should prompt the checkout clerk to input the identifier of each shopping cart item, one at a time. - DONE
# When the clerk inputs a product identifier, the program should validate it, displaying a helpful message like "Hey, are you sure that product identifier is correct? Please try again!" if there are no products matching the given identifier. - DONE
# At any time the clerk should be able to indicate there are no more shopping cart items by inputting the word DONE or otherwise indicating they are done with the process. - DONE

# A grocery store name of your choice - DONE
# A grocery store phone number and/or website URL and/or address of choice - DONE
# The date and time of the beginning of the checkout process, formatted in a human-friendly way (e.g. 2019-06-06 11:31 AM) - DONE
# The name and price of each shopping cart item, price being formatted as US dollars and cents (e.g. $1.50) - DONE
# The total cost of all shopping cart items, formatted as US dollars and cents (e.g. $4.50), calculated as the sum of their prices - DONE
# The amount of tax owed (e.g. $0.39), calculated by multiplying the total cost by a New York City sales tax rate of 8.75% (for the purposes of this project, groceries are not exempt from sales tax) - DONE
# The total amount owed, formatted as US dollars and cents (e.g. $4.89), calculated by adding together the amount of tax owed plus the total cost of all shopping cart items - DONE
# A friendly message thanking the customer and/or encouraging the customer to shop again - DONE