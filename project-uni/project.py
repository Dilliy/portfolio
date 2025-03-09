#LIBRARIES
import random
import csv
import tkinter as tk
from tkinter import ttk

#GLOBAL VARIABELS
temp_cart = []
cart = []
user_cart = []
product_list = []
product_list_temp = []
temp_output = []
discounts = []
remove_product_processing = False
add_product_processing = False
discount_process_going = False
discount_used = False
discount_recived = False

#WINDOW AND FRAME
window = tk.Tk()
window.geometry('800x600')
window.title("Cart")
window.minsize(700,200)

frame_product_list = tk.Frame(window,width=533.33,height=400)
frame_buttons_access = tk.Frame(window,width=266.66,height=400)
frame_user_input = tk.Frame(window,width=800,height=200)

frame_product_list.place(relx=0,rely=0,relheight=0.666,relwidth=0.666)
frame_buttons_access.place(relx=0.666,rely=0,relheight=0.666,relwidth=0.333)
frame_user_input.place(relx=0,rely=0.666,relheight=0.333,relwidth=1)

#UPLOUDING FROM THE FILE
with open("project-uni\shopping_cart.csv") as f:
    temp = csv.DictReader(f)
    for i in temp:
        cart.append(i)

#MAIN FUNCTIONS
def available_products():
    table.delete(*table.get_children())
    for i in cart:
        temp_cart.append((i["Name"],i["Price"],i["Description"]))
    
    for header in heads:
        table.heading(header,text=header,anchor="center")
        table.column(header,anchor="center" )

    for i in temp_cart:
        table.insert('',tk.END,values = i)
    
    temp_cart.clear()

def create_list():
    global discount_process_going
    global add_product_processing
    global remove_product_processing
    if remove_product_processing==False and discount_process_going==False:
        add_product_processing = True
        global product_list
        try:
            product_list+=product_list_temp
            product_list_temp.clear()
        except:
            pass
        stop = False
        temp = ""
        while not(stop):
            clear_lable()
            l_adding_product.grid(row=0,column=0,sticky="w")
            l_user_data.grid(row=3,column=0,sticky="w")
            button_entry.grid(row=4,column=0,sticky="w")
            user_name_product_entered = False
            while not(user_name_product_entered):
                button_entry.wait_variable(button_enter_pressed)
                temp = get_input().lower()
                if temp == "":
                    pass
                else:
                    clear_text()
                    user_name_product_entered = True
            l_adding_product.grid_remove()
            if temp.lower() == 'stop':
                stop = True
            else:
                stop_number = False
                while not(stop_number):
                    try:
                        l_adding_number.grid(row=0,column=0,sticky="w")
                        button_entry.wait_variable(button_enter_pressed)
                        num = int(get_input())
                        if num > 0:
                            l_incorrect_input_negative.grid_remove()
                            l_incorrect_input_number.grid_remove()
                            clear_text()
                            stop_number = True
                        else:
                            l_incorrect_input_number.grid_remove()
                            l_incorrect_input_negative.grid(row=1,column=0,sticky="w")
                    except:
                        l_incorrect_input_negative.grid_remove()
                        l_incorrect_input_number.grid(row=1,column=0,sticky="w")
                l_adding_number.grid_remove()
                
                changed = False
                for i in range(len(product_list)):
                    if product_list[i][0] == temp:
                        product_list[i][1]+=num
                        changed = True
                        break

                if len(product_list) == 0 or not(changed):
                    product_list.append([temp.lower(), num])
        user_cart.clear()
        add_product()
        update_table()
        price = get_costs()
        l_price.configure(text = f"Price: {price} euro")
        l_price.pack(fill=tk.X)
        add_product_processing = False

    else:
        l_process_interupted.grid(row=2,column=0,sticky='w')

def add_product():
    for i in cart:
        for f in product_list:
            if f[0] == i.get("Name").lower():
                dict_num = {"Number": product_list[product_list.index(f)][1]}
                i.update(dict_num)
                user_cart.append(i)
                product_list_temp.append(product_list.pop(product_list.index(f)))
    if len(product_list) == 0:
        l_user_finished_adding.grid(row=0,column=0,sticky="w")
    else:

        for i in product_list:
            temp_output.append(i[0])
        l_user_not_found.configure(text=f'We were not able to find these products: {",".join(temp_output)}.Please check available products')
        l_user_not_found.grid(row=0,column=0,sticky="w")
    product_list.clear()

def update_table():
    table_user.delete(*table_user.get_children())

    for i in user_cart:
        temp_cart.append((i["Name"],i["Number"]))

    for header in heads_user:
        table_user.heading(header,text=header,anchor="center")
        table_user.column(header,anchor="center" )

    for i in temp_cart:
        table_user.insert('',tk.END,values = i)
    temp_cart.clear()

    table_user.pack(expand=tk.YES, fill=tk.BOTH)    

