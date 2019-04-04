from tkinter import *

root = Tk()
root.geometry('500x500')

username_label = Label(root, text="username").grid(row=0)
username_input = Text(root, height=1, width=20).grid(row=0, column=1)

password_label = Label(root, text="password").grid(row=1)
password_input = Text(root, height=1, width=20).grid(row=1, column=1)
remember_password = Checkbutton(root, text="remember password").grid(row=1, column=2)

ttr_label = Label(root, text="hours to run").grid(row=2)
ttr_input = Text(root, height=1, width=20).grid(row=2, column=1)

frequency_label = Label(root, text="frequency").grid(row=3)
tk_var = StringVar(root)
choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
tk_var.set('5 minutes')
frequency_menu = OptionMenu(root, tk_var, *choices).grid(row=3, column=1)

upgrade_buildings = Checkbutton(root, text="Upgrade City Buildings?").grid(row=4, column=1)
reap_villages = Checkbutton(root, text="Reap Villages?").grid(row=5, column=1)


root.mainloop()