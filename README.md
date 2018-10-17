# currency-prediction
Django REST app. Reads a public currency exchange rates API, and tries to predict future values for a specific currency.

This repo is a simple django application for a simple time series forecasting test. The application features are:

- Read information about currency conversion (EUR to USD, for instance) from a public API. In this case I use https://exchangeratesapi.io/, which is very nice, free API. Please, don't abuse of this API, use it with responsibility.
- Load this retrieved information into the local database.
- Train a statistic model to predict the next possible value.
- Allows to retrieve information using commands, REST views or HTML pages.

The goal here is not to preform a 100% accurate prediction (if I was able to do that, I won't publish the code!), but simply to create a test application to demonstrate some Django features:

- Django models.
- Read data from a REST API.
- Use a serializer to load the read info into the database.
- Use of a statistic model with statsmodels to perform forecasting for a time series, using the SARIMAX model.
- Django management command to load data and to run a prediction.
- REST view to retrieve information and to retrieve a prediction.
- Automatic testing for serializer, components and REST views.
- MVT (model view template) Django views using Semantic UI to retrieve information and to perform predictions.

I've tried to do everything as clear as I could, so this can be used by other developers starting with Django.

Installation:

- Install Django
- Create a virtual environment and activate it
- Clone or download this repo.
- Install requirements with pip install -r requirements.txt
- Execute manage.py migrate to create the required tables.
- Now the application can be started with manage.py runserver

Use of the application:

- Commands:
	- Load data. You can execute manage.py load to load data in batch coming from the API. The command receives startdate and enddate as arguments. The command will sleep a second between calls to not overload the API. If no dates passed, the last 3 months will be loaded.
	- Predict. You can execute manage.py predict to predict the possible value for the next date, considering the last date loaded.

- REST views.
	- /exchanges/?date=dd-mm-yyyy. Retrieves the loaded information for a specific day.
	- /exchanges/predict/?currency=USD. Performs a prediction for the next date, for the specified currency.

- Pages (MVT views)
	- Retrieve. Allows to query the existing data for a specific date.
	- Forecast. With the stored information, predicts the next rate for a selected currency (base is EUR always)