def remove_product():
    global add_product_processing
    global remove_product_processing
    global discount_process_going
    if add_product_processing==False and discount_process_going==False:
        remove_product_processing = True
        clear_lable()
        l_remove_product.grid(row=0,column=0,sticky="w")
        l_user_data.grid(row=3,column=0,sticky="w")
        button_entry.grid(row=4,column=0,sticky="w")
        user_name_product_entered = False
        while not(user_name_product_entered):
            button_entry.wait_variable(button_enter_pressed)
            product_to_remove = get_input().lower()
            if product_to_remove == "":
                pass
            else:
                clear_text()
                user_name_product_entered = True
        l_remove_product.grid_remove()
        if product_to_remove == "stop":
            clear_lable()
            l_remove_left.grid(row=0,column=0,sticky='w')
        else:
            stop = False
            while not(stop):
                try:
                    l_removing_number.grid(row=0,column=0,sticky='w')
                    button_entry.wait_variable(button_enter_pressed)
                    num = int(get_input())
                    if num > 0:
                        l_incorrect_input_number.grid_remove()
                        l_incorrect_input_negative.grid_remove()
                        clear_text()
                        stop = True
                    else:
                        l_incorrect_input_number.grid_remove()
                        l_incorrect_input_negative.grid(row=1,column=0,sticky='w')
                except:
                    l_incorrect_input_negative.grid_remove()
                    l_incorrect_input_number.grid(row=1,column=0,sticky='w')
            l_removing_number.grid_remove()
            len_of_usercart = len(user_cart)
            found = False
            counter = 0
            while not(found) and counter != len_of_usercart:
                if user_cart[counter].get("Name").lower() == product_to_remove:
                    if user_cart[counter].get("Number") <= num:
                        user_cart.pop(counter)
                        found = True
                    else:
                        user_cart[counter]["Number"]-=num
                        found = True
                else:
                    counter+=1
            clear_lable()
            if found == True:
                l_remove_removed.grid(row=0,column=0,sticky='w')
            else:
                l_remove_notFound.grid(row=0,column=0,sticky='w')
            product_list_temp.clear()
            for i in user_cart:
                product_list_temp.append([i["Name"].lower(),i["Number"]])
            update_table()
        price = get_costs()
        l_price.configure(text = f"Price: {price} euro")
        l_price.pack(fill=tk.X)
        remove_product_processing = False
    else:
        l_process_interupted.grid(row=2,column=0,sticky='w')

def discount():
    global discount_used
    global discount_process_going
    global remove_product_processing
    global add_product_processing
    if remove_product_processing or add_product_processing:
        l_process_interupted.grid(row=2,column=0,sticky='w')
    else:
        discount_process_going = True
        clear_lable()
        try:
            with open("project-uni\discount.txt") as f:
                for i in f:
                    discounts.append(str(i.rstrip()))
                l_discount.grid(row=0,column=0,sticky="w")
                l_user_data.grid(row=3,column=0,sticky="w")
                button_entry.grid(row=4,column=0,sticky="w")
                button_entry.wait_variable(button_enter_pressed)
                cupon = get_input().lower()
                clear_lable()
                if discount_used == False:
                    if cupon in discounts:
                        discount_used = True
                        match cupon:
                            case "14435":
                                discount_product = "Vegetable"
                                l_discount_vegetables.grid(row=0,column=0,sticky='w')
                            case "10098":
                                discount_product = "Meat"
                                l_discount_meat.grid(row=0,column=0,sticky='w')
                            case "12443":
                                discount_product = "Fish"
                                l_discount_fish.grid(row=0,column=0,sticky='w')
                            case "19932":
                                discount_product = "Drinks"
                                l_discount_drinks.grid(row=0,column=0,sticky='w')
                            case "10003":
                                discount_product = "Sweets"
                                l_discount_sweets.grid(row=0,column=0,sticky='w')
                            case _:
                                pass
                        discounts.remove(cupon)
                        discount_cart(discount_product)
                        discount_process_going = False
                    else:
                        clear_lable()
                        l_discount_notFound.grid(row=0,column=0,sticky='w')
                        discount_process_going = False
                else:
                    discount_process_going = False
                    l_discount_used.grid(row=0,column=0,sticky='w')

        except:
            discount_process_going = False
            l_discount_error.grid(row=0,column=0,sticky='w')
        price = get_costs()
        l_price.configure(text = f"Price: {price} euro")
        l_price.pack(fill=tk.X)
    clear_text()

