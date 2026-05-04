import tkinter as tk
from tkinter import messagebox
from database import cursor
from register import open_register
from dashboard import dashboard


root = tk.Tk()
root.title("Gym System - Login")
root.geometry("450x420")
root.configure(bg="#1e1e2f")


frame = tk.Frame(root, bg="#2c2c3e")
frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=350)


tk.Label(frame, text="Login",
         bg="#2c2c3e", fg="white",
         font=("Arial", 20, "bold")).pack(pady=15)


# Username
tk.Label(frame, text="Username", bg="#2c2c3e", fg="white").pack()
entry_username = tk.Entry(frame, font=("Arial", 12))
entry_username.pack(pady=8, ipady=4)


# Password
tk.Label(frame, text="Password", bg="#2c2c3e", fg="white").pack()
entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
entry_password.pack(pady=8, ipady=4)


show_pass = False

def toggle_password():
    global show_pass
    show_pass = not show_pass
    entry_password.config(show="" if show_pass else "*")


tk.Button(frame, text="👁 Show/Hide",
          command=toggle_password,
          bg="#444", fg="white").pack(pady=5)


# Login Function
def login():
    u = entry_username.get().strip()
    p = entry_password.get().strip()

    if u == "" or p == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (u, p)
    )

    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", f"Welcome {u} 🎉")
        root.withdraw()
        dashboard(u)
    else:
        messagebox.showerror("Error", "Wrong data")
        entry_password.delete(0, tk.END)  # يمسح الباسورد بس



root.bind("<Return>", lambda event: login())


# Buttons
tk.Button(frame, text="Login",
          bg="#4CAF50", fg="white",
          width=20,
          command=login).pack(pady=12)

tk.Button(frame, text="Create Account",
          bg="#2196F3", fg="white",
          width=20,
          command=lambda: open_register(root)).pack(pady=5)


entry_username.focus()

root.mainloop()
