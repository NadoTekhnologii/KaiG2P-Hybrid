FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для сборки eSpeak и Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip git cmake gcc g++ libpcaudio-dev libsonic-dev \
    && rm -rf /var/lib/apt/lists/*

# Собираем кастомный eSpeak-ng (с поддержкой акутов)
RUN git clone https://github.com/kirill-jjj/espeak-ng-russian-fix.git /tmp/espeak-ng-russian-fix && \
    cd /tmp/espeak-ng-russian-fix && \
    cmake -Bbuild -DCMAKE_INSTALL_PREFIX=/opt/espeak-ng-russian-fix && \
    cmake --build build -j$(nproc) && \
    cmake --install build && \
    cd dictsource && \
    /opt/espeak-ng-russian-fix/bin/espeak-ng --compile=ru --path=/opt/espeak-ng-russian-fix/share/espeak-ng-data/ && \
    rm -rf /tmp/espeak-ng-russian-fix

WORKDIR /app

# Копируем проект и устанавливаем Python-зависимости
COPY . /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# По умолчанию запускаем пример
CMD ["python3", "examples/basic_usage.py"]