def discount_cart(product):
    for i in range(len(cart)):
        if cart[i].get("Kategory") == product:
            s = int(cart[i]["Price"])
            s = round(s*0.7)
            cart[i]["Price"] = s
    #with open("project-uni\discount.txt",'w') as f:
        #for i in discounts:
            #f.write(i+"\n")
    available_products()

def get_costs():
    price = 0
    for i in user_cart:
        price = price + int(i.get("Price"))*int(i.get("Number"))
    return price

#OUTPUT FUNCTIONS
def receipt_output():
    if len(user_cart)>0:
        global discount_recived
        window_receipt = tk.Toplevel(window)
        window_receipt.geometry("400x600")
        window_receipt.title("Receipt")
        window_receipt.minsize(400,600)
        window_receipt.maxsize(400,600)

        frame_receipt_product = tk.Frame(window_receipt,width=400,height=500)
        frame_receipt_price = tk.Frame(window_receipt,width=400,height=100)

        #TREE
        heads_receipt = ["Name","Price","","Number","Total"]
        table_receipt = ttk.Treeview(frame_receipt_product,show="headings")
        table_receipt["columns"] = heads_receipt

        frame_receipt_product.place(relx=0,rely=0,relwidth=1,relheight=0.833)
        frame_receipt_price.place(relx=0,rely=0.833,relwidth=1,relheight=0.166)

        l_top_level = tk.Label(frame_receipt_product,text = "Receipt",font="14px",bg="White")
        l_top_level.pack(side = "top",fill="both")

        temp_receipt = []
        for i in user_cart:
            total = int(i["Price"])*int(i["Number"])
            temp_receipt.append((i["Name"],i["Price"],"x",i["Number"],total))
        for header in heads_receipt:
            table_receipt.heading(header,text=header,anchor="center")
        table_receipt.column(heads_receipt[0],anchor="center",width=95)
        table_receipt.column(heads_receipt[1],anchor="center",width=95)
        table_receipt.column(heads_receipt[2],anchor="center",width=20)
        table_receipt.column(heads_receipt[3],anchor="center",width=95)
        table_receipt.column(heads_receipt[4],anchor="center",width=95)
        for i in temp_receipt:
            table_receipt.insert('',tk.END,values = i)
        temp_receipt.clear()
        table_receipt.pack(expand=tk.YES, fill=tk.BOTH)

        price = get_costs()
        l_price_total = tk.Label(frame_receipt_price,text=f"The total price is {price}",font=('Times', 14),anchor="center")
        l_price_total.place(x=120,y=10)

        l_receipt_cupon_mistake = tk.Label(frame_receipt_price,text="Mistake occured and we could not get a cupon for you",anchor="center")
        l_receipt_cupon_recived = tk.Label(frame_receipt_price,text="You have recived your discount coupon for today.",anchor="center")
        cupon = random.randint(0,4)
        discounts_temp = []
        if discount_recived == False:
            try:
                with open("project-uni\discount.txt") as f:
                    for i in f:
                        discounts_temp.append(str(i.rstrip()))
                match discounts_temp[cupon]:
                                case "14435":
                                    discount_product = "vegetable"
                                case "10098":
                                    discount_product = "meat"
                                case "12443":
                                    discount_product = "fish"
                                case "19932":
                                    discount_product = "drinks"
                                case "10003":
                                    discount_product = "sweets"
                l_receipt_cupon = tk.Label(frame_receipt_price,text=f"Your coupon number is {discounts_temp[cupon]} for {discount_product} for 30%",font=('Arial', 10))
                l_receipt_cupon.place(x=55,y=50)
                discount_recived = True
            except:
                l_receipt_cupon_mistake.place(x=60,y=50)
        else:
            l_receipt_cupon_recived.place(x=68,y=50)
    else:
        global discount_process_going
        global add_product_processing
        global remove_product_processing
        if discount_process_going == False and add_product_processing==False and remove_product_processing == False:
            clear_lable()
            l_receipt_none.grid(row=0,column=0)
        else:
            l_process_interupted.grid(row=2,column=0,sticky='w')

#SMALL FUNCTIONS FOR GUI
def clear_text():
   l_user_data.delete(0, tk.END)

def get_input():
    temp = l_user_data.get()
    return temp

