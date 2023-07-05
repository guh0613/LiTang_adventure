from items.rooms import *
from system.system import CIRCUM_ROOM, RET_ERROR, BATTLE_ROOM, BOSS_ROOM
from .system import System
from items.boss_rooms import *


# 选择分支文本生成
def choicemsgbuilder(self: System):
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

    if self.pos == BOSS_ROOM:
        boss_dict = LEVELONE_BOSS_ROOMS.copy()
        boss_dict = boss_dict[self.roomid]
        msg += f"{boss_dict['name']}\n\n"
        msg += f"{boss_dict['des']}\n\n"
        msg += f"(a) 开始战斗！"
        msg += f"\n(b) 放弃"
        return msg

# 选择分支处理
def choicehandler(self, choice):
    if self.pos == CIRCUM_ROOM:
        circum_dict = LEVELONE_CIRCUM_ROOMS.copy()
        circum_dict = circum_dict[self.roomid]
        match self.roomid:
            case 9001:
                if choice == 'a':
                    return "choose_a"
                if 'choice_b' in circum_dict and choice == 'b':
                    return "choose_b"
                if 'choice_c' in circum_dict and choice == 'c':
                    return "choose_c"
                return RET_ERROR


    if self.pos == BATTLE_ROOM:
        battle_dict = LEVELONE_BATTLE_ROOMS.copy()
        battle_dict = battle_dict[self.roomid]
        if choice == 'a':
            self.choice = CHOICE_BATTLE
            self.status = STATUS_BATTLE
            return self.battlemsgbuilder()
        if choice == 'b':
            self.go_on()
            return self.choicemsgbuilder()