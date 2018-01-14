[![Build Status](https://travis-ci.org/RoySegall/linkedin-python-parser.svg?branch=master)](https://travis-ci.org/RoySegall/linkedin-python-parser)

# Linked in parser

This project parsing LinkedIn profiles.

## Before installing

1. Make sure you have a [RethinkDB](https://www.rethinkdb.com) instance running.
2. Make sure the [geckdriver](https://github.com/mozilla/geckodriver) is located in a place you know
3. Run [Selenium](http://www.seleniumhq.org/) in the background.
4. Register to linkedin and set the user credentials under the
`linkedin` property.

## Settings
Copy the example settings file to a custom one:

`cp settings.example.yml settings.yml`

Edit the settings.

## Installation
```bash
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
Scraping a user is very easy. Create a `POST` request to
`http://localhost:8080/scrape/{user_id}` when `user_id` it's the user
ID.

*You can ge the the user ID from the address.*
