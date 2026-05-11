import telebot
import requests
import os

API_TOKEN = '8434419214:AAECtjHW0mJTXYFtlNIKmDhFaV9OIXQf22E'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(content_types=['photo'])
def guardar_portada(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    user_data[message.chat.id] = file_info.file_path
    bot.reply_to(message, "📸 Portada recibida. Envía el video ahora.")

@bot.message_handler(content_types=['video'])
def enviar_video(message):
    foto_path = user_data.get(message.chat.id)
    if not foto_path:
        bot.reply_to(message, "❌ Envía la foto primero.")
        return

    # Descargar la foto localmente
    url_foto = f"https://api.telegram.org/file/bot{API_TOKEN}/{foto_path}"
    img_data = requests.get(url_foto).content
    with open("thumb.jpg", "wb") as f:
        f.write(img_data)

    bot.reply_to(message, "⚡ Intentando forzar la portada...")

    try:
        with open("thumb.jpg", "rb") as t:
            # Intentamos enviarlo de una forma que Telegram RE-PROCESE la miniatura
            bot.send_video(
                message.chat.id, 
                message.video.file_id, 
                thumb=t, 
                caption=message.caption or "🎬 Flixmore",
                supports_streaming=True,
                width=640, # Forzamos dimensiones para que Telegram crea que es nuevo
                height=360
            )
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()
