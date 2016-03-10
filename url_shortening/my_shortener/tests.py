from datetime import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Wordlist, UrlMap

# Create your tests here.
class ShortenerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ShortenerTests, cls).setUpClass()
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

    def test_home_page_opening_correctly(self):
        print '\nRunning Test Home Page Opens Correctly'
        response = self.client.get(reverse('my_shortener:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_add_new_url_with_relevant_word(self):
        print '\nRunning Test Add New Url Containing Word In Wordlist'
        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'lawsuit' in each[0]

        for each in Wordlist.objects.all():
            print each.word
            print each.is_used
            print each.created_at
            for url in each.urlmap_set.all():
                print url.url_actual

    def test_add_new_url_without_relevant_word(self):
        print '\nRunning Test Add New Url Not Containing Any Word in Wordlist'
        test_url = 'https://docs.djangoproject.com/en/1.9/topics/testing/tools/'
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'lawsuit' in each[0]

        for each in Wordlist.objects.all():
            print each.word
            print each.is_used
            print each.created_at
            for url in each.urlmap_set.all():
                print url.url_actual

    def test_add_new_url_with_word_then_add_new_url_without_relevant_word(self):
        print '\nRunning Test Add New Url Containing Word In Wordlist',
        print 'Then Add New Url Not Containing Any Word In Wordlist'
        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'lawsuit' in each[0]

        test_url = 'https://docs.djangoproject.com/en/1.9/topics/testing/tools/'
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'symbolic')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'symbolic' in each[0]

        for each in Wordlist.objects.all():
            print each.word
            print each.is_used
            print each.created_at
            for url in each.urlmap_set.all():
                print url.url_actual

    def test_add_url_and_add_same_url_again(self):
        print '\nRunning Test Add New Url Containing Word In Wordlist',
        print 'Then Add Same Url Again'
        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'lawsuit' in each[0]

        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My URL Shortening Tool')
        self.assertContains(response, 'This URL is already entered:')
        self.assertContains(response, 'my_shortener.com/lawsuit')

    def test_use_all_words_in_wordlist_then_add_new_url(self):
        print '\nRunning Test Add New Urls And Use All Words In Wordlist',
        print 'Then Add New Url'
        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')


        test_url = 'https://docs.djangoproject.com/en/1.9/topics/testing/tools/'
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'symbolic')

        test_url = 'http://django-testing-docs.readthedocs.org/en/latest/fixtures.html'
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'patient')
        self.assertEqual(Wordlist.objects.get(word='lawsuit').urlmap_set.all()[0].url_actual,"http://techcrunch.com/2012/12/28/pinterest-lawsuit/")

        test_url = 'http://stackoverflow.com/questions/979434/how-to-load-fixtures-only-once-in-django-unit-tests'
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        for each in response.redirect_chain:
            print each[0]
            self.assertEqual(each[1], 302)
            assert 'lawsuit' in each[0]

        self.assertEqual(Wordlist.objects.get(word='lawsuit').urlmap_set.all()[0].url_actual,"http://stackoverflow.com/questions/979434/how-to-load-fixtures-only-once-in-django-unit-tests")

        for each in Wordlist.objects.all():
            print each.word
            print each.is_used
            print each.created_at
            for url in each.urlmap_set.all():
                print url.url_actual

    def test_new_url_redirects(self):
        print '\nRunning Test Actual Url Redirection'
        test_url = "http://techcrunch.com/2012/12/28/pinterest-lawsuit/"
        response = self.client.post('/my_shortener.com/result/', {'url': test_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lawsuit')

        redirect_response = self.client.get('/my_shortener.com/lawsuit/')
        self.assertEqual(redirect_response.status_code, 302)