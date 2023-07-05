from enum import IntEnum

MAX_CRIT = 100

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

