import telebot

# Tu Token
API_TOKEN = '8434419214:AAECtjHW0mJTXYFtlNIKmDhFaV9OIXQf22E'
bot = telebot.TeleBot(API_TOKEN)

# Guardar la foto en memoria rápida
portadas = {}

@bot.message_handler(content_types=['photo'])
def guardar(message):
    portadas[message.chat.id] = message.photo[-1].file_id
    bot.send_message(message.chat.id, "✅ Portada lista. Pásame el video.")

@bot.message_handler(content_types=['video'])
def procesar(message):
    if message.chat.id not in portadas:
        bot.send_message(message.chat.id, "❌ Primero manda la foto.")
        return
    
    # Esto es lo más rápido que permite Telegram
    try:
        bot.send_video(
            message.chat.id, 
            message.video.file_id, 
            thumb=portadas[message.chat.id],
            caption=message.caption or "Copiado con éxito"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"Hubo un error: {e}")

# Esto evita que el bot se caiga por errores tontos
bot.infinity_polling(timeout=10, long_polling_timeout=5)
