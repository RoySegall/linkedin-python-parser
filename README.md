[![Build Status](https://travis-ci.org/RoySegall/linkedin-python-parser.svg?branch=master)](https://travis-ci.org/RoySegall/linkedin-python-parser)

# Linked in parser

This project parses LinkedIn profiles.

## First thing.
Copy the example settings file to a `settings.yml`:

`cp settings.example.yml settings.yml`

Edit the settings.

## Before installing

1. Make sure you have a [RethinkDB](https://www.rethinkdb.com).
2. Make sure the [geckdriver](https://github.com/mozilla/geckodriver)
is located in a path which you know and set under the `gecko` property
in the settings file.
3. Make sure you have [Selenium](http://www.seleniumhq.org/).
4. Register to linkedin and set the user credentials under the
`linkedin` property in the settings file you created.

*Please note*: If you want to scrape for associated people, the scraped
profile need to be connected with you.

## Installation
```bash
rethinkdb --http-port 8090
pip3 install -r requirements.txt
python install.py
```

## Finally
Run the server:
```bash
apistar run
```

Awesome! Have a slice of pizza: :pizza:

## Rest endpoints

### Scraping
Scraping a user is very easy. Create a `GET` request against
`http://localhost:8080/scrape/{user_id}` when `user_id` it's the user
ID which you want to scrape.

*You can ge the the user ID from the address.*

### Searching by added users
In order to get a user with the name `John` you'll need to create a
`POST` request against `http://localhost:8080/search-by-name` with a
JSON payload as:
```json
{
    "name": "John"
}
```

### Searching by skill
In order to get a user with a skill in `Go` you'll need to create a
`POST` request against `http://localhost:8080/search-by-skills` with a
JSON payload as:
```json
{
    "skill": "Go"
}
```
