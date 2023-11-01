

#import necessary libraries
import pickle
import streamlit as st
import requests

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# function to scrape movie poster
def img_scrape(movie_id):

    url = f"https://www.themoviedb.org/movie/{movie_id}" #url to scrape data

    # prevent access denying error
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    # Make HTTP request to above url
    request = Request(url, headers=headers)

    response = urlopen(request)

    bsoup = BeautifulSoup(response,'html.parser')

    # find relevant class
    div = bsoup.find('div', class_ = 'image_content backdrop')

    # check for div element
    if div:
        img = div.find('img') # search div element with img element

        # check for img element within div
        if img:

            source = img['src']

            # splitting the relevant link
            splitter = source.split('/')

            # remove .jpg for concatenation
            img_id = splitter[-1].replace('.jpg', '')

        else:
            print('Image not found')

    else:
        print("div not found")

    # create link to the image
    poster_path = "https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+img_id +".jpg"

    return poster_path

# function to scrape user review
def review_scrape(movie_id):

    # url to extract data
    url = f"https://www.themoviedb.org/movie/{movie_id}"

    # prevent access denying error
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    # try-catch block is used to catch error while scrapping
    try:
        # Make HTTP request to above url
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            bsoup = BeautifulSoup(response.text, 'html.parser')

            #find review class in the web page
            div_rev = bsoup.find('div', class_ = 'review_container one')

            if div_rev:

                ##extract text in the th class
                movie_review = div_rev.text.strip()

                return movie_review

            else:
                return "Review Not Found"

        else:
            return "Review Search Failed"

    except Exception as e:

        print("Error while loading: ", e)
        return None


# function to scrape overview
def overview_scrape(movie_id):

    # link to reach the overview
    url = f"https://www.themoviedb.org/movie/{movie_id}"

    # prevent access denying error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        # Make HTTP request to above url
        request = Request(url, headers=headers)
        response = urlopen(request)

        bsoup = BeautifulSoup(response, 'html.parser')

        #find overview class
        div_overview = bsoup.find('div', class_ = 'overview')

        #extract the text and remove whitespaces
        movie_overview = div_overview.text.strip()

    except Exception as e:

        print("Error while scprapping: ", e)

    return movie_overview



# function to scrape release date
def reldt_scrape(movie_id):

    # link to reach the overview
    url = f"https://www.themoviedb.org/movie/{movie_id}"

    # prevent access denying error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        # Make HTTP request to above url
        request = Request(url, headers=headers)
        response = urlopen(request)

        bsoup = BeautifulSoup(response,'html.parser')

        rel_date =  bsoup.find('span', class_ = 'tag release_date')

        mov_date = rel_date.text.strip()
    except Exception as e:

        print("Release date not found")

    return mov_date





# implement recommend function
def recommend(movie):

    # find specific movie from db
    movie_index = movies[movies['title'] == movie].index[0]
    sim_distance = sorted(list(enumerate(similarity[movie_index])),reverse=True, key = lambda x:x[1])

    rec_movies = []

    for i in sim_distance[0:10]:

        movie_id = movies.iloc[i[0]].movie_id

        # assigning variable to values returned from functions
        mov_overview = overview_scrape(movie_id)
        release_date = reldt_scrape(movie_id)
        movie_reviews = review_scrape(movie_id)
        movie_poster = img_scrape(movie_id)

        rec_movie_info = {
            'title': movies.iloc[i[0]].title,
            'image':movie_poster,
            'date':release_date,
            'overview': mov_overview,
            'reviews': movie_reviews,
        }

        rec_movies.append(rec_movie_info)

    return rec_movies

##header
st.header("MoviePulse")

##load previously create models
movies = pickle.load(open('artifacts/movie_later.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# getting movie titles
list_movie = movies['title'].values

##getting user inputs
movie_drop = st.selectbox(
    'Type movie name to view recommendations:',
    list_movie
)



if st.button("Show Recommendations"):
    recommend_movies = recommend(movie_drop)
    col1, col2,col3, col4, col5 = st.columns(5)

    for i in range(10):
        with st.expander(recommend_movies[i]['title']):

            st.image(recommend_movies[i]['image'])
            st.write("Release Date: ",recommend_movies[i]['date'])
            st.write(recommend_movies[i]['overview'])
            st.write(recommend_movies[i]['reviews'])




