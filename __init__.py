import asyncio

from nonebot.params import CommandArg

from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER

from .utils.common_utils import *
from system.system import *
from .items.skills import *
from .items.blessings import *


mgr = Manager()
IN_MUSEUM = []

createlt = on_command('创建新探索', priority=5, block=True)
commandgt = on_command('a', aliases={'b', 'c'}, priority=5)
endgame = on_command('结束探索', priority=5, block=True)
museum = on_command('理塘博物馆', priority=5, block=True)
ltquery = on_command('技能详情', aliases={'祝福详情'}, priority=5, block=True)


@createlt.handle()
async def createlita(ev: GroupMessageEvent):
    gid, uid = ev.group_id, ev.user_id
    username = sender2name(ev)

    if mgr.is_playing(gid):
        await createlt.finish("现在有人正在探索中！请等待他探索完毕。")
    else:
        with mgr.start(gid, uid) as game:
            game.choice = CHOICE_STARTGAME
            await createlt.send(
                f"欢迎你，勇敢的探索者{username}.理塘是一个神秘而危险的地方，你是否能够突破重重难关，到达传说中的世界最高峰呢？"
                f"\n...准备好了吗？\n\na: 开始吧！\nb: 算了...")
            for i in range(60):  # 从等待到正式开始的循环等待
                await asyncio.sleep(WAIT_TIME)
                if game.status in (STATUS_FINISH, STATUS_END, STATUS_READY):
                    break

            if game.status in (STATUS_FINISH, STATUS_END, STATUS_PREPARE):
                await createlt.finish(
                    MessageSegment.at(uid) + '看起来你探索的意志不是特别坚定呢....没关系，Ophelia会一直在这里等待你的！')
            else:
                while True:
                    await asyncio.sleep(WAIT_TIME)
                    if game.status in (STATUS_END, STATUS_WIN):
                        break
                if game.status == STATUS_WIN:
                    await createlt.finish('test complete')
                if game.status == STATUS_END:
                    await createlt.finish('真遗憾...下次再来探索吧！')


@ltquery.handle()
async def litangquery(ev: GroupMessageEvent, arg: Message = CommandArg()):
    no = arg.extract_plain_text().strip()
    try:
        no = int(no)
    except Exception:
        ltquery.finish('你输入的技能编号有误！')
    txt = ev.get_plaintext()
    if txt.startswith('技能详情'):
        if no in SKILLS.keys():
            skill = SKILLS[no]
            msg = f"技能名称：{skill['name']}\n"
            msg += f"技能类别：{skill['class']}\n"
            msg += f"技能效果：{skill['effect_text']}\n"
            msg += f"技能描述：{skill['des']}"
            await ltquery.finish(msg)
        else:
            await ltquery.finish('没有找到对应的技能信息......')
    else:
        if no in BLESSINGS.keys():
            bless = BLESSINGS[no]
            msg = f"祝福名称：{bless['name']}\n"
            msg += f"祝福类别：{bless['class']}\n"
            msg += f"祝福效果：{bless['effect_text']}\n"
            msg += f"祝福描述：{bless['des']}"
            await ltquery.finish(msg)
        else:
            await ltquery.finish('没有找到对应的祝福信息......')


@endgame.handle()
async def gameend(bot, ev: GroupMessageEvent):
    gid, uid = ev.group_id, ev.user_id
    game = mgr.get_game(gid)

    if not game or game.status == STATUS_END:
        return
    if not await GROUP_ADMIN(bot, ev) and not await GROUP_OWNER(bot, ev) and not uid == game.user_id:
        await endgame.finish('只有群管理或房主才能强制结束', at_sender=True)

    game.status = STATUS_END
    await endgame.finish('请稍候...正在收拾行李...')


@museum.handle()
async def ltmuseum(ev: GroupMessageEvent):
    gid = ev.group_id
    if gid not in IN_MUSEUM:
        IN_MUSEUM.append(gid)

    await museum.finish(
        f'欢迎来到理塘博物馆！在这里你可以确认当前理塘所有的技能与雪豹祝福。\n(当前游戏版本：{__plugin_version__})\n'
        f'\na: 查看所有技能\nb: 查看所有雪豹祝福\nc: 离开博物馆')


