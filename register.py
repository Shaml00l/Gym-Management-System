import tkinter as tk
from tkinter import messagebox
from database import cursor, conn


def open_register(root):

    win = tk.Toplevel(root)
    win.title("Gym - Create Account")
    win.geometry("450x520")
    win.configure(bg="#1e1e2f")

    frame = tk.Frame(win, bg="#2c2c3e")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)

    tk.Label(frame, text="Create Account",
             bg="#2c2c3e", fg="white",
             font=("Arial", 18, "bold")).pack(pady=15)

    
    
    tk.Label(frame, text="Username", bg="#2c2c3e", fg="white").pack()
    username = tk.Entry(frame, font=("Arial", 12))
    username.pack(pady=6, ipady=4)

    
    
    tk.Label(frame, text="Email", bg="#2c2c3e", fg="white").pack()
    email = tk.Entry(frame, font=("Arial", 12))
    email.pack(pady=6, ipady=4)

    
    
    tk.Label(frame, text="Password", bg="#2c2c3e", fg="white").pack()
    password = tk.Entry(frame, show="*", font=("Arial", 12))
    password.pack(pady=6, ipady=4)

    
    
    tk.Label(frame, text="Confirm Password", bg="#2c2c3e", fg="white").pack()
    confirm = tk.Entry(frame, show="*", font=("Arial", 12))
    confirm.pack(pady=6, ipady=4)

    
    
    
    show_pass = False
    def toggle_password():
        nonlocal show_pass
        show_pass = not show_pass
        password.config(show="" if show_pass else "*")
        confirm.config(show="" if show_pass else "*")

    tk.Button(frame, text="👁 Show/Hide Password",
              bg="#444", fg="white",
              command=toggle_password).pack(pady=8)

    
    
    def register():

        u = username.get().strip()
        e = email.get().strip()
        p = password.get().strip()
        c = confirm.get().strip()

        if u == "" or e == "" or p == "" or c == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        if "@" not in e:
            messagebox.showerror("Error", "Invalid email")
            return

        if len(p) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return

        if p != c:
            messagebox.showerror("Error", "Passwords do not match")
            password.delete(0, tk.END)
            confirm.delete(0, tk.END)
            return

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (u, e, p)
            )
            conn.commit()

            messagebox.showinfo("Success", "Account created 🎉")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", "Username already exists")

   
   
    win.bind("<Return>", lambda event: register())

    tk.Button(frame, text="Create Account",
              bg="#4CAF50", fg="white",
              width=20,
              command=register).pack(pady=15)

    
    
    username.focus()
