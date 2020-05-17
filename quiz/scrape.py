# Script to scrape IMDB website, generate datasets and load into Movie database to generate questions.

import re

from bs4 import BeautifulSoup
from requests import get

from quiz import db
from quiz.models import Movie


#url = "https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=A7DWVBMKT01YRE5MZX0R&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1"
url = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=action"
page = get(url)
soup = BeautifulSoup(page.content, 'lxml')
content = soup.find(id="main")

articleTitle = soup.find("h1", class_="header").text.replace("\n","")
movieFrame = content.find_all("div", class_="lister-item mode-advanced")

movieTitle=[]
movieDate=[]
movieRuntime=[]
movieGenre=[]
movieRating=[]
movieDirector=[]
movieStars=[]

for movie in movieFrame:
    movieFirstLine = movie.find("h3", class_="lister-item-header")
    movieCast = movie.find("p", class_="")

    movieTitle.append(movieFirstLine.find("a").text)
    movieDate.append(re.sub(r"[()]","", movieFirstLine.find("span", class_="lister-item-year").text))
    movieRuntime.append(movie.find("span", class_="runtime").text)
    movieGenre.append(movie.find("span", class_="genre").text.rstrip().replace("\n", ""))
    movieRating.append(movie.find("strong").text)

    casts = movieCast.text.replace("\n", "").split('|')
    casts = [x.strip() for x in casts]
    casts = [x.split(':')[1] for x in casts]
    movieDirector.append(casts[0])
    stars = casts[1].split(",")
    movieStars.append(stars[0]+', '+stars[1])

movieData = [movieTitle, movieDate, movieRuntime, movieGenre, movieRating, movieDirector, movieStars]

for i in range(len(movieData[0])):
    movie = Movie(movietitle=movieData[0][i], movieyear=movieData[1][i], movielength=movieData[2][i], moviegenre=movieData[3][i], movierating=movieData[4][i], moviedirector=movieData[5][i], moviestars=movieData[6][i])
    db.session.add(movie)

db.session.commit()

