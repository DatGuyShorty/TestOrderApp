import csv
import pathlib
import tkinter as tk
from datetime import datetime
from tkinter import  ttk
from ttkthemes import ThemedStyle

print("Current working directory:", pathlib.Path().resolve())
MACHINE_DROP_OPTIONS = [
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

ORDER_STATUS_OPTIONS = [
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
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")  # You can change the theme here

        self.orders = []
        self.init_ui()
        self.load_from_csv()

        self.tree.bind(
            "<<TreeviewSelect>>", self.on_tree_select
        )  # Bind the selection event

    def init_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Create and configure labels
        ttk.Label(frame, text="Test Order Tracker", font=("Helvetica", 16)).grid(
            row=0, columnspan=2, pady=10
        )
        ttk.Label(frame, text="Machine").grid(row=1, column=0, sticky="w")
        ttk.Label(frame, text="Order number").grid(row=2, column=0, sticky="w")
        ttk.Label(frame, text="Pcs").grid(row=3, column=0, sticky="w")
        ttk.Label(frame, text="Pcs tested").grid(row=4, column=0, sticky="w")
        ttk.Label(frame, text="Order Status").grid(row=5, column=0, sticky="w")

        # Create and configure input widgets
        self.MachineDrop = ttk.Combobox(
            frame, values=MACHINE_DROP_OPTIONS, state="readonly"
        )
        self.MachineDrop.grid(row=1, column=1)
        self.order_entry = ttk.Entry(frame)
        self.order_entry.grid(row=2, column=1)
        self.pcs_entry = ttk.Entry(frame)
        self.pcs_entry.grid(row=3, column=1)
        self.pcs_tested_entry = ttk.Entry(frame)
        self.pcs_tested_entry.grid(row=4, column=1)
        self.orderStatus = ttk.Combobox(
            frame, values=ORDER_STATUS_OPTIONS, state="readonly"
        )
        self.orderStatus.grid(row=5, column=1)

        # Create buttons
        ttk.Button(frame, text="Update Order", command=self.update_status).grid(
            row=6, column=0, padx=10, pady=10, sticky="w"
        )
        # Define the custom style for the red button
        self.style.configure("Red.TButton", foreground="black", background="red")
        ttk.Button(
            frame, text="Delete Order", style="Red.TButton", command=self.delete_order
        ).grid(row=6, column=1, padx=10, pady=10, sticky="e")

        # Create and configure Treeview
        columns = ("Machine", "Order", "PCS", "PCS Tested", "Status", "Last Updated")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust column width as needed
        self.tree.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Created by Tibor Hoppan").grid(
            row=8, column=1, sticky="e"
        )

        ttk.Label(frame, text="Ver. 0.2.0 / 5.09.2023").grid(
            row=9, column=1, sticky="e"
        )

    def load_from_csv(self):
        try:
            with open("orders.csv", mode="r") as file:
                reader = csv.reader(file)
                self.orders = [row for row in reader]
                self.update_tree()
                print("Order list loaded!")
        except FileNotFoundError:
            print("No file found! Continuing with an empty order list.")

    def save_to_csv(self):
        with open("orders.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.orders)
            print("Saved to CSV")

    def update_status(self):
        machine = self.MachineDrop.get()
        order = self.order_entry.get()
        pcs = self.pcs_entry.get()
        pcs_tested = self.pcs_tested_entry.get()
        status = self.orderStatus.get()
        now = datetime.now()
        update_time = now.strftime("%d/%m/%Y %H:%M:%S")
        tuple_item = (machine, order, pcs, pcs_tested, status, update_time)

        for index, (_, existingOrder, _, _, _, _) in enumerate(self.orders):
            if existingOrder == order:
                if status != self.orders[index][4]:
                    print(f"Status of order '{order}' changed. Updating status.")
                    self.orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif machine != self.orders[index][0]:
                    print(f"Machine of order '{order}' changed. Updating machine.")
                    self.orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif pcs != self.orders[index][2]:
                    print(f"PCS of order '{order}' changed. Updating pcs.")
                    self.orders[index] = (
                        machine,
                        order,
                        pcs,
                        pcs_tested,
                        status,
                        update_time,
                    )
                    self.save_to_csv()
                elif pcs_tested != self.orders[index][3]:
                    print(
                        f"PCS tested of order '{order}' changed. Updating pcs tested."
                    )
                    self.orders[index] = (
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
            self.orders.append(tuple_item)
            self.save_to_csv()

        self.update_tree()

    def delete_order(self):
        order_to_delete = self.order_entry.get()

        for index, (_, existing_order, _, _, _, _) in enumerate(self.orders):
            if existing_order == order_to_delete:
                del self.orders[index]
                self.save_to_csv()
                print(f"Order '{order_to_delete}' has been deleted.")
                self.update_tree()
                break
        else:
            print(f"Order '{order_to_delete}' not found in the list. Deletion failed.")

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for machine, order, pcs, pcs_tested, status, update_time in self.orders:
            self.tree.insert(
                "",
                "end",
                values=(machine, order, pcs, pcs_tested, status, update_time),
            )

    def on_tree_select(self, event):
        selected_items = self.tree.selection()

        if selected_items:
            selected_item = self.tree.item(selected_items[0])["values"]
            machine, order, pcs, pcs_tested, status, _ = selected_item

            self.MachineDrop.set(machine)
            self.order_entry.delete(0, tk.END)
            self.order_entry.insert(0, order)
            self.pcs_entry.delete(0, tk.END)
            self.pcs_entry.insert(0, pcs)
            self.pcs_tested_entry.delete(0, tk.END)
            self.pcs_tested_entry.insert(0, pcs_tested)
            self.orderStatus.set(status)


def main():
    root = tk.Tk()
    app = TestOrderApp(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
