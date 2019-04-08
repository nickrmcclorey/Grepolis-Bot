from tkinter import *
import json
from grepolis import play_grepolis
from Grid_manager import Grid_manager
import threading

class grepolis_gui:

    def __init__(self):

        self.root = Tk()
        self.settings_frame = Frame(self.root)
        self.control_frame = Frame(self.root)
        self.settings = load_settings()

        self.root.geometry('500x300')
        self.root.title('Grepolis Farming Bot')
        self.setup_settings_frame(self.settings_frame)


    def setup_settings_frame(self, frame):
        manager = Grid_manager(frame)

        self.cancel_flag = BooleanVar(frame)
        self.cancel_flag.set(False)

        # username label and input
        manager.insert(Label(frame, text="username"))
        self.username_input = Entry(frame, width=30, name='username')
        self.username_input.insert(0, self.settings['player']['username'])
        manager.insert(self.username_input)
        manager.new_row()

        # password row
        manager.insert(Label(frame, text="password"))
        self.password_input = Entry(frame, width=30, show='*', name='password')
        self.password_input.insert(0, self.settings['player']['password'])
        manager.insert(self.password_input)

        self.rem_pass = BooleanVar()
        remember_password = Checkbutton(frame, variable=self.rem_pass, text="remember password", name="rem_pass")
        if len(self.settings['player']['password']) > 0:
            remember_password.select()
        manager.insert(remember_password)
        manager.new_row()

        # hours to run row
        manager.insert(Label(frame, text="max hours to run"))
        self.max_hours = Entry(frame, width=30, name='max_hours')
        self.max_hours.insert(0, self.settings['player']['max_hours_to_run'])
        manager.insert(self.max_hours)
        manager.new_row()

        # game sessions row
        manager.insert(Label(frame, text="max game sessions"))
        self.max_sessions = Entry(frame, width=30, name='max_sessions')
        self.max_sessions.insert(0, self.settings['player']['max_sessions'])
        manager.insert(self.max_sessions)
        manager.new_row()

        # frequency label and selector
        manager.insert(Label(frame, text="frequency"))
        self.frequency = StringVar(frame)
        choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
        self.frequency.set('5 minutes')
        manager.insert(OptionMenu(frame, self.frequency, *choices))
        manager.new_row(1)

        self.upgrade_buildings = BooleanVar()
        upgrade_buildings_button = Checkbutton(frame, variable=self.upgrade_buildings, text="Upgrade City Buildings?", name='upgrade_buildings')
        manager.insert(upgrade_buildings_button)
        if self.settings['player']['manageSenate']:
            upgrade_buildings_button.select()
        manager.new_row(1)

        self.reap_villages = BooleanVar()
        reap_villages_button = Checkbutton(frame, variable=self.reap_villages, name='reap_villages', text="Reap Villages?")
        manager.insert(reap_villages_button)
        if self.settings['player']['reapVillages']:
            reap_villages_button.select()
        manager.new_row(1)

        run_button = Button(frame, text="    run    ")
        run_button.bind('<Button-1>', self.run_button_callback)
        manager.insert(run_button)
        
        cancel_button = Button(frame, text="    cancel    ")
        cancel_button.bind('<Button-1>', self.cancel_button_callback)
        manager.insert(cancel_button, nextSpot=False, stick='E')

        frame.grid(column=1, pady=10)
        for k in range(3):
            self.root.columnconfigure(k, weight=1)


    def setup_control_frame(self, frame):
        # frame.grid()
        print('cool')

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

def load_settings():
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    file.close()
    return settings

if __name__ == '__main__':
    gui = grepolis_gui()
    gui.root.mainloop()