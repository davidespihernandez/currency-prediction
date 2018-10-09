from django.db import models


class Exchange(models.Model):
    base = models.CharField(max_length=3)
    date = models.DateField(db_index=True)
    goal = models.CharField(max_length=3)
    rate = models.DecimalField(decimal_places=6, max_digits=14)

    class Meta:
        unique_together = ('base', 'date', 'goal', )
