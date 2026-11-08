"""
KaiG2P - мультиязычный роутер (RU + EN + пунктуация + нормализация IPA).
v1.3: пост-нормализация IPA — убираем диакритики, акуты, пробелы из выхода.
"""
import re
from kai_g2p import phonemize_word as ru_phonemize
from en_g2p import phonemize_word as en_phonemize

VERSION = '1.3'

WORD_RE = re.compile(r'[а-яёА-ЯЁ\u0301]+|[a-zA-Z]+|[.,?!—…:;"]+')
PUNCT = set('.,?!—…:;"')
STRIP_CHARS = set('()[]{}*')

REPLACEMENTS = {
    '%': ' проце́нт ',
    '№': ' но́мер ',
    '&': ' и ',
}

# Нормализация IPA после G2P (убираем всё, чего нет в 63-токенном словаре)
IPA_NORMALIZE = {
    'ḱ': 'k', 'ś': 's', 'ŕ': 'r', 'ź': 'z', 'ḿ': 'm', 'ṕ': 'p',
    '\u0301': '',   # combining acute
    '\u0306': '',   # combining breve
    ' ': '',        # пробелы внутри IPA
    'ʧ': 't͡ʃ', 'ʤ': 'd͡ʒ',
}

def normalize_ipa(ipa):
    for src, dst in IPA_NORMALIZE.items():
        ipa = ipa.replace(src, dst)
    return ipa

def normalize_text(text):
    for ch, repl in REPLACEMENTS.items():
        text = text.replace(ch, repl)
    text = ''.join(c for c in text if c not in STRIP_CHARS)
    return re.sub(r' +', ' ', text).strip()

def phonemize_word(word):
    if re.search(r'[а-яёА-ЯЁ]', word):
        return normalize_ipa(ru_phonemize(word))
    if re.search(r'[a-zA-Z]', word):
        return normalize_ipa(en_phonemize(word))
    return ''

def phonemize_phrase(text):
    text = normalize_text(text)
    tokens = WORD_RE.findall(text)
    result = []
    for t in tokens:
        if t and all(c in PUNCT for c in t):
            for c in t:
                result.append(c)
        else:
            ipa = phonemize_word(t)
            if ipa:
                result.append(ipa)
    return result

def phonemize_text_flat(text):
    return ' '.join(phonemize_phrase(text))

if __name__ == '__main__':
    tests = ['Привет, я Кай.', 'ТВ и США.', 'Hello, world!',
             '»d́Пентервильское привиде́ние»', 'church and judge']
    for t in tests:
        print(f'{t}')
        print(f'  -> {phonemize_phrase(t)}')
        print()
