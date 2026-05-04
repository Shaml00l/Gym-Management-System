import tkinter as tk
from database import cursor

from members import open_members
from trainers import open_trainers
from subscriptions import open_subscriptions
from payments import open_payments
from attendance import open_attendance
from reports import open_reports
from expired import open_expired


# COLORS
BG = "#020617"
SIDEBAR = "#0b1220"
CARD = "#0f172a"

TEXT = "#e5e7eb"
MUTED = "#94a3b8"

PRIMARY = "#3b82f6"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"
ACCENT = "#06b6d4"


def dashboard(username):

    win = tk.Toplevel()
    win.title("Gym Dashboard")
    win.attributes('-zoomed', True)
    win.configure(bg=BG)


# SIDEBAR 
    sidebar = tk.Frame(win, bg=SIDEBAR, width=280)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)


    tk.Label(
        sidebar,
        text="🏋 GYM System",
        bg=SIDEBAR,
        fg="white",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=30)
    

    tk.Label(
        sidebar,
        text=f"Welcome,\n{username}",
        bg=SIDEBAR,
        fg="#38bdf8",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=10)



    active = {"btn": None}

    def menu_button(text, command):

        def click():
            if active["btn"]:
                active["btn"].configure(bg=SIDEBAR)

            btn.configure(bg="#1d4ed8")
            active["btn"] = btn
            command()


        btn = tk.Button(
            sidebar,
            text="   " + text,
            anchor="w",
            bg=SIDEBAR,
            fg=TEXT,
            bd=0,
            height=2,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=click
        )

        btn.pack(fill="x", padx=15, pady=5)


        def hover(e):
            if btn != active["btn"]:
                btn.configure(bg="#1f2937")

        def leave(e):
            if btn != active["btn"]:
                btn.configure(bg=SIDEBAR)

        btn.bind("<Enter>", hover)
        btn.bind("<Leave>", leave)


    menu_button("👥 Members", open_members)
    menu_button("🏋 Trainers", open_trainers)
    menu_button("📅 Subscriptions", open_subscriptions)
    menu_button("💳 Payments", open_payments)
    menu_button("✅ Attendance", open_attendance)
    menu_button("📊 Reports", open_reports)
    menu_button("⚠ Expired Subs", open_expired)


    tk.Button(
        sidebar,
        text="Logout",
        bg=DANGER,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        height=2,
        bd=0,
        cursor="hand2",
        command=win.destroy
    ).pack(side="bottom", fill="x", padx=15, pady=20)



#  MAIN 
    main = tk.Frame(win, bg=BG)
    main.pack(fill="both", expand=True)


# HEADER 
    header = tk.Frame(main, bg=BG)
    header.pack(fill="x", pady=15)

    tk.Label(
        header,
        text="Dashboard Overview",
        bg=BG,
        fg="white",
        font=("Segoe UI", 26, "bold")
    ).pack(side="left", padx=25)


    tk.Label(
        header,
        text="Live system stats",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 11)
    ).pack(side="left", padx=10)



# DATABASE 
    def get_count(table):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]


    def get_revenue():
        cursor.execute("SELECT IFNULL(SUM(amount),0) FROM payments")
        return cursor.fetchone()[0]


    def get_today_attendance():
        cursor.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date = DATE('now')
            AND status='Present'
        """)
        return cursor.fetchone()[0]


#  CARDS 
    cards_frame = tk.Frame(main, bg=BG)
    cards_frame.pack(pady=30)


    def create_card(title, value, color, row, col):

        card = tk.Frame(
            cards_frame,
            bg=CARD,
            width=270,
            height=150,
            highlightbackground="#1f2937",
            highlightthickness=1
        )
        card.grid(row=row, column=col, padx=20, pady=20)
        card.pack_propagate(False)

        
        tk.Frame(card, bg=color, height=5).pack(fill="x")

        tk.Label(
            card,
            text=title,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(15, 5))

        tk.Label(
            card,
            text=value,
            bg=CARD,
            fg="white",
            font=("Segoe UI", 28, "bold")
        ).pack()


    def load_dashboard():

        for widget in cards_frame.winfo_children():
            widget.destroy()

        create_card("Members", get_count("members"), SUCCESS, 0, 0)
        create_card("Trainers", get_count("trainers"), PRIMARY, 0, 1)
        create_card("Subscriptions", get_count("subscriptions"), WARNING, 0, 2)

        create_card("Revenue", f"{get_revenue()} EGP", DANGER, 1, 0)
        create_card("Attendance Today", get_today_attendance(), ACCENT, 1, 1)


#  REFRESH 
    tk.Button(
        main,
        text=" Refresh Dashboard",
        bg=ACCENT,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=load_dashboard
    ).pack(pady=20)


#  FOOTER 
    tk.Label(
        main,
        text=" Gym Managament System ",
        bg=BG,
        fg="#475569",
        font=("Segoe UI", 10)
    ).pack(side="bottom", pady=10)


    load_dashboard()
