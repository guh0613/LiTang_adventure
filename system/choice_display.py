import asyncio
import random

from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.matcher import Matcher

from .attrs import Attr
from .system import *
from ..items.blessings import *
from ..utils.common_utils import id2blessname, id2skillname
from .status import *


async def choicedisplayer(game: System, ev: GroupMessageEvent, matcher: Matcher):
    choose = ev.get_plaintext()
    gid, uid = ev.group_id, ev.user_id
    if game.choice == CHOICE_STARTGAME:
        match choose:
            case 'a':
                game.status = STATUS_READY
                game.choice = CHOICE_FIRST_TIME
                await matcher.finish(
                    '那就让我们开始吧！在进入理塘探索之前，首先我们需要进行一些准备工作。请问这是你第一次探索吗？\n\na: 是的！\nb: 不是')
            case 'b':
                game.status = STATUS_FINISH
                await matcher.finish('请稍候...正在收拾行李...')
            case _:
                return

    if game.choice == CHOICE_FIRST_TIME:
        game.initplayer(uid)
        player = game.role
        player.initdata()

        match choose:
            case 'a':
                game.choice = CHOICE_FIRST_TIME
                await matcher.send(
                    '嗯哼，是新面孔呢。那就让我来给你讲一讲吧！理塘是一座神秘的古代山峰，在这里，到处都是奇珍异宝...更不用说还有各种神秘现象！据说，这是理塘的守护神“丁真”的魔力造成的。')
                await asyncio.sleep(WAIT_TIME)
                await matcher.send('有点扯远啦，虽说理塘到处都是宝藏，但在这里，危险也与我们相伴而行。所幸的是，丁真的力量能够成为我们的助力！'
                                   "\n首先是'技能'！技能是每一个理塘生物都拥有的能力，他们在战斗时会发挥作用！作为探索者，技能是我们驱散危险的重要工具。"
                                   "\n然后是'雪豹祝福'！祝福是由丁真直接赋予的一种赐福，能够在探索的途中产生各种有益的效果。"
                                   "\n还有诅....啊好了就先不说这么多了！")
                await asyncio.sleep(WAIT_TIME)
                game.choice = CHOICE_START
                await matcher.finish(
                    "在每一次探索开始前，你都有机会从3个选项中选择一个，作为你的起始装备！\n现在就来选择吧！\n"
                    "\na: 获得一个随机边境祝福\nb: 升级'普通攻击'技能\nc: 角色的生命值上限、攻击力、防御力各增加10")
            case 'b':
                game.choice = CHOICE_START
                await matcher.finish("好的，那么现在是常规的起始装备选择时间！\n"
                                     "\na: 获得一个随机边境祝福\nb: 升级'普通攻击'技能\nc: 角色的生命值上限、攻击力、防御力各增加10")
            case _:
                return

    if game.choice == CHOICE_START:
        match choose:
            case 'a':
                allblessnum = len(EDGEBLESSINGS)
                result = random.choice(range(5001, 5001 + allblessnum))
                player = game.role
                player.blessings.append(result)
                await matcher.send(f"你获得了雪豹祝福：{id2blessname(result)}！")
                await matcher.send(f"正在进入理塘...")
                await asyncio.sleep(WAIT_TIME)
                game.gamestart()
                result_msg = game.gamemessangebuilder()
                await matcher.finish(result_msg)
            case 'b':
                player = game.role
                del player.skills[1001]
                player.skills[1002] = 1
                await matcher.send(f"你的普通攻击变为了升级版！")
                await matcher.send(f"正在进入理塘...")
                await asyncio.sleep(WAIT_TIME)
                game.gamestart()
                result_msg = game.gamemessangebuilder()
                await matcher.finish(result_msg)
            case 'c':
                player = game.role
                player.attrChange(Attr.MAX_HEALTH, 10)
                player.attrChange(Attr.ATTACK, 10)
                player.attrChange(Attr.DEFENSIVE, 10)
                await matcher.send(f"你的生命值上限、攻击力、防御力各增加了10！")
                await matcher.send(f"正在进入理塘...")
                await asyncio.sleep(WAIT_TIME)
                game.gamestart()
                result_msg = game.gamemessangebuilder()
                await matcher.finish(result_msg)

    if game.choice == CHOICE_ROOM:
        result = game.gamechoicehandler(choose)
        if result == RET_ERROR:
            await matcher.finish('你的选择有误，请重新输入！')
        else:
            await matcher.send(result)

            if game.roomid < 90000:
                await matcher.send('正在进入下一个房间...')
                game.go_on()
                await asyncio.sleep(WAIT_TIME)
                newchoicemsg = game.gamemessangebuilder()
                await matcher.finish(newchoicemsg)
