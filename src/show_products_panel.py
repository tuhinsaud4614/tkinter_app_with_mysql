from tkinter import *
from tkinter import ttk


def custom_tree_view(parent, *headers):
    scroll_bar = ttk.Scrollbar(
        parent, orient="vertical")
    scroll_bar.pack(side=RIGHT, fill="y")

    tree_view = ttk.Treeview(parent, columns=headers,
                             yscrollcommand=scroll_bar.set, show="headings", selectmode="browse")
    # tree_view = ttk.Treeview(parent, columns=headers,
    #                          yscrollcommand=scroll_bar.set,selectmode="browse")
    for i in headers:
        tree_view.column(str(i), width=10, anchor="center")
        tree_view.heading(str(i), text=str(i))
    
    tree_view.pack(expand=True, fill=BOTH)
    scroll_bar.config(command=tree_view.yview)
    
    return tree_view
