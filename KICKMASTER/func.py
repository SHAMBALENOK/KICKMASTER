import asyncio
import time

import cons
import cons as c

sticker_control = c.settings['sticker_con']
num = 0
start_num = True
dam = cons.settings['sticker_count']
rep_block = False
sticker_time = 0


def delete():
    global start_num, num
    num = 0
    start_num = True


def kick(message, idd: int = None):
    chat_id = message.json['chat']['id']
    if idd:
        c.bot.kick_chat_member(chat_id, idd)
    else:
        chat_id = message.json['chat']['id']
        from_id = message.json['from']['id']
        try:
            user_id = message.json['reply_to_message']['from']['id']
            get = c.bot.get_chat_member
            if get(chat_id, from_id).status == 'restricted' or get(chat_id, from_id).status == 'member':
                c.bot.reply_to(message, 'Недостоин')
            elif get(chat_id, user_id).status == 'creator' or get(chat_id, user_id).status == 'administrator':
                c.bot.reply_to(message, 'Недостоин')
            else:
                c.bot.reply_to(message, f'Раба {get(chat_id, user_id).user.first_name} шлепнули по попе насмерть')
                time.sleep(5)
                c.bot.kick_chat_member(chat_id, user_id)
        except KeyError:
            c.bot.reply_to(message, 'Я запрещаю использовать ее не в ответ')


def mute(message, idd: int = None, du: int = None):
    global rep_block
    chat_id = message.json['chat']['id']
    if idd and du:
        c.bot.restrict_chat_member(chat_id, idd, until_date=time.time() + du * 60)
    else:
        from_id = message.json['from']['id']
        try:
            user_id = message.json['reply_to_message']['from']['id']
            get = c.bot.get_chat_member
            if get(chat_id, from_id).status == 'restricted' or get(chat_id, from_id).status == 'member':
                c.bot.reply_to(message, 'Недостоин')
            elif get(chat_id, user_id).status == 'creator' or get(chat_id, user_id).status == 'administrator':
                c.bot.reply_to(message, 'Недостоин')
            else:
                dur = 60
                args = message.text.split()[1:]
                if args:
                    try:
                        dur = int(args[0])
                    except ValueError:
                        c.bot.reply_to(message, 'Неправильно, переделывай')
                        return
                    if dur < 1:
                        c.bot.reply_to(message, 'С таким наказанием даже я справлюсь, переделывай')
                        return
                    if dur > 43200:
                        c.bot.reply_to(message, 'Слишком жоска')
                        return
                else:
                    c.bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + dur * 60)
                    c.bot.reply_to(message,
                                   f"Рабу {get(chat_id, user_id).user.first_name} заклеили ротик на {dur} минут.")
        except KeyError:
            c.bot.reply_to(message, 'Я запрещаю использовать ее не в ответ')


def unmute(message):
    chat_id = message.json['chat']['id']
    from_id = message.json['from']['id']
    try:
        user_id = message.json['reply_to_message']['from']['id']
        get = c.bot.get_chat_member
        if get(chat_id, from_id).status == 'restricted' or get(chat_id, from_id).status == 'member':
            c.bot.reply_to(message, 'Недостоин')
        elif get(chat_id, user_id).status == 'creator' or get(chat_id, user_id).status == 'administrator':
            c.bot.reply_to(message, 'Недостоин')
        else:
            c.bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                       can_send_other_messages=True, can_add_web_page_previews=True)
            c.bot.reply_to(message, f"Рабу {message.reply_to_message.from_user.username} отклеили ротик.")
    except KeyError:
        c.bot.reply_to(message, 'Я запрещаю использовать ее не в ответ')


def auto_sticker(message):
    global sticker_control, dam
    chat_id = message.json['chat']['id']
    from_id = message.json['from']['id']
    get = c.bot.get_chat_member
    if get(chat_id, from_id).status == 'restricted' or get(chat_id, from_id).status == 'member':
        c.bot.reply_to(message, 'Недостоин')
    else:
        try:
            dam = int(message.json['text'].split()[1])
            cons.settings['sticker_count'] = dam
            open('settings.txt', 'w').write(str(cons.settings).replace('\'', '\"'))
        except IndexError:
            c.bot.reply_to(message, 'Ку-ку, где циферка!?')
            return
        try:
            1 / int(dam)
        except ZeroDivisionError:
            c.bot.reply_to(message, 'Переделывай')
            return
        sticker_control = True
        cons.settings['sticker_con'] = sticker_control
        open('settings.txt', 'w').write(str(cons.settings).replace('\'', '\"').lower())

        c.bot.reply_to(message, 'Ломатель спама#1 активирован')


def sticker(message):
    global sticker_control, dam
    chat_id = message.json['chat']['id']
    from_id = message.json['from']['id']
    get = c.bot.get_chat_member
    if get(chat_id, from_id).status == 'restricted' or get(chat_id, from_id).status == 'member':
        c.bot.reply_to(message, 'Недостоин')
    else:
        sticker_control = False
        cons.settings['sticker_con'] = sticker_control
        open('settings.txt', 'w').write(str(cons.settings).replace('\'', '\"').lower())
        c.bot.reply_to(message, 'Ломатель спама#1 диактивирован')


def chat_control(message):
    global start_num, num, sticker_control, dam, sticker_time, rep_block
    if sticker_control:
        if time.time() - sticker_time >= 3:
            sticker_time = 0
            num = 0
            start_num = True

        if num == dam:
            c.bot.reply_to(message, 'Запретил рабу обезьяничать')
            idd = message.json['from']['id']
            mute(message, idd, 720)
            sticker_time = 0
            num = 0
            start_num = True

        if num != 0:
            num += 1

        if message.content_type == 'sticker' and start_num:
            sticker_time = time.time()
            start_num = False
            num += 1
