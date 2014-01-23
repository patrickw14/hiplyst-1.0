# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    vk_name = models.CharField(
        u"VK name",
        max_length=100
    )


class AccessTokens(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    token = models.CharField(
        u"Token",
        max_length=100
    )

    user_id = models.CharField(
        u"VK user ID",
        max_length=20,
        blank=True
    )

    time = models.DateTimeField(
        u"Added",
        auto_now_add=True
    )

    last_access_time = models.DateTimeField(
        u"Last access",
        auto_now=True
    )

    bad_times = models.PositiveIntegerField(
        u"Number of failures",
        default=0
    )

    class Meta:
        get_latest_by = 'last_access_time'
        ordering = ('-id',)
        verbose_name = u"Token"
        verbose_name_plural = u"Tokens"

    def __unicode__(self):
        return u"%s" % self.token

    @staticmethod
    def get_random_token():
        try:
            token = AccessTokens.objects.order_by('last_access_time')[0]
            token.last_access_time = datetime.now()
            token.save()
            return token.token
        except:
            return ""
