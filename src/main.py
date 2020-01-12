# ! Author tuhinsaud@tuhinsaud
# version: 1

import os
from io import BytesIO
from PIL import ImageTk, Image as PILImage
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox

import database_helper as db_helper
from show_products_panel import *
from update_window import update_window_frame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.expanduser("~"))

root = Tk()
root.title("Shop Management System")
root.geometry("600x400")

note_book = ttk.Notebook(root)
note_book.pack(fill=tk.BOTH)

# TODO:Show Products Starts
show_products_frame = ttk.Frame(note_book)
note_book.add(show_products_frame, text="Show Products", sticky="nesw")

show_products_tree_view_headers = (
    "Name", "Price", "Category", "Created at")
show_products_tree = custom_tree_view(
    show_products_frame, *show_products_tree_view_headers)


def show_all_data():
    global show_products_tree
    for i in show_products_tree.get_children():
        show_products_tree.delete(i)
    for data in db_helper.all_products():
        show_products_tree.insert(
            "", "end", value=data[1:len(data)], text=data[0])


show_all_data()

selected_item_id = None
selected_item_values = None


def on_select(event):
    global show_products_tree
    global selected_item_id
    global selected_item_values
    for idx in event.widget.selection():
        selected_item_id = show_products_tree.item(idx)['text']
        selected_item_values = show_products_tree.item(idx)['values']


show_products_tree.bind("<<TreeviewSelect>>", on_select)


def update_item_handler():
    global root
    global selected_item_id
    global selected_item_values
    if selected_item_id is None or selected_item_values is None:
        return
    else:
        # update_window = tk.Toplevel(root)
        # update_window.title("Update for {}".format(selected_item_values[0]))
        # update_window.geometry("600x400")
        # update_window.grab_set()
        update_window_frame(root, selected_item_id,
                            selected_item_values, show_all_data)
        selected_item_values = None
        selected_item_id = None


update_product_btn = Button(
    show_products_frame, text="UPDATE", bg="GREEN", fg="WHITE", command=update_item_handler)
update_product_btn.pack()


def delete_item_handler():
    global selected_item_id
    if selected_item_id is None:
        return
    else:
        db_helper.delete_product(selected_item_id)
        show_all_data()


delete_product_btn = Button(
    show_products_frame, text="DELETE", bg="RED", fg="WHITE", command=lambda: delete_item_handler())
delete_product_btn.pack()
# TODO:Show Products Ends

# TODO: ADD Products
# This for category popup
category = ("Laptop", "Desktop", "Mobile")
global_product_data = {
    "name": None,
    "price": 0,
    "image": None,
    "category_name": category[0]
}
product_frame = ttk.Frame(note_book)
note_book.add(product_frame, text="Add Product")
product_name_label = Label(product_frame, text="Name")
product_name_label.grid(row="0", column="0", pady="5")

product_name_txt = Entry(product_frame)
product_name_txt.grid(row="0", column="1", pady="5")

product_price_label = Label(product_frame, text="Price")
product_price_label.grid(row="1", column="0", pady="5")

product_price_txt = Entry(product_frame)
product_price_txt.grid(row="1", column="1", pady="5")


def open_file_selector():
    root.filename = filedialog.askopenfilename(title="select Image", filetypes=(
        ("jpg files", "*.jpg"), ("png files", "*.png")))
    # image = ImageTk.PhotoImage(PILImage.open(root.filename))
    # # image_path_label = Label(add_product_frame, text=root.filename)
    # image_path_label = Label(add_product_frame, image=image, height=30, width=30)
    # image_path_label.grid(row="2", column="1", columnspan="3", pady="5")
    if root.filename:
        global_product_data["image"] = root.filename
    image_path_label = Label(product_frame, text=root.filename)
    image_path_label.grid(row="2", column="1", pady="5")


product_image_btn = Button(
    product_frame, text="Select image.", command=open_file_selector)
product_image_btn.grid(row="2", column="0", pady="5")

# TODO:Category start
category_variable = StringVar()
category_variable.set(category[0])

product_category_label = Label(product_frame, text="Category")
product_category_label.grid(row="3", column="0", pady="5")
product_category_selection = OptionMenu(
    product_frame, category_variable, *category)
product_category_selection.grid(row="3", column="1", pady="5")
# TODO:Category end


def clear_form_data():
    global product_name_txt
    global product_price_txt
    global category_variable
    product_name_txt.delete(0, "end")
    product_price_txt.delete(0, "end")
    category_variable.set(category[0])


def saveData():
    global_product_data["name"] = str(product_name_txt.get())
    if len(global_product_data["name"]) == 0:
        messagebox.showerror("Error", "Name must not be empty.")
        return

    temp_price = str(product_price_txt.get()).replace(" ", "")
    # if not re.search('[+-]?[0-9]+\.[0-9]+', temp_price):
    if not re.search('[0-9]+\.?[0-9]*', temp_price):
        messagebox.showerror("Error", "Invalid price.")
        return
    else:
        global_product_data["price"] = float(temp_price)

    global_product_data["category_name"] = category_variable.get()

    db_helper.insert_product(**global_product_data)
    clear_form_data()
    show_all_data()
    note_book.select(0)


insert_product_btn = Button(
    product_frame, text="Save", command=lambda: saveData())
insert_product_btn.grid(row="7", column="0", columnspan="2", pady="5")
# TODO:Add Product end
root.mainloop()
