from django.db.models import F
from .models import Page
import datetime


def vue_stats_middleware(get_response):
	def middleware(request):
		# Avant chaque exécution de la vue, on incrémente 
		# le nombre de page vues à chaque appel de vues
		try:
			# Le compteur lié à la page est récupéré et incrémenté
			p = Page.objects.get(url=request.path)  
			p.nb_visites = p.nb_visites + 1
			
		except Page.DoesNotExist:
			# Un nouveau compteur à 1 par défaut est créé
			p = Page.objects.create(url=request.path)
		request.time = datetime.datetime.now()
		# Appel de la vue Django
		response = get_response(request)

		if p.nb_visites != 1:
			total_vue = p.temps_vue*(p.nb_visites-1)
		else:
			total_vue = 0
		temps_vue = (datetime.datetime.now() - request.time).seconds
		p.temps_vue = int((total_vue + temps_vue)/p.nb_visites)
		p.save()
		# Une fois la vue exécutée, on ajoute à la fin le nombre
		# de vues de la page 
		response.content += bytes(
			"Cette page a été vue {0} fois pendant une durée moyenne de {1}".format(p.nb_visites, p.temps_vue),
			"utf8"
			)
		# Et on retourne le résultat
		return response

	return middleware