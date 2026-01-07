FROM python:3.10-bookworm

WORKDIR /app

# 1️⃣ Устанавливаем системные зависимости ДЛЯ PILLOW
# Полный стек для Pillow + AVIF
RUN apt-get update && apt-get install -y \
    gcc \
    gettext \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libwebp-dev \
    libavif-dev \
    libaom-dev \
    libdav1d-dev \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Устанавливаем Python-зависимости ПОСЛЕ библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir pillow==11.2.1 \
    && pip install --no-cache-dir -r requirements.txt

# 3️⃣ Копируем проект
COPY . .


