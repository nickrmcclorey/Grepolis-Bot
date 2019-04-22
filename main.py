import tkinter as tk
import json
from grepolis import play_grepolis
from Grid_manager import Grid_manager
import threading


# class that sets up and handles the GUI
class grepolis_gui:

    def __init__(self):

        self.root = tk.Tk()
        self.settings_frame = tk.Frame(self.root)
        self.control_frame = tk.Frame(self.root)
        self.settings = load_settings()
        self.cancel_flag = tk.BooleanVar(self.root)

        self.root.geometry('500x300')
        self.root.title('Grepolis Farming Bot')
        self.setup_settings_frame(self.settings_frame)
        self.setup_control_frame(self.control_frame)
        self.settings_frame.grid(column=1, pady=10)
        for k in range(3):
            self.root.columnconfigure(k, weight=1)


    def setup_settings_frame(self, frame):
        manager = Grid_manager(frame)

        # username label and input
        manager.insert(tk.Label(frame, text="username"))
        self.username_input = tk.Entry(frame, width=30, name='username')
        self.username_input.insert(0, self.settings['player']['username'])
        manager.insert(self.username_input)
        manager.new_row()

        # password row
        manager.insert(tk.Label(frame, text="password"))
        self.password_input = tk.Entry(frame, width=30, show='*', name='password')
        self.password_input.insert(0, self.settings['player']['password'])
        manager.insert(self.password_input)

        self.rem_pass = tk.BooleanVar()
        remember_password = tk.Checkbutton(frame, variable=self.rem_pass, text="remember password", name="rem_pass")
        if len(self.settings['player']['password']) > 0:
            remember_password.select()
        manager.insert(remember_password)
        manager.new_row()

        # hours to run row
        manager.insert(tk.Label(frame, text="max hours to run"))
        self.max_hours = tk.Entry(frame, width=30, name='max_hours')
        self.max_hours.insert(0, self.settings['player']['max_hours_to_run'])
        manager.insert(self.max_hours)
        manager.new_row()

        # game sessions row
        manager.insert(tk.Label(frame, text="max game sessions"))
        self.max_sessions = tk.Entry(frame, width=30, name='max_sessions')
        self.max_sessions.insert(0, self.settings['player']['max_sessions'])
        manager.insert(self.max_sessions)
        manager.new_row()

        # frequency label and selector
        manager.insert(tk.Label(frame, text="frequency"))
        self.frequency = tk.StringVar(frame)
        choices = { '5 minutes', '20 minutes', '90 minutes', '4 hours'}
        self.frequency.set('5 minutes')
        manager.insert(tk.OptionMenu(frame, self.frequency, *choices))
        manager.new_row(1)

        # checkbox to upgrade buildings
        self.upgrade_buildings = tk.BooleanVar()
        upgrade_buildings_button = tk.Checkbutton(frame, variable=self.upgrade_buildings, text="Upgrade City Buildings?", name='upgrade_buildings')
        manager.insert(upgrade_buildings_button)
        if self.settings['player']['manageSenate']:
            upgrade_buildings_button.select()
        manager.new_row(1)

        # checkbox to reap villages
        self.reap_villages = tk.BooleanVar()
        reap_villages_button = tk.Checkbutton(frame, variable=self.reap_villages, name='reap_villages', text="Farm Village Resources?")
        manager.insert(reap_villages_button)
        if self.settings['player']['reapVillages']:
            reap_villages_button.select()
        manager.new_row(1)

        run_button = tk.Button(frame, text="    run    ")
        run_button.bind('<Button-1>', self.run_button_callback)
        manager.insert(run_button)

    # defines the layout for the screen when farming has started (the control frame)
    def setup_control_frame(self, frame):
        cancel_button = tk.Button(frame, text="    cancel    ")
        cancel_button.bind('<Button-1>', self.cancel_button_callback)
        cancel_button.grid(row=0, column=0, padx=10, pady=10, stick='W')
        self.message_board = tk.Label(frame, text="Message Board")
        self.message_board.grid(row=0, column=1, padx=(30, 10), pady=10, stick='W')

    # hides the control_frame and shows the settings_frame
    def show_settings_frame(self):
        self.control_frame.grid_remove()
        self.settings_frame.grid()

    # used by the farming thread to update user on progress
    def set_message_board(self, text):
        self.message_board.config(text=text)

    # launched by the cancel button on the control_frame
    def cancel_button_callback(self, e):
        self.cancel_flag.set(True)
        self.message_board.grid(stick= 'W', row=1, column=1)
        tk.Label(self.control_frame, text='Ending game session...').grid(stick='W', row=0, column=1)

    # launched by the "run" button. It begins farming
    def run_button_callback(self, e):
        self.save_settings()
        self.cancel_flag.set(False)
        threadLauncher = lambda: play_grepolis(self.cancel_flag, self.set_message_board, self.show_settings_frame)
        self.farming_thread = threading.Thread(target=threadLauncher)
        self.farming_thread.start()
        self.settings_frame.grid_remove()
        self.control_frame.grid(column=0, stick="W")

    # settings are always saved to settings.json so they are the same when the user loads the program again
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