import re

def open_file(file_path):
    """Открывает текстовый файл и возвращает его содержимое."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")
        return None

def find_char_at_start(text, char):
    """Ищет строки, начинающиеся с указанного символа."""
    pattern = rf'^{char}'
    return re.findall(pattern, text, re.MULTILINE)

def find_char_at_end(text, char):
    """Ищет строки, заканчивающиеся указанным символом."""
    pattern = rf'{char}$'
    return re.findall(pattern, text, re.MULTILINE)

def find_group_at_start(text, group):
    """Ищет строки, начинающиеся с указанной группы символов."""
    pattern = rf'^{group}'
    return re.findall(pattern, text, re.MULTILINE)

def find_group_at_end(text, group):
    """Ищет строки, заканчивающиеся указанной группой символов."""
    pattern = rf'{group}$'
    return re.findall(pattern, text, re.MULTILINE)

def find_char_in_text(text, char):
    """Ищет строки, содержащие указанный символ."""
    pattern = rf'{char}'
    return re.findall(pattern, text)

def find_group_in_text(text, group):
    """Ищет строки, содержащие указанную группу символов."""
    pattern = rf'{group}'
    return re.findall(pattern, text)

def find_two_or_more_char(text, char):
    """Ищет вхождения одного символа два и более раза подряд."""
    pattern = rf'{char}{{2,}}'
    return re.findall(pattern, text)

def find_two_or_more_group(text, group):
    """Ищет вхождения группы символов два и более раза подряд."""
    pattern = rf'(?:{group}){{2,}}'
    return re.findall(pattern, text)

def find_exactly_two_char(text, char):
    """Ищет ровно два вхождения одного символа подряд."""
    pattern = rf'{char}{{2}}'
    return re.findall(pattern, text)

def find_exactly_two_group(text, group):
    """Ищет ровно два вхождения группы символов подряд."""
    pattern = rf'(?:{group}){{2}}'
    return re.findall(pattern, text)

def find_m_to_n_repeats(text, pattern, m, n):
    """Ищет от m до n повторений заданного символа или группы символов."""
    repeat_pattern = rf'(?:{pattern}){{{m},{n}}}'
    return re.findall(repeat_pattern, text)

def find_whole_word(text, word):
    """Ищет отдельное слово, учитывая границы слова."""
    pattern = rf'\b{word}\b'
    return re.findall(pattern, text)

def find_multiple_words_in_line(text, words):
    """Ищет несколько слов в одной строке одновременно, учитывая их границы."""
    words_pattern = r'\b' + r'\b.*\b'.join(words) + r'\b'
    return [line for line in text.splitlines() if re.search(words_pattern, line)]

def find_exactly_n_occurrences_of_word(text, word, n):
    """Ищет строки, содержащие ровно n вхождений указанного слова."""
    pattern = rf'(?=(\b{word}\b))'
    return [line for line in text.splitlines() if len(re.findall(pattern, line)) == n]

def find_exactly_n_occurrences_of_words(text, words, n):
    """Ищет строки, содержащие ровно n вхождений каждого из указанных слов."""
    results = []
    for line in text.splitlines():
        if all(len(re.findall(rf'(?=(\b{w}\b))', line)) == n for w in words):
            results.append(line)
    return results

def find_ip_addresses(text):
    """Ищет IP-адреса в формате IPv4."""
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    return re.findall(pattern, text)

def find_email_addresses(text):
    """Ищет email-адреса в тексте."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def find_dates(text):
    """Ищет даты в формате ДД/ММ/ГГГГ или ДД-ММ-ГГГГ."""
    pattern = r'\b(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b'
    return re.findall(pattern, text)

def find_phone_numbers(text):
    """Ищет номера телефонов в различных общих форматах."""
    pattern = r'\b(?:\+?\d{1,3}[ -]?)?(?:\(?\d{1,4}\)?[ -]?)?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,9}\b'
    return re.findall(pattern, text)

# Пример использования
if __name__ == "__main__":
    file_path = 'wiki.txt' # Укажите путь к вашему файлу
    content = open_file(file_path)

    if content:
        # Примеры использования всех функций
        print("Начинается с 'a':", find_char_at_start(content, 'a'))
        print("Заканчивается на 'z':", find_char_at_end(content, 'z'))
        print("Начинается с 'Hello':", find_group_at_start(content, 'Hello'))
        print("Заканчивается на 'World':", find_group_at_end(content, 'World'))
        print("Содержит 'x':", find_char_in_text(content, 'x'))
        print("Содержит 'group':", find_group_in_text(content, 'group'))
        print("Два и более 'o':", find_two_or_more_char(content, 'o'))
        print("Два и более 'test':", find_two_or_more_group(content, 'test'))
        print("Ровно два 'n':", find_exactly_two_char(content, 'n'))
        print("Ровно два 'repeat':", find_exactly_two_group(content, 'repeat'))

        # Пример использования новой функции поиска от m до n повторений
        print("От 2 до 4 'l':", find_m_to_n_repeats(content, 'l', 2, 4))
        print("От 3 до 5 'abc':", find_m_to_n_repeats(content, 'abc', 3, 5))

        # Пример использования поиска слова и нескольких слов
        print("Слово 'example':", find_whole_word(content, 'example'))
        print("Слова 'first' и 'second' в строке:", find_multiple_words_in_line(content, ['first', 'second']))

        # Пример использования поиска n вхождений слова и слов
        print("Ровно 3 вхождения 'apple':", find_exactly_n_occurrences_of_word(content, 'apple', 3))
        print("Ровно 2 вхождения 'banana' и 'orange' в строке:", find_exactly_n_occurrences_of_words(content, ['banana', 'orange'], 2))

        # Пример использования поиска IP-адресов, email-адресов, дат и номеров телефонов
        print("IP-адреса:", find_ip_addresses(content))
        print("Email-адреса:", find_email_addresses(content))
        print("Даты:", find_dates(content))
        print("Номера телефонов:", find_phone_numbers(content))
