import os
import json
import random
import asyncio
from datetime import datetime
from telethon import TelegramClient, functions

# Путь к папке с сессиями
sessions_path = './sessions'

# Получаем список всех файлов в папке sessions
files = os.listdir(sessions_path)

# Фильтруем файлы, оставляем только те, которые заканчиваются на .session и .json
session_files = [f for f in files if f.endswith('.session')]
json_files = [f for f in files if f.endswith('.json')]

# Создаем соответствие session файлов и json файлов
session_json_map = {}
for session_file in session_files:
    phone = session_file.split('.')[0]
    json_file = f'{phone}.json'
    if json_file in json_files:
        session_json_map[session_file] = json_file

# Функция для отправки сообщения в Избранное
async def send_message_to_saved(client, phone):
    await client.send_message('me', f'Привет от {phone}')

# Функция для имитации онлайн аккаунта
async def simulate_online(client, offline_secods, online_secods, phone):
    print(f"\n{datetime.now()}: {phone} будет в сети {online_secods} сек\n")
    await client(functions.account.UpdateStatusRequest(offline=False))
    await asyncio.sleep(online_secods)
    print(f"\n{datetime.now()}: {phone} будет спать {offline_secods} сек\n")
    await client(functions.account.UpdateStatusRequest(offline=True))
    await asyncio.sleep(offline_secods)

# Асинхронная функция для работы с одним аккаунтом
async def handle_account(session_file, json_file):
    session_path = os.path.join(sessions_path, session_file)
    json_path = os.path.join(sessions_path, json_file)
    phone = session_file.split('.')[0]

    # Читаем данные из json файла
    with open(json_path, 'r') as f:
        data = json.load(f)
        api_id = data['api_id']
        api_hash = data['api_hash']

    # Создаем клиента
    client = TelegramClient(session_path, api_id, api_hash)

    # Подключаемся к клиенту
    await client.start()

    while True:
        # Генерируем случайное количество часов онлайн
        offline_secods = random.randint(5, 100)
        online_secods = random.randint(60, 100)

        await simulate_online(client, offline_secods, online_secods, phone)

    await client.disconnect()

    print(f"{datetime.now()}: Аккаунт {phone} завершил работу")

# Основная асинхронная функция для запуска всех аккаунтов
async def main():
    tasks = []

    for session_file, json_file in session_json_map.items():
        tasks.append(handle_account(session_file, json_file))

    # Запускаем все задачи параллельно
    await asyncio.gather(*tasks)

# Запускаем основной цикл
if __name__ == '__main__':
    asyncio.run(main())
