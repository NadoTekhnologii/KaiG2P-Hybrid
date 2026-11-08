import sys
from pathlib import Path

# Добавляем текущую папку в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from multi_g2p import phonemize_phrase

def run_tests():
    tests = [
        "Молоко́, во́рона, звони́т, краси́вее, догово́р.",
        "ТВ и США.",
        "Hello, world!",
        "Привет, hello — как дела?",
        "»d́Пентервильское привиде́ние»", # Проверка очистки от артефактов
    ]
    print("=== ТЕСТЫ KaiG2P ===")
    for t in tests:
        print(f"Текст: {t}")
        print(f"IPA:   {phonemize_phrase(t)}\n")

if __name__ == '__main__':
    run_tests()
