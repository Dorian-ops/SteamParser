import requests
from bs4 import BeautifulSoup
import re
import subprocess


def download_mod(urlgame):
    # Получение HTML контента страницы модификации
    response = requests.get(urlgame)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск изображения и извлечение ID игры
    img_tag = soup.find('div', class_='apphub_AppIcon')
    if img_tag:
        img_tag = img_tag.find('img')
        if img_tag:
            src_url = img_tag['src']
            match = re.search(r'/apps/(\d+)/', src_url)
            if match:
                app_id = match.group(1)
                print("ID игры:", app_id)
            else:
                print("ID не найден в URL изображения.")
                return
        else:
            print("Тег <img> не найден внутри div с классом 'apphub_AppIcon'.")
            return
    else:
        print("Div с классом 'apphub_AppIcon' не найден.")
        return

    # Извлечение ID модификации из URL
    match = re.search(r'[?&]id=(\d+)', urlgame)
    if match:
        mod_id = match.group(1)
        print("ID модификации:", mod_id)
    else:
        print("ID модификации не найден в URL.")
        return

    # Запрос на подтверждение скачивания
    while True:
        user_input = input("Выполнить скачивание? (Y/N): ").strip().upper()
        if user_input in ('Y', 'N'):
            break
        else:
            print("Пожалуйста, введите только 'Y' или 'N'.")

    if user_input == 'Y':
        try:
            result = subprocess.run(
                [r"C:\SteamCMD\steamcmd.exe", "+login", "anonymous", "+force_install_dir", r"C:\Mods",
                 "+workshop_download_item", str(app_id), str(mod_id), "+validate", "+quit"],
                cwd=r"C:\SteamCMD",
                capture_output=True,
                text=True,
                timeout=60
            )
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print("Время выполнения команды истекло.")
    else:
        print("Отменено!")


def is_collection(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    collection_div = soup.find('div', class_='collectionChildren')
    if not collection_div:
        return False

    # Проверяем наличие элементов управления
    control_elements = ['subscribe', 'unsubscribe', 'SaveCollectionToCollection']
    for class_name in control_elements:
        if collection_div.find(attrs={'class': class_name}):
            return True

    onclick_tags = collection_div.find_all(attrs={'onclick': True})
    for tag in onclick_tags:
        if any(func in tag['onclick'] for func in control_elements):
            return True

    return False
