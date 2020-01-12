import tkinter as tk
from tkinter import *
import database_helper as db_helper

category = ("Laptop", "Desktop", "Mobile")
global_product_data = {
    "name": None,
    "price": None,
    "category_name": None
}


def updateData(product_name, product_price, product_category, product_id, parent, show_all_handler):
    global_product_data["name"] = str(product_name)
    if len(global_product_data["name"]) == 0:
        messagebox.showerror("Error", "Name must not be empty.")
        return

    temp_price = str(product_price).replace(" ", "")
    # if not re.search('[+-]?[0-9]+\.[0-9]+', temp_price):
    if not re.search('[0-9]+\.?[0-9]*', temp_price):
        messagebox.showerror("Error", "Invalid price.")
        return
    else:
        global_product_data["price"] = float(temp_price)

    global_product_data["category_name"] = product_category

    db_helper.update_product(product_id, **global_product_data)
    parent.grab_release()
    parent.destroy()
    show_all_handler()


def update_window_frame(parent, product_id, product_values, show_all_handler):
    update_window = tk.Toplevel(parent)
    update_window.title("Update for {}".format(product_values[0]))
    update_window.geometry("600x400")
    update_window.grab_set()

    global global_product_data
    global_product_data = {
        "name": product_values[0],
        "price": product_values[1],
        "category_name": product_values[2]
    }

    product_name_label = Label(update_window, text="Name")
    product_name_label.grid(row="0", column="0", pady="5")

    product_name_txt = Entry(update_window)
    product_name_txt.insert(0, global_product_data['name'])
    product_name_txt.grid(row="0", column="1", pady="5")

    product_price_label = Label(update_window, text="Price")
    product_price_label.grid(row="1", column="0", pady="5")

    product_price_txt = Entry(update_window)
    product_price_txt.insert(0, global_product_data['price'])
    product_price_txt.grid(row="1", column="1", pady="5")

    # TODO:Category start
    global category
    category_variable = StringVar()
    category_variable.set(global_product_data['category_name'])

    product_category_label = Label(update_window, text="Category")
    product_category_label.grid(row="3", column="0", pady="5")
    product_category_selection = OptionMenu(
        update_window, category_variable, *category)
    product_category_selection.grid(row="3", column="1", pady="5")
    # TODO:Category end

    update_product_btn = Button(
        update_window, text="UPDATE", command=lambda: updateData(product_name_txt.get(), product_price_txt.get(), category_variable.get(), product_id, update_window, show_all_handler))
    update_product_btn.grid(row="7", column="0", columnspan="2", pady="5")
