# This program crawls the present Rotten Tomatoes Movies In Theaters webpage, sorting the list from most to least popular, returning up to four pages worth of data

from bs4 import BeautifulSoup
import requests
from xlwt import *


url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=4"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
titleList = soup.find_all('a', {'data-qa': 'discovery-media-list-item'})
movies_list = {}
num = 0

workbook = Workbook(encoding='utf-8')
table = workbook.add_sheet('TopMoviesData')
table.write(0, 0, 'Number')
table.write(0, 1, 'Title')
table.write(0, 2, 'Rotten Tomatoes URL')
table.write(0, 3, 'Poster Image')
table.write(0, 4, 'Synopsis')
table.write(0, 5, 'Theater Release Date')
table.write(0, 6, 'Audience Score')
table.write(0, 7, 'Critics Score')
line = 1


def write(title):

    if title.get_text():
        global num
        num += 1
        movieUrls = 'https://www.rottentomatoes.com' + title['href']
        # print(movieUrls)
        movieTitles = title.find(
            "span", {"data-qa": "discovery-media-list-item-title"}).get_text().strip()
        releaseDate = title.find(
            "span", {"data-qa": "discovery-media-list-item-start-date"}).get_text().strip()
        audienceScore = title.find('score-pairs').get('audiencescore')
        criticScore = title.find('score-pairs').get('criticsscore')
        posterImg = title.find('img').get('src')
        movieReq = requests.get(movieUrls)
        movieSoup = BeautifulSoup(movieReq.content, 'html.parser')
        synopsis = movieSoup.find(
            'div', {'id': 'movieSynopsis'}).get_text().strip()

        movies_list[num] = {'movie_title': movieTitles,
                            'urls': {
                                'rt_url': movieUrls,
                                'poster_img': posterImg,
                            },
                            'movie_info': {
                                'synopsis': synopsis,
                                'release_date': releaseDate,
                                'audience_score': audienceScore,
                                'critics_score': criticScore,
                            }}

        global line
        table.write(line, 0, num)
        table.write(line, 1, movieTitles)
        table.write(line, 2, movieUrls)
        table.write(line, 3, posterImg)
        table.write(line, 4, synopsis)
        table.write(line, 5, releaseDate)
        table.write(line, 6, audienceScore)
        table.write(line, 7, criticScore)
        line += 1


[write(title) for title in titleList]
workbook.save('movies_top100.xls')

# Adding on inquirer (future)

# questions1 = [
#     inquirer.List('type',
#                   message="Please choose what form of media you would like to search",
#                   choices=['In Theaters', 'At Home',
#                            'Coming Soon', 'TV Shows'],
#                   ),
#     inquirer.Checkbox('genres',
#                       message="Please choose your desired genres",
#                       choices=['ACTION', 'ADVENTURE', 'ANIMATION', 'ANIME', 'BIOGRAPHY', 'COMEDY', 'CRIME', 'DOCUMENTARY', 'DRAMA', 'ENTERTAINMENT', 'FAITH AND SPIRITUALITY', 'FANTASY', 'GAME SHOW', 'LGBTQ', 'HEALTH AND WELLNESS', 'HISTORY', 'HOLIDAY', 'HORROR',
#                                'HOUSE AND GARDEN', 'KIDS AND FAMILY', 'MUSIC', 'MUSICAL', 'MYSTERY AND THRILLER', 'NATURE', 'NEWS', 'REALITY', 'ROMANCE', 'SCI FI', 'SHORT', 'SOAP', 'SPECIAL INTEREST', 'SPORTS', 'STAND UP', 'TALK SHOW', 'TRAVEL', 'VARIETY', 'WAR', 'WESTERN'],
#                       carousel=True
#                       ),
#     inquirer.Checkbox('audience',
#                       message="Please choose your Rotten Tomatoes audience rating(s)",
#                       choices=['Fresh', 'Rotten'],
#                       ),
#     inquirer.Checkbox('critics',
#                       message="Please choose your Rotten Tomatoes critics score(s) (Tomatometer®): ",
#                       choices=['Certified Fresh', 'Fresh', 'Rotten'],
#                       ),
#     inquirer.Checkbox('rating',
#                       message="Please choose your TV show/movie rating",
#                       choices=['G', 'PG', 'PG-13', 'R',
#                                'NC-17', 'NOT RATED', 'UNRATED'],
#                       ),
#     inquirer.List('type',
#                   message="Please choose how you would like to sort your results",
#                   choices=['None', 'Most Popular', 'Newest', 'A -> Z', 'Critics Tomatometer® (Highest)',
#                            'Critics Tomatometer® (Lowest)', 'Audience Score (Highest)', 'Audience Score (Lowest)'],
#                   ),
# ]
# questions2 = [
#     inquirer.Checkbox('services',
#                       message="Please choose your streaming services",
#                       choices=['Amazon Prime', 'Apple TV', 'Apple TV Plus', 'Disney Plus', 'HBO Max', 'Hulu', 'Netflix', 'Paramount Plus', 'Peacock', 'Showtime', 'VUDU'],
#                       ),
# ]

# answers1 = inquirer.prompt(questions1)

# if answers1['type'] == 'At Home' or 'TV Shows':
#     answers2 = inquirer.prompt(questions2)

# Potential Class Version

# class newRequest():
#     def __init__(self):
#         url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular"
#         req = requests.get(url)
#         self.movies_list = {}
#         soup = BeautifulSoup(req.content, 'html.parser')
#         self.num = 0
#         self.titleList = soup.find_all(
#             'a', {'data-qa': 'discovery-media-list-item'})

#     def write(self, title):
#         if title.get_text():
#             self.num += 1
#             movieUrls = 'https://www.rottentomatoes.com' + title['href']
#             # print(movieUrls)
#             movieTitles = title.find(
#                 "span", {"data-qa": "discovery-media-list-item-title"}).get_text().strip()
#             movieReq = requests.get(movieUrls)
#             movieSoup = BeautifulSoup(movieReq.content, 'html.parser')
#             synopsis = movieSoup.find(
#                 'div', {'id': 'movieSynopsis'}).get_text().strip()
#             movieInfo = movieSoup.find_all(
#                 'li', {'data-qa': 'movie-info-item-value'})
#             self.info = self.movieInfo(movieInfo)

#             movies_list[num] = {'movie_title': movieTitles,
#                                 'rt_url': movieUrls, 'movie_info': {'synopsis': synopsis, 'ratings': self.info.ratings}}

#     def movieInfo(self, movieInfo):
#         self.ratings = movieInfo[0]
#         self.genre = movieInfo[1]
#         self.language = movieInfo[2]
#         self.directors = movieInfo[3]
#         self.producers = movieInfo[4]
#         self.writers = movieInfo[5]
#         self.releaseDate =
