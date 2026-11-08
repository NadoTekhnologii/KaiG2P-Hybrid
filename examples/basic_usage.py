import sys
import os

# Добавляем корневую папку проекта в пути, чтобы импортировать модуль
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kai_g2p_hybrid import hybrid_phrase

def main():
    texts = [
        "Привет, как дела?",
        "Ма́ма мы́ла ра́му, па́па чини́л сто́л.",
        "Это тест гибридного фонемизатора KaiG2P."
    ]

    print("--- Тест KaiG2P Hybrid ---")
    for text in texts:
        result = hybrid_phrase(text)
        print(f"Текст:  {text}")
        print(f"IPA:    {result}\n")

if __name__ == "__main__":
    main()
