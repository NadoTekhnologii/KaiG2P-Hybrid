import re
import subprocess
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from multi_g2p import phonemize_word

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tokens_multi_ipa_v17.txt')
with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    VALID_TOKENS = set(line.strip().split()[0] for line in f if line.strip())

NORMALIZE_MAP = {
    'ɑ': 'a',
    'ɭ': 'ɫ',
    'tʃʲ': 'tɕ',
    't͡ɕ': 'tɕ', 
    't͜ɕ': 'tɕ',
    'y': 'ɨ',
    'ʑ': 'ɕ',
    '«': '"',
    '»': '"',
    ' ': '',
    '\n': ''
}

def espeak_phonemize(word):
    word = word.replace('-', ' ')
    cmd = ['/opt/espeak-ng-russian-fix/bin/espeak-ng', '-v', 'ru', '-q', '--ipa', word]
    result = subprocess.run(cmd, capture_output=True, text=True)
    ipa = result.stdout.strip()
    
    ipa = re.sub(r'\((en|ru|de|fr)\)', '', ipa)
    
    for old, new in NORMALIZE_MAP.items():
        ipa = ipa.replace(old, new)
        
    allowed = VALID_TOKENS.union({'ˈ', 'ʲ', 'ː', ' '})
    ipa = ''.join(c for c in ipa if c in allowed)
    
    return ipa.strip()

def is_valid_ipa(ipa_str):
    for char in ipa_str:
        if char not in VALID_TOKENS and char not in ['ˈ', 'ʲ', 'ː', ' ']:
            return False
    return True

def hybrid_word(word):
    clean_word = re.sub(r'[^\w\u0301-]', '', word)
    if not clean_word:
        return ''
    try:
        res = phonemize_word(clean_word)
        if res:
            # ФИКС: применяем нормализацию и к KaiG2P тоже!
            for old, new in NORMALIZE_MAP.items():
                res = res.replace(old, new)
            if is_valid_ipa(res):
                return res
    except Exception:
        pass
    return espeak_phonemize(clean_word)

def hybrid_phrase(text):
    text = text.replace('«', '"').replace('»', '"')
    text = re.sub(r'[^\w\u0301\s\.,?!—…:;"-]', ' ', text)
    
    tokens = re.findall(r'[\w\u0301-]+|[^\w\s]', text)
    result = []
    for t in tokens:
        if re.match(r'[\w\u0301-]+', t):
            result.append(hybrid_word(t))
        else:
            result.append(t)
    return ' '.join(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_text = ' '.join(sys.argv[1:])
        print(hybrid_phrase(test_text))
    else:
        print("Введите текст для проверки.")
