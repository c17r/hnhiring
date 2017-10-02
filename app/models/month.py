from django.db import models


class MonthManager(models.Manager):
    def get_or_create(self, name, hn_id=None):
        month, created = super().get_or_create(name=name, defaults={'hn_id': hn_id})
        if not created:
            if month.hn_id is None and hn_id is not None:
                month.hn_id = hn_id
                month.save()
        return month


class Month(models.Model):
    id = models.AutoField(primary_key=True)

    hn_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True)

    objects = MonthManager()

    class Meta:
        db_table = 'month'

    def __str__(self):
        return self.name
