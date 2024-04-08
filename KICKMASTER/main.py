import asyncio
import cons as c
import func as f


@c.bot.message_handler(content_types=["photo", "sticker", "video", "text"])
def handler(message):
    if message.content_type == 'text':
        if '/kick' in message.text:
            f.kick(message)
        elif '/mute' in message.text:
            f.mute(message)
        elif '/unmute' in message.text:
            f.unmute(message)
        elif '-sticker' in message.text:
            f.auto_sticker(message)
        elif '+sticker' in message.text:
            f.sticker(message)
    else:
        f.chat_control(message)


c.bot.infinity_polling()
