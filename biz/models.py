
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
from django.contrib.auth.models import User

from osmapi import OsmApi

import json


# Create your models here.

class Business(models.Model):
	owner = models.ForeignKey(User, blank=True, null=True)
	osm_id = models.IntegerField()

	cached = models.TextField(editable=False, default="{}")

	def save(self, *args, **kwargs):
		MyApi = OsmApi()
		data = MyApi.NodeGet(self.osm_id)
		self.cached = json.dumps(data)
		if self.id is not None:
			super(Business, self).save(force_insert=False, force_update=True )
		else:
			super(Business, self).save()
	def __str__(self):
		try:
			a = self.cached
			name = json.loads(a).get("tag").get("name")
			t = json.loads(a).get("tag").get("office")
			o = json.loads(a).get("tag").get("operator")
			return name if name is not None else t if t is not None else o if o is not None else str(self.osm_id)
		except:
			return "ERRORE"

	@property
	def j(self):
		return json.loads(self.cached)

	@property
	def safej(self):
		return json.dumps(json.loads(self.cached))

	def update(self):
		MyApi = OsmApi()
		data = MyApi.NodeGet(self.osm_id)
		n_cached = json.dumps(data)

		Business.objects.filter(id=self.id).update(cached=n_cached)



