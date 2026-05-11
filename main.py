import telebot

# --- CONFIGURACIÓN ---
API_TOKEN = '8434419214:AAECtjHW0mJTXYFtlNIKmDhFaV9OIXQf22E'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(content_types=['photo'])
def guardar_portada(message):
    user_data[message.chat.id] = message.photo[-1].file_id
    bot.reply_to(message, "✅ Portada guardada. Ahora pásame el video.")

@bot.message_handler(content_types=['video'])
def poner_portada(message):
    foto_id = user_data.get(message.chat.id)
    if not foto_id:
        bot.reply_to(message, "❌ Envía primero una foto.")
        return
    
    bot.reply_to(message, "⏳ Poniendo portada... (esto es rápido)")
    bot.send_video(message.chat.id, message.video.file_id, thumb=foto_id, caption=message.caption or "")

bot.infinity_polling()
