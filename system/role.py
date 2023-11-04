import math
from typing import List, Dict
from .attrs import Attr, MAX_CRIT
from .status import STATUS_END


class Role:
    def __init__(self, s, uid):
        self.game = s
        self.attr = {}
        self.uid = uid
        self.skills: Dict = {}
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
        self.skills[1001] = 1

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
            if attr_type == Attr.NOW_HEALTH:
                self.attr[Attr.NOW_HEALTH] = 0
                self.outDispose()
            else:
                self.attr[attr_type] = 0
        return self.attr[attr_type]

    def playerpropcalculate(self):
        if 5001 in self.blessings:
            num5001 = math.floor(0.3 * self.attr[Attr.ATTACK])
            self.attrChange(Attr.ATTACK, num5001)
        if 5002 in self.blessings:
            num5002 = math.floor(0.3 * self.attr[Attr.MAX_HEALTH])
            self.attrChange(Attr.MAX_HEALTH, num5002)

    def outDispose(self):
        game = self.game
        game.status = STATUS_END

