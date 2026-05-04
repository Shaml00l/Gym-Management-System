import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import cursor


def open_reports():

    win = tk.Toplevel()
    win.title("Reports Dashboard")

    
    win.geometry("950x650")
    win.resizable(False, False)
    win.configure(bg="#0f172a")


    # HEADER 
    tk.Label(
        win,
        text="Reports Dashboard",
        bg="#0f172a",
        fg="white",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=15)


    # FUNCTIONS 
    def count(table):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def revenue():
        cursor.execute("SELECT IFNULL(SUM(amount),0) FROM payments")
        return cursor.fetchone()[0]

    def attendance():
        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE status='Present'
        """)
        return cursor.fetchone()[0]


    # CARDS
    stats = tk.Frame(win, bg="#0f172a")
    stats.pack(pady=10)

    def card(title, value, color, col):

        box = tk.Frame(
            stats,
            bg="#1e293b",
            width=200,
            height=100
        )

        box.grid(row=0, column=col, padx=10)
        box.pack_propagate(False)

        tk.Frame(box, bg=color, height=4).pack(fill="x")

        tk.Label(
            box,
            text=title,
            bg="#1e293b",
            fg="#9ca3af",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=5)

        tk.Label(
            box,
            text=value,
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack()


    card("Members", count("members"), "#22c55e", 0)
    card("Trainers", count("trainers"), "#3b82f6", 1)
    card("Revenue", f"{revenue()} EGP", "#ef4444", 2)
    card("Attendance", attendance(), "#8b5cf6", 3)


    # TABLE 
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#1e293b",
        foreground="white",
        fieldbackground="#1e293b",
        rowheight=25
    )

    style.configure(
        "Treeview.Heading",
        background="#334155",
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )


    # TABLE 
    table_frame = tk.Frame(win, bg="#0f172a")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    cols = ("Report", "Value")

    tree = ttk.Treeview(table_frame, columns=cols, show="headings")

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=250, anchor="center")

    tree.pack(fill="both", expand=True)


    data = [
        ("Total Members", count("members")),
        ("Total Trainers", count("trainers")),
        ("Subscriptions", count("subscriptions")),
        ("Total Revenue", revenue()),
        ("Attendance", attendance())
    ]

    for row in data:
        tree.insert("", "end", values=row)


# BUTTONS 
    btn_frame = tk.Frame(win, bg="#0f172a")
    btn_frame.pack(pady=15)

    btn_style = {
        "width": 12,
        "fg": "white",
        "bd": 0,
        "font": ("Segoe UI", 10, "bold")
    }


    def refresh():
        win.destroy()
        open_reports()


    def export():

        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file:
            return

        with open(file, "w") as f:
            f.write("GYM REPORT\n")
            f.write("-----------------\n")
            f.write(f"Members: {count('members')}\n")
            f.write(f"Trainers: {count('trainers')}\n")
            f.write(f"Subscriptions: {count('subscriptions')}\n")
            f.write(f"Revenue: {revenue()} EGP\n")
            f.write(f"Attendance: {attendance()}\n")

        messagebox.showinfo("Success", "Report exported")


    tk.Button(btn_frame, text="Refresh", bg="#3b82f6", command=refresh, **btn_style).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Export", bg="#22c55e", command=export, **btn_style).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Close", bg="#ef4444", command=win.destroy, **btn_style).grid(row=0, column=2, padx=5)
