import sqlite3

import assessment

db_file = "C:/Users/pinix/OneDrive/Ambiente de Trabalho/Solent/Year 1/2 Semester/" \
          "COM417 - Databases/Assessment/Assessment.db"
db = sqlite3.connect(db_file)
cursor = db.cursor()
shopper = 10000
get_basket_query = "SELECT product_description, seller_name, quantity, PRINTF('£ %.2f',price),\
                          PRINTF('%.2f',(quantity*price)), p.product_id\
                              FROM basket_contents bc\
                                   INNER JOIN shopper_baskets sb ON sb.basket_id = bc.basket_id\
                                   INNER JOIN products p ON bc.product_id = p.product_id\
                                   INNER JOIN sellers s ON bc.seller_id = s.seller_id \
                              where shopper_id = ? "
cursor.execute(get_basket_query, (shopper,))
all_rows = cursor.fetchall()
assessment.option_3(10000, 4)

selected_option = 0
while selected_option > len(all_rows) or selected_option == 0:
    prompt = "Enter the basket item no. of the item you want to remove: "
    selected_option = int(input(prompt))
    if selected_option > len(all_rows) or selected_option == 0:
        print("The Basket item no. you have entered is not in you basket")
item = all_rows[selected_option - 1]
product = item[5]

confirm = uinput("Do you definitely want to delete this product from your basket (Y/N)? ")
if confirm.upper() == "N":
    return
else
basketid = 4
delete_item = "DELETE from basket_contents\
                 WHERE basket_id = ? AND product_id = ?"
cursor.execute(delete_item, (basketid, product,))
db.commit()
assessment.option_3(10000, 4)
