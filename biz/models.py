from django.db import models
from django.contrib.auth.models import User

from osmapi import OsmApi

import json

# Create your models here.

class Business(models.Model):
	owner = models.ForeignKey(User, blank=True, null=True)
	osm_id = models.IntegerField()

	cached = models.TextField(visible=False, default="{}")

	def save(self, *args, **kwargs):
		MyApi = OsmApi.OsmApi()
		data = MyApi.NodeGet(self.osm_id)
		self.cached = json.dumps(data)
		super(Business, self).save(self, args, kwargs)


