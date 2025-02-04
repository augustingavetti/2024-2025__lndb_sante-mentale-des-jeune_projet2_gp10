import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def import_db():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("SQLite Database Files", "*.db")])
    if file_path:
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_list.delete(0, tk.END)
            for table in tables:
                table_list.insert(tk.END, table[0])
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import database: {e}")

def search_table():
    search_term = search_entry.get().lower()
    for i in range(table_list.size()):
        table_name = table_list.get(i).lower()
        if search_term in table_name:
            table_list.selection_set(i)
            table_list.see(i)
            return
    messagebox.showinfo("Search Result", "No matching table found.")

def display_table_data(event):
    selected_table = table_list.get(table_list.curselection())
    if selected_table:
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {selected_table}")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            conn.close()

            # Clear previous data
            for item in tree.get_children():
                tree.delete(item)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display table data: {e}")

# Create the main window
root = tk.Tk()
root.title("SQLite Database Viewer")
root.configure(bg='blue')

# Create and place the import button
import_button = tk.Button(root, text="Import Database", command=import_db, bg='white', fg='blue', font=('Arial', 12, 'bold'))
import_button.pack(pady=10)

# Create and place the search bar
search_frame = tk.Frame(root, bg='blue')
search_frame.pack(pady=10)
search_label = tk.Label(search_frame, text="Search Table:", bg='blue', fg='white', font=('Arial', 12, 'bold'))
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, font=('Arial', 12))
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_table, bg='white', fg='blue', font=('Arial', 12, 'bold'))
search_button.pack(side=tk.LEFT)

# Create and place the listbox to display tables
table_list = tk.Listbox(root, width=50, height=15, font=('Arial', 12))
table_list.pack(pady=10)
table_list.bind('<<ListboxSelect>>', display_table_data)

# Create and place the treeview to display table data
tree = ttk.Treeview(root)
tree.pack(pady=10)

# Run the application
root.mainloop()
