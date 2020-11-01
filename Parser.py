import re
import string
import logging
from lxml import etree as ET


class Parser():
    def __init__(self, file):
        self.file = file
        logging.info("Parser initialized")

    def get_book_name(self):
        book_name = []
        for event, elem1 in ET.iterparse(self.file):
            elem1.tag = elem1.tag.partition('}')[-1]
            if elem1.tag == "book-name":
                book_name.append(elem1.text)
        return book_name

    def get_number_of_paragraph(self):
        tree = ET.parse(self.file)
        number_of_paragraph = []
        num_p = []
        a = []
        for event, elem2 in ET.iterparse(self.file):
            if elem2.tag.partition('}')[-1] == "p":
                paragraphs = tree.findall('*/p')
                num_p.append(len(paragraphs))
                a.append(len(num_p))
        number_of_paragraph.append(len(a))
        return number_of_paragraph

    def get_text_without_punctuation(self):
        with open(self.file, 'r', encoding='utf8') as file:
            text = file.read()
            book_text_pattern = r"<body>(.*?)<\/body>"
            text_of_book = re.findall(book_text_pattern, text, flags=re.DOTALL)
            clean_pattern = re.compile('[^а-яА-ЯёЁ]')
            book_text = re.sub(clean_pattern, ' ', str(text_of_book))
            extra_symbols = string.punctuation.join('«»…—№\\n’' + string.digits)
            clean_text = ''.join(word for word in book_text if word not in extra_symbols)
        return clean_text

    def get_number_of_words(self):
        number_of_words = []
        words = re.findall(r'\w+', self.get_text_without_punctuation())
        number_of_words.append(len(words))
        return number_of_words

    def get_number_of_letters(self):
        number_of_letters = []
        letters = re.findall(r'\w', self.get_text_without_punctuation())
        number_of_letters.append(len(letters))
        return number_of_letters

    def get_words_in_uppercase(self):
        word_upper = 0
        for word in self.get_text_without_punctuation().split():
            if word == word.upper():
                word_upper += 1
            else:
                continue
        return word_upper

    def get_words_in_lower(self):
        word_lower = 0
        for word in self.get_text_without_punctuation().split():
            if word == word.lower():
                word_lower += 1
            else:
                continue
        return word_lower

    def get_words_stats(self):
        words_stat = {}
        for word in self.get_text_without_punctuation().split():
            if word.capitalize() not in words_stat and word == word.capitalize():
                words_stat[word.capitalize()] = [1, 1]
            elif word.capitalize() not in words_stat and word != word.capitalize():
                words_stat[word.capitalize()] = [1, 0]
            elif word.capitalize() in words_stat and word != word.capitalize():
                words_stat[word.capitalize()][0] += 1
            else:
                words_stat[word.capitalize()][0] += 1
                words_stat[word.capitalize()][1] += 1
        return words_stat