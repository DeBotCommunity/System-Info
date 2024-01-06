# Module by DeCoded
# EW: https://endway.su/@decoded
# TG: https://t.me/whynothacked
# Канал с модулями: https://t.me/DeBot_userbot

import asyncio
import platform
from datetime import datetime

import psutil
from telethon import __version__, events

from userbot import client

info = {'category': 'tools', 'pattern': '.sys', 'description': 'Информация о системе'}

async def format_size(bytes, suffix="Б"):
    factor = 1024
    for unit in ["", "К", "М", "Г", "Т", "П"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


@client.on(events.NewMessage(outgoing=True, pattern=".sys"))
async def sys_info(event):
    system_info = platform.uname()
    software_info = f"<b>Информация о системе</b>\n"
    software_info += f"<code>Система: {system_info.system}</code>\n"
    software_info += f"<code>Версия: {system_info.release}</code>\n"
    software_info += f"<code>Версия ОС: {system_info.version}</code>\n"
    software_info += f"<code>Архитектура: {system_info.machine}</code>\n"

    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    software_info += f"<code>Время загрузки: {boot_time.day}/{boot_time.month}/{boot_time.year}  {boot_time.hour}:{boot_time.minute}:{boot_time.second}</code>"

    cpu_info = f"<b>Информация о процессоре</b>\n"
    cpu_info += f"<code>Физические ядра: {psutil.cpu_count(logical=False)}</code>\n"
    cpu_info += f"<code>Логические ядра: {psutil.cpu_count(logical=True)}</code>\n"

    cpu_freq = psutil.cpu_freq()
    cpu_info += f"<code>Максимальная частота: {cpu_freq.max:.2f}МГц</code>\n"
    cpu_info += f"<code>Минимальная частота: {cpu_freq.min:.2f}МГц</code>\n"
    cpu_info += f"<code>Текущая частота процессора: {cpu_freq.current:.2f}МГц</code>\n"

    cpu_info += "<b>Использование ЦП</b>\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_info += f"<code>Ядро {i}: {percentage}%</code>\n"

    cpu_info += f"<b>Использование ЦП (Всего)</b>\n"
    cpu_info += f"<code>Все ядра: {psutil.cpu_percent()}%</code>"

    memory_info = f"<b>Использование памяти</b>\n"
    svmem = psutil.virtual_memory()
    memory_info += f"<code>Всего: {await format_size(svmem.total)}</code>\n"
    memory_info += f"<code>Доступно: {await format_size(svmem.available)}</code>\n"
    memory_info += f"<code>Использовано: {await format_size(svmem.used)}</code>\n"
    memory_info += f"<code>Загрузка: {svmem.percent}%</code>"

    network_info = "<b>Использование сети</b>\n"
    network_info += f"<code>Отправлено: {await format_size(psutil.net_io_counters().bytes_sent)}</code>\n"
    network_info += f"<code>Получено: {await format_size(psutil.net_io_counters().bytes_recv)}</code>"

    engine_info = "<b>Информация о движке</b>\n"
    engine_info += f"<code>Python: {platform.python_version()}</code>\n"
    engine_info += f"<code>Telethon: {__version__}</code>"

    result = f"{software_info}\n{cpu_info}\n{memory_info}\n{network_info}\n{engine_info}"

    await client.edit_message(
        event.chat_id,
        event.message.id,
        result,
        parse_mode="HTML",
    )
