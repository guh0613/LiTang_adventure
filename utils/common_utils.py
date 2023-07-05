from nonebot.adapters.onebot.v11 import GroupMessageEvent
from system.attrs import Attr
from ..items.skills import SKILLS
from ..items.blessings import BLESSINGS


def sender2name(ev: GroupMessageEvent):
    return ev.sender.card or ev.sender.nickname


def AttrTextChange(attr_type):
    if attr_type == Attr.ATTACK:
        return "攻击力"
    elif attr_type == Attr.DEFENSIVE:
        return "防御力"
    elif attr_type == Attr.MAX_HEALTH:
        return "最大生命值"
    elif attr_type == Attr.NOW_HEALTH:
        return "生命值"
    elif attr_type == Attr.NOW_TP:
        return "TP"
    elif attr_type == Attr.MAX_TP:
        return "最大TP"
    elif attr_type == Attr.CRIT:
        return "暴击"
    elif attr_type == Attr.CRIT_HURT:
        return "暴击伤害"


def id2skillname(skid: int):
    return SKILLS[skid]['name']

def id2blessname(blid: int):
    return BLESSINGS[blid]['name']

