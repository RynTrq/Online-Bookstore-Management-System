import mysql.connector


def customer_login(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="d2xBYdt2x.a",
            database="shoponize"
        )
        
        cursor = connection.cursor()

        cursor.execute("SELECT password, loginAttempts, isLocked FROM customer WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            print("Username not found")
            return -1
        else:
            db_password, login_attempts, is_locked = result

            if is_locked:
                print("Account is locked")
                return -1

            if db_password != password:
                login_attempts += 1
                if login_attempts > 3:
                    cursor.execute("UPDATE customer SET loginAttempts = %s, isLocked = TRUE WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Maximum number of attempts exceeded, account is locked")
                    return -1
                else:
                    cursor.execute("UPDATE customer SET loginAttempts = %s WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Wrong password")
                    return -1
            else:
                cursor.execute("UPDATE customer SET loginAttempts = 0 WHERE username = %s", (username,))
                connection.commit()
                return 0

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL: ")
        return -1

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def admin_login(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="d2xBYdt2x.a",
            database="shoponize"
        )
        
        cursor = connection.cursor()

        cursor.execute("SELECT password, loginAttempts, isLocked FROM admin WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            print("Username not found")
            return -1
        else:
            db_password, login_attempts, is_locked = result

            if is_locked:
                print("Account is locked")
                return -1

            if db_password != password:
                login_attempts += 1
                if login_attempts > 3:
                    cursor.execute("UPDATE admin SET loginAttempts = %s, isLocked = TRUE WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Maximum number of attempts exceeded, account is locked")
                    return -1
                else:
                    cursor.execute("UPDATE admin SET loginAttempts = %s WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Wrong password")
                    return -1
            else:
                cursor.execute("UPDATE admin SET loginAttempts = 0 WHERE username = %s", (username,))
                connection.commit()
                return 0

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL: ")
        return -1

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def supplier_login(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="d2xBYdt2x.a",
            database="shoponize"
        )
        
        cursor = connection.cursor()

        cursor.execute("SELECT password, loginAttempts, isLocked FROM supplier WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            print("Username not found")
            return -1
        else:
            db_password, login_attempts, is_locked = result

            if is_locked:
                print("Account is locked")
                return -1

            if db_password != password:
                login_attempts += 1
                if login_attempts > 3:
                    cursor.execute("UPDATE supplier SET loginAttempts = %s, isLocked = TRUE WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Maximum number of attempts exceeded, account is locked")
                    return -1
                else:
                    cursor.execute("UPDATE supplier SET loginAttempts = %s WHERE username = %s", (login_attempts, username))
                    connection.commit()
                    print("Wrong password")
                    return -1
            else:
                cursor.execute("UPDATE supplier SET loginAttempts = 0 WHERE username = %s", (username,))
                connection.commit()
                return 0

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL: ")
        return -1

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





def customer_page(username):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="d2xBYdt2x.a",
            database="shoponize"
        )
        
        cursor = connection.cursor()

        query = "SELECT name_first,name_middle,name_last FROM customer WHERE username = %s"
        cursor.execute(query, (username,))

        result = cursor.fetchone()

        name_first , name_middle, name_last = result
        if name_first is None:
            name_first = ""
        if name_middle is None:
            name_middle = ""
        if name_last is None:
            name_last = ""

        print("--------------------")
        print("Welcome " + name_first + " " + name_middle + " " + name_last)
        print("--------------------")

        query = "SELECT customerID FROM customer WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        customer_id = result[0]

#DEFINITIONS OF FUNCTIONS
        def add_to_cart(product_id, quantity):
            query = "SELECT name, price, quantityAvailable FROM product WHERE productID = %s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found")
            else:
                name, price, quantity_available = result
                if quantity > quantity_available:
                    print("Quantity exceeds available stock")
                else:
                    query = "INSERT INTO cart (productID, customerID, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(query, (product_id, customer_id, quantity))
                    print("Added to cart")
                    connection.commit()
        def view_product_details(product_id):
            query = "SELECT name, price, quantityAvailable, description FROM product WHERE productID = %s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found")
            else:
                name, price, quantity_available, description = result
                print("NAME:", name, "     PRICE:", price, "     QUANTITY AVAILABLE:", quantity_available, "     DESCRIPTION:", description)
        def search_products(product_name):
            query = "SELECT productID, name, price FROM product WHERE name = %s"
            cursor.execute(query, (product_name,))
            result = cursor.fetchall()
            if not result:
                print("No products found")
            else:
                for row in result:
                    print("PRDUCT ID:", row[0], "     NAME:", row[1], "     PRICE:", row[2])

                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   Add to cart")
                    print("2.   View product details")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter product ID: ")
                        product_id = int(input())
                        print("Enter quantity: ")
                        quantity = int(input())
                        add_to_cart(product_id, quantity)
                    elif inp == 2:
                        print("Enter product ID: ")
                        product_id = int(input())
                        view_product_details(product_id)
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        


        def remove_from_cart(product_id):
            query = "SELECT productID FROM cart WHERE productID = %s AND customerID = %s"
            cursor.execute(query, (product_id, customer_id))
            result = cursor.fetchone()
            if not result:
                print("Product not found in cart")
            else:
                query = "DELETE FROM cart WHERE productID = %s AND customerID = %s"
                cursor.execute(query, (product_id, customer_id))
                print("Removed from cart")
                connection.commit()
        def checkout():
            query = "SELECT productID, quantity FROM cart WHERE customerID = %s"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchall()
            if not result:
                print("Cart is empty")
            else:
                for row in result:
                    query = "SELECT quantityAvailable FROM product WHERE productID = %s"
                    cursor.execute(query, (row[0],))
                    quantity_available = cursor.fetchone()[0]
                    if row[1] > quantity_available:
                        print("Quantity exceeds available stock for productID:", row[0])
                    else:
                        print("Are you sure you want to place the order for productID:", row[0], " (y/n)")
                        inp = input()
                        if inp == "y":
                            query = "UPDATE product SET quantityAvailable = quantityAvailable - %s WHERE productID = %s"
                            cursor.execute(query, (row[1], row[0]))
                            connection.commit()
                            query = "DELETE FROM cart WHERE productID = %s AND customerID = %s"
                            cursor.execute(query, (row[0], customer_id))
                            connection.commit()
                            print("ProductID:", row[0], " purchased successfully")
                            if quantity_available - row[1] < 3:
                                query = "UPDATE product SET isLowStock = TRUE WHERE productID = %s"
                                cursor.execute(query, (row[0],))
                                connection.commit()
                        else:
                            print("Order for productID:", row[0], " cancelled")
        def view_cart():
            query = "SELECT productID, quantity FROM cart WHERE customerID = %s"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchall()
            if not result:
                print("Cart is empty")
            else:
                for row in result:
                    query = "SELECT name, price FROM product WHERE productID = %s"
                    cursor.execute(query, (row[0],))
                    result = cursor.fetchone()
                    name, price = result
                    print("PRODUCT ID:", row[0], "     NAME:", name, "     PRICE:", price, "     QUANTITY:", row[1])
                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   Remove from cart")
                    print("2.   Checkout")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter product ID: ")
                        product_id = int(input())
                        remove_from_cart(product_id)
                    elif inp == 2:
                        checkout()
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        


        def place_order(product_id, quantity):
            query = "SELECT quantityAvailable FROM product WHERE productID = %s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found")
            else:
                quantity_available = result[0]
                if quantity > quantity_available:
                    print("Quantity exceeds available stock")
                else:
                    print("Are you sure you want to place the order for productID:", product_id, " (y/n)")
                    inp = input()
                    if inp == "y":
                        query = "UPDATE product SET quantityAvailable = quantityAvailable - %s WHERE productID = %s"
                        cursor.execute(query, (quantity, product_id))
                        print("Order placed successfully")
                        connection.commit()
                        if quantity_available - quantity < 3:
                            query = "UPDATE product SET isLowStock = TRUE WHERE productID = %s"
                            cursor.execute(query, (product_id,))
                            connection.commit()
                    else:
                        print("Order for productID:", product_id, " cancelled")



        def view_products_in_category(category_id):
            query = "SELECT productID, name, price FROM product WHERE categoryID = %s"
            cursor.execute(query, (category_id,))
            result = cursor.fetchall()
            if not result:
                print("No products found")
            else:
                for row in result:
                    print("PRODUCT ID:", row[0], "     NAME:", row[1], "     PRICE:", row[2])
                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   Add to cart")
                    print("2.   View product details")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter product ID: ")
                        product_id = int(input())
                        print("Enter quantity: ")
                        quantity = int(input())
                        add_to_cart(product_id, quantity)
                    elif inp == 2:
                        print("Enter product ID: ")
                        product_id = int(input())
                        view_product_details(product_id)
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        def view_category_description(category_id):
            query = "SELECT description FROM productCategory WHERE categoryID = %s"
            cursor.execute(query, (category_id,))
            result = cursor.fetchone()
            if not result:
                print("Category not found")
            else:
                print("DESCRIPTION:", result[0])
        def view_product_categories():
            query = "SELECT categoryID, name FROM productCategory"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                print("No categories found")
            else:
                for row in result:
                    print("CATEGORY ID:", row[0], "     NAME:", row[1])
                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   View products in category")
                    print("2.   View category description")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter category ID: ")
                        category_id = int(input())
                        view_products_in_category(category_id)
                    elif inp == 2:
                        print("Enter category ID: ")
                        category_id = int(input())
                        view_category_description(category_id)
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")



        inp = 0
        while inp != 6:
            print("--------------------")
            print("1.   Search products")
            print("2.   View product categories")
            print("3.   View cart")
            print("4.   Checkout")
            print("5.   Place an Order")
            print("6.   Logout")
            print("--------------------")
            inp = int(input())
            print("--------------------")

            if inp == 1:
                print("Enter product name: ")
                product_name = input()
                search_products(product_name)
            elif inp == 2:
                view_product_categories()
            elif inp == 3:
                view_cart()
            elif inp == 4:
                checkout()
            elif inp == 5:
                print("Enter product ID: ")
                product_id = int(input())
                print("Enter quantity: ")
                quantity = int(input())
                place_order(product_id, quantity)
            elif inp == 6:
                print("Logging out...")
            else:
                print("Invalid input. Please try again.")



    except mysql.connector.Error as error:
        print("Failed to connect to MySQL: ")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





