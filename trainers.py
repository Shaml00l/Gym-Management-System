import tkinter as tk
from tkinter import ttk, messagebox
from database import cursor, conn


def open_trainers():

    win = tk.Toplevel()
    win.title("Trainers Management")
    win.geometry("900x600")
    win.configure(bg="#0f172a")

    #FORM 
    form = tk.Frame(win, bg="#1e293b")
    form.pack(fill="x", padx=10, pady=10)

    tk.Label(form, text="Name", bg="#1e293b", fg="white").grid(row=0, column=0, padx=5)
    name = tk.Entry(form)
    name.grid(row=0, column=1, padx=5)

    tk.Label(form, text="Specialty", bg="#1e293b", fg="white").grid(row=0, column=2, padx=5)

    spec = ttk.Combobox(form, values=[
        "Personal Trainer",
        "Fitness Coach",
        "Yoga Trainer",
        "Bodybuilding Coach",
        "CrossFit Trainer"
    ], state="readonly")
    spec.grid(row=0, column=3, padx=5)

    tk.Label(form, text="Phone", bg="#1e293b", fg="white").grid(row=0, column=4, padx=5)
    phone = tk.Entry(form)
    phone.grid(row=0, column=5, padx=5)

    # SEARCH 
    tk.Label(form, text="Search", bg="#1e293b", fg="white").grid(row=1, column=0, pady=10)
    search = tk.Entry(form)
    search.grid(row=1, column=1, padx=5)

    #  TABLE STYLE 
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#1e293b",
                    foreground="white",
                    fieldbackground="#1e293b",
                    rowheight=25)

    style.configure("Treeview.Heading",
                    background="#334155",
                    foreground="white")
    

    # TABLE 
    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Name", "Specialty", "Phone")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)
    

    #  FUNCTIONS 
    def load():
        for i in tree.get_children():
            tree.delete(i)

        cursor.execute("SELECT * FROM trainers")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)



    def add():
        if name.get() == "" or spec.get() == "" or phone.get() == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        cursor.execute(
            "INSERT INTO trainers(name, specialty, phone) VALUES (?, ?, ?)",
            (name.get(), spec.get(), phone.get())
        )
        conn.commit()
        load()

        name.delete(0, tk.END)
        spec.set("")
        phone.delete(0, tk.END)



    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select trainer")
            return

        data = tree.item(selected)["values"]
        cursor.execute("DELETE FROM trainers WHERE id=?", (data[0],))
        conn.commit()
        load()



    def select_item(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")

            name.delete(0, tk.END)
            spec.set("")
            phone.delete(0, tk.END)

            name.insert(0, values[1])
            spec.set(values[2])
            phone.insert(0, values[3])



    def update():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select trainer")
            return

        data = tree.item(selected)["values"]

        cursor.execute(
            "UPDATE trainers SET name=?, specialty=?, phone=? WHERE id=?",
            (name.get(), spec.get(), phone.get(), data[0])
        )
        conn.commit()
        load()



    def search_trainer():
        keyword = search.get()

        for i in tree.get_children():
            tree.delete(i)

        cursor.execute(
            "SELECT * FROM trainers WHERE name LIKE ?",
            ('%' + keyword + '%',)
        )

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    #EVENTS 
    tree.bind("<ButtonRelease-1>", select_item)


    # BUTTONS
    btn_frame = tk.Frame(win, bg="#0f172a")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add", bg="#22c55e", fg="white",
              width=12, command=add).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Update", bg="#f59e0b", fg="white",
              width=12, command=update).grid(row=0, column=1, padx=5)

    tk.Button(btn_frame, text="Delete", bg="#ef4444", fg="white",
              width=12, command=delete).grid(row=0, column=2, padx=5)

    tk.Button(btn_frame, text="Search", bg="#3b82f6", fg="white",
              width=12, command=search_trainer).grid(row=0, column=3, padx=5)

    tk.Button(btn_frame, text="Refresh", bg="gray", fg="white",
              width=12, command=load).grid(row=0, column=4, padx=5)

    load()
