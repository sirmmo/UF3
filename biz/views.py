from django.shortcuts import render
from django import forms

from django.http import HttpResponse

from osmapi import OsmApi
from django.conf import settings
from biz.models import * 

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
	payment_coins = forms.BooleanField()
	payment_notes = forms.BooleanField()
	payment_cash = forms.BooleanField()
	currency_eur = forms.BooleanField()
	currency_others = forms.BooleanField()

class CardPaymentForm(forms.Form):
	payment_credit_cards = forms.BooleanField()
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



def index(request):
	return render(request, "map.html")

def stats(request):
	return render(request, "stats.html")

def business_info(request, business_id):
	return render(request, "business.html", {"business":Business.objects.get(id=business_id)})	

def geojson(request):
	ret = []
	for b in Business.objects.all():
		data = json.loads(b.cached)
		to_add = {
		  "type": "Feature",
		  "geometry": {
		    "type": "Point",
		    "coordinates": [data["lon"], data["lat"]]
		  },
		  "properties": data["tag"],
		  "id":data["uid"]
		}
		ret.append(to_add)

	return HttpResponse(json.dumps({"type":"FeatureCollection", "features":ret}))

def complex(request):
	ret = []
	for b in Business.objects.all():
		ret.append(json.loads(b.cached))
	return HttpResponse(json.dumps(ret))

def add(request):
	if request.method == "GET":
		return render(request, "add_point.html")
	else:
		pass


def put_point(request):
	api = OsmApi()
	api = OsmApi.OsmApi(username = settings.OSM_USER, password = settings.OSM_PASSWORD)
	api.ChangesetCreate({"comment": "Urban Fabric Node Creation"})
	res =api.NodeCreate({"lon":float(request.REQUEST.get("lng")), "lat":float(request.REQUEST.get("lat")), "tag": {"name":request.REQUEST.get("name"), 	}})
	api.ChangesetClose()
	b = Business()
	b.osm_id = res["id"]
	b.owner = request.user
	b.save()

	return HttpResponseRedirect("/edit/"+b.id)

def edit(request, business_id):
	b = Business.objects.get(id=business_id)
	return render("editor.html", {"business":b})

def upload(request, business_id):
	b = Business.objects.get(id=business_id)

	new_tags = json.loads(request.REQUEST.get("data", b.j["tag"]))
	cs = api.ChangesetCreate({"comment": "Urban Fabric Node Update"})
	api = OsmApi.OsmApi(username = settings.OSM_USER, password = settings.OSM_PASSWORD)
	data = api.NodeGet(b.osm_id)
	data = api.NodeUpdate(b.osm_id, data["lat"], data["lng"], new_tags, cs, int(data["version"])+1)
	api.ChangesetClose()

	return HttpResponseRedirect("/edit/"+b.id)




#API

from oauth2_provider.decorators import protected_resource

@protected_resource()
def business_details(request, business_id):
	b = Business.objects.get(id=business_id)
	return HttpResponse(json.dumps(b))


