from auto_skillcheck import AutoSkillCheck
from auto_m1 import AutoM1
from auto_wigle import AutoWigle
from utility import Utility


class DbdFuncs(AutoSkillCheck, AutoM1, AutoWigle):
    def __init__(self):
        AutoSkillCheck().__init__()
        AutoM1().__init__()
        AutoWigle().__init__()
        Utility().__init__()