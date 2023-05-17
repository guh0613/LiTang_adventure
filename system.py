import math
import random
from typing import List
from enum import IntEnum
from .items.rooms import *

WAIT_TIME = 3
MAX_CRIT = 100

BATTLE_ROOM = 'battle_room'
CIRCUM_ROOM = 'circum_room'
BOSS_ROOM = 'boss_room'

# 游戏状态常量
STATUS_READY = "ready"
STATUS_PREPARE = "prepare"
STATUS_START = "start"
STATUS_FINISH = "finish"
STATUS_END = 'end'
STATUS_WIN = 'win'

# 游戏选择状态常量
CHOICE_STARTGAME = "c_startgame"
CHOICE_FIRST_TIME = "c_firsttime"
CHOICE_START = "c_start"
CHOICE_ROOM = "c_room"

MAX_LEVEL1 = 5

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

    def attrChange(self, attr_type, num):

        # 属性数值改变前的处理
        if attr_type == Attr.NOW_HEALTH and num < 0:
            # 如果生命值减少，则按百分比回复tp
            hurt_tp = math.floor(abs(num) / self.attr[Attr.MAX_HEALTH] * 100 / 2)
            self.attrChange(Attr.NOW_TP, hurt_tp)

        self.attr[attr_type] += num

        # 属性数值改变后的处理
        if attr_type == Attr.MAX_HEALTH and num > 0:
            # 如果增加的是生命最大值，则当前生命也增加同等数值
            self.attr[Attr.NOW_HEALTH] += num
        if attr_type == Attr.MAX_TP and num > 0:
            # 如果增加的是tp最大值，则当前tp也增加同等数值
            self.attr[Attr.NOW_TP] += num
        if ((attr_type == Attr.NOW_HEALTH or attr_type == Attr.MAX_HEALTH) and
                self.attr[Attr.NOW_HEALTH] > self.attr[Attr.MAX_HEALTH]):
            # 当前生命值不能超过最大生命值
            self.attr[Attr.NOW_HEALTH] = self.attr[Attr.MAX_HEALTH]
        if ((attr_type == Attr.NOW_TP or attr_type == Attr.MAX_TP) and
                self.attr[Attr.NOW_TP] > self.attr[Attr.MAX_TP]):
            # 不能超过最大tp
            self.attr[Attr.NOW_TP] = self.attr[Attr.MAX_TP]
        if attr_type == Attr.CRIT and self.attr[Attr.CRIT] > MAX_CRIT:
            # 不能超过最大暴击
            self.attr[Attr.CRIT] = MAX_CRIT

        # 已消耗生命值特殊处理
        if attr_type == Attr.NOW_HEALTH:
            self.attr[Attr.COST_HEALTH] = self.attr[Attr.MAX_HEALTH] - self.attr[Attr.NOW_HEALTH]

        if self.attr[attr_type] <= 0:
            self.attr[attr_type] = 0
        return self.attr[attr_type]

    def playerpropcalculate(self):
        if 5001 in self.blessings:
            num5001 = math.floor(0.3 * self.attr[Attr.ATTACK])
            self.attrChange(Attr.ATTACK,num5001)
        if 5002 in self.blessings:
            num5002 = math.floor(0.3 * self.attr[Attr.MAX_HEALTH])
            self.attrChange(Attr.MAX_HEALTH, num5002)




class System:
    def __init__(self, user_id, mgr, gid) -> None:
        self.user_id = user_id  # 玩家的qq号
        self.level = 0
        self.room = 0
        self.pos = ''
        self.roomid = 0
        self.mgr = mgr
        self.gid = gid
        self.choice = None
        self.status = STATUS_PREPARE
        self.role: Role = None

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


    def gamestart(self):
        self.status = STATUS_START
        player = self.role
        player.playerpropcalculate()
        self.level = 1
        self.go_on()

    def go_on(self):
        self.choice = CHOICE_ROOM
        match self.level:
            case 1:
                if self.room < MAX_LEVEL1:
                    self.room += 1
                    result = random.choice(range(1, 11))
                    if result <= 4:
                        self.pos = BATTLE_ROOM
                        self.roomid = random.choice(range(9101, 9101+len(LEVELONE_CIRCUM_ROOMS)))

                    else:
                        self.pos = CIRCUM_ROOM
                        self.roomid = random.choice(range(9001, 9001+len(LEVELONE_BATTLE_ROOMS)))
                else:
                    self.room += 1
                    self.pos = BOSS_ROOM
                    self.roomid = 10001

    def choicemsgbuilder(self):
        msg = f"第{self.level}层\t{LEVEL[self.level]}\n事件{self.room}\n"
        if self.pos == CIRCUM_ROOM:
            circum_dict = LEVELONE_CIRCUM_ROOMS.copy()
            circum_dict = circum_dict[self.roomid]
            msg += f"{circum_dict['name']}\n\n"
            msg += f"{circum_dict['des']}\n\n"
            msg += f"(a) {circum_dict['choice_a']}"
            if 'choice_b' in circum_dict:
                msg += f"\n(b) {circum_dict['choice_b']}"
            if 'choice_c' in circum_dict:
                msg += f"\n(c) {circum_dict['choice_c']}"
            return msg

        if self.pos == BATTLE_ROOM:
            battle_dict = LEVELONE_BATTLE_ROOMS.copy()
            battle_dict = battle_dict[self.roomid]
            msg += f"{battle_dict['name']}\n\n"
            msg += f"{battle_dict['des']}\n\n"
            msg += f"(a) 开始战斗！"
            msg += f"\n(b) 放弃"
            return msg














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
