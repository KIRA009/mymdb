from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, username, password, **extra_details):
		"""
		Creates and saves a User with the given contact, password, name, gender, location_id
		"""

		extra_details['is_superuser'] = False

		user = self.model(username=username, **extra_details)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password, **extra_details):
		"""
		Creates and saves a user with the given email, password
		"""

		extra_details['is_superuser'] = True

		user = self.model(username=username, **extra_details)
		user.set_password(password)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=128, unique=True, primary_key=True)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = UserManager()


class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
	movie_id = models.CharField(max_length=32)

	objects = models.Manager()


class Favorited(models.Model):
	movie_id = models.CharField(max_length=32, primary_key=True)
	movie_title = models.CharField(max_length=128)
	release_date = models.CharField(max_length=16)
	movie_desc = models.TextField()
	movie_img = models.URLField()

	objects = models.Manager()


class Rated(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
	movie_id = models.CharField(max_length=32)
	rating = models.IntegerField()

	objects = models.Manager()


class AllTimeWatchlist(models.Model):
	movie_id = models.CharField(max_length=32, primary_key=True)
	movie_title = models.CharField(max_length=128)
	release_date = models.CharField(max_length=16)
	movie_desc = models.TextField()
	movie_img = models.URLField()

	objects = models.Manager()


class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
	movie_id = models.CharField(max_length=32)
	watched = models.BooleanField(default=False)

	objects = models.Manager()


class Activity(models.Model):
	ACTIVITIES = {
		'fav': 'Favorited {movie_name}',
		'del_fav': 'Removed {movie_name} from favorites',
		'rate': 'Rated {movie_name} {rating} out of 10',
		'add_watch': 'Added {movie_name} to watchlist with status {watchlist_status}',
		'change_watch': 'Changed status of {movie_name} in watchlist from {prev_status} to {new_status}',
		'del_watch': 'Removed {movie_name} from watchlist'
	}

	user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
	movie_name = models.CharField(max_length=32)
	activity = models.TextField()
	time_of_activity = models.DateTimeField(auto_now_add=True)

	objects = models.Manager()
