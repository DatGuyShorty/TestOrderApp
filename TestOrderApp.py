import tkinter as tk
from tkinter import ttk
import csv
import atexit


machineDrop = [
    "ULB-05",
    "KD-25",
    "LHP-01",
    "LHP-02",
    "LHP-03",
    "LHP-04"
]

orderStatusDrop = [
    "Assigned",
    "Setting Up",
    "Running",
    "Fixture design / Manufacturing",
    "Finished"
]

orders = []


class TestOrderApp:
    def __init__(self, root):

        # Register the save function to be called at exit
        atexit.register(self.save_to_csv)

        self.root = root
        self.root.title("Test Order Tracker")

        self.label = tk.Label(root, text="Test Order Tracker")
        self.label.pack()
        
        self.label = tk.Label(root,text="Machine")
        self.label.pack()

        self.MachineDrop = tk.StringVar()
        self.MachineDrop.set( "ULB-05")
        self.drop = tk.OptionMenu( root , self.MachineDrop , *machineDrop )
        self.drop.pack()

        self.label = tk.Label(root,text="order")
        self.label.pack()
        self.order_entry = tk.Entry(root)
        self.order_entry.pack()
        
        self.label = tk.Label(root,text="Order Status")
        self.label.pack()
        self.orderStatus = tk.StringVar()
        self.orderStatus.set("Assigned")
        self.drop = tk.OptionMenu( root , self.orderStatus , *orderStatusDrop )
        self.drop.pack()

        self.status_button = tk.Button(root, text="Update Status", command=self.update_status)
        self.status_button.pack()

        self.tree = ttk.Treeview(root, columns=("Machine", "Order", "Status"), show="headings")
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Order", text="Order")
        self.tree.heading("Status", text="Status")
        self.tree.pack()

        # Load orders from CSV on startup
        self.load_from_csv()
        # Update the tree with orders
        self.update_tree()

        


    def save_to_csv(self):
        with open("orders.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for order in orders:
                writer.writerow(order)

    def load_from_csv(self):
        global orders
        orders = []  # Clear existing orders
        try:
            with open("orders.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    orders.append(row)
        except FileNotFoundError:
            pass  # No file found, continue with an empty orders list


    def update_status(self):
        machine = self.MachineDrop.get()
        order = self.order_entry.get()
        status = self.orderStatus.get()
        tuple_item = (machine, order, status)
        # Update order status logic here
       
        for index, (_, existing_order, _) in enumerate(orders):
            if existing_order == order:
                if status != orders[index][2]:  # Check if the status has changed
                    print(f"Status of order '{order}' changed. Updating status.")
                    orders[index] = (machine, order, status)
                    self.save_to_csv()
                else:
                    print(f"Order '{order}' found in the list. Status unchanged.")
                break
        else:
            print(f"Order '{order}' not found in the list. Appending.")
            orders.append(tuple_item)
            self.save_to_csv()
        print(orders)

        self.update_tree()
    def update_tree(self):
         # Clear the existing rows in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Insert each order into the Treeview
        for machine, order, status in orders:
            self.tree.insert("", "end", values=(machine, order, status))
root = tk.Tk()
app = TestOrderApp(root)
root.mainloop()
