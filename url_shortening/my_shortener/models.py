from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Wordlist(models.Model):
    word = models.CharField(max_length=50, default="")
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UrlMap(models.Model):
    word = models.ForeignKey(Wordlist, blank=True, null=True)
    url_actual = models.URLField(default="")