import telebot
import requests

API_TOKEN = '8434419214:AAECtjHW0mJTXYFtlNIKmDhFaV9OIXQf22E'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(content_types=['photo'])
def guardar_portada(message):
    # Obtenemos la URL de la foto para descargarla temporalmente en el servidor
    file_info = bot.get_file(message.photo[-1].file_id)
    user_data[message.chat.id] = file_info.file_path
    bot.reply_to(message, "📸 Portada lista en el servidor. Envía el video.")

@bot.message_handler(content_types=['video'])
def enviar_video(message):
    foto_path = user_data.get(message.chat.id)
    if not foto_path:
        bot.reply_to(message, "❌ Envía la foto primero.")
        return

    bot.send_chat_action(message.chat.id, 'upload_video')
    
    # Descargamos la miniatura para mandarla como un ARCHIVO real, no como un ID
    url_foto = f"https://api.telegram.org/file/bot{API_TOKEN}/{foto_path}"
    response = requests.get(url_foto)
    
    with open("thumb.jpg", "wb") as f:
        f.write(response.content)

    try:
        # Enviamos el video usando el archivo físico de la miniatura
        with open("thumb.jpg", "rb") as thumb_file:
            bot.send_video(
                message.chat.id, 
                message.video.file_id, 
                thumb=thumb_file, 
                caption=message.caption or "",
                supports_streaming=True
            )
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()
