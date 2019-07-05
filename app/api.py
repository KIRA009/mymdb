import requests

from mymdb.settings import API_KEY


class Api:
	def __init__(self):
		self.params = {'api_key': API_KEY}
		self.BASE_URL = 'https://api.themoviedb.org/3/'
		self.genres = {28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime', 99: 'Documentary',
		               18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History', 27: 'Horror', 10402: 'Music',
		               9648: 'Mystery', 10749: 'Romance', 878: 'Science Fiction', 10770: 'TV Movie', 53: 'Thriller',
		               10752: 'War', 37: 'Western'}

	@staticmethod
	def get(url, params):
		res = requests.get(url, params)
		return res.json()

	def get_trending(self, page=1):
		url = self.BASE_URL + 'trending/movie/day'
		params = self.params.copy()
		params['page'] = page
		return self.get(url, params)['results']

	def get_movie(self, movie_id, **args):
		url = self.BASE_URL + f'movie/{movie_id}'
		params = self.params.copy()
		if len(args) > 0:
			params['append_to_response'] = ','.join(args)
		movie = self.get(url, params)
		return movie
