from tkinter import *
import json
from grepolis import play_grepolis

def open_gui():

    root = Tk()
    root.geometry('500x300')
    root.title('Grepolis Farming Bot')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    pady=3
    Label(root, text="username").grid(row=0, padx=(0, 10), pady=pady, stick='W')
    username_input = Entry(root, width=30, name='username')
    username_input.insert(0, settings['player']['username'])
    username_input.grid(row=0, column=1, pady=pady, stick='W')

    Label(root, text="password").grid(row=1, pady=pady, stick='W')
    password_input = Entry(root, width=30, show='*', name='password')
    password_input.insert(0, settings['player']['password'])
    password_input.grid(row=1, column=1, stick='W')

    rem_pass = BooleanVar()
    remember_password = Checkbutton(root, variable=rem_pass, text="remember password", name="rem_pass")
    if len(settings['player']['password']) > 0:
        remember_password.select()
    remember_password.grid(row=1, column=2, stick='W')

    Label(root, text="max hours to run").grid(row=2, pady=pady, stick='W')
    Entry(root, width=30, name='max_hours_to_run').grid(row=2, column=1, pady=pady, stick='W')

    Label(root, text="max game sessions").grid(row=3, pady=pady, stick='W', padx=(0, 10))
    Entry(root, width=30, name='max_sessions').grid(row=3, column=1, pady=pady, stick='W')

    Label(root, text="frequency").grid(row=4, pady=pady, stick='W')
    frequency = StringVar(root)
    choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
    frequency.set('5 minutes')
    OptionMenu(root, frequency, *choices).grid(row=4, column=1, stick='W', pady=pady)

    upgrade_buildings = BooleanVar()
    upgrade_buildings_button = Checkbutton(root, variable=upgrade_buildings, text="Upgrade City Buildings?", name='upgrade_buildings')
    upgrade_buildings_button.grid(row=5, column=1, stick='W', pady=pady)
    if settings['player']['manageSenate']:
        upgrade_buildings_button.select()

    reap_villages = BooleanVar()
    reap_villages_button = Checkbutton(root, variable=reap_villages, name='reap_villages', text="Reap Villages?")
    reap_villages_button.grid(row=6, column=1, stick='W', pady=pady)
    if settings['player']['reapVillages']:
        reap_villages_button.select()

    def run_button_callback(e):
        save_settings(e, rem_pass.get(), reap_villages.get(), upgrade_buildings.get(), frequency.get())
        play_grepolis()

    run_button = Button(text="    run    ")
    run_button.bind('<Button-1>', run_button_callback)
    run_button.grid(row=7, column=1, stick='W', pady=pady)

    root.mainloop()


def save_settings(e, remember_password, reap_villages, upgrade_buildings, frequency):
    root = e.widget.master
    settings['player']['username'] = root.nametowidget('username').get()
    settings['player']['max_hours_to_run'] = float(root.nametowidget('max_hours_to_run').get() or 0.01)
    settings['player']['max_sessions'] = int(root.nametowidget('max_sessions').get() or 0)
    settings['player']['manageSenate'] = upgrade_buildings
    settings['player']['reapVillages'] = reap_villages
    settings['player']['frequency'] = frequency
    settings['player']['password'] = ''

    if remember_password:
        settings['player']['password'] = root.nametowidget('password').get()

    outfile = open('settings.json', 'w')
    outfile.write(json.dumps(settings, indent=4))

if __name__ == '__main__':
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    open_gui()