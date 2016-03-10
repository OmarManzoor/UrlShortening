__author__ = 'Omar Salman'

## this is just a shell script to load all the words from the wordlist into the database
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_shortening.settings")
django.setup()

from my_shortener.models import Wordlist

fin = open('test_words.txt')

words_list = []
for line in fin:
    line = line.rstrip()
    line = line.lower()
    line = ''.join(character for character in line if character.isalnum())
    db_word = Wordlist(word=line, is_used=False)
    words_list.append(db_word)

Wordlist.objects.bulk_create(words_list)

fin.close()

