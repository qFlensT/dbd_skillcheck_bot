# Default imports
import PyQt5
from PyQt5.QtWidgets import (QTabWidget,QWidget, QLabel, QPushButton, QTextBrowser,
                            QCheckBox, QMainWindow, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, Qt
from threading import Thread
from multiprocessing import Process, Value, Array, freeze_support
from ctypes import c_bool, c_int
from pynput.keyboard import Key, KeyCode, Listener
import configparser
import sys
import os

# Importing script functions
from utility import Utility
from auto_m1 import auto_m1
from auto_m2 import auto_m2
from auto_wigle import auto_wigle
from auto_skillcheck import auto_skillcheck
from get_target_info import get_target_window_info
from configurate_monitor import ConfigureMonitor


class DeadByDaylightScript(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Needed for windows (multiprocessing cause to spawn new window)
        freeze_support()
        
        # Init configparser
        self.config = configparser.ConfigParser()

        # Init Utility
        self.utility = Utility()
        
        # Init parent gui
        self.init_gui()

        # Script functions toggle
        self.gti_toogle = Value(c_bool, 1) # get target info
        self.asc_toggle = Value(c_bool, 0) # auto skillcheck
        self.am1_toggle = Value(c_bool, 0) # auto m1
        self.am2_toggle = Value(c_bool, 0) # auto m1
        self.aw_toggle = Value(c_bool, 0) # auto wigle
        
        """ПОТОМ УБРАТЬ"""
        self.asc_ai_toggle = Value(c_bool, 1)
        
        # Load keycodes (params for script's functions)
        self.asc_keycode = None
        self.am1_keycode = None
        self.am2_keycode = None
        
        # Screen capture zones
        self.asc_monitor = None
        self.aw_monitor_hand = None
        self.aw_monitor_arrow = None
        
        # Load config
        self.__load_config()

        # Sync variables, information about target window
        self.is_target_active = Value(c_bool, False) # true if target window foregrounded
        self.window_rect = Array(c_int, range(4)) # target window rect (from win32gui)

        # Starting necessary thread to get information about target window
        self.get_target_info_thread = Thread(target=get_target_window_info,
                                            args=(self.gti_toogle, self.is_target_active, 
                                            self.window_rect))
        
        self.get_target_info_thread.start()

    def init_gui(self) -> None:
        def __set_pointer_size(widget: PyQt5.QtWidgets, size: int) -> None:
            """Sets pointer size of text

            Args:
                widget (PyQt5.QtWidgets): like QCheckBox
                size (int): size of pointer (px)
            """
            font = QFont()
            font.setPointSize(size)
            widget.setFont(font)
        
        self.setFixedSize(520, 155)
        self.setWindowTitle("DeadByDaylight Script [by FlensT]")
        
        self.tabs = QTabWidget(self)
        self.tabs.resize(302, 155)
        self.asc_tab = QWidget()
        self.am1_tab = QWidget()
        self.am2_tab = QWidget()
        self.aw_tab = QWidget()
        
        self.tabs.addTab(self.asc_tab, "Auto SkillCheck")
        self.tabs.addTab(self.am1_tab, "Auto M1")
        self.tabs.addTab(self.am2_tab, "Auto M2")
        self.tabs.addTab(self.aw_tab, "Auto Wigle")
        
        # Auto SkillCheck
        # Checkbox
        self.asc_checkbox = QCheckBox(self.asc_tab)
        __set_pointer_size(self.asc_checkbox, 10)
        self.asc_checkbox.setText("Auto SkillCheck")
        self.asc_checkbox.adjustSize()
        self.asc_checkbox.move(10, 10)
        
        # AI Checkbox
        self.asc_ai_checkbox = QCheckBox(self.asc_tab)
        self.asc_ai_checkbox.setChecked(True)
        __set_pointer_size(self.asc_ai_checkbox, 10)
        self.asc_ai_checkbox.setText("AI Improve")
        self.asc_ai_checkbox.adjustSize()
        self.asc_ai_checkbox.move(130, 10)
        
        # Change Keybind
        self.asc_keybind_lbl = QLabel(self.asc_tab)
        __set_pointer_size(self.asc_keybind_lbl, 10)
        self.asc_keybind_lbl.setText("Change Keybind:")
        self.asc_keybind_lbl.adjustSize()
        self.asc_keybind_lbl.move(10, 40)
        
        self.asc_keybind_btn = QPushButton(self.asc_tab)
        self.asc_keybind_btn.resize(60, 25)
        self.asc_keybind_btn.move(115, 35)
        
        # Configurate monitor
        self.asc_monitor_lbl = QLabel(self.asc_tab)
        __set_pointer_size(self.asc_monitor_lbl, 10)
        self.asc_monitor_lbl.setText("Configure screen capture zone: ")
        self.asc_monitor_lbl.adjustSize()
        self.asc_monitor_lbl.move(10, 70)
        
        self.asc_monitor_btn = QPushButton(self.asc_tab)
        self.asc_monitor_btn.resize(60, 25)
        self.asc_monitor_btn.move(10, 90)
        self.asc_monitor_btn.setText("Configure")
        
        self.asc_std_monitor_btn = QPushButton(self.asc_tab)
        self.asc_std_monitor_btn.resize(60, 25)
        self.asc_std_monitor_btn.move(75, 90)
        self.asc_std_monitor_btn.setText("Default")
        
        # Connecting
        self.asc_keybind_btn.clicked.connect(lambda x: self.__change_keybind_btn_handle("AutoSkillCheck", "keycode"))

        self.asc_checkbox.stateChanged.connect(lambda x: self.__checkbox_handle(self.asc_toggle, 
                                                                                Process,
                                                                                auto_skillcheck,
                                                                                self.asc_toggle, # args
                                                                                True,
                                                                                self.window_rect,
                                                                                self.asc_monitor,
                                                                                self.asc_ai_toggle, 
                                                                                self.asc_keycode))
        self.asc_ai_checkbox.stateChanged.connect(self.__ai_checkbox_handle)
        
        self.asc_monitor_btn.clicked.connect(lambda x: self.__change_monitor_btn_handle("AutoSkillCheck", "monitor"))
        
        self.asc_std_monitor_btn.clicked.connect(lambda x: self.update_config("AutoSkillCheck", "monitor", "default"))
        
        # Auto M1
        # Checkbox
        self.am1_checkbox = QCheckBox(self.am1_tab)
        __set_pointer_size(self.am1_checkbox, 10)
        self.am1_checkbox.setText("Auto M1")
        self.am1_checkbox.adjustSize()
        self.am1_checkbox.move(10, 10)
        
        # Change Keybind
        self.am1_keybind_lbl = QLabel(self.am1_tab)
        __set_pointer_size(self.am1_keybind_lbl, 10)
        self.am1_keybind_lbl.setText("Change Keybind:")
        self.am1_keybind_lbl.adjustSize()
        self.am1_keybind_lbl.move(10, 40)
        
        self.am1_keybind_btn = QPushButton(self.am1_tab)
        self.am1_keybind_btn.resize(60, 25)
        self.am1_keybind_btn.move(115, 35)
        
        # Connecting
        self.am1_keybind_btn.clicked.connect(lambda x: self.__change_keybind_btn_handle("AutoM1", "keycode"))

        self.am1_checkbox.stateChanged.connect(lambda x: self.__checkbox_handle(self.am1_toggle, 
                                                                                Thread,
                                                                                auto_m1,
                                                                                self.am1_toggle, # args
                                                                                True, 
                                                                                self.am1_keycode))
        
        # Auto M2
        # Checkbox
        self.am2_checkbox = QCheckBox(self.am2_tab)
        __set_pointer_size(self.am2_checkbox, 10)
        self.am2_checkbox.setText("Auto M2")
        self.am2_checkbox.adjustSize()
        self.am2_checkbox.move(10, 10)
        
        # Change Keybind
        self.am2_keybind_lbl = QLabel(self.am2_tab)
        __set_pointer_size(self.am2_keybind_lbl, 10)
        self.am2_keybind_lbl.setText("Change Keybind:")
        self.am2_keybind_lbl.adjustSize()
        self.am2_keybind_lbl.move(10, 40)
        
        self.am2_keybind_btn = QPushButton(self.am2_tab)
        self.am2_keybind_btn.resize(60, 25)
        self.am2_keybind_btn.move(115, 35)
        
        # Connecting
        self.am2_keybind_btn.clicked.connect(lambda x: self.__change_keybind_btn_handle("AutoM2", "keycode"))

        self.am2_checkbox.stateChanged.connect(lambda x: self.__checkbox_handle(self.am2_toggle, 
                                                                                Thread,
                                                                                auto_m2,
                                                                                self.am2_toggle, # args
                                                                                True, 
                                                                                self.am2_keycode))
                
        # Auto Wigle
        # Checkbox
        self.aw_checkbox = QCheckBox(self.aw_tab)
        __set_pointer_size(self.aw_checkbox, 10)
        self.aw_checkbox.setText("Auto Wigle")
        self.aw_checkbox.adjustSize()
        self.aw_checkbox.move(10, 10)
                
        # Configurate monitor
        self.aw_monitor_lbl = QLabel(self.aw_tab)
        __set_pointer_size(self.aw_monitor_lbl, 10)
        self.aw_monitor_lbl.setText("Configure screen capture zone: ")
        self.aw_monitor_lbl.adjustSize()
        self.aw_monitor_lbl.move(10, 70)
        
        self.aw_monitor_hand_btn = QPushButton(self.aw_tab)
        self.aw_monitor_hand_btn.resize(60, 25)
        self.aw_monitor_hand_btn.move(10, 90)
        self.aw_monitor_hand_btn.setText("Hand")
        
        self.aw_monitor_arrow_btn = QPushButton(self.aw_tab)
        self.aw_monitor_arrow_btn.resize(60, 25)
        self.aw_monitor_arrow_btn.move(75, 90)
        self.aw_monitor_arrow_btn.setText("Arrow")
        
        self.aw_std_monitor_btn = QPushButton(self.aw_tab)
        self.aw_std_monitor_btn.resize(60, 25)
        self.aw_std_monitor_btn.move(140, 90)
        self.aw_std_monitor_btn.setText("Default")
        
        # Connecting
        self.aw_checkbox.stateChanged.connect(lambda x: self.__checkbox_handle(self.aw_toggle, 
                                                                            Thread,
                                                                            auto_wigle,
                                                                            self.aw_toggle, # args
                                                                            True,
                                                                            self.aw_monitor_hand,
                                                                            self.aw_monitor_arrow))
        
        self.aw_monitor_hand_btn.clicked.connect(lambda x: self.__change_monitor_btn_handle("AutoWigle", "monitor_hand"))
        self.aw_monitor_arrow_btn.clicked.connect(lambda x: self.__change_monitor_btn_handle("AutoWigle", "monitor_arrow"))
        
        self.aw_std_monitor_btn.clicked.connect(lambda x: self.update_config("AutoWigle", "monitor_hand", "default"))
        self.aw_std_monitor_btn.clicked.connect(lambda x: self.update_config("AutoWigle", "monitor_arrow", "default"))
        
        # Logging
        self.log_lbl = QLabel(self)
        self.log_lbl.setText("Logging")
        self.log_lbl.adjustSize()
        self.log_lbl.move(390, 5)

        self.log_browser = QTextBrowser(self)
        self.log_browser.resize(208, 132)
        self.log_browser.move(305, 20)
        
        self.show()

    def __ai_checkbox_handle(self):
        sender = self.sender()
        if sender.isChecked():
            self.asc_ai_toggle.value = True
        else:
            self.asc_ai_toggle.value = False

    def __checkbox_handle(self, toggle: bool, launch_method: object, function: object, *args, **kwargs) -> None:
        """Accepts a function enable signal from checkboxes and (starts / disables) (processes / threads)

        Args:
            toggle (bool): On / Off toggle
            launch_method (object): Process or Thread object like `multiprocessing.Process`
            function (object): function that's need to be started / stopped
        """
        sender = self.sender()
        if sender.isChecked():
            toggle.value = 1
            launch_method(target=function, args=args, kwargs=kwargs).start()
            self.log_browser.append(f"[+] {sender.text()} -> ON")
        else:
            toggle.value = 0
            self.log_browser.append(f"[+] {sender.text()} -> OFF")

    def __change_keybind_btn_handle(self, partition:str, param:str) -> None:
        
        """Changes keybind (via updating config.ini file) when the keybind button is clicked
        NEED TO COMPLETE
        WHAT NEEDED:
        1. Add processing  - if several buttons are pressed at the same time

        Args:
            partition (str): partition of cfg
            param (str): param of selected partition
        """
        self.log_browser.append("[=] Waiting for a button...")

        sender = self.sender()
        sender.setStyleSheet("background-color: #8A2BE2; color: #FFF;")
        self.__change_btn_name(sender, "Waiting...", False)

        def on_press(key):
            try:
                self.update_config(partition, param, key)
                return False
            except:
                self.log_browser.append("[ERROR] An error occured while changing the button")
                self.update_config(partition, param, "None")
                return False

        listener = Listener(on_press=on_press)
        listener.start()

    def __change_monitor_btn_handle(self, partition: str, param: str) -> None:
        file_path = self.utility.get_file_path(self)
        
        # Init child configure window
        if file_path:
            self.configure_window = ConfigureMonitor(file_path, partition, param, self)
            self.configure_window.show()
        
    def __create_config(self) -> None:
        """Creates a config file
        Runs if no config.ini file was found or need to be replaced
        """
         
        self.config.add_section("AutoSkillCheck")
        self.config.set("AutoSkillCheck", "keycode", "c") # c is default keybind
        self.config.set("AutoSkillCheck", "monitor", "default")

        self.config.add_section("AutoM1")
        self.config.set("AutoM1", "keycode", "Key.alt_l") # alt_l is default keybind
        
        self.config.add_section("AutoM2")
        self.config.set("AutoM2", "keycode", "Key.alt_gr") # alt_r is default keybind
        
        self.config.add_section("AutoWigle")
        self.config.set("AutoWigle", "monitor_hand", "default")
        self.config.set("AutoWigle", "monitor_arrow", "default")

        with open(f"{os.getcwd()}\\config.ini", "w") as config_file:
            self.config.write(config_file)

    def __load_config(self) -> None:
        """Loads settings from a configuration file
        """
        self.log_browser.append("[+] Loading config...")
        
        config_file_path = os.getcwd() + "\\config.ini"

        if not os.path.exists(config_file_path):
            self.log_browser.append("[=] Config not exists, creating new one")
            self.__create_config()
        
        self.config.read(f"{os.getcwd()}\\config.ini")

        # Here loading settings from config file 
        try:
            #Auto SkillCheck
            self.asc_keycode = self.__read_keycode(self.config.get("AutoSkillCheck", "keycode"))
            self.__change_btn_name(self.asc_keybind_btn, self.asc_keycode)
            self.asc_monitor = self.__read_monitor(self.config.get("AutoSkillCheck", "monitor")) # Make a dict() from str object

            # Auto M1
            self.am1_keycode = self.__read_keycode(self.config.get("AutoM1", "keycode"))
            self.__change_btn_name(self.am1_keybind_btn, self.am1_keycode)
            
            # Auto M2
            self.am2_keycode = self.__read_keycode(self.config.get("AutoM2", "keycode"))
            self.__change_btn_name(self.am2_keybind_btn, self.am2_keycode)

            # Auto Wigle
            self.aw_monitor_hand = self.__read_monitor(self.config.get("AutoWigle", "monitor_hand"))
            self.aw_monitor_arrow = self.__read_monitor(self.config.get("AutoWigle", "monitor_arrow"))

            self.log_browser.append("[+] Config loaded!")
        except:
            self.log_browser.append("[WARN] Config is uncorrect! Loading the standard settings file...")
            self.config = configparser.ConfigParser()
            self.__create_config()
            self.__load_config()

    def update_config(self, partition: str, param: str, value: str) -> None:
        """Updates the config file and calls the `self.__load_config()` function

        Args:
            partition (str): Partition of cfg file
            param (str): Parameter of cfg file
            value (str): The value to be written
        """
        self.config.set(partition, param, str(value).replace("'", ""))
        with open(f"{os.getcwd()}\\config.ini", "w") as config_file:
            self.config.read(f"{os.getcwd()}\\config.ini")
            self.config.write(config_file)
            self.log_browser.append(f"[+] [{param}] of [{partition}] has been set to [{value}]")
            self.__load_config()
    
    def __read_keycode(self, keycode_str: str) -> object:
        """Takes a string keycode object and returns it as an object of pynput.keyboard

        Args:
            keycode_str (str): keycode thats need to be converted in pynput.keyboard object

        Returns:
            object: pynput.keyboard object
        """
        keycode = None
        try:
            keycode = eval(keycode_str)
            # self.log_browser.append("[DEBUG] Config (keycode) has <Key> like keycode")
            return keycode
        except NameError:
            try:
                if len(keycode_str) == 1:
                    keycode = KeyCode.from_char(keycode_str)
                    # self.log_browser.append("[DEBUG] Config (keycode) has <KeyCode> like keycode")
                    return keycode
                else:
                    self.log_browser.append("[ERROR] Config (keycode) multiple characters found, delete config file and restart the program")
            except:
                self.log_browser.append("[ошибочка] не пиши гавно в конфиге")
        except:
            self.log_browser.append("[ERROR] Can't load config (keycode) - unknown type of keycode")

    def __read_monitor(self, monitor_str: str) -> dict:
        try:
            try:
                monitor = eval(monitor_str)
                return monitor
            except NameError:
                return monitor_str
        except:
            self.log_browser.append("[ERROR] Incorrect type of monitor (config.ini). Monitor has been set to default")
            return "default"

    def __change_btn_name(self, btn_object: object, name: str, use_keynames: bool=True) -> None:
        """Changes the name of the button

        Args:
            btn_object (object): The button whose name you want to change
            name (str): New name of button
            use_keynames (bool, optional): If necessary to use keynames dict(). Defaults to True.
        """
        keynames = {
            "Key.alt":"Alt",
            "Key.alt_gr":"AltGr",
            "Key.alt_l":"Left Alt",
            "Key.alt_r":"Right Alt",
            "Key.backspace":"BSPACE",
            "Key.caps_lock":"CapsLock",
            "Key.cmd":"Win",
            "Key.cmd_l":"Left Win",
            "Key.cmd_r":"Right Win",
            "Key.ctrl":"Ctrl",
            "Key.ctrl_l":"Left Ctrl",
            "Key.ctrl_r":"Right Ctrl",
            "Key.delete":"Delete",
            "Key.down":"Down",
            "Key.end":"End",
            "Key.enter":"Enter",
            "Key.esc":"Esc",
            "Key.f1":"F1",
            "Key.f2":"F2",
            "Key.f3":"F3",
            "Key.f4":"F4",
            "Key.f5":"F5",
            "Key.f6":"F6",
            "Key.f7":"F7",
            "Key.f8":"F8",
            "Key.f9":"F9",
            "Key.f10":"F10",
            "Key.f11":"F11",
            "Key.f12":"F12",
            "Key.f13":"F13",
            "Key.f14":"F14",
            "Key.f15":"F15",
            "Key.f16":"F16",
            "Key.f17":"F17",
            "Key.f18":"F18",
            "Key.f19":"F19",
            "Key.f20":"F20",
            "Key.home":"Home",
            "Key.insert":"INS",
            "Key.left":"Left",
            "Key.media_next":"Media NXT",
            "Key.media_play_pause":"Media Play",
            "Key.media_previous":"Media Prev",
            "Key.media_volume_down":"Vol Down",
            "Key.media_volume_mute":"Vol Mute",
            "Key.media_volume_up":"Vol Up",
            "Key.menu":"Menu",
            "Key.num_lock":"NumLock",
            "Key.page_down":"PD",
            "Key.page_up":"PU",
            "Key.pause":"Pause",
            "Key.print_screen":"PS",
            "Key.right":"Right",
            "Key.scroll_lock":"SL",
            "Key.shift":"Shift",
            "Key.shift_l":"Left Shift",
            "Key.shift_r":"Right Shift",
            "Key.space":"Space",
            "Key.tab":"Tab",
            "Key.up":"Up"
        }
        try:
            name = str(name).replace("'", "")
            if use_keynames:
                
                btn_object.setStyleSheet("") # Set default style of btn_object
                keyname = keynames.get(name)
                
                if keyname == None:
                    keyname = name.upper()
            
                btn_object.setText(keyname)
            else:
                btn_object.setText(name)
        except:
            self.log_browser.append(f"[ERROR] Can't change name of btn ({btn_object})")
            btn_object.setText(":(")

    def __turn_off_tasks(self) -> None:
        """Turn off all tasks
        """
        self.gti_toogle.value = 0
        self.asc_toggle.value = 0
        self.am1_toggle.value = 0
        self.am2_toggle.value = 0
        self.aw_toggle.value = 0
        # Потом убрать 49 279 158

    def closeEvent(self, event) -> None:
        """Looking for a close event of PyQt
        """
        self.__turn_off_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = DeadByDaylightScript()
    sys.exit(app.exec_())