# KaiG2P Hybrid (v1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Tests](https://img.shields.io/badge/Tests-0%25_errors-brightgreen)]()

**KaiG2P Hybrid** — это каскадный (гибридный) фонемизатор для русского языка, разработанный для проекта KaiLuxTTS. 

Он объединяет в себе два движка:
1. **KaiG2P (основной):** Словарный G2P с точностью 99.9%, использующий акуты (знак ударения ´) как источник истины.
2. **eSpeak-ng (fallback):** Правиловый движок, модифицированный для поддержки акутов, который подхватывает незнакомые слова (неологизмы, аббревиатуры, редкие имена).

**Гарантия качества:** На выборке из 10 000 случайных фраз (42 560 слов) гибрид показал **0% критических ошибок**. 99.45% слов обрабатываются словарем KaiG2P, 0.55% — уходят в eSpeak.

## 📂 Структура проекта
* `kai_g2p_hybrid.py` — главный модуль (каскадный G2P).
* `examples/basic_usage.py` — пример использования.
* `tokens_multi_ipa_v17.txt` — словарь валидных IPA-токенов (63 токена). Используется для фильтрации вывода.
* `ru_g2p_ipa.tsv`, `ru_g2p_exceptions.tsv` — словари русского языка.

## ⚠️ Требования и Установка
1. Установите Python-зависимости:
```bash
pip install -r requirements.txt
```
2. Для работы fallback-механизма требуется **кастомная сборка eSpeak-ng**, которая понимает комбинирующий акут (U+0301). Стандартный `espeak-ng` из репозиториев Ubuntu **не подойдет**.

### Сборка кастомного eSpeak-ng (WSL/Linux)
```bash
sudo apt update
sudo apt install -y git cmake gcc g++ libpcaudio-dev libsonic-dev
git clone https://github.com/kirill-jjj/espeak-ng-russian-fix.git
cd espeak-ng-russian-fix
cmake -Bbuild -DCMAKE_INSTALL_PREFIX=/opt/espeak-ng-russian-fix
cmake --build build -j$(nproc)
sudo cmake --install build
cd dictsource
sudo /opt/espeak-ng-russian-fix/bin/espeak-ng --compile=ru --path=/opt/espeak-ng-russian-fix/share/espeak-ng-data/
```
*(Примечание: скрипт `kai_g2p_hybrid.py` ожидает, что eSpeak установлен именно по пути `/opt/espeak-ng-russian-fix/bin/espeak-ng`).*

## 🚀 Использование
```python
from kai_g2p_hybrid import hybrid_phrase

text = "Ма́ма мы́ла ра́му, па́па чини́л сто́л."
ipa = hybrid_phrase(text)
print(ipa) 
# Вывод: mˈamə mˈɨla rˈamʊ , pˈapə tɕɪnʲˈiɫ stˈol .
```

## ⚠️ Ограничения (Limitations)
* **Омографы без акутов:** KaiG2P Hybrid не разрешает контекстные омографы (например, `за́мок` vs `замо́к`) без явной разметки акутами. Если в тексте нет знаков ударения, слово будет обработано по умолчанию или отправлено в eSpeak.
* **Кастомный eSpeak:** Без специально собранного eSpeak-ng (см. выше) fallback-механизм не будет корректно обрабатывать ударения.

## 🔗 Ссылки и Поддержка
Проект развивается на энтузиазме. Если вы хотите поддержать разработку (это помогает оплачивать электричество для обучения нейросетей):
* **Boosty (донаты):** https://boosty.to/nadotechnologies
* **Группа ВК:** https://vk.ru/club213675354

## 📄 Лицензия и Цитирование
MIT / Apache 2.0 (в зависимости от компонентов eSpeak). 
Оригинальный код KaiG2P написан Михаилом (NadoTechnologies).

Если вы используете этот инструмент в научной работе, пожалуйста, ссылайтесь на репозиторий:
```bibtex
@misc{kaiG2P2026,
  author = {NadoTechnologies, Mikhail},
  title = {KaiG2P Hybrid: Cascading Phonemizer for Russian},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\\\\url{https://github.com/NadoTekhnologii/KaiG2P-Hybrid}}
}
```