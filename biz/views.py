from django.shortcuts import render
from django import forms
import django.contrib.auth as auth
from django.http import HttpResponse, HttpResponseRedirect

from osmapi import OsmApi
from django.conf import settings
from biz.models import * 
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, "map.html")

def stats(request):
	return render(request, "stats.html")

def business_info(request, business_id):
	return render(request, "business.html", {"business":Business.objects.get(id=business_id)})	

def login(request):
	return render(request, "login.html")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def profile(request):
	return HttpResponseRedirect("/users/%s" % request.user.username)

def user(request, username):
	return render(request, "profile.html", {"me":request.user.username==username})

def geojson(request):
	ret = []
	for b in Business.objects.all():
		data = json.loads(b.cached)
		if not "name" in data["tag"]:
			data["tag"]["name"] = str(b.osm_id)
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

@login_required
def add(request):
	if request.method == "GET":
		return render(request, "add_point.html")
	else:
		return put_point(request)

import csv

def get_csv(request):
	cols = ["name"]
	for b in Business.objects.all():
		cols.extend(b.j.get("tag").keys())
	cols = set(cols)
	cols = list(cols)

	cols.remove("name")
	cols.insert(0, "name")
	cols.insert(1, "lon")
	cols.insert(2, "lat")

	colnames = dict(zip(cols,cols)) 

	f = open("out.csv", "wb")
	listwriter = csv.DictWriter(f, fieldnames=cols)

	listwriter.writerow(colnames)
	for b in Business.objects.all():
		the_b = b.j.get("tag")
		the_b.update({"lon":b.j.get("lon"), "lat":b.j.get("lat")})
		listwriter.writerow(the_b)

	f.close()

	response = HttpResponse(open("out.csv"), content_type="text/csv")

	return response
	
def put_point(request):
	api = OsmApi()
	api = OsmApi(username = settings.OSM_USER, password = settings.OSM_PASSWORD)
	api.ChangesetCreate({"comment": "Urban Fabric Node Creation"})
	res =api.NodeCreate({"lon":float(request.REQUEST.get("lng")), "lat":float(request.REQUEST.get("lat")), "tag": {"name":request.REQUEST.get("name"), 	}})
	api.ChangesetClose()
	b = Business()
	b.osm_id = res["id"]
	if not request.user.is_anonymous():
		b.owner = request.user
	b.save()

	return HttpResponseRedirect("/edit/%s" % b.id)

def edit(request, business_id):
	b = Business.objects.get(id=business_id)
	return render(request, "editor.html", {"business":b})

@csrf_exempt
def update(request, business_id):
	b = Business.objects.get(id=business_id)
	new_tags = json.loads(request.REQUEST.get("data",json.dumps(b.j["tag"])))
	api = OsmApi(username = settings.OSM_USER, password = settings.OSM_PASSWORD)
	cs = api.ChangesetCreate({"comment": "Urban Fabric Node Update"})
	data = api.NodeGet(b.osm_id)
	data = api.NodeUpdate({"id":b.osm_id, "lat":data["lat"], "lon":data["lon"], "tag":new_tags, "changeset":cs, "version":int(data["version"])})
	api.ChangesetClose()
	b.update()

	return HttpResponse("OK")

#API

from oauth2_provider.decorators import protected_resource

@protected_resource()
def business_details(request, business_id):
	b = Business.objects.get(id=business_id)
	return HttpResponse(json.dumps(b))


