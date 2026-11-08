"""
KaiG2P - английский G2P через espeak-ng (espyak).
v1.2: нормализация — убираем U+0301, пробелы, польские/чешские диакритики.
"""
import re
from espyak import G2P

VERSION = '1.2'
_g2p = G2P('en')

NORMALIZE = {
    'ʧ': 't͡ʃ',
    'ʤ': 'd͡ʒ',
    'ḱ': 'k',
    'ś': 's',
    'ŕ': 'r',
    'ź': 'z',
    'ḿ': 'm',
    ' ': '',
    '\u0301': '',
}

def normalize_ipa(ipa):
    for src, dst in NORMALIZE.items():
        ipa = ipa.replace(src, dst)
    return ipa

def phonemize_word(word):
    clean = ''.join(c for c in word.lower() if c.isalpha())
    if not clean:
        return ''
    try:
        return normalize_ipa(_g2p.phonemize(clean))
    except Exception:
        return ''

def phonemize_phrase(text):
    words = re.findall(r'[a-zA-Z]+', text)
    return [phonemize_word(w) for w in words if phonemize_word(w)]

if __name__ == '__main__':
    print(f'English G2P v{VERSION}')
    for w in ['church', 'judge', 'hello', 'world', 'nature', 'question', 'kraków', 'škoda']:
        print(f'  {w:12} -> {phonemize_word(w)}')
