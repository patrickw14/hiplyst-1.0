# -*- encoding: utf-8 -*-
from django.db import models

class Pages(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    time = models.DateTimeField(
        u'When',
        auto_now_add=True
    )

    slug = models.SlugField(
        u"Slug"
    )

    title = models.CharField(
        u"Title artist",
        max_length=100
    )

    description = models.TextField(
        u"Biography"
    )

    big_image = models.CharField(
        u"Picture",
        max_length=100
    )

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Page"
        verbose_name_plural = u"Pages"

    def __unicode__(self):
        return u"%s" % self.title


class Albums(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    artist = models.ForeignKey(
        Pages,
        verbose_name=u"Performer",
        related_name="artist_album"
    )

    title = models.CharField(
        u"Title artist",
        max_length=100
    )

    cover = models.CharField(
        u"Picture",
        max_length=100
    )

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Album artist"
        verbose_name_plural = u"Album artists"

    def __unicode__(self):
        return u"%s" % self.title


class Tracks(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    artist = models.ForeignKey(
        Pages,
        verbose_name=u"Performer",
        related_name="artist_track"
    )

    title = models.CharField(
        u"Title artist",
        max_length=100
    )

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Track artist"
        verbose_name_plural = u"Track artist"

    def __unicode__(self):
        return u"%s" % self.title

class Similar(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    artist = models.ForeignKey(
        Pages,
        verbose_name=u"Performer",
        related_name="artist_similar"
    )

    title = models.CharField(
        u"Title artist",
        max_length=100
    )

    cover = models.CharField(
        u"Picture",
        max_length=100
    )

    class Meta:
        get_latest_by = 'id'
        ordering = ('-id',)
        verbose_name = u"Similar artists"
        verbose_name_plural = u"Similar artists"

    def __unicode__(self):
        return u"%s" % self.title
