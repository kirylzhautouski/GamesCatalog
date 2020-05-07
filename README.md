# GamesCatalog
Django powered games catalog web-site. Regularly (using Celery) takes data from IGDB API and saves it to the database using Django ORM and PostgreSQL. Provides the functionality of viewing all games, searching, filtering by many parameters, browsing through details of a certain game. Support registration and authentication with email confirmation with further creating of list of favourite games. 
Implemented the same API for existing database using both DRF and Flask. Used Docker and Docker Compose.

Link to the Flask API: https://github.com/KirillZhelt/GamesCatalogAPI
___

**Technologies:** Django, DRF, Celery, Docker Compose, Flask

___

### Example Screenshots

Paginated list of all games:

![All games screenshot](/screenshots/games_list.png?raw=true)

Search through all games and show paginated results:

![Search games screenshot](/screenshots/search_games.png?raw=true)

Filter games by platforms and genres:

![Filter games screenshot](/screenshots/filter_games.png?raw=true)

Game details page with tweets loaded using Twitter API:

![Game detail screenshot](/screenshots/game_detail.png?raw=true)

Favorite games of the logged user:

![Favorite games screenshot](/screenshots/favorite_games.png?raw=true)

Game detail page when user is logged:

![Game detail when user is logged screenshot](/screenshots/game_detail_logged.png?raw=true)
