# -*- coding: utf-8 -*-
import os.path
import re
from googletrans import Translator
from glob import glob

translator = Translator() # service_urls=['translate.google.ru']
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def translate_folders(source: str, dest: str):
    file_list = glob(source + "/*.srt")
    for file_name in file_list:
        try:
            with open(file_name, "r", encoding="utf-8", errors='replace') as src:
                dest_name = file_name.replace(source, dest)
                if os.path.isfile(dest_name):
                    print(f'Skipping {dest_name} - already exists')
                    continue
                with open(dest_name, "w") as dst:
                    print(f"{file_name} --> {dest_name}")
                    while line := src.readline():
                        # assuming we translate short videos where 00: is always in timecode
                        if isinstance(line, str) and (line.strip().isdecimal() or '00:' in line):
                            dst.write(line)
                        elif line.strip() == "":
                            dst.write(line)
                            dst.write('\n')
                        else:
                            translation = translator.translate(line.strip(), dest='en', src='ru')
                            dst.write(re.sub(r'[^a-zA-Z0-9 \n\.А-Яа-я]',
                                                                      '', translation.text))
        except Exception as ex:
            print(ex)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    translate_folders('rus_sources', 'eng_auto')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
