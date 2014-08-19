from django.shortcuts import render
from django import forms

# THE MAGIC http://taginfo.openstreetmap.org/api/4/key/values?key=shop&page=1&rp=10&sortname=count_ways&sortorder=desc&query=stor

class AddressForm(forms.Form):
	address_street = forms.CharField(max_length=100)
	address_housenumber = forms.CharField(max_length=100)
	address_postcode = forms.CharField(max_length=100)
	address_city = forms.CharField(max_length=100)
	address_country = forms.CharField(max_length=100)
	address_housename = forms.CharField(max_length=100)
	address_level = forms.CharField(max_length=100)

class ContactForm(forms.Form):
	phone = forms.CharField(max_length=100)
	fax = forms.CharField(max_length=100)
	website = forms.CharField(max_length=100)
	email = forms.CharField(max_length=100)
	contact_webcam = forms.CharField(max_length=100)
	wikipedia = forms.CharField(max_length=100)
	contact_twitter = forms.CharField(max_length=100)
	contact_facebook = forms.CharField(max_length = 100)

class OtherForm(forms.Form):
	brand = forms.CharField(max_length=100)
	description = forms.CharField(max_length=100)
	origin = forms.CharField(max_length=100)
	opening_hours = forms.CharField(max_length=100)
	operator = forms.CharField(max_length=100)
	sells = forms.CharField(max_length=100)
	wholesale = forms.CharField(max_length=100)

class WheelchairForm(forms.Form):
	wheelchair = forms.CharField(max_length=100)

class InternetForm(forms.Form):
	internet_access= forms.CharField(max_length=100)
	internet_access_fee= forms.CharField(max_length=100)
	wifi_access_operator= forms.CharField(max_length=100)
	wifi_access_technology= forms.CharField(max_length=100)
	wifi_access_ssid= forms.CharField(max_length=100)

class CashPaymentForm(forms.Form):
	payment_coins = forms.BooleanField(default = True)
	payment_notes = forms.BooleanField(default = True)
	payment_cash = forms.BooleanField(default = True)
	currency_eur = forms.BooleanField(default = True)
	currency_others = forms.BooleanField(default = False)

class CardPaymentForm(forms.Form):
	payment_credit_cards = forms.BooleanField(default = True)
	payment_mastercard = forms.BooleanField()
	payment_visa = forms.BooleanField()
	payment_diners_club = forms.BooleanField()
	payment_american_express = forms.BooleanField()
	payment_discover_card = forms.BooleanField()
	payment_girocard = forms.BooleanField()
	payment_debit_cards = forms.BooleanField()
	payment_bankaxess = forms.BooleanField()
	payment_bancomat = forms.BooleanField()
	payment_girogo = forms.BooleanField()
	payment_laser = forms.BooleanField()
	payment_maestro = forms.BooleanField()
	payment_v_pay = forms.BooleanField()
	payment_mastercard = forms.BooleanField()


class ShopForm(forms.Form):
	shop_type = forms.ChoiceField(choices = [])

class OfficeForm(forms.Form):
	office_type = forms.ChoiceField(choices = [])

class CraftForm(forms.Form):
	craft_type = forms.ChoiceField(choices = [])

class AmenityForm(forms.Form):
	amenity_type = forms.ChoiceField(choices = [])

def choices(request):
	pass




def map(request):
	return render(request, "map.html")

