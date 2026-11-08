r"""
KaiG2P v1.1 - гибридный G2P для русского языка.
Часть проекта KaiLuxTTS.

Изменение v1.1: при конфликте cstr и акута - идём в Epitran.
Это чинит автоматически 1723 слова, где cstr противоречит нашей разметке.

Три источника (в порядке приоритета):
1. Словарь исключений (топ-50 частых слов)
2. cstr/g2p-dicts - если ударение совпадает с акутом
3. Epitran fallback - при конфликте или отсутствии в cstr

Автор: Кай (совместно с Михаилом). Проект: K:\LuxTTS
"""
import re
from pathlib import Path
import epitran

VERSION = '1.1'

_HERE = Path(__file__).resolve().parent
EXCEPTIONS = _HERE / 'ru_g2p_exceptions.tsv'
DICT_TSV = _HERE / 'ru_g2p_ipa.tsv'

ACUTE_NFC = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ý': 'y',
}
COMBINING_ACUTE = '\u0301'

VOWELS_RU = 'аеёиоуыэюяАЕЁИОУЫЭЮЯ'
VOWELS_IPA = set('aeiouyɨɪʊʌəɐɛɔɵʉæɑɒ')

def acute_to_stress(ipa):
    out = []
    i = 0
    while i < len(ipa):
        ch = ipa[i]
        if i + 1 < len(ipa) and ipa[i+1] == COMBINING_ACUTE:
            out.append('ˈ' + ch)
            i += 2
            continue
        if ch in ACUTE_NFC:
            out.append('ˈ' + ACUTE_NFC[ch])
            i += 1
            continue
        out.append(ch)
        i += 1
    return ''.join(out)

def stress_pos_accent(word):
    """Номер ударной гласной в русском слове с акутом (1-based)."""
    count = 0
    for i, ch in enumerate(word):
        if ch in VOWELS_RU:
            count += 1
            if i + 1 < len(word) and word[i+1] == COMBINING_ACUTE:
                return count
    return -1

def stress_pos_ipa(ipa):
    """Номер ударной гласной в IPA (1-based)."""
    pos = ipa.find('ˈ')
    if pos == -1:
        return -1
    count = 0
    for ch in ipa[:pos]:
        if ch in VOWELS_IPA:
            count += 1
    for ch in ipa[pos:]:
        if ch in VOWELS_IPA:
            count += 1
            return count
    return -1

# Загрузка словарей
exc_vocab = {}
with open(EXCEPTIONS, encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) == 2:
            exc_vocab[parts[0]] = parts[1]

dict_vocab = {}
with open(DICT_TSV, encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) == 2:
            ipa = parts[1].strip('/')
            if 'ˈ' in ipa:
                dict_vocab[parts[0]] = ipa

epi = epitran.Epitran('rus-Cyrl')

def phonemize_word(word):
    w_clean = word.lower().replace(COMBINING_ACUTE, '')
    w_accent = word.lower()
    
    # 1. Исключения — но только если позиция ударения совпадает
    if w_clean in exc_vocab:
        pos_acc = stress_pos_accent(word)
        pos_exc = stress_pos_ipa(exc_vocab[w_clean])
        if pos_acc == -1 or pos_exc == -1 or pos_acc == pos_exc:
            return exc_vocab[w_clean]
        # не совпадает — идём дальше (cstr / Epitran)
    
    # 2. cstr — но только если ударение совпадает с акутом
    if w_clean in dict_vocab:
        pos_acc = stress_pos_accent(word)
        pos_cstr = stress_pos_ipa(dict_vocab[w_clean])
        if pos_acc == -1 or pos_cstr == -1 or pos_acc == pos_cstr:
            return dict_vocab[w_clean]
        # Конфликт — идём в Epitran
    
    # 3. Epitran fallback
    try:
        raw = epi.transliterate(w_accent)
        return acute_to_stress(raw)
    except Exception:
        return ''

def phonemize_phrase(text):
    words = re.findall(r'[а-яёА-ЯЁ\u0301]+', text)
    result = []
    for w in words:
        ipa = phonemize_word(w)
        if ipa:
            result.append(ipa)
    return result

def stats():
    return {
        'version': VERSION,
        'exceptions': len(exc_vocab),
        'dict_with_stress': len(dict_vocab),
    }

if __name__ == '__main__':
    print(f'KaiG2P v{VERSION}')
    print(f'Исключений: {len(exc_vocab)}')
    print(f'Словарь (с ударением): {len(dict_vocab)}')
    print()
    tests = [
        'Шо́йгу а́лгоритм люде́й включа́я',
        'молоко́ воро́на звони́т краси́вее догово́р',
    ]
    for t in tests:
        print(t)
        print(f'  -> {phonemize_phrase(t)}')
        print()
