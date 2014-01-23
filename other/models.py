# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class ListeningHistory(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=u'User',
        related_name="listening_user"
    )

    time = models.DateTimeField(
        u'When',
        auto_now_add=True
    )

    track_artist = models.CharField(
        u"Performer",
        max_length=100
    )

    track_title = models.CharField(
        u"Name",
        max_length=100
    )

    track_id = models.CharField(
        u"Track ID",
        max_length=20
    )

    def for_json(self):
        return "%s" % self.track_id

    def __unicode__(self):
        return u"User %s listened %s" % (self.user, self.track_title)

    class Meta:
        get_latest_by = 'time'
        ordering = ('-id',)
        verbose_name = u"Play history"
        verbose_name_plural = u"Play histories"

    @staticmethod
    def get_weighted_set(user):
        group_query = "select count(*) as cnt, track_artist from (select track_artist from other_listeninghistory where user_id = %s order by id desc limit 5000) as top group by track_artist order by cnt desc limit 100;" % user.id

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(group_query)

        row = cursor.fetchone()
        weighted_set = []
        if row is not None:
            max = row[0]
            while row:
                weighted_set.append((row[0] * 100 / max, row[1], row[0]))
                row = cursor.fetchone()

        return weighted_set


class SearchesHistory(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=u'User',
        related_name="savedsearch_user"
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
        return {"name": "%s" % self.query, "date": self.time.strftime("%d.%m.%Y %H:%M")}

    def __unicode__(self):
        return u"Search %s" % self.query

    class Meta:
        get_latest_by = 'time'
        ordering = ('-id',)
        verbose_name = u"Search history"
        verbose_name_plural = u"Search histories"
