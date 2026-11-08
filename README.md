# KaiG2P Hybrid (v1.0)

**KaiG2P Hybrid** — это каскадный (гибридный) фонемизатор для русского языка, разработанный для проекта KaiLuxTTS. 

Он объединяет в себе два движка:
1. **KaiG2P (основной):** Словарный G2P с точностью 99.9%, использующий акуты (знак ударения ´) как источник истины.
2. **eSpeak-ng (fallback):** Правиловый движок, модифицированный для поддержки акутов, который подхватывает незнакомые слова (неологизмы, аббревиатуры, редкие имена).

**Гарантия качества:** На выборке из 10 000 случайных фраз (42 560 слов) гибрид показал **0% критических ошибок**. 99.45% слов обрабатываются словарем KaiG2P, 0.55% — уходят в eSpeak.

## 📂 Структура проекта
* `kai_g2p_hybrid.py` — главный модуль (каскадный G2P).
* `kai_g2p.py`, `multi_g2p.py`, `en_g2p.py` — базовые скрипты KaiG2P.
* `tokens_multi_ipa_v17.txt` — словарь валидных IPA-токенов (63 токена).
* `ru_g2p_ipa.tsv`, `ru_g2p_exceptions.tsv` — словари русского языка.

## ⚠️ Требования
Для работы fallback-механизма требуется **кастомная сборка eSpeak-ng**, которая понимает комбинирующий акут (U+0301). Стандартный `espeak-ng` из репозиториев Ubuntu **не подойдет**, так как он игнорирует акуты.

### Установка кастомного eSpeak-ng (WSL/Linux)
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

## 🔗 Ссылки и Поддержка
Проект развивается на энтузиазме. Если вы хотите поддержать разработку (это помогает оплачивать электричество для обучения нейросетей):
* **Boosty (донаты):** https://boosty.to/nadotechnologies
* **Группа ВК:** https://vk.ru/club213675354

## 📄 Лицензия
MIT / Apache 2.0 (в зависимости от компонентов eSpeak). 
Оригинальный код KaiG2P написан Михаилом (NadoTechnologies).