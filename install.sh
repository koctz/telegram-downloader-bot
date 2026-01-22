#!/bin/bash

echo ""
echo "========================================"
echo "   Telegram Downloader Bot Installer"
echo "========================================"
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Docker не установлен."
    echo "Установи Docker и запусти скрипт снова."
    exit 1
fi

# Проверка Docker Compose v2
if ! docker compose version &> /dev/null
then
    echo "❌ Docker Compose v2 не установлен."
    echo "Установи Docker Compose и запусти скрипт снова."
    exit 1
fi

echo "✔ Docker найден"
echo "✔ Docker Compose найден"
echo ""

# Ввод токена
while [[ -z "$BOT_TOKEN" ]]; do
    read -p "Введите токен Telegram бота: " BOT_TOKEN
    if [[ -z "$BOT_TOKEN" ]]; then
        echo "Токен не может быть пустым."
    fi
done

# Ввод админов
read -p "Введите ID администратора (можно оставить пустым): " ADMINS

# Создание .env
echo ""
echo "Создаю .env файл..."

cat > .env <<EOF
BOT_TOKEN=$BOT_TOKEN
ADMINS=$ADMINS
DOWNLOAD_DIR=downloads
EOF

echo "✔ Файл .env создан"
echo ""

# Создание директории downloads
mkdir -p downloads
chmod 777 downloads

echo "✔ Папка downloads готова"
echo ""

# Сборка контейнера
echo "Собираю Docker контейнер..."
docker compose build

if [[ $? -ne 0 ]]; then
    echo "❌ Ошибка сборки Docker контейнера."
    exit 1
fi

echo "✔ Сборка завершена"
echo ""

# Запуск контейнера
echo "Запускаю бота..."
docker compose up -d

if [[ $? -ne 0 ]]; then
    echo "❌ Ошибка запуска контейнера."
    exit 1
fi

echo ""
echo "========================================"
echo "   🎉 Бот успешно установлен и запущен!"
echo "========================================"
echo ""
echo "Логи: docker compose logs -f"
echo "Остановить: docker compose down"
echo ""

