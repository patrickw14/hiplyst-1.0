# -*- encoding: utf-8 -*-
from django.db import models


class Radio(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    city = models.CharField(
        u"City",
        max_length=50
    )

    name = models.CharField(
        u"Name of radio station",
        max_length=100
    )

    code = models.CharField(
        u"Code for radio stations",
        max_length=50,
        unique=True
    )

    def for_json(self):
        return {"id": self.code, "name": self.name}

    def __unicode__(self):
        return u"Radio: %s" % self.name

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Radio"
        verbose_name_plural = u"Radios"


class RadioTracks(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    radio = models.ForeignKey(
        Radio,
        verbose_name=u"Radio",
        related_name="playlist_track"
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

    def for_json(self):
        return {"title": self.track_title, "artist": self.track_artist}

    def __unicode__(self):
        return u"Radio track: %s - %s" % (self.track_artist, self.track_title)

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Track"
        verbose_name_plural = u"Track"
