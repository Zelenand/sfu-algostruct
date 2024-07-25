def generate_ngrams(text, n):
    """Генерирует n-граммы для заданного текста"""
    # Разбиваем текст на слова
    tokens = [token for token in text.split(" ") if token != ""]
    # Генерируем n-граммы
    ngrams = []
    for i in range(len(tokens)-n+1):
        ngram = " ".join(tokens[i:i+n])
        ngrams.append(ngram)
    return ngrams

def search_word(word, text, n):
    """Ищет слово в тексте с использованием метода n-грамм"""
    # Генерируем н-граммы для слова и текста
    word_ngrams = generate_ngrams(word, n)
    text_ngrams = generate_ngrams(text, n)
    print(word_ngrams)
    print(text_ngrams)
    # Ищем слово в текстовых н-граммах
    for i in range(len(text_ngrams)):
        if word_ngrams == [text_ngrams[i]]:
            return True
    return False

# Пример использования
text = "Это пример текста, в котором мы будем искать слово."
word = "слово"
n = 3
if search_word(word, text, n):
    print("Слово найдено в тексте.")
else:
    print("Слово не найдено в тексте.")