import idlelib.run
import math
import os
from collections import Counter

from Lesta import settings


class FileService:

    @staticmethod
    def get_wordlist_from_file(filepath):
        """Возвращает список слов, содержащихся в файле. За исключением чисел"""
        wordlist = list()
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read().split()
            for word in text:
                word = word.strip(',.!?:()+-').lower()  # Очищаем слова от лишних символов
                if word.isdigit() or word == '':
                    continue
                wordlist.append(word)
        return wordlist


    @staticmethod
    def get_td_and_idf(filepath):
        """
        Функция вычисляет tf и idf для каждого слова и возвращает в виде словаря с ключом 'info',
        и значением в виде списка кортежей (слово, значение tf, значение idf).
        Список ограничен 50 словами, отсортированных по убыванию значения idf.
        :param filepath: path
        :return: dict {'info': (word, tf, idf)}
        """
        # получаем список слов, содержащийся в файле
        word_list = FileService.get_wordlist_from_file(filepath)
        # подсчитываем количество повторений слов в файле
        tf = dict(Counter(word_list))
        # получаем список имеющихся файлов
        files_root = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'files')
        file_list = [
            os.path.join(files_root, f)
            for f in os.listdir(files_root)
            if os.path.isfile(os.path.join(files_root, f))
        ]
        # получаем количество файлов, содержащих слова из загружаемого файла (загружаемый файл тоже учитывается)
        file_list.remove(filepath)
        containing_files = {word: 1 for word in tf.keys()}
        for archive_file in file_list:
            for list_word in containing_files.keys():
                if list_word in FileService.get_wordlist_from_file(archive_file):
                    containing_files[list_word] = containing_files[list_word] + 1
        # вычисляем idf для каждого слова
        idf = {word: math.log((len(file_list)+1)/containing_files[word]) for word in containing_files.keys()}
        # формируем список кортежей (слово, tf, idf)
        info = [(word, tf[word], idf[word]) for word in idf.keys()]
        # сортируем список по убыванию idf
        info.sort(key=lambda el: -idf[el[0]])
        # ограничиваем вывод до 50 слов
        data = {'info': info[0:50]}
        return data

