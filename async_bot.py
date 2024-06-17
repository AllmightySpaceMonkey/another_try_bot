import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# настроим модуль ведения журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# определяем асинхронную функцию
async def start(update, context):
    # ожидание отправки сообщения по сети - нужен `await`
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="I'm a bot, please talk to me!")
    
async def echo(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ == '__main__':
    TOKEN = '7333214196:AAH6Qh31JIoXGcJAaG4ji8BvUzNBywsUywE'
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()

    # создаем новый обработчик для функции `caps()`
    caps_handler = CommandHandler('caps', caps)
    # здесь регистрируются созданные обработчики
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    # вот регистрация для функции `caps()`
    application.add_handler(caps_handler)
    # создаем обработчик для функции `inline_caps()`
    inline_caps_handler = InlineQueryHandler(inline_caps)
    # регистрируем обработчик
    application.add_handler(inline_caps_handler)
    # запускаем приложение
    application.run_polling()