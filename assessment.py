import sqlite3

db_file = "C:/Users/pinix/OneDrive/Ambiente de Trabalho/Solent/Year 1/2 Semester/" \
          "COM417 - Databases/Assessment/Assessment.db"
db = sqlite3.connect(db_file)
cursor = db.cursor()


def menu():
    print("\nORINOCO – SHOPPER MAIN MENU")
    print(50 * "-")
    print("\n1.	 Display your order history"
          "\n2.   Add an item to your basket"
          "\n3.   View your basket"
          "\n4.   Change the quantity of an item in your basket"
          "\n5.   Remove an item from your basket"
          "\n6.   Checkout"
          "\n7.   Exit\n")
    option = int(input("Please choose an option:"))
    return option


def check_basket(shopper):
    basket_query = "SELECT basket_id\
                            FROM shopper_baskets\
                            WHERE shopper_id = ?\
                            AND DATE(basket_created_date_time) = DATE('now')\
                            ORDER BY basket_created_date_time DESC\
                            LIMIT 1"
    cursor.execute(basket_query, (shopper,))
    basket = cursor.fetchone()
    basketid = None
    if basket is not None:
        basketid = basket[0]
    return basketid


def option_1(shopper):
    order_history = f"SELECT so.order_id, order_date,product_description, seller_name,\
                             price, quantity, ordered_product_status\
                FROM shoppers s\
                    INNER JOIN shopper_orders so ON so.shopper_id = s.shopper_id\
                    INNER JOIN ordered_products op ON op.order_id = so.order_id\
                    INNER JOIN products p ON op.product_id = p.product_id\
                    INNER JOIN sellers ON op.seller_id = sellers.seller_id\
                WHERE s.shopper_id = {shopper}\
                ORDER BY order_date DESC"
    cursor.execute(order_history)
    all_rows = cursor.fetchall()

    if all_rows:
        print("{0:7}\t{1:8}\t{2:45}\t{3:18}\t{4:8}\t{5:2}\t{6:8}".format("OrderID", "Order Date",
              "Product Description", "Seller", "Price", "Qty", "Status"))
        for order in all_rows:
            orderid = order[0]
            orderdate = order[1]
            proddes = order[2]
            seller = order[3]
            price = order[4]
            qty = order[5]
            status = order[6]
            print("{0:7}\t{1:8}\t{2:45}\t{3:18}\t£{4:8.2f}\t{5:3}\t{6:8}".format(orderid, orderdate,
                  proddes, seller, price, qty, status))
    else:
        print("No orders placed by this customer")
    return


def option_2(shopper, basketid):
    category = "SELECT category_id, category_description\
                FROM categories\
                ORDER BY category_description Asc"
    cursor.execute(category)
    all_rows_categories = cursor.fetchall()
    category_id = display_options(all_rows_categories, "Product Categories", "product category")
    product = "SELECT product_id, product_description\
               FROM products\
               WHERE category_id = ?\
               ORDER BY product_description Asc"
    cursor.execute(product, (category_id,))
    all_rows_products = cursor.fetchall()
    product_id = display_options(all_rows_products, "Products", "product")
    seller = "SELECT ps.seller_id, seller_name || PRINTF(' £%.2f',price)\
              FROM product_sellers ps\
                   INNER JOIN sellers ON ps.seller_id = sellers.seller_id\
              WHERE product_id = ?\
              ORDER BY seller_name"
    cursor.execute(seller, (product_id,))
    all_rows_seller = cursor.fetchall()
    seller_id = display_options(all_rows_seller, "Sellers who sell this product", "seller")
    quantity = 0
    while quantity <= 0:
        quantity = int(input("Enter the quantity of the selected product you want to buy: "))
    price_query = "SELECT price\
                   FROM product_sellers ps\
                        INNER JOIN sellers ON ps.seller_id = sellers.seller_id\
                   WHERE product_id = ? AND ps.seller_id = ?"
    cursor.execute(price_query, (product_id, seller_id,))
    price = cursor.fetchone()[0]
    if basketid is None:
        next_basket_id_query = "SELECT seq\
                                FROM sqlite_sequence\
                                WHERE name = 'shopper_baskets'"
        cursor.execute(next_basket_id_query)
        basketid = cursor.fetchone()[0] + 1
        create_basket_query = "INSERT INTO shopper_baskets \
                                    VALUES (?, ?, datetime('now'))"
        cursor.execute(create_basket_query, (basketid, shopper,))
        add_item_query = "INSERT INTO basket_contents \
                               VALUES (?, ?, ?, ?, ?)"
        cursor.execute(add_item_query, (basketid, product_id, seller_id, quantity, price,))
        db.commit()
    else:
        add_item_query = f"INSERT INTO basket_contents \
                                       VALUES ({basketid}, {product_id}, {seller_id}, {quantity}, {price})"
        cursor.execute(add_item_query, (basketid, product_id, seller_id, quantity, price,))
        db.commit()
    print("\n\nItem added to the basket")
    return


def option_3(shopper, basketid):
    if basketid is None:
        print("Your basket is empty")
    else:
        display_basket_query = "SELECT product_description, seller_name, quantity, price, (quantity*price)\
                                FROM basket_contents bc\
                                     INNER JOIN shopper_baskets sb ON sb.basket_id = bc.basket_id\
                                     INNER JOIN products p ON bc.product_id = p.product_id\
                                     INNER JOIN sellers s ON bc.seller_id = s.seller_id \
                                where shopper_id = ? "
        cursor.execute(display_basket_query, (shopper,))
        all_rows = cursor.fetchall()
        print("\nBasket Contents\n"
              "-------------------\n")
        print("{0:7}\t{1:45}\t{2:18}\t{3:8}\t{4:2}".format("Basket Item", "Product Description", "Seller Name",
                                                           "Price", "Total"))
        #for row in all_rows:

    return


def display_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
            code = option[0]
            desc = option[1]
            print("{0}.\t{1}".format(option_num, desc))
            option_num = option_num + 1
            option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
            prompt = "Enter the number against the " + type + " you want to choose: "
            selected_option = int(input(prompt))
    return option_list[selected_option - 1]


def run():
    shopper = int(input("Please enter your shopper ID: "))
    sql_query = "SELECT *\
                 FROM shoppers \
                 WHERE shopper_id = ?"
    cursor.execute(sql_query, (shopper,))
    shop_row = cursor.fetchone()
    basketid = None
    if shopper == shop_row[0]:
        first_name = shop_row[2]
        last_name = shop_row[3]
        print(f"Welcome {first_name} {last_name}!")
        basketid = check_basket(shopper)
        while True:
            option = menu()
            if option == 1:
                option_1(shopper)
            elif option == 2:
                option_2(shopper, basketid)
            elif option == 3:
                option_3(shopper, basketid)
            elif option == 7:
                db.close()
                break

    else:
        print("No shopper was found")
    db.close()


if __name__ == "__main__":
    run()
