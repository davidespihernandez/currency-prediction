# SARIMA prediction example
from statsmodels.tsa.statespace.sarimax import SARIMAX

from predictor.models import Exchange


class Predictor:
    def predict(self, goal):
        exchanges = Exchange.objects.filter(goal=goal).order_by('date')
        data = []
        max_date = None
        last_value = None
        for e in exchanges:
            data.append(float(e.rate))
            max_date = e.date
            last_value = e.rate
        # fit model
        model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
        model_fit = model.fit(disp=False)
        # make prediction
        return max_date, last_value, model_fit.predict(len(data), len(data))
