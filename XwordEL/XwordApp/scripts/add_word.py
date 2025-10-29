from XwordApp.models import common_word
from time import sleep
import os

def run():
    file_folder  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = file_folder + '/scripts/1000-most-common-words.txt'
    file_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), file_name)

    #clear the table (flush the table)
    common_word.objects.all().delete()

    with open(file_path, 'r') as f:
        for line in f:

            word = line.strip()
            common_word.objects.create(word=word)
            print(word)
    