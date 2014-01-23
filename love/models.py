# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Love(models.Model):
    id = models.AutoField(
        '#',
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=u'User',
        related_name="love_user"
    )

    time = models.DateTimeField(
        u'When',
        auto_now_add=True
    )

    track_id = models.CharField(
        u"Track ID",
        max_length=20
    )

    track_position = models.PositiveIntegerField(
        u"Position in the playlist",
        default=0,
    )

    def for_json(self):
        return "%s" % self.track_id

    class Meta:
        get_latest_by = 'time'
        ordering = ('-id',)
        verbose_name = u"Favorite"
        verbose_name_plural = u"Favorites"

    def __unicode__(self):
        return u"%s Loves %s" % (self.user, self.track_id)

    def save_without_recount(self, *args, **kwargs):
        super(Love, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.track_position = Love.objects.filter(user=self.user).count()
        super(Love, self).save(*args, **kwargs)
