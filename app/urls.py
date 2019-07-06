from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .views import Index, Login, Register, Home, Search, Movie, Profile, Favorites, WatchlistView, Rate, Activities, Logout

cache_time = 60 * 60

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('login/', Login.as_view(), name='login'),
	path('register/', Register.as_view(), name='register'),
	path('home/', cache_page(cache_time)(login_required(Home.as_view())), name='home'),
	path('search/<str:movie_name>', login_required(Search.as_view()), name='search'),
	path('home/<int:id>/', cache_page(cache_time)(login_required(Home.as_view())), name='home'),
	path('movie/<int:id>/',  (login_required(Movie.as_view())), name='movie'),  # cache_page(cache_time)
	path('movie/favorite/', login_required(csrf_exempt(Favorites.as_view())), name='favorite'),
	path('movie/watchlist/', login_required(csrf_exempt(WatchlistView.as_view())), name='watchlist'),
	path('movie/rate/', login_required(csrf_exempt(Rate.as_view())), name='rate'),
	path('profile/', login_required(Profile.as_view()), name='profile'),
	path('activities/', login_required(Activities.as_view()), name='activities'),
	path('logout/', login_required(Logout.as_view()), name='logout')
]
