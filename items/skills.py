EDGE = '边境技能'
DINGZHEN_BASE = '丁真基础技能'

EDGESKILLS = {
    1001:{
        'name': '普通攻击',
        'class': EDGE,
        'des': '最朴实无华的技能，却也是理塘中最常见的技能之一。',
        'effect_text': '对敌人造成攻击力100%的伤害'
    },
    1002:{
        'name': '普通攻击(升级！)',
        'class': EDGE,
        'des': '最朴实无华的技能的升级版，它想成为陪伴你时间最久的技能！',
        'effect_text': '对敌人造成攻击力120%的伤害'
    }
}

DINGZHEN_BASE_SKILLS = {
    1101:{
        'name': '丁真气焰',
        'class': DINGZHEN_BASE,
        'des': "丁真的'气焰'————可能说的是电子烟吧。",
        'effect_text': '战斗开始前，攻击力增加{技能等级}%'
    },
    1102:{
        'name': '丁真气势',
        'class': DINGZHEN_BASE,
        'des': "丁真的'气势'————据说丁真有许多动物朋友，他的气势可能就来自于此。",
        'effect_text': '战斗开始前，攻击力增加{技能等级}'
    },
    1103:{
        'name': '丁真强健',
        'class': DINGZHEN_BASE,
        'des': "'强健'表示的是一种状态，这意味着，丁真已经准备好进行一场大战了。",
        'effect_text': '战斗开始前，防御力增加{技能等级}'
    },
}

SKILLS = {**EDGESKILLS, **DINGZHEN_BASE_SKILLS}
