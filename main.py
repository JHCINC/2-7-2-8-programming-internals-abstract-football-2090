import time
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import ttk
from PIL import Images, ImageTK




root = tk.Tk()
root.geometry('800x800')
root.config(bg="#1D1D29")
root.resizable(width=False, height=False)
root.title("Abstract Football 2025")
arsenal_logo = Images.open("arsenal_logo.png")
mancity_logo = Images.open("man_city_logo.png")

# Labels for Heading and Subheading of GUIS
lb_heading1 = tk.Label(root, text="Ultimate Team Football 2025", font=("Times New Roman", 28, "bold italic"), fg="lightgrey", bg="#1D1D29")
lb_heading2 = tk.Label(root, text="Team Selection", font=("Times New Roman", 20, "bold"), fg="lightgrey", bg="#1D1D29")

# Labels for teams
lb_heading3 = tk.Label(root, text="Select Your Teams:", font=("Ariel", 15), fg="lightgrey", bg="#1D1D29")
lb_vs = tk.Label(root, text="VS", font=("Sans-serif", 25, "bold italic"), fg="White", bg="#1D1D29")


n = tk.StringVar()
n1 = tk.StringVar()
hometeam_chosen = ttk.Combobox(root, textvariable=n, width=20, state="readonly")
awayteam_chosen = ttk.Combobox(root, textvariable=n1, width=20, state="readonly")

# Team Selection Dropdown
teams = ('Select a team', 'Man City', 'Real Madrid', 'Barcelona', 'Arsenal', 'Liverpool', 'Bayern Munich')
hometeam_chosen['values'] = teams
awayteam_chosen['values'] = teams

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)



frame1 = create_widget(root, tk.Frame, bg='white', bd=0, cursor='hand2', height=180,
                      highlightthickness=0, relief=tk.RAISED, width=150)

frame2 = create_widget(root, tk.Frame, bg='white', bd=0, cursor='hand2', height=180,
                      highlightthickness=0, relief=tk.RAISED, width=150)



lb_heading1.place(x=150 , y=90)
lb_heading2.place(x=280, y=140)
lb_heading3.place(x=285, y=210)
lb_vs.place(x=350, y=280)
hometeam_chosen.place(x=180, y=290)
awayteam_chosen.place(x=430, y=290)
frame1.place(x=600, y=230)
frame2.place(x=20, y=230)
mancity_logo.place(x=398, y=321)





def main():
    root.after(1, main)


root.after(1, main)
root.mainloop()
