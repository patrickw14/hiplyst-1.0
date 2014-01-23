# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Searches(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=u'User',
        related_name="saved_search_user"
    )

    time = models.DateTimeField(
        u'When',
        auto_now_add=True
    )

    query = models.CharField(
        u"Inquiry",
        max_length=200
    )

    def for_json(self):
        return {"_id": self.id, "name": self.query, "date": self.time.strftime("%d.%m.%Y %H:%M")}

    def __unicode__(self):
        return u"Search %s" % self.query

    class Meta:
        get_latest_by = 'time'
        ordering = ('-id',)
        verbose_name = u"Saved search"
        verbose_name_plural = u"Saved searches"
