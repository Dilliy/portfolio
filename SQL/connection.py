import psycopg2
from config import HOST, USER, PASSWORD, PORT, db_name
from psycopg2 import sql
from psycopg2 import Error
import csv
try:
    #CONNECTION TO THE DATA BASE
    with psycopg2.connect (
        dbname = db_name,
        user = USER,
        password = PASSWORD,
        port = PORT
    ) as conn:
        conn.autocommit = True
        #CREATION OF CUSTOMERS TABLE WITH CUSTOMERID AS PRIMARY KEY
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {Customer_table}(
                    {CustomerID} serial PRIMARY KEY,
                    {CustomerName} varchar(50) NOT NULL,
                    {CustomerPh} varchar(50) NOT NULL,
                    {CustomerD} date);"""
                ).format(
                    Customer_table = sql.Identifier('customers'),
                    CustomerID = sql.Identifier('CustomerID'),
                    CustomerName = sql.Identifier('CustomerName'),
                    CustomerPh = sql.Identifier('CustomerPhone'),
                    CustomerD = sql.Identifier('CustomerDOB')
                ))
                conn.commit()

            except Error as e:
                conn.rollback()
                print(f'Faile: {e}')
        
        #CREATION OF EMPLOYEES TABLE WITH EMPLOYEEID AS PRIMARY KEY
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {Employees_table}(
                            {EmployeeID} serial PRIMARY KEY,
                            {EmployeeName} varchar(50) NOT NULL,
                            {EmployeeRole} varchar(50) NOT NULL,
                            {EmployeeD} date,
                            {ManagerID} int);"""
                            ).format(
                                Employees_table = sql.Identifier('employees'),
                                EmployeeID = sql.Identifier('EmployeeID'),
                                EmployeeName = sql.Identifier('EmployeeName'),
                                EmployeeRole = sql.Identifier('EmployeeRole'),
                                EmployeeD = sql.Identifier('EmployeeDOB'),
                                ManagerID = sql.Identifier('ManagerID')
                            )
                )
                conn.commit()
            
            except Error as e:
                conn.rollback()
                print(f'Faile: {e}')
        
        #CREATION OF MENU TABLE WITH ITEMID AS PRIMARY KEY
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {Menu_table}(
                            {ItemID} serial PRIMARY KEY,
                            {ItemName} varchar(50) NOT NULL,
                            {Price} float NOT NULL)"""
                            ).format(
                                Menu_table = sql.Identifier('menu'),
                                ItemID = sql.Identifier('ItemID'),
                                ItemName = sql.Identifier('ItemName'),
                                Price = sql.Identifier('Price')
                            )
                )
                conn.commit()
            except Error as e:
                conn.rollback()
                print(f'Faile: {e}')
        #CREATION OF ORDER TABLE WITH ORDERID AS PRIMARY KEY
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {Order_table}(
                            {ID} serial PRIMARY KEY,
                            {Date} date NOT NULL,
                            {Type} varchar(10) NOT NULL,
                            {TableNum} varchar(4),
                            {Payment} varchar(6) NOT NULL,
                            {EmployeeID} int REFERENCES {Employees_table}({EmployeeID}),
                            {CustomerID} int REFERENCES {Customer_table}({CustomerID}))"""
                            ).format(
                                Order_table = sql.Identifier('orders'),
                                ID = sql.Identifier('OrderID'),
                                Date = sql.Identifier('OrderDate'),
                                Type = sql.Identifier('OrdertType'),
                                TableNum = sql.Identifier('Table Number'),
                                Payment = sql.Identifier('Payment'),
                                EmployeeID = sql.Identifier('EmployeeID'),
                                CustomerID = sql.Identifier('CustomerID'),
                                Employees_table = sql.Identifier('employees'),
                                Customer_table = sql.Identifier('customers')
                            )
                )
                conn.commit()
            except Error as e:
                conn.rollback()
                print(f"Failed: {e}")
        #CREATION OF ORDERITEMS TABLE WITH ORDERITEMSID AS PRIMARY KEY
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {Items_table}(
                            {OrderItemID} serial PRIMARY KEY,
                            {OrderID} int REFERENCES {Order_table}({OrderID}),
                            {ItemID} int REFERENCES {Menu_table}({ItemID}),
                            {Quantity} int NOT NULL)"""
                            ).format(
                                Items_table = sql.Identifier('orderitem'),
                                OrderItemID = sql.Identifier('OrderItemID'),
                                OrderID = sql.Identifier('OrderID'),
                                ItemID = sql.Identifier('ItemID'),
                                Quantity = sql.Identifier('Quantity'),
                                Order_table = sql.Identifier('orders'),
                                Menu_table = sql.Identifier('menu'),
                            )
                )
                conn.commit()
            except Error as e:
                conn.rollback()
                print(f"Filed: {e}")
        #INSERT DATA TO MENU TABLE
        try:
            with open('menu.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                with conn.cursor() as cur:
                    for row in reader:
                        try:
                            cur.execute(
                                sql.SQL("""INSERT INTO {Menu_table} ({ItemID},{ItemName},{Price}) VALUES (%s,%s,%s)
                                        ON CONFLICT ({ItemID}) DO UPDATE SET
                                            {ItemName} = EXCLUDED.{ItemName},
                                            {Price} = EXCLUDED.{Price}"""
                                        ).format(
                                            Menu_table = sql.Identifier('menu'),
                                            ItemID = sql.Identifier('ItemID'),
                                            ItemName = sql.Identifier('ItemName'),
                                            Price = sql.Identifier('Price')
                                        ),row
                            )
                        except Error as e:
                            conn.rollback()
                            print(f'CSV insert failed: {e}')
                conn.commit()
                print("Data was iserted to Menu table.")
        except:
            print("CSV file was not found.")
        #INSERT DATA TO CUSTOMER TABLE
        try:
            with open('customers.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                with conn.cursor() as cur:
                    for row in reader:
                        try:
                            cur.execute(
                                sql.SQL("""INSERT INTO {Customer_table} ({CustomerID},{CustomerName},{CustomerPh},{CustomerD}) VALUES (%s,%s,%s,%s)
                                        ON CONFLICT ({CustomerID}) DO UPDATE SET
                                            {CustomerName} = EXCLUDED.{CustomerName},
                                            {CustomerPh} = EXCLUDED.{CustomerPh},
                                            {CustomerD} = EXCLUDED.{CustomerD}"""
                                        ).format(
                                            Customer_table = sql.Identifier('customers'),
                                            CustomerID = sql.Identifier('CustomerID'),
                                            CustomerName = sql.Identifier('CustomerName'),
                                            CustomerPh = sql.Identifier('CustomerPhone'),
                                            CustomerD = sql.Identifier('CustomerDOB')
                                        ),row
                            )
                        except Error as e:
                            conn.rollback()
                            print(f'CSV insert failed: {e}')
                conn.commit()
                print("Data was iserted to Customer table.")
        except:
            print("CSV file was not found.")
        #INSERT DATA TO EMPLOYEE TABLE
        try:
            with open('employees.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                with conn.cursor() as cur:
                    for row in reader:
                        try:
                            cur.execute(
                                sql.SQL("""INSERT INTO {Employees_table} ({EmployeeID},{EmployeeName},{EmployeeRole},{EmployeeD},{ManagerID}) VALUES (%s,%s,%s,%s,%s)
                                        ON CONFLICT ({EmployeeID}) DO UPDATE SET
                                            {EmployeeName} = EXCLUDED.{EmployeeName},
                                            {EmployeeRole} = EXCLUDED.{EmployeeRole},
                                            {EmployeeD} = EXCLUDED.{EmployeeD},
                                            {ManagerID} = EXCLUDED.{ManagerID}"""
                                        ).format(
                                            Employees_table = sql.Identifier('employees'),
                                            EmployeeID = sql.Identifier('EmployeeID'),
                                            EmployeeName = sql.Identifier('EmployeeName'),
                                            EmployeeRole = sql.Identifier('EmployeeRole'),
                                            EmployeeD = sql.Identifier('EmployeeDOB'),
                                            ManagerID = sql.Identifier('ManagerID')
                                        ),row
                            )
                        except Error as e:
                            conn.rollback()
                            print(f'CSV insert failed: {e}')
                conn.commit()
                print("Data was iserted to Employees table.")
        except:
            print("CSV file was not found.")
        #INSERT DATA TO ORDERS TABLE
        try:
            with open('orders.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                with conn.cursor() as cur:
                    for row in reader:
                        try:
                            cur.execute(
                                sql.SQL("""INSERT INTO {Order_table} ({ID},{CustomerID},{Date},{Type},{TableNum},{Payment},{EmployeeID}) VALUES (%s,%s,%s,%s,%s,%s,%s)
                                        ON CONFLICT ({ID}) DO UPDATE SET
                                            {Date} = EXCLUDED.{Date},
                                            {Type} = EXCLUDED.{Type},
                                            {TableNum} = EXCLUDED.{TableNum},
                                            {Payment} = EXCLUDED.{Payment},
                                            {EmployeeID} = EXCLUDED.{EmployeeID},
                                            {CustomerID} = EXCLUDED.{CustomerID}"""
                                        ).format(
                                            Order_table = sql.Identifier('orders'),
                                            ID = sql.Identifier('OrderID'),
                                            Date = sql.Identifier('OrderDate'),
                                            Type = sql.Identifier('OrdertType'),
                                            TableNum = sql.Identifier('Table Number'),
                                            Payment = sql.Identifier('Payment'),
                                            EmployeeID = sql.Identifier('EmployeeID'),
                                            CustomerID = sql.Identifier('CustomerID')
                                        ),row
                            )
                        except Error as e:
                            conn.rollback()
                            print(f'CSV insert failed: {e}')
                conn.commit()
                print("Data was iserted to Orders table.")
        except:
            print("CSV file was not found.")
        #INSERT DATA TO ORDERITEMS TABLE
        try:
            with open('orderitems.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                with conn.cursor() as cur:
                    for row in reader:
                        try:
                            cur.execute(
                                sql.SQL("""INSERT INTO {Items_table} ({OrderItemID},{OrderID},{ItemID},{Quantity}) VALUES (%s,%s,%s,%s)
                                        ON CONFLICT ({OrderItemID}) DO UPDATE SET
                                            {OrderID} = EXCLUDED.{OrderID},
                                            {ItemID} = EXCLUDED.{ItemID},
                                            {Quantity} = EXCLUDED.{Quantity}"""
                                        ).format(
                                            Items_table = sql.Identifier('orderitem'),
                                            OrderItemID = sql.Identifier('OrderItemID'),
                                            OrderID = sql.Identifier('OrderID'),
                                            ItemID = sql.Identifier('ItemID'),
                                            Quantity = sql.Identifier('Quantity'),
                                        ),row
                            )
                        except Error as e:
                            conn.rollback()
                            print(f'CSV insert failed: {e}')
                conn.commit()
                print("Data was iserted to OrderItems table.")
        except:
            print("CSV file was not found.")

        print("Total for each order:")
        with conn.cursor() as cur:
            query = sql.SQL("""
                            WITH {temp} AS (
                            SELECT 
                            {orders}.{order_id},
                            {orders}.{Date},
                            {orders}.{Type},
                            {orders}.{TableNum},
                            {orders}.{Payment},
                            {orders}.{EmployeeID},
                            {orders}.{CustomerID},
                            {order_items}.{order_id} as {orders_2},
                            {order_items}.{item_id},
                            {order_items}.{quantity},
                            {menu}.{price},
                            {customers}.{customer_name},
                            {employee}.{employee_name}
                            FROM {orders} 
                            INNER JOIN {order_items} ON {orders}.{order_id} = {order_items}.{order_id}
                            INNER JOIN {menu} ON {order_items}.{item_id} = {menu}.{item_id}
                            INNER JOIN {customers} ON {orders}.{CustomerID} = {customers}.{CustomerID}
                            INNER JOIN {employee} ON {orders}.{EmployeeID} = {employee}.{EmployeeID}
                            )
                            SELECT DISTINCT
                            {temp}.{order_id},
                            {temp}.{Date},
                            {temp}.{Type},
                            {temp}.{TableNum},
                            {temp}.{Payment},
                            {temp}.{customer_name},
                            {temp}.{employee_name},
                            SUM({temp}.{price}*{temp}.{quantity}) OVER (PARTITION BY {order_id}) as {total}
                            FROM {temp}
                            ORDER BY {temp}.{order_id}
                            """).format(
                price = sql.Identifier("Price"),
                quantity = sql.Identifier("Quantity"),
                order_items = sql.Identifier("orderitem"),
                menu = sql.Identifier("menu"),
                item_id = sql.Identifier("ItemID"),
                order_id = sql.Identifier("OrderID"),
                orders = sql.Identifier("orders"),
                orders_2 = sql.Identifier("orders_items"),
                temp =sql.Identifier('temp'),
                total = sql.Identifier("Total"),
                Date = sql.Identifier('OrderDate'),
                Type = sql.Identifier('OrdertType'),
                TableNum = sql.Identifier('Table Number'),
                Payment = sql.Identifier('Payment'),
                EmployeeID = sql.Identifier('EmployeeID'),
                CustomerID = sql.Identifier('CustomerID'),
                customers = sql.Identifier('customers'),
                customer_name = sql.Identifier('CustomerName'),
                employee = sql.Identifier('employees'),
                employee_name = sql.Identifier('EmployeeName')
                )
            cur.execute(query)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                print(row)

        print("Total by date:")
        with conn.cursor() as cur:
            query = sql.SQL("""
                            WITH {temp} AS (
                            SELECT 
                            {orders}.{order_id},
                            to_char({orders}.{Date},'mon-dd') as {Day},
                            {orders}.{Type},
                            {orders}.{TableNum},
                            {orders}.{Payment},
                            {orders}.{EmployeeID},
                            {orders}.{CustomerID},
                            {order_items}.{order_id} as {orders_2},
                            {order_items}.{item_id},
                            {order_items}.{quantity},
                            {menu}.{price},
                            {customers}.{customer_name},
                            {employee}.{employee_name}
                            FROM {orders} 
                            INNER JOIN {order_items} ON {orders}.{order_id} = {order_items}.{order_id}
                            INNER JOIN {menu} ON {order_items}.{item_id} = {menu}.{item_id}
                            INNER JOIN {customers} ON {orders}.{CustomerID} = {customers}.{CustomerID}
                            INNER JOIN {employee} ON {orders}.{EmployeeID} = {employee}.{EmployeeID}
                            )
                            SELECT DISTINCT 
                            {Day},
                            SUM({price}*{quantity}) OVER (PARTITION BY {Day}) as {total}
                            FROM {temp}
                            ORDER BY {Day}
                            """).format(
                price = sql.Identifier("Price"),
                quantity = sql.Identifier("Quantity"),
                order_items = sql.Identifier("orderitem"),
                menu = sql.Identifier("menu"),
                item_id = sql.Identifier("ItemID"),
                order_id = sql.Identifier("OrderID"),
                orders = sql.Identifier("orders"),
                orders_2 = sql.Identifier("orders_items"),
                temp =sql.Identifier('temp'),
                total = sql.Identifier("Total"),
                Date = sql.Identifier('OrderDate'),
                Type = sql.Identifier('OrdertType'),
                TableNum = sql.Identifier('Table Number'),
                Payment = sql.Identifier('Payment'),
                EmployeeID = sql.Identifier('EmployeeID'),
                CustomerID = sql.Identifier('CustomerID'),
                customers = sql.Identifier('customers'),
                customer_name = sql.Identifier('CustomerName'),
                employee = sql.Identifier('employees'),
                employee_name = sql.Identifier('EmployeeName'),
                Day = sql.Identifier('Day')
                )
            cur.execute(query)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                print(row)

        print("Amount and revenue for every menu item:")
        with conn.cursor() as cur:
            query = sql.SQL("""
                            WITH {temp} AS(
                            SELECT
                            {order_items}.{item_id},
                            {quantity},
                            {menu}.{item_name},
                            {menu}.{price}
                            FROM {order_items}
                            INNER JOIN {menu} ON {order_items}.{item_id} = {menu}.{item_id})
                            SELECT DISTINCT
                            {item_name},
                            SUM({quantity}) OVER (PARTITION BY {item_name}) as {total_quantity},
                            SUM({price}*{quantity}) OVER (PARTITION BY {item_name}) as {total}
                            FROM {temp}
                            ORDER BY {total}"""
                            ).format(
                                temp =sql.Identifier('temp'),
                                price = sql.Identifier("Price"),
                                quantity = sql.Identifier("Quantity"),
                                menu = sql.Identifier("menu"),
                                item_id = sql.Identifier("ItemID"),
                                order_items = sql.Identifier("orderitem"),
                                total = sql.Identifier("Total"),
                                total_quantity = sql.Identifier("Total_quantity"),
                                item_name = sql.Identifier("ItemName")
                            )
            cur.execute(query)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                print(row)

        print("Repeated customers:")
        with conn.cursor() as cur:
            query = sql.SQL("""
                            WITH {temp} AS(
                            SELECT
                            {orders}.{CustomerID},
                            {OrderDate},
                            {customers}.{CustomerName}
                            FROM {orders}
                            INNER JOIN {customers} ON {orders}.{CustomerID} = {customers}.{CustomerID})
                            SELECT
                            {CustomerName},
                            COUNT(DISTINCT {OrderDate})
                            FROM {temp}
                            GROUP BY {CustomerName} 
                            HAVING COUNT(DISTINCT {OrderDate}) > 1
                            """).format(
                                customers = sql.Identifier('customers'),
                                temp = sql.Identifier('temp'),
                                orders = sql.Identifier('orders'),
                                CustomerID = sql.Identifier('CustomerID'),
                                OrderDate = sql.Identifier('OrderDate'),
                                CustomerName =sql.Identifier('CustomerName'),
                                Count = sql.Identifier('Count')
                            )
   
            cur.execute(query)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                print(row)

        print("Selected employee hierarchy:")
        with conn.cursor() as cur:
            query = sql.SQL("""
                            WITH RECURSIVE {manager_h} AS(
                            SELECT {id}, {name}, {ManagerID}, 1 AS {lvl}
                            FROM {employee} where {name} = 'Matie Ball'
                            UNION
                            SELECT E.{id},E.{name},E.{ManagerID}, H.{lvl}+1 AS {lvl}
                            FROM {manager_h} H
                            JOIN {employee} E ON H.{ManagerID} = E.{id}
                            )
                            SELECT H2.{id} AS {employee_id},H2.{name} AS {employee_name},E2.{name} AS {manager_name}, H2.{lvl} as {level}
                            FROM {manager_h} H2
                            JOIN {employee} E2 ON E2.{id} = H2.{ManagerID}
                            """).format(
                                manager_h = sql.Identifier('manager_hierarchy'),
                                manager_name = sql.Identifier('manager_name'),
                                employee_name = sql.Identifier('employee_name'),
                                employee_id = sql.Identifier('employee_id'),
                                employee = sql.Identifier("employees"),
                                lvl = sql.Identifier("lvl"),
                                level = sql.Identifier("level"),
                                id = sql.Identifier("EmployeeID"),
                                name = sql.Identifier("EmployeeName"),
                                ManagerID = sql.Identifier("ManagerID")
                            )
            cur.execute(query)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                print(row)

except Exception as _ex:
    print("[INFO] Error", _ex)
finally:
    if conn:
        print("[INFO] Connection closed")
