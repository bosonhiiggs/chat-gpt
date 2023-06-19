from aiogram import Bot
from aiogram.types import Message

from pydub import AudioSegment
from pathlib import Path

import openai
import io

from config import OPENAI_KEY


openai.api_key = OPENAI_KEY


async def refactoring_answer(message_text: str, answer: str) -> str:
    """
    Корректировка сообщение, если последний символ не является символом окончания предложения.
    :param message_text: Исходное сообщение
    :param answer: Ответное сообщение
    :return: Корректное сообщение
    """
    if answer[0] != answer[0].upper() or not(answer[0].isalpha()):
        answer = message_text + answer

    rev_answer = answer[::-1]
    for i_sym in rev_answer:
        if i_sym in '.?!':
            rev_index = rev_answer.find(i_sym)
            answer = answer[:len(answer) - rev_index]
            break
    return answer


async def voice_to_text_transcribe(bot: Bot, message: Message) -> str:
    """
    Расшифровка голосовых сообщений пользователя в текстовый формат с использованием OpenAI: .ogg -> .mp3.
    :param bot: Экземпляр бота, который необходим для загрузки голосового сообщения .
    :param message: Сообщение от пользователя с голосовым сообщением в формате OGG.
    :return: Текстовая расшифровка сообщения.
    """
    voice = message.voice

    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)

    voice_mp3_path = f"voice_files/voice-{voice.file_unique_id}.mp3"
    Path('voice_files').mkdir(parents=True, exist_ok=True)
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        voice_mp3_path, format="mp3"
    )

    with open(f'voice_files/voice-{voice.file_unique_id}.mp3', 'rb') as audio_file:
        transcript = openai.Audio.transcribe(
            'whisper-1', audio_file
        )
        audio_file.close()
    Path(voice_mp3_path).unlink()
    return transcript['text']
