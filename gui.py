from tkinter import *
import json
from grepolis import play_grepolis
import threading

class grepolis_gui:

    def __init__(self):

        root = Tk()
        root.geometry('500x300')
        root.title('Grepolis Farming Bot')
        for k in range(4):
            root.columnconfigure(k, weight=1)

        file = open('settings.json', 'r')
        self.settings = json.loads(file.read())
        self.cancel_flag = BooleanVar(root)
        self.cancel_flag.set(False)
        pady=3

        # username label and input
        Label(root, text="username").grid(row=0, column=1, padx=(0, 10), pady=pady, stick='W')
        self.username_input = Entry(root, width=30, name='username')
        self.username_input.insert(0, self.settings['player']['username'])
        self.username_input.grid(row=0, column=2, pady=pady, stick='W')

        # password row
        Label(root, text="password").grid(row=1, column=1, pady=pady, stick='W')
        self.password_input = Entry(root, width=30, show='*', name='password')
        self.password_input.insert(0, self.settings['player']['password'])
        self.password_input.grid(row=1, column=2, stick='W', pady=pady)

        self.rem_pass = BooleanVar()
        remember_password = Checkbutton(root, variable=self.rem_pass, text="remember password", name="rem_pass")
        if len(self.settings['player']['password']) > 0:
            remember_password.select()
        remember_password.grid(row=1, column=3, stick='W')

        # hours to run row
        Label(root, text="max hours to run").grid(row=2, column=1, pady=pady, stick='W')
        self.max_hours = Entry(root, width=30, name='max_hours')
        self.max_hours.insert(0, self.settings['player']['max_hours_to_run'])
        self.max_hours.grid(row=2, column=2, pady=pady, stick='W')

        # game sessions row
        Label(root, text="max game sessions").grid(row=3, column=1, pady=pady, stick='W', padx=(0, 10))
        self.max_sessions = Entry(root, width=30, name='max_sessions')
        self.max_sessions.insert(0, self.settings['player']['max_sessions'])
        self.max_sessions.grid(row=3, column=2, pady=pady, stick='W')

        # frequency label and selector
        Label(root, text="frequency").grid(row=4, pady=pady, stick='W', column=1)
        self.frequency = StringVar(root)
        choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
        self.frequency.set('5 minutes')
        OptionMenu(root, self.frequency, *choices).grid(row=4, column=2, stick='W', pady=pady)

        self.upgrade_buildings = BooleanVar()
        upgrade_buildings_button = Checkbutton(root, variable=self.upgrade_buildings, text="Upgrade City Buildings?", name='upgrade_buildings')
        upgrade_buildings_button.grid(row=5, column=2, stick='W', pady=pady)
        if self.settings['player']['manageSenate']:
            upgrade_buildings_button.select()

        self.reap_villages = BooleanVar()
        reap_villages_button = Checkbutton(root, variable=self.reap_villages, name='reap_villages', text="Reap Villages?")
        reap_villages_button.grid(row=6, column=2, stick='W', pady=pady)
        if self.settings['player']['reapVillages']:
            reap_villages_button.select()

        run_button = Button(text="    run    ")
        run_button.grid(row=7, column=2, stick='W', pady=pady)
        run_button.bind('<Button-1>', self.run_button_callback)
        
        cancel_button = Button(text="    cancel    ")
        cancel_button.bind('<Button-1>', self.cancel_button_callback)
        cancel_button.grid(row=7, column=2, pady=pady)

        self.root = root


    def cancel_button_callback(self, e):
        self.cancel_flag.set(True)


    def run_button_callback(self, e):
        self.save_settings()
        self.cancel_flag.set(False)
        self.farming_thread = threading.Thread(target=lambda: play_grepolis(self.cancel_flag))
        self.farming_thread.start()


    def save_settings(self):
        self.settings['player']['username'] = self.username_input.get()
        self.settings['player']['max_hours_to_run'] = float(self.max_hours.get() or 0.01)
        self.settings['player']['max_sessions'] = int(self.max_sessions.get() or 0)
        self.settings['player']['manageSenate'] = self.upgrade_buildings.get()
        self.settings['player']['reapVillages'] = self.reap_villages.get()
        self.settings['player']['frequency'] = self.frequency.get()
        self.settings['player']['password'] = ''

        if self.rem_pass:
            self.settings['player']['password'] = self.password_input.get()

        outfile = open('settings.json', 'w')
        outfile.write(json.dumps(self.settings, indent=4))


if __name__ == '__main__':
    gui = grepolis_gui()
    gui.root.mainloop()