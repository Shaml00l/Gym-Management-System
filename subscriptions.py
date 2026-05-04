import tkinter as tk
from tkinter import ttk, messagebox
from database import cursor, conn
from datetime import datetime, timedelta


def open_subscriptions():

    win = tk.Toplevel()
    win.title("Subscriptions Management")
    win.geometry("1000x600")
    win.configure(bg="#0f172a")

    # FORM 
    form = tk.Frame(win, bg="#1e293b")
    form.pack(fill="x", padx=10, pady=10)

    tk.Label(form, text="Member", bg="#1e293b", fg="white").grid(row=0, column=0)
    member_combo = ttk.Combobox(form, state="readonly")
    member_combo.grid(row=0, column=1, padx=5)


    tk.Label(form, text="Plan", bg="#1e293b", fg="white").grid(row=0, column=2)
    plan = ttk.Combobox(form, values=["1 Month", "3 Months", "6 Months"], state="readonly")
    plan.grid(row=0, column=3, padx=5)


    tk.Label(form, text="Price", bg="#1e293b", fg="white").grid(row=0, column=4)
    price = tk.Entry(form)
    price.grid(row=0, column=5, padx=5)


    #  TABLE 
    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Member", "Plan", "Start", "End", "Price")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)



    # FUNCTIONS 

    def load_members():
        cursor.execute("SELECT id, name FROM members")
        members = cursor.fetchall()
        member_combo['values'] = [f"{m[0]} - {m[1]}" for m in members]

    def load():
        for i in tree.get_children():
            tree.delete(i)

        cursor.execute("""
        SELECT subscriptions.id, members.name, plan, start_date, end_date, price
        FROM subscriptions
        JOIN members ON subscriptions.member_id = members.id
        """)

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)


    def calculate_end(start, plan):
        start_date = datetime.strptime(start, "%Y-%m-%d")

        if plan == "1 Month":
            end = start_date + timedelta(days=30)
        elif plan == "3 Months":
            end = start_date + timedelta(days=90)
        else:
            end = start_date + timedelta(days=180)

        return end.strftime("%Y-%m-%d")



    def add():
        if member_combo.get() == "" or plan.get() == "" or price.get() == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        member_id = member_combo.get().split(" - ")[0]
        start = datetime.now().strftime("%Y-%m-%d")
        end = calculate_end(start, plan.get())

        cursor.execute("""
        INSERT INTO subscriptions(member_id, plan, start_date, end_date, price)
        VALUES (?, ?, ?, ?, ?)
        """, (member_id, plan.get(), start, end, price.get()))

        conn.commit()
        load()


    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select subscription")
            return

        data = tree.item(selected)["values"]
        cursor.execute("DELETE FROM subscriptions WHERE id=?", (data[0],))
        conn.commit()
        load()



    #  BUTTONS 
    btn_frame = tk.Frame(win, bg="#0f172a")
    btn_frame.pack(pady=10)


    tk.Button(btn_frame, text="Add Subscription", bg="#22c55e", fg="white",
              command=add).grid(row=0, column=0, padx=10)


    tk.Button(btn_frame, text="Delete", bg="#ef4444", fg="white",
              command=delete).grid(row=0, column=1, padx=10)


    tk.Button(btn_frame, text="Refresh", bg="#3b82f6", fg="white",
              command=load).grid(row=0, column=2, padx=10)


    load_members()
    load()
