from aiogram import Bot, Dispatcher, executor, types
import feedparser # подключаю библиотеки
def getDescriptions(url_feed): #функция получает ссылку на rss ленту, возвращает        
# ленту, распаршенную с помощью feedparser
    lenta = feedparser.parse(url_feed)
    descriptions = []
    for item_of_news in lenta['items']:
        descriptions.append(item_of_news ['description']) # вытаскиваю из ленты описание всех новостей в виде списка
    a = str()
    for g in range(len(descriptions) - 10, len(descriptions)):
        a = a + descriptions[g] + '\n' # преобразую последние десять новостей в строку и добавляю в переменную a. добавляю туда же \n для разделения новостей.
    return a

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# создаю основу бота с помощью классов Dispatcher и bot библиотеки aiogram
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message   .reply("я новостной бот. введите команду /news для получения последних новостей.") # создаю обработчика команды /start
@dp.message_handler(commands=['news'])
async def news(message: types.Message):
    b = getDescriptions('https://lenta.ru/rss/')
    await message   .answer(b)
# создаю обработчика для команды /news
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('некорректное сообщение. введите либо команду /start, либо команду /news') # создаю обработчика всех текстовых сообщений.

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) # создаю точку входа и активирую бота с помощью класса executor.