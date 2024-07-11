import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# function to add expenses
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "All fields are required.")
        return

    if not os.path.exists('data/expenses.csv'):
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
        df.to_csv('data/expenses.csv', index=False)
    else:
        df = pd.read_csv('data/expenses.csv')

    new_expense = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
    df = pd.concat([df, new_expense], ignore_index=True)

    df.to_csv('data/expenses.csv', index=False)
    
    messagebox.showinfo("Success", "Expense added successfully ")
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    load_expenses()
    calculate_total()

#function to load expenses
def load_expenses():
    if not os.path.exists('data/expenses.csv'):
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
        df.to_csv('data/expenses.csv', index=False)
    else:
        df = pd.read_csv('data/expenses.csv')
    
    for i in tree.get_children():
        tree.delete(i)
    for idx, row in df.iterrows():
        tree.insert('', tk.END, values=(row['Date'], row['Category'], row['Amount']))
    calculate_total()

# function to remove a selected expense
def remove_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No expense selected.")
        return

    selected_index = tree.index(selected_item)
    df = pd.read_csv('data/expenses.csv')
    df.drop(selected_index, inplace=True)
    df.to_csv('data/expenses.csv', index=False)

    load_expenses()
    calculate_total()
    messagebox.showinfo("Success", "Expense removed!")

# function to show the data
def visualize_data():
    if not os.path.exists('data/expenses.csv'):
        messagebox.showwarning("Warning", "No data to view.")
        return

    df = pd.read_csv('data/expenses.csv')
    if df.empty:
        messagebox.showwarning("Warning", "No data to view.")
        return

    plt.figure(figsize=(10, 5))
    sns.barplot(x='Category', y='Amount', data=df, estimator=sum, ci=None)
    plt.xticks(rotation=45)
    plt.title('Total expenses by category')
    plt.show()

# function to calculate and show all expenses
def calculate_total():
    if not os.path.exists('data/expenses.csv'):
        messagebox.showwarning("Warning", "No data to calculate.")
        return

    df = pd.read_csv('data/expenses.csv')
    if df.empty:
        messagebox.showwarning("Warning", "No data to calculate.")
        return

    total = df['Amount'].astype(float).sum()
    label_total.config(text=f"Total das Despesas: R$ {total:.2f}")

#config principal window
root = tk.Tk()
root.title("Expense tracker")
# Frame to enter the data
frame_entry = tk.Frame(root)
frame_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
# entry field
tk.Label(frame_entry, text="Data (AAAA-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_date = tk.Entry(frame_entry)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Categoria:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_category = tk.Entry(frame_entry)
entry_category.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Valor:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_amount = tk.Entry(frame_entry)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

# buttons
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tk.Button(frame_buttons, text="Add expense", command=add_expense).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Visualize Data", command=visualize_data).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Remove expense", command=remove_expense).grid(row=2, column=0, padx=5, pady=5)

# expenses table
frame_table = tk.Frame(root)
frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

columns = ('Date', 'Category', 'Value')
tree = ttk.Treeview(frame_table, columns=columns, show='headings')
tree.heading('Date', text='Date')
tree.heading('Category', text='Category')
tree.heading('Value', text='Value')
tree.grid(row=0, column=0, sticky='nsew')

# resizing
frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

label_total = tk.Label(root, text="Total expenses: R$ 0.00", font=('Arial', 14))
label_total.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
# playing function load expenses
load_expenses()
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
# opem the app
root.mainloop()
