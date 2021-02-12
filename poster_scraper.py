from api.models import MoviePoster, MovieSchema, Movies
import requests
from bs4 import BeautifulSoup
import shutil


def scrape_movie_posters():
    movie_schema = MovieSchema(many=True)
    movie_id = Movies.query.order_by(Movies.title).filter_by(type='movie').limit(100).offset(1100).all()
    for movie in movie_schema.dump(movie_id):
        print(movie['imdb_id'])
        r = requests.get('https://imdb.com/title/{}'.format(movie['imdb_id']))
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            image_url = soup.find('div', class_='poster').a.img['src']
            print(image_url)
            download_image = requests.get(image_url, stream=True)
            if download_image.status_code == 200:
                poster = MoviePoster(id=movie['imdb_id'],
                                 url="{}.jpg".format(movie['imdb_id']))
                try:
                    poster.save_to_db()
                    with open('downloaded-images/{}.jpg'.format(movie['imdb_id']), 'wb') as out_file:
                        shutil.copyfileobj(download_image.raw, out_file)

                except:
                    print("Failed inserting into database and download image")

        except:
            print("Failed getting image url")


scrape_movie_posters()
