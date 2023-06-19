from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ContentType

from main import dp, bot
from config import OPENAI_KEY
from keyboards import keyboard_main_menu, keyboard_back_main_menu
from state import MainMenuStates
from work_func import refactoring_answer, voice_to_text_transcribe

from base64 import b64decode

import openai


openai.api_key = OPENAI_KEY


@dp.message_handler(Command('start'))
async def start_message(message: Message):
    """
    Стартовое сообщение.
    :param message: Сообщение от пользователя(в частности start).
    :return: Ответ для запуска главного меню.
    """
    await message.answer('To start:\n/mainmenu')


async def back_call(message):
    """
    Переход в главное меню.
    :param message: Сообщение назад.
    :return: Перевод машины состояний в главное меню.
    """
    await main_menu_setter(message)


@dp.message_handler(Command('mainmenu'))
async def main_menu_setter(message: Message):
    """
    Шапка главного меню. Необходимо для навигации и передачи выбора пользователя в машину состояний.
    :param message: Сообщение от пользователя(в частности /mainmenu).
    :return: Вывод легенды навигации и переход в состояние главного меню.
    """
    await message.answer('Main menu')
    await message.answer("!!!DEMO!!!\nIt's main menu. Please enter the point menu:\n"
                         "1. Echo mod 1\n"
                         # "2. GPT chat mode 2\n"
                         "3. GPT QA mode \n"
                         "4. GPT image \n",
                         # "/back to main menu",
                         reply_markup=keyboard_main_menu,)
    await MainMenuStates.main_menu.set()


@dp.message_handler(state=MainMenuStates.main_menu)
async def main_main_handler(message: Message):
    """
    Обработчик выбора пункта меню.
    :param message: Пункт меню.
    :return: Шапка пункта меню и перевод машину состояния в определенный режим работы.
    """
    user_choice = message.text

    if user_choice == 'Echo mode':
        await message.answer('Echo mod\nEnter something', reply_markup=keyboard_back_main_menu)
        await MainMenuStates.menu_point_1.set()
    #
    # elif user_choice == 'GPT chat mode':
    #     await message.answer('GPT chat mode\nEnjoy:', reply_markup=keyboard_back_main_menu)
    #     await MainMenuStates.menu_point_2.set()

    elif user_choice == 'GPT QA mode':
        await message.answer('GPT QA mode\nEnjoy:', reply_markup=keyboard_back_main_menu)
        await MainMenuStates.menu_point_3.set()

    elif user_choice == 'GPT Image mode':
        await message.answer('GPT image\nEnjoy:', reply_markup=keyboard_back_main_menu)
        await MainMenuStates.menu_point_4.set()

    elif user_choice == '/back':
        await MainMenuStates.main_menu.set()

    else:
        await message.answer('Enter error')


@dp.message_handler(state=MainMenuStates.menu_point_1, content_types=[
    ContentType.TEXT,
    ContentType.VOICE,
])
async def menu_echo(message: Message):
    """
    Эхо модуль бота.
    :param message: Сообщение пользователя.
    :return: Ответ сообщением message.
    """
    await message.answer('Обработка запроса', reply_markup=ReplyKeyboardRemove())

    user_text = message.text
    if user_text == '/back':
        await back_call(message)
    else:
        if message.content_type == ContentType.VOICE:
            user_text = await voice_to_text_transcribe(bot=bot, message=message)

        await message.answer(
            f'You say:\n{user_text}',
            reply_markup=keyboard_back_main_menu,
        )


# @dp.message_handler(state=MainMenuStates.menu_point_2)
# async def menu_gpt_chat(message: Message):
#     """
#     Модуль бота, который получает ответ от нейронной сети (GPT)
#         - version: 3.5
#         - Example: chat
#     :param message: Запрос пользователя к нейронной сети
#     :return: Ответ нейронной сети
#     """
#     await message.answer('Обработка запроса', reply_markup=ReplyKeyboardRemove())
#
#     user_text = message.text
#     if user_text == '/back':
#         await back_call(message)
#     else:
#         response = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             message=[
#                 {'role': 'system', 'content': 'You are a helpful assistant.'},
#                 {'role': 'user', 'content': user_text},
#             ],
#             temperature=float(0.5),
#             max_tokens=256,
#             n=int(1),
#             stop=['Human:'],
#             presence_penalty=float(0),
#             frequency_penalty=float(0.1),
#         )
#         # gpt_answer = str(response['choices'][0]['text'])
#         #
#         # if gpt_answer[-1] not in '.?!':
#         #     gpt_answer = await refactoring_answer(gpt_answer)
#
#         # await message.answer(gpt_answer, reply_markup=keyboard_back_main_menu)
#         await message.answer(response, reply_markup=keyboard_back_main_menu)


@dp.message_handler(state=MainMenuStates.menu_point_3, content_types=[
    ContentType.TEXT,
    ContentType.VOICE,
])
async def menu_gpt_qa(message: Message):
    """
    Модуль бота, который получает ответ от нейронной сети (GPT)
        - version: 3.5
        - Example: QA
    :param message: Запрос пользователя к нейронной сети
    :return: Ответ нейронной сети
    """
    user_text = message.text

    if user_text == '/back':
        await back_call(message)
    else:
        if message.content_type == ContentType.VOICE:
            user_text = await voice_to_text_transcribe(bot=bot, message=message)
        await message.answer(f'Запрос:\n{user_text}', reply_markup=ReplyKeyboardRemove())
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_text,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

        gpt_answer = str(response['choices'][0]['text']).strip()
        if gpt_answer == '':
            await message.answer('Very difficult', reply_markup=keyboard_back_main_menu)
        else:
            if (gpt_answer[-1] not in '.?!') or \
                    (gpt_answer[0] != gpt_answer[0].upper()) or not(gpt_answer.isalpha()):
                gpt_answer = await refactoring_answer(user_text, gpt_answer)

            await message.answer(gpt_answer, reply_markup=keyboard_back_main_menu)


@dp.message_handler(state=MainMenuStates.menu_point_4, content_types=[
    ContentType.TEXT,
    ContentType.VOICE,
])
async def menu_gpt_image(message: Message):
    """
    Отправляет сгенерированное изображение по запросу пользователя
    :param message: Запрос пользователя
    :return: Изображение по запросу
    """
    user_text = message.text

    if user_text == '/back':
        await back_call(message)
    else:
        if message.content_type == ContentType.VOICE:
            user_text = await voice_to_text_transcribe(bot=bot, message=message)

        await message.answer(f'Запрос:\n{user_text}', reply_markup=ReplyKeyboardRemove())
        response = openai.Image.create(
            prompt=user_text,
            n=1,
            size='256x256',
            response_format='b64_json'
        )

        image_data = b64decode(response['data'][0]['b64_json'])
        await bot.send_photo(chat_id=message.chat.id, photo=image_data, reply_markup=keyboard_back_main_menu)
