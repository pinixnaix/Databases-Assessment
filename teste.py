import sqlite3

import assessment

db_file = "C:/Users/pinix/OneDrive/Ambiente de Trabalho/Solent/Year 1/2 Semester/" \
          "COM417 - Databases/Assessment/Assessment.db"
db = sqlite3.connect(db_file)
cursor = db.cursor()
shopper = 10000
display_basket_query = "SELECT product_description, seller_name, quantity, price,\
                                  (quantity*price), p.product_id\
                                      FROM basket_contents bc\
                                           INNER JOIN shopper_baskets sb ON sb.basket_id = bc.basket_id\
                                           INNER JOIN products p ON bc.product_id = p.product_id\
                                           INNER JOIN sellers s ON bc.seller_id = s.seller_id \
                                      where shopper_id = ? "
cursor.execute(display_basket_query, (shopper,))
all_rows = cursor.fetchall()
print("\nBasket Contents\n"
      "----------------\n")
print("{0:7}\t{1:70}\t{2:26}\t{3:5}\t{4:10}\t{5:2}".format("Basket Item", "Product Description", "Seller Name",
                                                           "Qty", "Price", "Total"))
basket_item = 0
total_basket = 0.00
for row in all_rows:
    basket_item += 1
    product_description = row[0]
    seller_name = row[1]
    quantity = row[2]
    price = float(row[3])
    total = float(row[4])
    total_basket += float(total)
    print("{0:11}\t{1:70}\t{2:24}\t{3:4}\t£ {4:5.2f}\t£ {5:1.2f}".format(basket_item, product_description,
                                                                          seller_name,
                                                                           quantity, price, total))
print("\n\t{0:78}\t{1:45}\t£ {2:1.2f}\n".format("", "Basket Total", total_basket))

db.close()
