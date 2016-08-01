import os
import sys

from char_translator import Translator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


class FileHandler(object):
    xr = Translator()

    def __init__(self, abs_file_path=''):
        self.fpath = abs_file_path

    def append_binary(self, ascii_text):
        if isinstance(ascii_text, str):
            binary = self.xr.ascii_to_binary(ascii_text)
        if isinstance(ascii_text, (list, tuple)):
            binary = self.xr.ascii_list_to_binary(ascii_text)
        with open(self.fpath, 'ab') as fh:
            fh.write(binary)

    def write(self, text):
        with open(self.fpath, 'rw') as wb:
            wb.write(text)

    def read(self):
        with open(self.fpath, 'rb') as rb:
            line = rb.readline()
            print line


if __name__ == '__main__':
    abs_fpath = os.path.join(DATA_DIR, 'test_fh.tbl')
    datax = [
            '1, sita, ram',
            '2, radhe, sam'
            ]

    fh = FileHandler(abs_file_path=abs_fpath)
    fh.append_binary(ascii_text=datax)
