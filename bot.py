import telebot  # импортируем модуль telebot
import logging  # импортируем модуль logging для ведения логов
import openai  # импортируем openai для использования API ChatGPT
import random  # импортируем random для генерации случайных чисел
from telebot.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

API_TOKEN = "7844529337:AAEzyxNayk0lMf7tfKmv2J4hOQeCb8zFRAY"  # токен вашего бота
OPENAI_API_KEY = "sk-OoFmHEGZxO98KmA6F3yRdpcO4BLstNGtss6N5RpQ3IT3BlbkFJnlP7Pq9q8ImFpuKhmXg9BU0D9s6RwLfiK5eaQg6RkA"  # токен вашего OpenAI API

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Initialize bot and OpenAI API
bot = telebot.TeleBot(API_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.inline_handler(func=lambda query: True)  # обработчик инлайн-запросов
def handle_inline_query(inline_query: InlineQuery):
    try:
        if not inline_query.query:
            return

        question = inline_query.query

        # Generate a random percentage result
        percentage = random.randint(0, 100)
        response_text = f"Вы на {percentage}%"

        # Use OpenAI API to enhance the response in a humorous and playful way
        openai_response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Ты шуточный бот, который всегда отвечает на вопросы в шутливой форме, используя случайные проценты. Не давай серьёзные ответы и не пытайся объяснить что-то логически, просто шути одним коротким предложением."},
                {"role": "user", "content": f"{question} Ответь на вопрос с учетом процента: {percentage}%."}
            ],
            max_tokens=50
        )
        enhanced_response = openai_response.choices[0].message['content'].strip()

        # Create the inline query result
        result = InlineQueryResultArticle(
            id='1',
            title='Ответить на вопрос',
            input_message_content=InputTextMessageContent(enhanced_response)
        )

        # Send the result
        bot.answer_inline_query(inline_query.id, [result])

    except Exception as e:
        logging.error(f"Ошибка: {e}")

@bot.message_handler(commands=['test'])  # определяем обработчик команды /test
def handle_test_command(message):
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            bot.send_message(message.chat.id, "Использование: /test вопрос")
            return

        question = command_parts[1]

        # Generate a random percentage result
        percentage = random.randint(0, 100)
        response_text = f"Вы на {percentage}%"

        # Use OpenAI API to enhance the response in a humorous and playful way
        openai_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты шуточный бот, который всегда отвечает на вопросы в шутливой форме, используя случайные проценты. Не давай серьёзные ответы и не пытайся объяснить что-то логически, просто шути одним коротким предложением."},
                {"role": "user", "content": f"{question} Ответь на вопрос с учетом процента: {percentage}%."}
            ],
            max_tokens=50
        )
        enhanced_response = openai_response.choices[0].message['content'].strip()

        # Reply with the enhanced response
        bot.send_message(message.chat.id, enhanced_response)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")

bot.polling()  # запускаем бота
