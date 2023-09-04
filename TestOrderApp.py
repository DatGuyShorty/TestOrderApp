import tkinter as tk
from tkinter import Frame, ttk
import csv
import atexit
from datetime import datetime

machineDrop = [
    "ULB-05",
    "KD-25",
    "LHP-01",
    "LHP-02",
    "LHP-03",
    "LHP-04",
    "K-ME-50",
    "BI3P",
    "LAC-S-100",
    "K-DK-24-1",
    "K-DK-24-2",
    "K-DK-24-3",
    "W12",
]

orderStatusDrop = [
    "Assigned",
    "Setting Up",
    "Fixture design",
    "Fixture manufacturing",
    "Testing",
    "Finished",
]


class TestOrderApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Test Order Tracker App")
        self.label = tk.Label(root, text="Test Order Tracker")
        self.label.pack()
        frame = Frame(root)
        frame.pack()
        frame_entries = Frame(root)
        frame_entries.pack()

        frame_update = Frame(root)
        frame_update.pack()

        self.label = tk.Label(frame, text="Machine")
        self.label.pack(side="left")

        self.MachineDrop = tk.StringVar()
        self.MachineDrop.set("ULB-05")
        self.drop_machine = tk.OptionMenu(frame_entries, self.MachineDrop, *machineDrop)
        self.drop_machine.pack(side="left")

        self.label = tk.Label(
            frame,
            text="Order number",
        )
        self.label.pack(side="left")
        self.order_entry = tk.Entry(frame_entries)
        self.order_entry.pack(side="left")

        self.label = tk.Label(frame, text="Pcs")
        self.label.pack(side="left")
        self.pcs_entry = tk.Entry(frame_entries)
        self.pcs_entry.pack(side="left")

        self.label = tk.Label(frame, text="Pcs tested")
        self.label.pack(side="left")
        self.pcs_tested_entry = tk.Entry(frame_entries)
        self.pcs_tested_entry.pack(side="left")

        self.label = tk.Label(frame, text="Order Status")
        self.label.pack(side="left")
        self.orderStatus = tk.StringVar()
        self.orderStatus.set("Assigned")
        self.drop_status = tk.OptionMenu(
            frame_entries, self.orderStatus, *orderStatusDrop
        )
        self.drop_status.pack(side="left")

        self.status_button = tk.Button(
            frame_update, text="Update order", command=self.update_status
        )
        self.status_button.pack(side="left")
        self.delete_entry = tk.Entry(frame_update)
        self.delete_entry.pack(side="left")
        self.delete_button = tk.Button(
            frame_update, text="Delete order", command=self.delete_order
        )
        self.delete_button.pack(side="right")

        self.tree = ttk.Treeview(
            root,
            columns=("Machine", "Order", "PCS", "PCS Tested", "Status", "Last Updated"),
            show="headings",
            selectmode="extended",
        )
        self.tree.bind(
            "<<TreeviewSelect>>", self.on_tree_select
        )  # Bind the selection event
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Order", text="Order")
        self.tree.heading("PCS", text="PCS")
        self.tree.heading("PCS Tested", text="PCS Tested")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Last Updated", text="Last Updated")
        self.tree.pack()

        # Load orders from CSV on startup
        self.load_from_csv()

        # Update the tree with orders
        self.update_tree()

        # Register the save function to be called at exit
        atexit.register(self.save_to_csv)

    def save_to_csv(self):
        with open("orders.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(orders)

    def load_from_csv(self):
        global orders
        # Clear existing orders
        orders = []
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
        pcs = self.pcs_entry.get()
        pcs_tested = self.pcs_tested_entry.get()
        status = self.orderStatus.get()
        now = datetime.now()
        update_time = now.strftime("%d/%m/%Y %H:%M:%S")
        tuple_item = (machine, order, pcs, pcs_tested, status, update_time)

        # Update order status logic here
        for index, (_, existingOrder, _, _, _, _) in enumerate(orders):
            if existingOrder == order:
                if status != orders[index][4]:  # Check if the status has changed
                    print(f"Status of order '{order}' changed. Updating status.")
                    orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif machine != orders[index][0]:  # Check if the machine has changed
                    print(f"Machine of order '{order}' changed. Updating machine.")
                    orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif order != orders[index][1]:  # Check if the order has changed
                    print(f"'{order}' has changed. Updating.")
                    orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif pcs != orders[index][2]:  # Check if the pcs has changed
                    print(f"PCS of order '{order}' changed. Updating pcs.")
                    orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif pcs_tested != orders[index][3]:  # Check if pcs_tested has changed
                    print(
                        f"PCS tested of order '{order}' changed. Updating pcs tested."
                    )
                    orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                else:
                    print(f"Order '{order}' found in the list. Status unchanged.")
                break
        else:
            print(f"Order '{order}' not found in the list. Appending.")
            orders.append(tuple_item)
            self.save_to_csv()

        self.update_tree()

    def delete_order(self):
        order_to_delete = self.delete_entry.get()

        for index, (_, existing_order, _, _, _, _) in enumerate(orders):
            if existing_order == order_to_delete:
                del orders[index]
                self.save_to_csv()
                print(f"Order '{order_to_delete}' has been deleted.")
                self.update_tree()
                break
        else:
            print(f"Order '{order_to_delete}' not found in the list. Deletion failed.")

    def update_tree(self):
        # Clear the existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert each order into the Treeview
        for machine, order, pcs, pcs_tested, status, update_time in orders:
            self.tree.insert(
                "",
                "end",
                values=(machine, order, pcs, pcs_tested, status, update_time),
            )

    def on_tree_select(self, event):
        # Get the selected item(s) from the tree view
        selected_items = self.tree.selection()

        if selected_items:
            # Get the data from the first selected item (assuming single selection)
            selected_item = self.tree.item(selected_items[0])["values"]
            machine, order, pcs, pcs_tested, status, _ = selected_item

            # Update the entry fields with the selected item's data
            self.MachineDrop.set(machine)
            self.order_entry.delete(0, tk.END)
            self.order_entry.insert(0, order)
            self.pcs_entry.delete(0, tk.END)
            self.pcs_entry.insert(0, pcs)
            self.pcs_tested_entry.delete(0, tk.END)
            self.pcs_tested_entry.insert(0, pcs_tested)
            self.orderStatus.set(status)


root = tk.Tk()
app = TestOrderApp(root)
root.mainloop()
