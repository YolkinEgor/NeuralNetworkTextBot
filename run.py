from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from neural_network.neural_network import NNTGModel
from utils.config import TELEGRAM_API_KEY
from aiogram.utils import executor
from utils.keyboards import *
from sqlite3 import connect
from utils.states import *
from aiogram import types
from aiogram import Bot

bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher(bot=bot,
                storage=MemoryStorage())
db = connect('database.db')
cur = db.cursor()


@dp.message_handler(commands=['start'], state='*')
async def start_handler(msg: types.Message):
    await msg.answer(text='🌐 Привет, это NNTB.\n'
                          'Я могу генерировать тексты длинной '
                          'до 2000 символов.\n'
                          'Просто напиши /text.')


@dp.message_handler(commands=['text'], state='*')
async def text_handler(msg: types.Message, state: FSMContext):
    args = msg.get_args()
    text_length = 500
    if args and args.isdigit():
        text_length = int(args)

    await SelectTextTypeStatesGroup.select_type_state.set()

    data = {
        'text_len': text_length
    }
    await state.set_data(data=data)
    await msg.answer(text='🌐 Укажите стиль генерируемого текста:',
                     reply_markup=select_type_keyboard)


@dp.callback_query_handler(state=SelectTextTypeStatesGroup.select_type_state)
async def callback_query_handler(cq: types.CallbackQuery, state: FSMContext):
    await cq.answer()
    cq_data = cq.data
    text_length = dict(await state.get_data()).get('text_len')

    text_length = 2000 if text_length > 2000 else text_length

    await cq.message.edit_text(text='📈 Генерирую текст длинной в {} ' \
                                    'символов'.format(text_length))

    model = NNTGModel(cq_data, text_length)
    text = model.generator()

    await cq.message.edit_text(text='Текст, сгенерированный нейросетью:\n\n'
                                    '{}'.format(text))
    await state.finish()


async def start(dispatcher: Dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    print(f'#    start on @{bot_name}')


async def end(dispatcher: Dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=start,
                           on_shutdown=end)
