import re
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import  View, TemplateView
from .models import Wordlist, UrlMap

# Create your views here.
class Home(TemplateView):
    template_name = 'my_shortener/home.html'

class ResultRedirect(View):
    template_name = 'my_shortener/result.html'

    def get(self, request, short_word):
        word_url_object = Wordlist.objects.get(word=short_word)
        map_object = word_url_object.urlmap_set.all()[0]
        actual_url = map_object.url_actual
        context = {'org_url' : actual_url,
                'new_url' : 'localhost:8000/my_shortener.com/' + short_word + '/',
        }

        return render(request, self.template_name, context)

# def result_redirect(request, short_word):
#     word_url_object = Wordlist.objects.get(word=short_word)
#     map_object = word_url_object.urlmap_set.all()[0]
#     actual_url = map_object.url_actual
#     context = {'org_url' : actual_url,
#                 'new_url' : 'my_shortener.com/' + short_word + '/',
#     }
#
#     return render(request, 'my_shortener/result.html', context)

class Result(View):

    def post(self, request):
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
            if list_unused_words:
                url_word = list_unused_words[0]
            else:
                url_word = Wordlist.objects.all().order_by('created_at')[0]
                url_word.created_at = datetime.now()
                url_word.urlmap_set.clear()

        url_word.is_used = True
        url_word.urlmap_set.create(url_actual=org_url)
        url_word.save()

        return HttpResponseRedirect(reverse('my_shortener:result_redirect', args=(url_word.word,)))

# def result(request):
#     org_url = request.POST['url']
#
#     try:
#         a = UrlMap.objects.filter(url_actual=org_url)
#         if a:
#             print 'Already exists redirect'
#             return render(request, 'my_shortener/home.html', { 'error_message': 'my_shortener.com/' + a[0].word.word })
#     except:
#         print 'Url okay to go'
#
#     words = re.findall('\w+', org_url)
#     url_word = None
#     for each in words:
#         try:
#             db_word = Wordlist.objects.get(word=each, is_used=False)
#             url_word = db_word
#             break
#         except:
#             print "No such word found"
#             url_word = None
#
#     if not url_word:
#         list_unused_words = Wordlist.objects.filter(is_used=False)
#         if list_unused_words:
#             url_word = list_unused_words[0]
#         else:
#             first_word_record = Wordlist.objects.all()[0]
#             first_word_record.delete()
#             db_word = Wordlist(word=first_word_record.word)
#             db_word.save()
#             url_word = Wordlist.objects.get(word=db_word.word)
#
#     url_word.is_used = True
#     url_word.urlmap_set.create(url_actual=org_url)
#     url_word.save()
#
#     return HttpResponseRedirect(reverse('my_shortener:result_redirect', args=(url_word.word,)))


class Actual(View):

    def get(self, request, short_word):
        word_url_object = Wordlist.objects.get(word=short_word)
        map_object = word_url_object.urlmap_set.all()[0]
        actual_url = map_object.url_actual
        return redirect(actual_url)

# def actual(request, short_word):
#     word_url_object = Wordlist.objects.get(word=short_word)
#     map_object = word_url_object.urlmap_set.all()[0]
#     actual_url = map_object.url_actual
#     return redirect(actual_url)