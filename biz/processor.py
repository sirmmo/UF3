
from .models import Business

def req(request):
	data = {}
	data["user"] = request.user
	if request.user.is_anonymous():
		data["businesses"] = []
	else:
		data["businesses"] = Business.objects.filter(owner=request.user)
	return data