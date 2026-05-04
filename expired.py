import tkinter as tk
from tkinter import ttk
from database import cursor

def open_expired():

    win = tk.Toplevel()
    win.title("Expired Subscriptions")
    win.geometry("600x400")
    win.configure(bg="#0f172a")


    tk.Label(
        win,
        text="Expired Subscriptions",
        bg="#0f172a",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=15)



    frame = tk.Frame(win, bg="#0f172a")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    cols = ("Name", "End Date")

    tree = ttk.Treeview(frame, columns=cols, show="headings")


    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=200)


    tree.pack(fill="both", expand=True)


    cursor.execute("""
        SELECT members.name, subscriptions.end_date
        FROM subscriptions
        JOIN members ON members.id = subscriptions.member_id
        WHERE date(subscriptions.end_date) < DATE('now')
    """)



    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
