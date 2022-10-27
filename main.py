from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import create_bot as cb
from keyboards.client import kb_client, kb_admin



async def on_startup(_):
    print('Готов к работе! Данные обновлены')
# Клиентская часть*************************************************************************************************


@cb.dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    await cb.bot.send_message(message.from_user.id, f'Доброго дня! {message.from_user.first_name} {message.from_user.last_name},'
                                                 f' Давай найдем хулиганов - расхитителей', reply_markup=kb_client)
    await message.delete()


@cb.dp.message_handler(text=['Поиск по лицевому счету'])
async def search_by_ls(message: types.Message):
    await cb.bot.send_message(message.from_user.id, 'Введите номер лицевого счета')
    print(message.text)


@cb.dp.message_handler(text=['Поиск по ФИО, названию'])
async def search_by_fio(message: types.Message):
    await cb.bot.send_message(message.from_user.id, 'Обработка поиска по ФИО')

@cb.dp.message_handler(text=['Поиск по адресу'])
async def search_by_address(message: types.Message):
    await cb.bot.send_message(message.from_user.id, 'Обработка поиска по адресу')


@cb.dp.message_handler(text=['Выборка на номеру ТП'])
async def search_by_tp(message: types.Message):
    await cb.bot.send_message(message.from_user.id, 'Обработка поиска по номеру ТП')


# Админская часть****************************************************************************************************
@cb.dp.message_handler(commands=['admin'])
async def commands_admin(message: types.Message):
    await cb.bot.send_message(message.from_user.id, f'Вы админ, можете добавлять или удалять данные', reply_markup=kb_admin)
    await message.delete()

# Общая часть********************************************************************************************************


@cb.dp.message_handler()
async def echo_send(message : types.Message):
    await message.reply('разговаривать будем в другом месте, а теперь за работу!!!')

executor.start_polling(cb.dp, skip_updates=True, on_startup=on_startup)
