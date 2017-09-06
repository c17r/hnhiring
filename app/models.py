from django.db import models


class Month(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    hn_id = models.IntegerField(
        blank=True,
        null=True
    )
    name = models.TextField(
        blank=True
    )

    class Meta:
        db_table = 'month'

    def __str__(self):
        return self.name


class Entry(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    month = models.ForeignKey(
        Month,
        db_column="month_id",
        related_name="entries"
    )
    hn_id = models.IntegerField(
        blank=True,
        null=True
    )
    content = models.TextField(
        blank=True
    )
    date = models.DateTimeField(
        blank=True
    )

    class Meta:
        db_table = 'entry'
