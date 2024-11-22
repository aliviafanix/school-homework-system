#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Подготовка к запуску приложения...${NC}"

# Активируем виртуальное окружение, если оно существует
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Активация виртуального окружения${NC}"
    source venv/bin/activate
fi

# Удаляем старую базу данных
if [ -f "school.db" ]; then
    echo -e "${BLUE}🗑️  Удаление старой базы данных...${NC}"
    rm school.db
    echo -e "${GREEN}✓ База данных успешно очищена${NC}"
fi

# Проверяем и освобождаем порт 5000 если он занят
PORT_PID=$(lsof -ti:5000)
if [ ! -z "$PORT_PID" ]; then
    echo -e "${YELLOW}⚠️  Порт 5000 занят (PID: $PORT_PID), освобождаем...${NC}"
    kill -9 $PORT_PID
    echo -e "${GREEN}✓ Порт 5000 освобожден${NC}"
fi

echo -e "${BLUE}🚀 Запуск Flask-приложения...${NC}"
# Запускаем Flask-приложение
python3 app.py
