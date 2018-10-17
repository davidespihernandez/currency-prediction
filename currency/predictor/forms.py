from django import forms


class RetrieveForm(forms.Form):
    date = forms.DateField(label="Date",
                           required=True,
                           widget=forms.SelectDateWidget())


CURRENCIES = (
    ("BGN", "BGN"),
    ("INR", "INR"),
    ("CHF", "CHF"),
    ("SGD", "SGD"),
    ("CNY", "CNY"),
    ("RUB", "RUB"),
    ("SEK", "SEK"),
    ("PLN", "PLN"),
    ("NZD", "NZD"),
    ("MYR", "MYR"),
    ("THB", "THB"),
    ("CZK", "CZK"),
    ("ISK", "ISK"),
    ("ZAR", "ZAR"),
    ("HKD", "HKD"),
    ("KRW", "KRW"),
    ("IDR", "IDR"),
    ("AUD", "AUD"),
    ("MXN", "MXN"),
    ("USD", "USD"),
    ("NOK", "NOK"),
    ("HRK", "HRK"),
    ("PHP", "PHP"),
    ("GBP", "GBP"),
    ("RON", "RON"),
    ("TRY", "TRY"),
    ("ILS", "ILS"),
    ("JPY", "JPY"),
    ("DKK", "DKK"),
    ("HUF", "HUF"),
    ("BRL", "BRL"),
    ("CAD", "CAD"),
)


class ForecastForm(forms.Form):
    currency = forms.ChoiceField(label="Currency code",
                                 choices=sorted(CURRENCIES),
                                 widget=forms.RadioSelect)
