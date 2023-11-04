from ..items.rooms import *
from .status import *
from ..items.boss_rooms import *


# 选择分支文本生成
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
    result_msg = ""
    if self.pos == CIRCUM_ROOM:
        match self.roomid:
            case 9001:
                if choice == 'a':
                    result_msg += "你的话激怒了眼前的这个人，‘原神怎么你了？’他的语气中透出一丝愤怒，看来只能用武力说服他了。"
                    result_msg += "\n\n(a) 开始战斗！"
                    result_msg += "\n(b) 放弃"
                    self.roomid = 90011
                if choice == 'b':
                    result_msg = "choose_b"
            case 90011:
                if choice == 'a':
                    result_msg = "choose_a"
                if choice == 'b':
                    result_msg = "你逃出了理塘......"
                    self.status = STATUS_END


        return result_msg if result_msg != "" else RET_ERROR

    if self.pos == BATTLE_ROOM:
        pass
        # battle_dict = LEVELONE_BATTLE_ROOMS.copy()
        # battle_dict = battle_dict[self.roomid]
        # if choice == 'a':
        #     self.choice = CHOICE_BATTLE
        #     self.status = STATUS_BATTLE
        #     return self.battlemsgbuilder()
        # if choice == 'b':
        #     self.go_on()
        #     return self.choicemsgbuilder()