def clear_lable():
    try:
        l_user_finished_adding.grid_remove()
    except:
        pass
    try:
        l_user_not_found.grid_remove()
    except:
        pass
    try:
        l_remove_removed.grid_remove()
    except:
        pass
    try:
        l_remove_notFound.grid_remove()
    except:
        pass
    try:
        l_adding_product.grid_remove()
    except:
        pass
    try:
        l_remove_product.grid_remove()
    except:
        pass
    try:
        l_removing_number.grid_remove()
    except:
        pass
    try:
        l_discount_vegetables.grid_remove()
    except:
        pass
    try:
        l_discount_drinks.grid_remove()
    except:
        pass
    try:
        l_discount_fish.grid_remove()
    except:
        pass
    try:
        l_discount_meat.grid_remove()
    except:
        pass
    try:
        l_discount_sweets.grid_remove()
    except:
        pass
    try:
        l_discount_notFound.grid_remove()
    except:
        pass
    try:
        l_discount_error.grid_remove()
    except:
        pass
    try:
        l_discount_used.grid_remove()
    except:
        pass
    try:
        l_discount.grid_remove()
    except:
        pass
    try:
        l_process_interupted.grid_remove()
    except:
        pass
    try: 
        l_remove_left.grid_remove()
    except:
        pass
    try:
        l_receipt_none.grid_remove()
    except:
        pass

#BUTTON ACCESS
l_button_title = tk.Label(frame_buttons_access,text="User cart control buttons",font="14px",bg="White")
button_add = tk.Button(frame_buttons_access,text="Add",command=create_list)
button_remove = tk.Button(frame_buttons_access,text="Remove",command=remove_product)
button_print_receipt = tk.Button(frame_buttons_access,text="Receipt",command=receipt_output)
button_discount = tk.Button(frame_buttons_access,text="Discount",command= discount)
l_price = tk.Label(frame_buttons_access)

heads_user = ["Name","Number"]
table_user = ttk.Treeview(frame_buttons_access,show="headings")
table_user["columns"] = heads_user
table_user["displaycolumns"] = ["Name","Number"]

l_button_title.pack(side = "top", fill="both")
button_add.pack(fill=tk.X)
button_remove.pack(fill=tk.X)
button_print_receipt.pack(fill=tk.X)
button_discount.pack(fill=tk.X)

#USER INPUT
    #ADDING
l_adding_product = tk.Label(frame_user_input, text="Enter the name of the product that u are looking for. If u want to finish please enter 'stop'.")
l_adding_number = tk.Label(frame_user_input, text="How much product you want to add?")
l_user_finished_adding = tk.Label(frame_user_input, text="You finished adding products to ur cart.")
l_user_not_found = tk.Label(frame_user_input)

    #REMOVING
l_remove_product = tk.Label(frame_user_input,text="Please enter product that you want to remove: If u want to finish please enter 'stop'.")
l_removing_number = tk.Label(frame_user_input, text="How much product you want to remove?")
l_remove_removed = tk.Label(frame_user_input,text="Product is removed.")
l_remove_notFound = tk.Label(frame_user_input,text="Product is not found, please, check your spelling.")
l_remove_left = tk.Label(frame_user_input,text="You left removing process")

    #COMMON
l_incorrect_input_negative = tk.Label(frame_user_input, text="Please, enter positive number.")
l_incorrect_input_number = tk.Label(frame_user_input, text="Enter number.")
l_process_interupted = tk.Label(frame_user_input,text="Please finish going process first.")

    #DISCOUNTS
l_discount = tk.Label(frame_user_input,text="Enter cupon number: ")
l_discount_error = tk.Label(frame_user_input,text="Text file is not found.")
l_discount_drinks = tk.Label(frame_user_input,text="You get discount for drinks")
l_discount_vegetables = tk.Label(frame_user_input,text="You get discount for vegetables")
l_discount_meat = tk.Label(frame_user_input,text="You get discount for meat")
l_discount_fish = tk.Label(frame_user_input,text="You get discount for fish")
l_discount_sweets = tk.Label(frame_user_input,text="You get discount for sweets")
l_discount_notFound = tk.Label(frame_user_input,text="Such cupon is not found.")
l_discount_used = tk.Label(frame_user_input,text="You already used discount.")

    #RECEIPT
l_receipt_none = tk.Label(frame_user_input,text="Please, add some products first")

    #BUTTON
button_enter_pressed = tk.StringVar()
l_user_data = tk.Entry(frame_user_input)
button_entry = tk.Button(frame_user_input,text="Enter",command=lambda: button_enter_pressed.set("button pressed"))

#AVAILABLE PRODUCTS
heads = ["Name","Price","Description"]
table = ttk.Treeview(frame_product_list,show="headings")
table['columns'] = heads
table["displaycolumns"] = ["Name","Price","Description"]

available_products()
update_table()

scroll_pane = ttk.Scrollbar(frame_product_list,command=table.yview)
scroll_pane.pack(side=tk.LEFT,fill=tk.Y)   
table.configure(yscrollcommand=scroll_pane.set)

table.pack(expand=tk.YES, fill=tk.BOTH)

window.mainloop()