import os
from string import Template


class SQLProvider:
    def __init__(self, file_path: str) -> None:
    #путь до папки со sql-скрпитами
        self._scripts = {}

        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, name_of_file, **kwargs):
    #name_of_file - имя того файла, который хотим передать; **kwargs для прокидывания аргументов в .sql
        return self._scripts[name_of_file].substitute(**kwargs)