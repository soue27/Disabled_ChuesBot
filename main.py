from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from keyboards.client import kb_client, kb_admin, kb_delete
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import my_db
import os


class ProfileStatesGroup(StatesGroup):
    Mydata = State()


search_pos: int = 0

storage = MemoryStorage()
Token = os.getenv('BOT_TOKEN')
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Готов к работе! Данные обновлены')
    my_db.open_db()
# Клиентская часть*************************************************************************************************


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, f'Доброго дня! {message.from_user.first_name} {message.from_user.last_name},'
                                                 f' Давай найдем хулиганов - расхитителей', reply_markup=kb_client)
    await message.delete()

# 'Поиск по лицевому счету'


@dp.message_handler(content_types=['text'])
async def search_by_data(message: types.Message):
    global search_pos
    if message.text == 'Поиск по лицевому счету':
        search_pos = 1
        await bot.send_message(message.from_user.id, 'Введите номер лицевого счета, можно неполностью', reply_markup=kb_delete())
        await ProfileStatesGroup.Mydata.set()
    elif message.text == 'Поиск по ФИО, названию':
        search_pos = 2
        await bot.send_message(message.from_user.id, 'Введите ФИО/название, можно неполностью', reply_markup=kb_delete())
        await ProfileStatesGroup.Mydata.set()
    elif message.text == 'Поиск по адресу':
        search_pos = 3
        await bot.send_message(message.from_user.id, f'Введите адрес в формате, можно неполностью\n'
                               f'"Чусовой,Клубная,6" либо "Чусовой,Клубная,?"', reply_markup=kb_delete())
        await ProfileStatesGroup.Mydata.set()
    elif message.text == 'Выборка на номеру ТП':
        search_pos = 4
        await bot.send_message(message.from_user.id, 'Введите номер ТП, можно неполностью', reply_markup=kb_delete())
        await ProfileStatesGroup.Mydata.set()
    else:
        await message.reply('Разговаривать будем в другом месте, а теперь за работу!!!')


@dp.message_handler(state=ProfileStatesGroup.Mydata)
async def search_data(message: types.Message, state: FSMContext):
    stroka = message.text
    if search_pos == 1:
        list = my_db.search_by_contract(stroka)
    elif search_pos == 2:
        list = my_db.search_by_counterparty(stroka)
    elif search_pos == 3:
        list = my_db.search_by_address(stroka)
    elif search_pos == 4:
        list = my_db.search_by_tp(stroka)
    if list:
        if len(list) < 5:
            for qw in list:
                await message.reply(
                    f'<u>Отключены: </u> \n'
                    f'ЛС №- <u>{qw[0]} </u>\n'
                    f'ФИО- <u>{qw[1]} </u>\n'
                    f'Адрес- <u>н.п.{qw[2]}, {qw[3]} , ул. {qw[4]}, д. {qw[5]} </u>\n'
                    f'ТП- <u>{qw[6]}</u>', parse_mode='HTML', reply_markup=kb_client)
        else:
            for qw in list:
                await bot.send_message(message.from_user.id, f'Отключен {qw}', reply_markup=kb_client)
    else:
        await message.reply('Потребитель с такими данными не отключен', reply_markup=kb_client)
    await state.finish()


# Админская часть****************************************************************************************************
@dp.message_handler(commands=['admin'])
async def commands_admin(message: types.Message):
    await bot.send_message(message.from_user.id, f'Вы админ, можете добавлять или удалять данные', reply_markup=kb_admin)
    await message.delete()

# Общая часть********************************************************************************************************

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
