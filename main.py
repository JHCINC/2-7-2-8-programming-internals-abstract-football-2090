import time
import tkinter as tk


root = tk.Tk()
root.geometry('600x600')
root.resizable(width=False, height=False)
root.title('Abstract Football')

t_time = tk.Text(root)
t_time.pack()


def main():
    t_time.config(state='normal')
    t_time.delete('1.0', tk.END)
    t_time.insert(tk.END, str(time.time()))
    t_time.config(state='disabled')

    root.after(1, main)


root.after(1, main)
root.mainloop()
