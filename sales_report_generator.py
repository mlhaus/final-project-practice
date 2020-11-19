from datetime import date
 
def print_header(file_name, todays_date, current_page):
    with open(file_name, "a") as file:
        file.write("\n" + todays_date + (" " * 55) + "Page: " + str(current_page))
        file.write("\n" + (" " * 34) + "SALES REPORT\n")
        file.write("\n" + (" " * 23) + "NAME" + (" " * 23) + "|" + (" " * 5) + "TOTAL" + (" " * 5) + "|" + (" " * 5) + "AVERAGE")
        file.write("\n" + ("-" * 80))
 
def create_blank_file(file_name):
    file = open(file_name, "w")
    file.close()

def print_footer(file_name, total_sales):
    with open(file_name, "a") as file:
        file.write("\n\n" + ("-" * 80) + "\n" + ("-" * 80))
        file.write("\n*** Report Total")
        file.write(" " * (50 - 16)) # Prints spaces to fill column 1
        # file.write("|")
        file.write(f"{total_sales:14,.2f}\n\n\n")
        
def print_division(division_name, sales_data, file_name, line_count, current_page, todays_date):
    with open(file_name, "a") as file:
        division_sales = 0
        file.write("\n** DIVISION: " + division_name + " **")
        line_count += 1
        for sales_person in sales_data:
            if(sales_data[sales_person]["division"] == division_name):
                if(line_count >= 40):
                    current_page += 1
                    print_header(file_name, todays_date, current_page)
                    line_count = 5
                file.write("\n" + sales_person)
                file.write(" " * (50 - len(sales_person)))
                salesperson_total = sales_data[sales_person]["sales_total"]
                division_sales += salesperson_total
                file.write(f"{salesperson_total:14,.2f}")
                salesperson_average = sales_data[sales_person]["sales_average"]
                file.write(f"{salesperson_average:16,.2f}")
                line_count += 1
        file.write("\n\n" + ("-" * 80))
        file.write("\n** Division Total - " + division_name)
        file.write(" " * (50 - 20 - len(division_name)))
        file.write(f"{division_sales:14,.2f}\n\n")
        line_count += 5
        return division_sales, line_count, current_page

def print_report(salespeople_data):
    todays_date = str(date.today())
    current_page = 1
    file_name = todays_date + "_SalesReport.txt"
    create_blank_file(file_name)
    print_header(file_name, todays_date, current_page)
    line_count = 5
    divisions = get_divisions()
    total_sales = 0
    for id in divisions:
        division_sales, line_count, current_page = print_division(divisions[id], salespeople_data, file_name, line_count, current_page, todays_date)
        total_sales += division_sales
    print_footer(file_name, total_sales)

def get_divisions():
    result = {}
    with open("divisions.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            result[data[0]] = data[1]
    return result

def get_salespeople_divisions():
    divisions = get_divisions()
    result = {}
    with open("DivisionSalesPeople.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            division = divisions.get(data[0], "Unknown")
            result[data[1] + ", " + data[2]] = {}
            result[data[1] + ", " + data[2]]["division"] = division
    return result

def get_sales(salespeople_dictionary):
    with open("sales.txt", "r") as file:
        salesperson = ""
        sales_data = []
        for line in file:
            try:
                sales_item = float(line.strip())
                sales_data.append(sales_item)
            except ValueError:
                salesperson = line.strip()
                sales_data = []
                if salesperson in salespeople_dictionary:
                    salespeople_dictionary[salesperson]["sales_data"] = sales_data

def get_sales_total_and_average(salespeople_dictionary):
    for salesperson in salespeople_dictionary:
        total = 0
        count = 0
        for sale_item in salespeople_dictionary[salesperson]["sales_data"]:
            total += sale_item
            count += 1
        salespeople_dictionary[salesperson]["sales_total"] = round(total, 2)
        salespeople_dictionary[salesperson]["sales_average"] = round(total / count, 2)

def main():
    salespeople_data = get_salespeople_divisions()
    get_sales(salespeople_data)
    get_sales_total_and_average(salespeople_data)
    print_report(salespeople_data)

main()