# 游戏内选择分支的统一处理
@commandgt.handle()
async def commandget(ev: GroupMessageEvent):
    choose = ev.get_plaintext()
    gid, uid = ev.group_id, ev.user_id
    game = mgr.get_game(gid)

    if not game and gid not in IN_MUSEUM:
        return

    if gid in IN_MUSEUM:
        match choose:
            case 'a':
                IN_MUSEUM.remove(gid)
                msg = '当前版本全技能列表：\n\n边境技能：\n'
                for k, v in EDGESKILLS.items():
                    msg += f"{k} : {v['name']}\n"
                msg += '\n丁真基础技能：\n'
                for k, v in DINGZHEN_BASE_SKILLS.items():
                    msg += f"{k} : {v['name']}\n"
                msg += f"\n全技能共{len(SKILLS)}个\n(发送'技能详情 技能编号'来获得技能的具体信息)"
                await commandgt.finish(msg)
            case 'b':
                IN_MUSEUM.remove(gid)
                msg = '当前版本全祝福列表：\n\n边境祝福：\n'
                for k, v in EDGEBLESSINGS.items():
                    msg += f"{k} : {v['name']}\n"
                msg += f"\n全祝福共{len(BLESSINGS)}个\n(发送'祝福详情 祝福编号'来获得技能的具体信息)"
                await commandgt.finish(msg)
            case 'c':
                IN_MUSEUM.remove(gid)
                await commandgt.finish('没关系，随时欢迎你来博物馆参观哦！')
            case _:
                return

    if game.choice == CHOICE_STARTGAME:
        match choose:
            case 'a':
                game.status = STATUS_READY
                game.choice = CHOICE_FIRST_TIME
                await commandgt.finish(
                    '那就让我们开始吧！在进入理塘探索之前，首先我们需要进行一些准备工作。请问这是你第一次探索吗？\n\na: 是的！\nb: 不是')
            case 'b':
                game.status = STATUS_FINISH
                await commandgt.finish('请稍候...正在收拾行李...')
            case _:
                return

    if game.choice == CHOICE_FIRST_TIME:
        game.initplayer(uid)
        player = game.role
        player.initdata()

        match choose:
            case 'a':
                game.choice = CHOICE_FIRST_TIME
                await commandgt.send(
                    '嗯哼，是新面孔呢。那就让我来给你讲一讲吧！理塘是一座神秘的古代山峰，在这里，到处都是奇珍异宝...更不用说还有各种神秘现象！据说，这是理塘的守护神“丁真”的魔力造成的。')
                await asyncio.sleep(WAIT_TIME)
                await commandgt.send('有点扯远啦，虽说理塘到处都是宝藏，但在这里，危险也与我们相伴而行。所幸的是，丁真的力量能够成为我们的助力！'
                                     "\n首先是'技能'！技能是每一个理塘生物都拥有的能力，他们在战斗时会发挥作用！作为探索者，技能是我们驱散危险的重要工具。"
                                     "\n然后是'雪豹祝福'！祝福是由丁真直接赋予的一种赐福，能够在探索的途中产生各种有益的效果。"
                                     "\n还有诅....啊好了就先不说这么多了！")
                await asyncio.sleep(WAIT_TIME)
                game.choice = CHOICE_START
                await commandgt.finish(
                    "在每一次探索开始前，你都有机会从3个选项中选择一个，作为你的起始装备！\n现在就来选择吧！\n"
                    "\na: 获得一个随机边境祝福\nb: 升级'普通攻击'技能\nc: 角色的生命值上限、攻击力、防御力各增加10")
            case 'b':
                game.choice = CHOICE_START
                await commandgt.finish("好的，那么现在是常规的起始装备选择时间！\n"
                                       "\na: 获得一个随机边境祝福\nb: 升级'普通攻击'技能\nc: 角色的生命值上限、攻击力、防御力各增加10")
            case _:
                return

    if game.choice == CHOICE_START:
        match choose:
            case 'a':
                allblessnum = len(EDGEBLESSINGS)
                result = random.choice(range(5001, 5001+allblessnum))
                player = game.role
                player.blessings.append(result)
                await commandgt.send(f"你获得了雪豹祝福：{id2blessname(result)}！")
                await commandgt.send(f"正在进入理塘...")
                player.skills.append(1001)
                await asyncio.sleep(WAIT_TIME)
                game.gamestart()
                result_msg = game.game_MessangeBuilder()
                await commandgt.finish(result_msg)
            case 'b':
                game.status = STATUS_FINISH
                await commandgt.finish(
                    MessageSegment.at(uid) + '看起来你探索的意志不是特别坚定呢....没关系，Ophelia会一直在这里等待你的！')
            case _:
                return

    if game.choice == CHOICE_ROOM:
        result = game.GameChoiceHandler(choose)
        if result == RET_ERROR:
            await commandgt.finish('你的选择有误，请重新输入！')
        else:
            await commandgt.send(result)
            await asyncio.sleep(WAIT_TIME)
            newchoicemsg = game.GameMessangeBuilder()
            await commandgt.finish(newchoicemsg)

