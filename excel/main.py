import csv

input_file = "excel/sample.csv"
output_file = "excel/result.csv"

sum_prices_list = []

with open(input_file, newline="\n") as f_in:
    reader = csv.reader(f_in)

    with open(output_file, "w", newline="\n") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["product name", "price", "quantitie", "sumPrice"])
        for index, row in enumerate(reader):
            if index == 0:
                continue
            price = int(row[1])
            quantity = int(row[2])
            sum_price = price * quantity
            sum_prices_list.append(sum_price)
            writer.writerow([row[0], price, quantity, sum_price])
            print([row[0], price, quantity, sum_price])

print("Total sum of prices:", sum(sum_prices_list))
