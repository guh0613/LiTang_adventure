from typing import List
from enum import IntEnum

WAIT_TIME = 3

# 游戏状态常量
STATUS_READY = "ready"
STATUS_PREPARE = "prepare"
STATUS_FINISH = "finish"
STATUS_END = 'end'
STATUS_WIN = 'win'

# 游戏选择状态常量
CHOICE_STARTGAME = "c_startgame"
CHOICE_FIRST_TIME = "c_firsttime"
CHOICE_START = "c_start"


class Attr(IntEnum):
    ATTACK = 1  # 攻击力
    DEFENSIVE = 2  # 防御力
    MAX_HEALTH = 3  # 最大生命值
    NOW_HEALTH = 4  # 当前生命值
    NOW_TP = 5  # 当前tp
    MAX_TP = 6  # 最大tp
    CRIT = 7  # 暴击
    CRIT_HURT = 8  # 暴击伤害

    COST_HEALTH = 1000  # 已损失生命值（特殊属性，不能直接变动数值）


class Role:
    def __init__(self, uid):
        self.attr = {}
        self.uid = uid
        self.skills: List[int] = []
        self.blessings = []

    def initdata(self):
        self.attr[Attr.MAX_HEALTH] = 100
        self.attr[Attr.NOW_HEALTH] = self.attr[Attr.MAX_HEALTH]
        self.attr[Attr.MAX_TP] = 100
        self.attr[Attr.NOW_TP] = 0
        self.attr[Attr.ATTACK] = 10
        self.attr[Attr.DEFENSIVE] = 10
        self.attr[Attr.CRIT] = 10
        self.attr[Attr.CRIT_HURT] = 2
        self.skills.append(1001)





class System:
    def __init__(self, user_id, mgr, gid) -> None:
        self.user_id = user_id  # 玩家的qq号
        self.mgr = mgr
        self.gid = gid
        self.choice = None
        self.status = STATUS_PREPARE
        self.role = None

    def __enter__(self):
        self.mgr.playing[self.gid] = self
        return self

    def __exit__(self, type_, value, trace):
        del self.mgr.playing[self.gid]

    def initplayer(self, uid):
        role = Role(uid)
        self.role = role

    def getplayerobj(self) -> Role:
        return self.role


# 管理器
class Manager:
    def __init__(self):
        self.playing: List[System] = {}

    def is_playing(self, gid):
        return gid in self.playing

    def start(self, gid, uid):
        return System(uid, self, gid)

    def get_game(self, gid):
        return self.playing[gid] if gid in self.playing else None
