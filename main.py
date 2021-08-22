import PyQt5
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QTextBrowser,
                            QCheckBox, QMainWindow, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect
from functions import DbdFuncs
from threading import Thread
from multiprocessing import Process, Value, Array
from ctypes import c_bool, c_int
from pynput.keyboard import Key, KeyCode, Listener
from time import sleep
import configparser
import sys
import os


class DeadByDaylightScript(QMainWindow):
    def __init__(self):
        super().__init__()

        # Init script functions
        self.dbd_funcs = DbdFuncs()

        # Init gui
        self.init_gui()

        # Script functions toggle
        self.gti_toogle = Value(c_bool, 1) # get target info
        self.asc_toggle = Value(c_bool, 0) # auto skillcheck
        self.am1_toggle = Value(c_bool, 0) # auto m1
        self.aw_toggle = Value(c_bool, 0) # auto wigle

        # Load keycodes (params for script's functions)
        self.asc_keycode = None
        self.am1_keycode = None

        # Init configparser
        self.config = configparser.ConfigParser()

        # Load config
        self.__load_config()

        # Sync variables, information about target window
        self.is_target_active = Value(c_bool, False) # true if target window foregrounded
        self.window_rect = Array(c_int, range(4)) # target window rect (from win32gui)

        # Starting necessary thread to get information about target window
        self.get_target_info_thread = Thread(target=self.dbd_funcs.get_target_window_info,
                                            args=(self.gti_toogle, self.is_target_active, 
                                            self.window_rect))
        self.get_target_info_thread.start()

    def init_gui(self):
        """Initing gui
        """
        self.setFixedSize(500, 118)
        self.setWindowTitle("DeadByDaylight Script [by FlensT]")

        # Auto SkillCheck
        self.asc_checkbox = QCheckBox(self)
        self.asc_checkbox.setGeometry(QRect(10, 10, 111, 17))
        self.__set_pointer_size(self.asc_checkbox, 10)
        self.asc_checkbox.setText("Auto SkillCheck")

        self.asc_btn = QPushButton(self)
        self.asc_btn.setGeometry(QRect(130, 10, 51, 23))

        self.asc_btn.clicked.connect(lambda x: self.__changekey_btn_handle("AutoSkillCheck", "keycode"))

        self.asc_checkbox.stateChanged.connect(self.__asc_checkbox_handle)

        # Auto M1
        self.am1_checkbox = QCheckBox(self)
        self.am1_checkbox.setGeometry(QRect(10, 40, 70, 17))
        self.__set_pointer_size(self.am1_checkbox, 10)
        self.am1_checkbox.setText("Auto M1")

        self.am1_btn = QPushButton(self)
        self.am1_btn.setGeometry(QRect(130, 40, 51, 23))

        self.am1_btn.clicked.connect(lambda x: self.__changekey_btn_handle("AutoM1", "keycode"))

        self.am1_checkbox.stateChanged.connect(self.__am1_checkbox_handle)

        # Auto Wigle
        self.aw_checkbox = QCheckBox(self)
        self.aw_checkbox.setGeometry(QRect(10, 70, 131, 17))
        self.__set_pointer_size(self.aw_checkbox, 10)
        self.aw_checkbox.setText("[BETA] Auto Wigle")

        self.aw_label = QLabel(self)
        self.aw_label.setGeometry(QRect(10, 90, 141, 16))
        self.aw_label.setStyleSheet("color: red;")
        self.aw_label.setText("WORKS ONLY AT 1920x1080")

        self.aw_checkbox.stateChanged.connect(self.__aw_checkbox_handle)

        # Logging
        self.log_label = QLabel(self)
        self.log_label.setGeometry(QRect(260, 10, 51, 16))
        self.__set_pointer_size(self.log_label, 10)
        self.log_label.setText("Logging")

        self.log_browser = QTextBrowser(self)
        self.log_browser.setGeometry(QRect(260, 30, 221, 81))

        self.show()

    def __set_pointer_size(self, widget: PyQt5.QtWidgets, size: int) -> None:
        """Sets pointer size of text

        Args:
            widget (PyQt5.QtWidgets): like QCheckBox
            size (int): size of pointer (px)
        """
        font = QFont()
        font.setPointSize(size)
        widget.setFont(font)

    def __asc_checkbox_handle(self):
        # Auto SkillCheck
        if self.asc_checkbox.isChecked():
            self.asc_toggle.value = 1
            self.asc_process = Process(target=self.dbd_funcs.auto_skillcheck, 
                                        args=(self.asc_toggle, self.is_target_active,
                                             self.window_rect, self.asc_keycode))
            self.asc_process.start()
            self.log_browser.append("[+] Auto SkillCheck -> ON")
        else:
            self.asc_toggle.value = 0
            self.log_browser.append("[-] Auto SkillCheck -> OFF")

    def __am1_checkbox_handle(self):
        # Auto M1
        if self.am1_checkbox.isChecked():
            self.am1_toggle.value = 1
            self.am1_thread = Thread(target=self.dbd_funcs.auto_m1, 
                                    args=(self.am1_toggle, self.is_target_active,
                                        self.am1_keycode))
            self.am1_thread.start()
            self.log_browser.append("[+] Auto M1 -> ON")
        else:
            self.am1_toggle.value = 0
            self.log_browser.append("[-] Auto M1 -> OFF")

    def __aw_checkbox_handle(self):
        # Auto Wigle
        if self.aw_checkbox.isChecked():
            self.aw_toggle.value = 1
            self.aw_thread = Thread(target=self.dbd_funcs.auto_wigle, 
                                    args=(self.aw_toggle, self.is_target_active))
            self.aw_thread.start()
            self.log_browser.append("[+] [BETA] Auto Wigle -> ON")
        else:
            self.aw_toggle.value = 0
            self.log_browser.append("[-] [BETA] Auto Wigle -> OFF")

    def __changekey_btn_handle(self, partition, param):
        self.log_browser.append("[=] Waiting for a button...")

        def on_press(key):
            try:
                self.log_browser.append(f"[+] Button {key} has been selected")
                self.__update_config(partition, param, str(key).replace("'", ""))
                self.sender().setStyleSheet("")
                return False
            except:
                self.log_browser.append("[ERROR] An error occured while changing the button")
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

        
    def __create_config(self):
        """Create config file
        """
        self.config.add_section("AutoSkillCheck")
        self.config.set("AutoSkillCheck", "keycode", "c")

        self.config.add_section("AutoM1")
        self.config.set("AutoM1", "keycode", "Key.alt_l")

        with open(f"{os.getcwd()}\\config.ini", "w") as config_file:
            self.config.write(config_file)

    def __load_config(self):
        self.log_browser.append("[+] Loading config...")

        if not os.path.exists(os.getcwd() + "\\config.ini"):
            self.log_browser.append("[=] Config not exists, creating new one")
            self.__create_config()
        
        self.config.read(f"{os.getcwd()}\\config.ini")

        # Here loading keycodes from config file (бля я уже устал, даже не буду проверять правильно ли я написал комент на англ)
        # Я в этой всей хуйне завтра даже сам не разберусь
        self.asc_keycode = self.__read_keycode(self.config.get("AutoSkillCheck", "keycode"))
        self.__change_btn_name(self.asc_btn, self.asc_keycode)

        self.am1_keycode = self.__read_keycode(self.config.get("AutoM1", "keycode"))
        self.__change_btn_name(self.am1_btn, self.am1_keycode)

        self.log_browser.append("[+] Config loaded!")
    
    def __read_keycode(self, keycode_str:str):
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
                    # self.log_browser.append("[DEBUG] Config (keycode) multiple characters found, delete config file and restart the program")
                    pass
            except:
                self.log_browser.append("[ошибочка] не пиши гавно в конфиге")
        except:
            self.log_browser.append("[DEBUG] Can't load config (keycode) - unknown type of keycode")

    def __change_btn_name(self, btn_object: object, name: str):
        """Need to finish

        Args:
            btn_object (object): [description]
            name (str): [description]
        """
        try:
            btn_object.setText(str(name))
        except:
            self.log_browser.append(f"[ERROR] Can't change name of btn ({btn_object})")
            btn_object.setText(":(")

    def __update_config(self, partition: str, param: str, value: str):
            self.config.set(partition, param, value)
            with open(f"{os.getcwd()}\\config.ini", "w") as config_file:
                self.config.read(f"{os.getcwd()}\\config.ini")
                self.config.write(config_file)
                self.__load_config()

    def closeEvent(self, event):
        self.gti_toogle.value = 0
        self.asc_toggle.value = 0
        self.am1_toggle.value = 0
        self.aw_toggle.value = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = DeadByDaylightScript()
    sys.exit(app.exec_())