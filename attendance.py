import tkinter as tk
from tkinter import ttk, messagebox
from database import cursor, conn
from datetime import datetime

def open_attendance():

    win = tk.Toplevel()
    win.title("Attendance System")
    win.geometry("950x600")
    win.configure(bg="#0f172a")

    # FORM 
    
    form = tk.Frame(win, bg="#1e293b")
    form.pack(fill="x", padx=10, pady=10)

    tk.Label(form, text="Member", bg="#1e293b", fg="white").grid(row=0, column=0)
    member_combo = ttk.Combobox(form, state="readonly")
    member_combo.grid(row=0, column=1, padx=5)

    tk.Label(form, text="Status", bg="#1e293b", fg="white").grid(row=0, column=2)
    status = ttk.Combobox(form, values=["Present", "Absent"], state="readonly")
    status.grid(row=0, column=3, padx=5)

    # TABLE
    
    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Member", "Date", "Status")
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
        SELECT attendance.id, members.name, date, status
        FROM attendance
        JOIN members ON attendance.member_id = members.id
        """)

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def mark_attendance():
        if member_combo.get() == "" or status.get() == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        member_id = member_combo.get().split(" - ")[0]
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
        INSERT INTO attendance(member_id, date, status)
        VALUES (?, ?, ?)
        """, (member_id, today, status.get()))

        conn.commit()
        load()

    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select record")
            return

        data = tree.item(selected)["values"]
        cursor.execute("DELETE FROM attendance WHERE id=?", (data[0],))
        conn.commit()
        load()

    #  BUTTONS 
    
    btn_frame = tk.Frame(win, bg="#0f172a")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Mark Attendance", bg="#22c55e", fg="white",
              command=mark_attendance, width=15).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="Delete", bg="#ef4444", fg="white",
              command=delete, width=15).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="Refresh", bg="#3b82f6", fg="white",
              command=load, width=15).grid(row=0, column=2, padx=10)

    
    
    load_members()
    load()
