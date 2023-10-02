import csv
import pandas as pd
from django.core.management import BaseCommand

from recommender.movierecommender.management.commands.make_recommendations import similarity_between_movies

#from recommender.movierecommender.management.commands.make_recommendations import similarity_between_movies
from ...models import Movie

class Command(BaseCommand):
    help = 'Load a movie csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        THRESHOLD = 0.8
        # Get all watched and unwatched movies
        watched_movies = Movie.objects.filter(
                watched=True)
        unwatched_movies = Movie.objects.filter(
                watched=False)
        # Start to generate recommendations in unwatched movies
        for unwatched_movie in unwatched_movies:
            max_similarity = 0
            will_recommend = False
            # For each watched movie
            for watched_movie in watched_movies:
                # Calculate the similarity between watched_movie and all unwatched movies
                similarity = similarity_between_movies(unwatched_movie, watched_movie)
                if similarity >= max_similarity:
                    max_similarity = similarity
                # early stop if the unwatched_movie is similar enough
                if max_similarity >= THRESHOLD:
                    break
            # If unwatched_movie is similar enough to watched movies
            # Then recommend it
            if max_similarity > THRESHOLD:
                will_recommend = True
                print(f"Find a movie recommendation: {unwatched_movie.original_title}")
            unwatched_movie.recommended = will_recommend
            unwatched_movie.save()

# python manage.py load_movies --path movies.csv