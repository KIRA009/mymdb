from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse

from .models import User, Favorite, Favorited, Watchlist, AllTimeWatchlist, Rated, Activity
from .api import Api

myapi = Api()


class Register(View):
	@staticmethod
	def get(request):
		if request.user.is_authenticated:
			return redirect('home')
		return render(request, 'register.html')

	@staticmethod
	def post(request):
		data = request.POST
		User.objects.create_user(data['username'], data['password'])
		return redirect('login')


class Login(View):
	@staticmethod
	def get(request):
		if request.user.is_authenticated:
			return redirect('home')
		return render(request, 'login.html')

	@staticmethod
	def post(request):
		data = request.POST
		user = authenticate(username=data['username'], password=data['password'])
		if not user:
			return redirect('login')
		login(request, user)
		return redirect('home', id=1)


class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		kwargs.setdefault('id', 1)
		if kwargs['id'] > 10:
			return super().get_context_data(**kwargs)
		movies = myapi.get_trending(page=kwargs['id'])
		for movie in movies:
			for ind, genre_id in enumerate(movie['genre_ids']):
				movie['genre_ids'][ind] = myapi.genres[genre_id]
		kwargs['movies'] = movies
		return super().get_context_data(**kwargs)


class Search(View):
	@staticmethod
	def get(request, movie_name):
		results = [[f'{movie["title"]} ({movie["release_date"][:4]})', movie['id']] for movie in
		           myapi.search(movie_name)]
		return JsonResponse({'movies': results})


class Favorites(View):
	@staticmethod
	def post(request):
		data = request.POST
		if len(data) == 5:
			Favorited.objects.get_or_create(movie_id=data['id'], movie_title=data['name'], release_date=data['date'],
			                                movie_desc=data['desc'], movie_img=data['img'])
		favorited = Favorited.objects.get(movie_id=data['id'])
		try:
			Favorite.objects.get(user=request.user, movie_id=data['id']).delete()
			Activity.objects.create(user=request.user, movie_name=favorited.movie_title,
			                        activity=Activity.ACTIVITIES['del_fav'].format(movie_name=favorited.movie_title))
			return JsonResponse({'status': 'Deleted'}, status=200)
		except Favorite.DoesNotExist:
			Favorite.objects.get_or_create(user=request.user, movie_id=data['id'])
			Activity.objects.create(user=request.user, movie_name=favorited.movie_title,
			                        activity=Activity.ACTIVITIES['fav'].format(movie_name=favorited.movie_title))
			return JsonResponse({'status': 'Favorited'}, status=200)


class WatchlistView(View):
	@staticmethod
	def post(request):
		data = request.POST
		alltimewatchlist = AllTimeWatchlist.objects.filter(movie_id=data['movie_id']).first()
		if not alltimewatchlist:
			movie = myapi.get_movie(data['movie_id'])
			alltimewatchlist = AllTimeWatchlist.objects.create(movie_id=movie['id'], movie_title=movie['title'],
			                                                   release_date=movie['release_date'], movie_desc=movie['overview'],
			                                                   movie_img=movie['poster_path'])
		watched = True if data['action'] == 'watched' else False
		watchlist = Watchlist.objects.filter(user=request.user, movie_id=data['movie_id']).first()
		if not watchlist:
			if data['action'] != 'remove':
				Watchlist.objects.create(user=request.user, movie_id=data['movie_id'], watched=watched)
				Activity.objects.create(user=request.user, movie_name=alltimewatchlist.movie_title,
				                        activity=Activity.ACTIVITIES['add_watch'].format(
					                        movie_name=alltimewatchlist.movie_title,
					                        watchlist_status='WATCHED' if watched else 'WATCH LATER'))
		else:
			if data['action'] == 'remove':
				watchlist.delete()
				Activity.objects.create(user=request.user, movie_name=alltimewatchlist.movie_title,
				                        activity=Activity.ACTIVITIES['del_watch'].format(movie_name=alltimewatchlist.movie_title))
			else:
				watchlist.watched = watched
				Activity.objects.create(user=request.user, movie_name=alltimewatchlist.movie_title,
				                        activity=Activity.ACTIVITIES['change_watch'].format(
					                        movie_name=alltimewatchlist.movie_title,
					                        new_status='WATCHED' if watched else 'WATCH LATER',
					                        prev_status='WATCH LATER' if watched else 'WATCHED'))
				watchlist.save()
		return JsonResponse({'status': 'Rated'}, status=200)


class Rate(View):
	@staticmethod
	def post(request):
		data = request.POST
		rated = Rated.objects.filter(user=request.user, movie_id=data['movie_id']).first()
		if not rated:
			Rated.objects.create(user=request.user, movie_id=data['movie_id'], rating=int(data['rating']))
		else:
			rated.rating = int(data['rating'])
			rated.save()
		Activity.objects.create(user=request.user, movie_name=data['movie_name'],
		                        activity=Activity.ACTIVITIES['rate'].format(movie_name=data['movie_name'],
		                                                                    rating=data['rating']))
		return JsonResponse({'status': 'Rated'}, status=200)


class Profile(View):
	@staticmethod
	def get(request):
		favorites = Favorite.objects.filter(user=request.user)
		favorites = [Favorited.objects.get(movie_id=favorite.movie_id) for favorite in favorites]
		rated = {rated.movie_id: rated.rating for rated in Rated.objects.filter(user=request.user)}
		watchlist = {movie.movie_id: movie.watched for movie in Watchlist.objects.filter(user=request.user)}
		user_watchlist = [(AllTimeWatchlist.objects.get(movie_id=watchlist_id), watched) for watchlist_id, watched in
		                  watchlist.items()]
		return render(request, 'profile.html', {'favorites': favorites, 'rated': rated, 'watchlist': watchlist,
		                                        'user_watchlist': user_watchlist})


class Activities(View):
	@staticmethod
	def get(request):

		return render(request, 'activities.html', {'activities': Activity.objects.filter(user=request.user).
		              order_by('-time_of_activity'), 'private': request.user.private})

	@staticmethod
	def post(request):
		request.user.private = not request.user.private
		request.user.save()
		return JsonResponse({})


class UserActivities(View):
	@staticmethod
	def get(request, user):
		user = User.objects.filter(username=user).first()
		if user is None:
			return redirect('home')
		if not user.private:
			return render(request, 'user_activities.html', {'activities': Activity.objects.filter(user=user).
			              order_by('-time_of_activity')})
		else:
			if not request.user.is_anonymous:
				if request.user == user:
					return render(request, 'user_activities.html', {'activities': Activity.objects.filter(user=user).
					              order_by('-time_of_activity')})
		return redirect('home')


class Movie(TemplateView):
	template_name = 'movie.html'

	def get_context_data(self, **kwargs):
		if Favorite.objects.filter(user=self.request.user, movie_id=kwargs['id']):
			kwargs['favorited'] = True
		rated = Rated.objects.filter(user=self.request.user, movie_id=kwargs['id']).first()
		watchlist = Watchlist.objects.filter(user=self.request.user, movie_id=kwargs['id']).first()
		if watchlist:
			kwargs['watched'] = {'watched': watchlist.watched}
		if rated:
			kwargs['rated'] = True
			kwargs['user_rating'] = rated.rating
		kwargs['movie'] = myapi.get_movie(kwargs['id'])
		return super().get_context_data(**kwargs)


class Logout(View):
	@staticmethod
	def get(request):
		logout(request)
		return redirect('login')
