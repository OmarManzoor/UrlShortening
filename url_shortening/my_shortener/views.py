import re
import random
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf.urls import url
from .models import Wordlist, UrlMap
from .urls import *

# Create your views here.
def home(request):
    return render(request, 'my_shortener/home.html')

def result_redirect(request, short_word):
    word_url_object = Wordlist.objects.get(word=short_word)
    map_object = word_url_object.urlmap_set.all()[0]
    actual_url = map_object.url_actual
    context = {'org_url' : actual_url,
                'new_url' : 'my_shortener.com/' + short_word + '/',
    }

    return render(request, 'my_shortener/result.html', context)

def result(request):
    org_url = request.POST['url']

    try:
        a = UrlMap.objects.filter(url_actual=org_url)
        if a:
            print 'Already exists redirect'
            return render(request, 'my_shortener/home.html', { 'error_message': 'my_shortener.com/' + a[0].word.word })
    except:
        print 'Url okay to go'

    words = re.findall('\w+', org_url)
    url_word = None
    for each in words:
        try:
            db_word = Wordlist.objects.get(word=each, is_used=False)
            url_word = db_word
            break
        except:
            print "No such word found"
            url_word = None

    if not url_word:
        list_unused_words = Wordlist.objects.filter(is_used=False)
        random_index = random.randint(0,len(list_unused_words))
        url_word = list_unused_words[random_index]

    new_url = url(r'^/' + url_word.word + '/$', org_url, name=url_word.word)
    url_word.is_used = True
    url_word.urlmap_set.create(url_actual=org_url)
    url_word.save()

    return HttpResponseRedirect(reverse('my_shortener:result_redirect', args=(url_word.word,)))

def actual(request, short_word):
    word_url_object = Wordlist.objects.get(word=short_word)
    map_object = word_url_object.urlmap_set.all()[0]
    actual_url = map_object.url_actual
    return redirect(actual_url)