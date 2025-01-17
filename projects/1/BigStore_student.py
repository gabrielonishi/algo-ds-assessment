from transaction import Transaction

from collections import deque
from customer import Customer, Purchase

import time


def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to complete.")
        return result

    return wrapper


def process_scanner_data_DO_NOT_PROFILE(file_path):
    """
    Process the scanner_data.csv file and create Transaction objects for each valid row.

    Args:
        file_path (str): The path to the scanner_data.csv file.

    Returns:
        list: A list of Transaction objects created from the CSV file.
    """
    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                # Strip leading/trailing whitespace
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip header (assuming it's the first line)
                if line_number == 1 and line.startswith("ID,Date,Customer_ID"):
                    continue

                try:
                    transaction = Transaction.from_csv_row(line)
                    transactions.append(transaction)
                except ValueError as e:
                    print(f"Error processing line {line_number}: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the file: {e}")

    return transactions


# -------------------------------------------------------------------------------------------------------------------

def find_product_index(lookfor,  products_counter) -> int:
    """
        find the product in the list and return the index

    :param products_counter:
    :return:
    """
    for which in range(len(products_counter)):
        if products_counter[which][0] == lookfor:
            return which
    return -1


def process_best_selling_product(transactions) -> str:
    header = "# Best products by sales (product, sales)  \n"
    r = report_best_selling_products(transactions)
    return header + r


def report_best_selling_products(transactions) -> str:

    products_counter = deque()
    for trans in transactions:

        prodName = trans.product
        index = find_product_index(prodName, products_counter)
        if index == -1:  # not found
            products_counter.append(
                (prodName, trans.Quantity, trans.Sales_Amount))
        else:
            assert index < len(products_counter), "impossible"

            record = products_counter[index]
            assert record[0] == prodName
            assert record[1] > 0
            newcount = record[1] + trans.Quantity
            newsales = record[2] + trans.Sales_Amount
            new_record = (prodName,  newcount,  newsales)
            products_counter[index] = new_record

    sorted_by_count = sorted(
        products_counter, key=lambda x: x[1], reverse=True)

    result = f"# number of products sold  = {len(sorted_by_count)}\n"
    assert len(sorted_by_count) > 0, "You don't have any products - some problem. "

    result = ""
    for item in sorted_by_count:
        prodct = item[0]
        # £{ valueCounter[prodct ]:.2f}
        result = result + f"|{prodct}|{item[1]:.0f}|£{item[2]:.2f}\n"
    return result
# ----------------------------------------------------------------


def report_daily_sales(transactions) -> str:
    assert transactions is not None, "No null transaction lists processed "
    header = "# Best products by sales (product, sales)  \n"
    r = process_daily_sales(transactions)
    return header + r


def process_daily_sales(transactions) -> str:
    daily_sales_counter = deque()

    for trans in transactions:

        prodDate = trans.Date

        index = find_product_index(prodDate, daily_sales_counter)
        if index == -1:  # not found
            daily_sales_counter.append(
                (prodDate, trans.Quantity, trans.Sales_Amount))
        else:
            assert index < len(daily_sales_counter), "impossible"

            record = daily_sales_counter[index]
            assert record[0] == prodDate
            assert record[1] > 0
            newcount = record[1] + trans.Quantity
            newsales = record[2] + trans.Sales_Amount
            new_record = (prodDate, newcount, newsales)
            daily_sales_counter[index] = new_record

    sorted_by_count = sorted(
        daily_sales_counter, key=lambda x: x[1], reverse=True)

    result = f"# number of products sold  = {len(sorted_by_count)}\n"
    assert len(sorted_by_count) > 0, "You don't have any products - some problem. "

    result = ""
    for item in sorted_by_count:
        day = item[0]
        number = item[1]
        totalvalue = item[2]
        result = result + f"|{day}|{number:.0f}|£ {totalvalue:.2f}|\n"
    return result

# ==============================================================================


def report_biggest_customers(transactions) -> str:
    header = "# Customers by total expenditure\n"
    r = process_biggest_customers(transactions)
    return header + r


def process_biggest_customers(transactions) -> str:
    # Changing the data structure to a dictionary
    per_cust_counter = dict()

    for trans in transactions:

        custID = trans.Customer_ID

        # Check if the customer is in the dictionary
        # Drop use of find_product_index
        if custID not in per_cust_counter:  # not found
            theCustomer = Customer(trans.Customer_ID)
            per_cust_counter[custID] = theCustomer
            theCustomer.addTransaction(trans)
        else:
            thecust = per_cust_counter[custID]
            assert isinstance(thecust, Customer), "Index error not a customer "
            thecust.addTransaction(trans)
    # end for
    
    table = []
    # Iterate over Customer instances 
    for cust in per_cust_counter.values():
        value = cust.get_total_cost_of_purchases()
        table.append((value, cust.getID()))
        
    sorted_by_count = sorted(table, reverse=True)

    # Code below unchanged
    result = ""
    for item in sorted_by_count:
        total = item[0]
        custname = item[1]
        result = result + f"| ID_{custname} | £{total:.2f} |\n"
    return result + "-----------------"

    # -------------------------------------------------------------------------------------------------------------------


def main_things_to_profile(tranactions):
    """
    Main function to process the scanner_data.csv file and display the transactions.
    """
    
    program_start = time.time()
    
    print("Creating best selling products report")
    start = time.time()
    prod_report = report_best_selling_products(transactions)  # string
    print("Best selling products report took", time.time() - start, "seconds to complete.")
    
    print("Creating daily sales report")
    start = time.time()
    daily_sales = report_daily_sales(transactions)
    print("Daily sales report took", time.time() - start, "seconds to complete.")
    
    print("Creating customer report")
    start = time.time()
    customers = report_biggest_customers(transactions) 
    print("Customer report took", time.time() - start, "seconds to complete.")

    print("Total time taken to process all reports:", time.time() - program_start, "seconds.")
    return prod_report, daily_sales,  customers


if __name__ == "__main__":
    DATA_PATH = 'data/original/'
    file_path = DATA_PATH + 'scanner_data.csv'  # Ensure this path is correct
    transactions = process_scanner_data_DO_NOT_PROFILE(file_path)

    # this is the stuff to profile
    prod_report, daily_sales, customers = main_things_to_profile(transactions)

    # DON'T PROFILE the code below -
    with open(DATA_PATH + "prod_report.csv", "w") as file:
        file.write(prod_report)

    with open(DATA_PATH + "daily_sales.csv", "w") as file:
        file.write(daily_sales)

    with open(DATA_PATH + "best_customers.csv", "w") as file:
        file.write(customers)
