from django.db import models


class Entry(models.Model):
    id = models.AutoField(primary_key=True)

    month = models.ForeignKey('app.Month', db_column='month_id', related_name='entries', on_delete=models.CASCADE)
    hn_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True)
    date = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'entry'
