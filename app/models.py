from django.db import models


class Month(models.Model):
    id = models.IntegerField(
        primary_key=True
    )  # AutoField?
    hn_id = models.IntegerField(
        blank=True,
        null=True
    )
    name = models.TextField(
        blank=True
    )

    class Meta:
        db_table = 'month'


class Entry(models.Model):
    id = models.IntegerField(
        primary_key=True
    )  # AutoField?
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