def admin_page(username):
    try:
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="d2xBYdt2x.a",
                database="shoponize"
            )
            
        cursor = connection.cursor()
        query = "SELECT name_first,name_middle,name_last FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        
        result = cursor.fetchone()
        
        name_first , name_middle, name_last = result
        if name_first is None:
            name_first = ""
        if name_middle is None:
            name_middle = ""
        if name_last is None:
            name_last = ""

        print("--------------------")
        print("Welcome " + name_first + " " + name_middle + " " + name_last)
        print("--------------------")

        query = "SELECT adminID FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        admin_id = result[0]


        #Definitions of functions
        def view_orders():
            query = "SELECT orderNumber, customerID, orderDate, AMOUNT, orderStatus FROM orders"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                print("No orders found")
            else:
                for row in result:
                    print("ORDER NUMBER:", row[0], "     CUSTOMER ID:", row[1], "     ORDER DATE:", row[2], "     AMOUNT:", row[3], "     ORDER STATUS:", row[4])
                
                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   Update order status")
                    print("2.   Delete order")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter order number: ")
                        order_number = int(input())
                        print("Enter new order status: ")
                        order_status = input()
                        #First check if order exists
                        query = "SELECT orderNumber FROM orders WHERE orderNumber = %s"
                        cursor.execute(query, (order_number,))
                        result = cursor.fetchone()

                        if not result:
                            print("Order not found")
                        else:
                            query = "UPDATE orders SET orderStatus = %s WHERE orderNumber = %s"
                            cursor.execute(query, (order_status, order_number))
                            connection.commit()
                            print("Order status updated")
                    elif inp == 2:
                        #To delete Order, we have to delete the order from contains table first
                        print("Enter order number: ")
                        order_number = int(input())
                        query = "SELECT orderNumber FROM orders WHERE orderNumber = %s"
                        cursor.execute(query, (order_number,))
                        result = cursor.fetchone()

                        if not result:
                            print("Order not found")
                        else:
                            query = "DELETE FROM contains WHERE orderNumber = %s"
                            cursor.execute(query, (order_number))
                            connection.commit()
                            query = "DELETE FROM orders WHERE orderNumber = %s"
                            cursor.execute(query, (order_number))
                            connection.commit()
                            print("Order deleted")
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        def view_products():
            query = "SELECT productID, name, price, quantityAvailable, isLowStock, categoryID FROM product"
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                print("No products found")
            else:
                for row in result:
                    print("PRODUCT ID:", row[0], "     NAME:", row[1], "     PRICE:", row[2], "     QUANTITY AVAILABLE:", row[3], "     IS LOW STOCK:", row[4], "     CATEGORY ID:", row[5])
                
                inp = 0
                while inp != 6:
                    print("--------------------")
                    print("1.   Update product price")
                    print("2.   Update product description")
                    print("3.   View product review")
                    print("4.   View products low on stock")
                    print("5.   Delete product")
                    print("6.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter product ID: ")
                        product_id = int(input())
                        print("Enter new price: ")
                        price = float(input())
                        query = "SELECT productID FROM product WHERE productID = %s"
                        cursor.execute(query, (product_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Product not found")
                        else:
                            query = "UPDATE product SET price = %s WHERE productID = %s"
                            cursor.execute(query, (price, product_id))
                            connection.commit()
                            print("Price updated")
                    elif inp == 2:
                        print("Enter product ID: ")
                        product_id = int(input())
                        print("Enter new description: ")
                        description = input()
                        query = "SELECT productID FROM product WHERE productID = %s"
                        cursor.execute(query, (product_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Product not found")
                        else:
                            query = "UPDATE product SET description = %s WHERE productID = %s"
                            cursor.execute(query, (description, product_id))
                            connection.commit()
                            print("Description updated")
                    elif inp == 3:
                        print("Enter product ID: ")
                        product_id = int(input())
                        query = "SELECT review FROM product WHERE productID = %s"
                        cursor.execute(query, (product_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Product not found")
                        else:
                            print("REVIEW:", result[0])
                    elif inp == 4:
                        query = "SELECT productID, name, price, quantityAvailable, isLowStock, categoryID FROM product WHERE isLowStock = TRUE"
                        cursor.execute(query)
                        result = cursor.fetchall()

                        if not result:
                            print("No products low on stock")
                        else:
                            for row in result:
                                print("PRODUCT ID:", row[0], "     NAME:", row[1], "     PRICE:", row[2], "     QUANTITY AVAILABLE:", row[3], "     IS LOW STOCK:", row[4], "     CATEGORY ID:", row[5])
                    elif inp == 5:
                        print("Enter product ID: ")
                        product_id = int(input())
                        query = "SELECT productID FROM product WHERE productID = %s"
                        cursor.execute(query, (product_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Product not found")
                        else:
                            query = "DELETE FROM product WHERE productID = %s"
                            cursor.execute(query, (product_id))
                            connection.commit()
                            print("Product deleted")
                    elif inp == 6:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        def view_customers():
            query = "SELECT customerID, name_first, name_middle, name_last, username FROM customer"
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                print("No customers found")
            else:
                for row in result:
                    IDCust, nameFirst, nameMiddle, nameLast, usrN = row 
                    if nameFirst is None:
                        nameFirst = ""
                    if nameMiddle is None:
                        nameMiddle = ""
                    if nameLast is None:
                        nameLast = ""
                    print("CUSTOMER ID:", row[0], "     NAME:", nameFirst, nameMiddle, nameLast, "     Username:", row[4])

                inp = 0
                while inp != 4:
                    print("--------------------")
                    print("1.   View customer orders")
                    print("2.   Delete customer")
                    print("3.   Unlock customer account")
                    print("4.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter customer ID: ")
                        customer_id = int(input())
                        query = "SELECT customerID FROM customer WHERE customerID = %s"
                        cursor.execute(query, (customer_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Customer not found")
                        else:
                            query = "SELECT orderNumber, orderDate, AMOUNT, orderStatus FROM orders WHERE customerID = %s"
                            cursor.execute(query, (customer_id,))
                            result = cursor.fetchall()

                            if not result:
                                print("No orders found")
                            else:
                                for row in result:
                                    print("ORDER NUMBER:", row[0], "     ORDER DATE:", row[1], "     AMOUNT:", row[2], "     ORDER STATUS:", row[3])

                    elif inp == 2:
                        print("Enter customer ID: ")
                        customer_id = int(input())
                        query = "SELECT customerID FROM customer WHERE customerID = %s"
                        cursor.execute(query, (customer_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Customer not found")
                        else:
                            query = "DELETE FROM customer WHERE customerID = %s"
                            cursor.execute(query, (customer_id))
                            connection.commit()
                            print("Customer deleted")
                    elif inp == 3:
                        print("Enter customer ID: ")
                        customer_id = int(input())
                        query = "SELECT customerID FROM customer WHERE customerID = %s"
                        cursor.execute(query, (customer_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Customer not found")
                        else:
                            query = "UPDATE customer SET isLocked = FALSE, loginAttempts = 0 WHERE customerID = %s"
                            cursor.execute(query, (customer_id))
                            connection.commit()
                            print("Customer account unlocked")
                    elif inp == 4:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        def view_suppliers():
            query = "SELECT supplierID, name_first, name_middle, name_last, username FROM supplier"
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                print("No suppliers found")
            else:
                for row in result:
                    IDSup, nameFirst, nameMiddle, nameLast, usrN = row 
                    if nameFirst is None:
                        nameFirst = ""
                    if nameMiddle is None:
                        nameMiddle = ""
                    if nameLast is None:
                        nameLast = ""
                    print("SUPPLIER ID:", row[0], "     NAME:", nameFirst, nameMiddle, nameLast, "     Username:", row[4])
                inp = 0
                while inp != 4:
                    print("--------------------")
                    print("1.   View supplier offers")
                    print("2.   Delete supplier")
                    print("3.   Unlock supplier account")
                    print("4.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter supplier ID: ")
                        supplier_id = int(input())
                        query = "SELECT supplierID FROM supplier WHERE supplierID = %s"
                        cursor.execute(query, (supplier_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Supplier not found")
                        else:
                            query = "SELECT productID, offerPrice FROM supplies WHERE supplierID = %s"
                            cursor.execute(query, (supplier_id,))
                            result = cursor.fetchall()

                            if not result:
                                print("No offers found")
                            else:
                                for row in result:
                                    print("PRODUCT ID:", row[0], "     PRICE:", row[1])
                    elif inp == 2:
                        print("Enter supplier ID: ")
                        supplier_id = int(input())
                        query = "SELECT supplierID FROM supplier WHERE supplierID = %s"
                        cursor.execute(query, (supplier_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Supplier not found")
                        else:
                            query = "DELETE FROM supplier WHERE supplierID = %s"
                            cursor.execute(query, (supplier_id))
                            connection.commit()
                            print("Supplier deleted")
                    elif inp == 3:
                        print("Enter supplier ID: ")
                        supplier_id = int(input())
                        query = "SELECT supplierID FROM supplier WHERE supplierID = %s"
                        cursor.execute(query, (supplier_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("Supplier not found")
                        else:
                            query = "UPDATE supplier SET isLocked = FALSE, loginAttempts = 0 WHERE supplierID = %s"
                            cursor.execute(query, (supplier_id))
                            connection.commit()
                            print("Supplier account unlocked")
                    elif inp == 4:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")
        def view_all_offers():
            query = "SELECT supplierID, productID, offerPrice FROM supplies"
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                print("No offers found")
            else:
                for row in result:
                    print("SUPPLIER ID:", row[0], "     PRODUCT ID:", row[1], "     OFFER PRICE:", row[2])

                inp = 0
                while inp != 3:
                    print("--------------------")
                    print("1.   Delete offer")
                    print("2.   Accept offer and get the stock in the inventory")
                    print("3.   Go back")
                    print("--------------------")
                    inp = int(input())
                    print("--------------------")

                    if inp == 1:
                        print("Enter supplier ID: ")
                        supplier_id = int(input())
                        print("Enter product ID: ")
                        product_id = int(input())
                        query = "SELECT supplierID, productID FROM supplies WHERE supplierID = %s AND productID = %s"
                        cursor.execute(query, (supplier_id, product_id))
                        result = cursor.fetchone()

                        if not result:
                            print("Offer not found")
                        else:
                            query = "DELETE FROM supplies WHERE supplierID = %s AND productID = %s"
                            cursor.execute(query, (supplier_id, product_id))
                            connection.commit()
                            print("Offer deleted")
                    elif inp == 2:
                        print("Enter supplier ID: ")
                        supplier_id = int(input())
                        print("Enter product ID: ")
                        product_id = int(input())
                        query = "SELECT supplierID, productID FROM supplies WHERE supplierID = %s AND productID = %s"
                        cursor.execute(query, (supplier_id, product_id))
                        result = cursor.fetchone()

                        if not result:
                            print("Offer not found")
                        else:
                            query = "SELECT quantity FROM supplies WHERE supplierID = %s AND productID = %s"
                            cursor.execute(query, (supplier_id, product_id))
                            quantity = cursor.fetchone()[0]
                            query = "UPDATE product SET quantityAvailable = quantityAvailable + %s WHERE productID = %s"
                            cursor.execute(query, (quantity, product_id))
                            connection.commit()
                            query = "DELETE FROM supplies WHERE supplierID = %s AND productID = %s"
                            cursor.execute(query, (supplier_id, product_id))
                            connection.commit()
                            print("Offer accepted and stock added to inventory")
                    elif inp == 3:
                        print("Going back...")
                    else:
                        print("Invalid input. Please try again.")

        inp = 0
        while inp != 6:
            print("--------------------")
            print("1.   View orders")
            print("2.   View products")
            print("3.   View customers")
            print("4.   View suppliers")
            print("5.   View all offers by suppliers")
            print("6.   Logout")
            print("--------------------")
            inp = int(input())
            print("--------------------")

            if inp == 1:
                view_orders()
            elif inp == 2:
                view_products()
            elif inp == 3:
                view_customers()
            elif inp == 4:
                view_suppliers()
            elif inp == 5:
                view_all_offers()
            elif inp == 6:
                print("Logging out...")
            else:
                print("Invalid input. Please try again.")

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL: ")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





# def supplier_page(username):
#     try:
#         connection = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="d2xBYdt2x.a",
#                 database="shoponize"
#             )
            
#         cursor = connection.cursor()
#         query = "SELECT name_first,name_middle,name_last FROM supplier WHERE username = %s"
#         cursor.execute(query, (username,))

#         result = cursor.fetchone()

#         name_first , name_middle, name_last = result
#         if name_first is None:
#             name_first = ""
#         if name_middle is None:
#             name_middle = ""
#         if name_last is None:
#             name_last = ""

#         print("--------------------")
#         print("Welcome " + name_first + " " + name_middle + " " + name_last)
#         print("--------------------")

#         query = "SELECT supplierID FROM supplier WHERE username = %s"
#         cursor.execute(query, (username,))
#         result = cursor.fetchone()
#         supplier_id = result[0]

#         inp = 0
#         while inp != 5:
#             print("--------------------")
#             print("1.   View all products.")
#             print("2.   View all required products.")
#             print("3.   Offer a product supply.")
#             print("4.   View all offers made by you.")
#             print("5.   Logout")
#             print("--------------------")
#             inp = int(input())
#             print("--------------------")

#             if inp == 1:
#                 view_all_products()
#             elif inp == 2:
#                 view_required_products()
#             elif inp == 3:
#                 offer_product_supply()
#             elif inp == 4:
#                 view_offers()
#             elif inp == 5:
#                 print("Logging out...")
#             else:
#                 print("Invalid input. Please try again.")

#     except mysql.connector.Error as error:
#         print("Failed to connect to MySQL: ")

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()










def startProgram():
    print("Shoponize Initialized...")

    inp = 0
    while inp != 3:
        print("--------------------")
        print("1.   Enter as a customer")
        print("2.   Enter as an admin")
        #print("3.   Enter as supplier")
        print("3.   Exit")
        print("--------------------")
        inp = int(input())
        print("--------------------")

        if inp == 1:
            print("Enter username: ")
            usr = input()
            print("Enter password: ")
            pwd = input()
            login_result = customer_login(usr, pwd)
            if login_result == 0:
                print("Login successful.")
                customer_page(usr)
            elif login_result == -1:
                print("Login failed")
        elif inp == 2:
            print("Enter username: ")
            usr = input()
            print("Enter password: ")
            pwd = input()
            login_result = admin_login(usr, pwd)
            if login_result == 0:
                print("Admin login successful")
                admin_page(usr)
            elif login_result == -1:
                print("Admin login failed")
        # elif inp == 3:
        #     print("Enter username: ")
        #     usr = input()
        #     print("Enter password: ")
        #     pwd = input()
        #     login_result = supplier_login(usr, pwd)
        #     if login_result == 0:
        #         print("Supplier login successful")
        #     elif login_result == -1:
        #         print("Supplier login failed")
        elif inp == 3:
            print("Thanks for visiting shoponize!")
        else:
            print("Invalid input. Please try again.")

startProgram()