import tkinter as tk
from tkinter import ttk, messagebox
from database import cursor, conn

def open_members():

    win = tk.Toplevel()
    win.title("Members Management")
    win.geometry("950x600")
    win.configure(bg="#0f172a")

    form = tk.Frame(win, bg="#1e293b")
    form.pack(fill="x", padx=10, pady=10)

    tk.Label(form, text="Name", bg="#1e293b", fg="white").grid(row=0, column=0, padx=5)
    name = tk.Entry(form)
    name.grid(row=0, column=1, padx=5)

    tk.Label(form, text="Age", bg="#1e293b", fg="white").grid(row=0, column=2, padx=5)
    age = tk.Entry(form)
    age.grid(row=0, column=3, padx=5)

    tk.Label(form, text="Phone", bg="#1e293b", fg="white").grid(row=0, column=4, padx=5)
    phone = tk.Entry(form)
    phone.grid(row=0, column=5, padx=5)

    # Trainer Dropdown
    tk.Label(form, text="Trainer", bg="#1e293b", fg="white").grid(row=0, column=6, padx=5)
    trainer_combo = ttk.Combobox(form, state="readonly")
    trainer_combo.grid(row=0, column=7, padx=5)

    # ================= SEARCH =================
    tk.Label(form, text="Search", bg="#1e293b", fg="white").grid(row=1, column=0, pady=10)
    search = tk.Entry(form)
    search.grid(row=1, column=1, padx=5)

    # ================= STYLE =================
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

    # ================= TABLE =================
    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Name", "Age", "Phone", "Trainer")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    # ================= FUNCTIONS =================

    def load_trainers():
        cursor.execute("SELECT id, name FROM trainers")
        trainers = cursor.fetchall()
        trainer_combo['values'] = [f"{t[0]} - {t[1]}" for t in trainers]

    def load():
        for i in tree.get_children():
            tree.delete(i)

        cursor.execute("""
        SELECT members.id, members.name, members.age, members.phone, trainers.name
        FROM members
        LEFT JOIN trainers ON members.trainer_id = trainers.id
        """)

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def add():
        try:
            if name.get() == "" or age.get() == "" or phone.get() == "":
                messagebox.showerror("Error", "Fill all fields")
                return

            if trainer_combo.get() == "":
                messagebox.showerror("Error", "Select Trainer")
                return

            trainer_id = trainer_combo.get().split(" - ")[0]

            cursor.execute(
                "INSERT INTO members(name, age, phone, trainer_id) VALUES (?, ?, ?, ?)",
                (name.get(), int(age.get()), phone.get(), int(trainer_id))
            )
            conn.commit()

            messagebox.showinfo("Success", "Added successfully 🎉")

            load()

            name.delete(0, tk.END)
            age.delete(0, tk.END)
            phone.delete(0, tk.END)
            trainer_combo.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select member")
            return

        data = tree.item(selected)["values"]
        cursor.execute("DELETE FROM members WHERE id=?", (data[0],))
        conn.commit()
        load()
    def select_item(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")

            name.delete(0, tk.END)
            age.delete(0, tk.END)
            phone.delete(0, tk.END)

            name.insert(0, values[1])
            age.insert(0, values[2])
            phone.insert(0, values[3])
            
            for item in trainer_combo['values']:
                if values[4] and values[4] in item:
                    trainer_combo.set(item)
                    break
    def update():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select member")
            return

        if name.get() == "" or age.get() == "" or phone.get() == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        if trainer_combo.get() == "":
            messagebox.showerror("Error", "Select Trainer")
            return
        try:
            data = tree.item(selected)["values"]
            trainer_id = trainer_combo.get().split(" - ")[0]

            cursor.execute(
                "UPDATE members SET name=?, age=?, phone=?, trainer_id=? WHERE id=?",
                (name.get(), int(age.get()), phone.get(), int(trainer_id), data[0])
            )
            conn.commit()

            messagebox.showinfo("Success", "Updated successfully ✏️")

            load()

            name.delete(0, tk.END)
            age.delete(0, tk.END)
            phone.delete(0, tk.END)
            trainer_combo.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_member():
        keyword = search.get()

        for i in tree.get_children():
            tree.delete(i)

        cursor.execute("""
        SELECT members.id, members.name, members.age, members.phone, trainers.name
        FROM members
        LEFT JOIN trainers ON members.trainer_id = trainers.id
        WHERE members.name LIKE ?
        """, ('%' + keyword + '%',))

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # ================= EVENTS =================
    tree.bind("<ButtonRelease-1>", select_item)

    # ================= BUTTONS =================
    btn_frame = tk.Frame(win, bg="#0f172a")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add", bg="#22c55e", fg="white",
              width=12, command=add).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Update", bg="#f59e0b", fg="white",
              width=12, command=update).grid(row=0, column=1, padx=5)

    tk.Button(btn_frame, text="Delete", bg="#ef4444", fg="white",
              width=12, command=delete).grid(row=0, column=2, padx=5)

    tk.Button(btn_frame, text="Search", bg="#3b82f6", fg="white",
              width=12, command=search_member).grid(row=0, column=3, padx=5)

    tk.Button(btn_frame, text="Refresh", bg="gray", fg="white",
              width=12, command=load).grid(row=0, column=4, padx=5)
  
    load_trainers()
    load()
