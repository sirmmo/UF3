from django.core.management.base import BaseCommand, CommandError
from biz.models import *

import overpass

class Command(BaseCommand):

	def handle(self, *args, **options):
		pre_coords = args[0:4]
		coords = [ "44.54478983370985","11.322011947631836", "44.602140637755014" ,"11.41256332397461"]
		
		coords = "(" + ",".join(coords) + ")"
		o = overpass.API()


		types = ['node', 'relation', 'way']

		queries = [
			'["office"]',
			'["shop"]',
			'["amenity"="bar"]',
			'["amenity"="pub"]',
			'["amenity"="restaurant"]',
			'["amenity"="cafe"]',
			'["amenity"="ice_cream"]',
			'["amenity"="pharmacy"]',
			'["craft"]'
		]

		for type in types:
			for query in queries:
				the_query = "%s%s%s" % (type, query, coords)
				print the_query
				items = o.Get(the_query)

				if "elements" in items:
					for item in items["elements"]:
						b = Business()
						b.osm_id = item['id']
						b.save()