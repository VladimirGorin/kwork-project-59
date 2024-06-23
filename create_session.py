import os
import json
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Функция для чтения файла с сессиями
def read_sessions(file_path):
    sessions = []
    with open(file_path, 'r') as file:
        for line in file:
            phone, api_id, api_hash = line.strip().split(',')
            sessions.append((phone, int(api_id), api_hash))
    return sessions

# Функция для сохранения данных api_id и api_hash
def save_api_data(phone, api_id, api_hash):
    api_data_path = os.path.join('sessions', f'{phone}.json')
    with open(api_data_path, 'w') as json_file:
        json.dump({'api_id': api_id, 'api_hash': api_hash}, json_file)

# Основная функция
def main():
    # Создаем директорию sessions, если она не существует
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

    # Читаем сессии из файла
    sessions = read_sessions('sessions.txt')

    for phone, api_id, api_hash in sessions:
        session_path = os.path.join('sessions', f'{phone}.session')
        client = TelegramClient(session_path, api_id, api_hash)

        async def authorize_and_save():
            await client.connect()
            if not await client.is_user_authorized():
                try:
                    await client.send_code_request(phone)
                    code = input(f'Enter the code for {phone}: ')
                    await client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    password = input(f'Password needed for {phone}: ')
                    await client.sign_in(password=password)
            save_api_data(phone, api_id, api_hash)
            await client.disconnect()

        client.loop.run_until_complete(authorize_and_save())

if __name__ == '__main__':
    main()
