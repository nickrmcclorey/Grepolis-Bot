from tkinter import *
import json
from grepolis import play_grepolis

def open_gui():
    file = open('settings.json', 'r')
    settings = json.loads(file.read())

    root = Tk()
    root.geometry('500x300')
    root.title('Grepolis Farming Bot')

    pady=3
    Label(root, text="username").grid(row=0,  padx=(0, 10), pady=pady, stick='W')
    username_input = Entry(root, width=30)
    username_input.insert(0, settings['player']['username'])
    username_input.grid(row=0, column=1, pady=pady, stick='W')

    Label(root, text="password").grid(row=1, pady=pady, stick='W')
    password_input = Entry(root, width=30, show='*')
    password_input.insert(0, settings['player']['password'])
    password_input.grid(row=1, column=1, stick='W')
    remember_password = Checkbutton(root, text="remember password")
    if len(settings['player']['password']) > 0:
        remember_password.select()
    remember_password.grid(row=1, column=2, stick='W')

    Label(root, text="max hours to run").grid(row=2, pady=pady, stick='W')
    Entry(root, width=30).grid(row=2, column=1, pady=pady, stick='W')

    Label(root, text="max game sessions").grid(row=3, pady=pady, stick='W', padx=(0, 10))
    Entry(root, width=30).grid(row=3, column=1, pady=pady, stick='W')

    Label(root, text="frequency").grid(row=4, pady=pady, stick='W')
    tk_var = StringVar(root)
    choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
    tk_var.set('5 minutes')
    OptionMenu(root, tk_var, *choices).grid(row=4, column=1, stick='W', pady=pady)

    upgrade_buildings = Checkbutton(root, text="Upgrade City Buildings?")
    upgrade_buildings.grid(row=5, column=1, stick='W', pady=pady)
    if settings['player']['manageSenate']:
        upgrade_buildings.select()

    reap_villages = Checkbutton(root, text="Reap Villages?")
    reap_villages.grid(row=6, column=1, stick='W', pady=pady)
    if settings['player']['reapVillages']:
        reap_villages.select()

    Button(text="    run    ", command=play_grepolis).grid(row=7, column=1, stick='W', pady=pady)

    root.mainloop()


def run_button_callback(e):
    print(e.widget)

if __name__ == '__main__':
    open_gui()