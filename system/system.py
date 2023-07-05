import random
from typing import List
from .role import Role
from .room_handler import *

WAIT_TIME = 3

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

# 状态常量
RET_SUCCESS = 0
RET_ERROR = -1


MAX_LEVEL1 = 5






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
        role = Role(self, uid)
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

    def GameMessangeBuilder(self):
        return choicemsgbuilder(self)

    def GameChoiceHandler(self, choice):
        return choicehandler(self, choice)










# 管理器
class Manager:
    def __init__(self):
        self.playing: List[System] = {}

    def is_playing(self, gid):
        return gid in self.playing

    def start(self, gid, uid):
        return System(uid, self, gid)

    def get_game(self, gid) -> System:
        return self.playing[gid] if gid in self.playing else None