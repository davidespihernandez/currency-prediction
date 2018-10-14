import datetime
import random

from predictor.models import Exchange


class Builder:
    def exchange(self, base=None, date=None, goal=None, rate=None):
        exchange, created = Exchange.objects.get_or_create(
            base=base or 'EUR',
            date=date or datetime.date.today(),
            goal=goal or 'USD',
            rate=rate or random.random()
        )
        return created
