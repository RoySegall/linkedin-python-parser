# Linked in parser

This project parsing LinkedIn profiles.

## Before installing

1. Make sure you have a [RethinkDB](https://www.rethinkdb.com) instance running.
2. Make sure the [geckdriver](https://github.com/mozilla/geckodriver) is located in a place you know

## Settings
Copy the example settings file to a custom one:

`cp settings.example.yml settings.yml`

Edit the settings.

## Installation
```bash
pip3 install -r /path/to/requirements.txt
python install.py
```

## Finally
Run the server:
```bash
apistar run
```

Awesome! Have a slice of pizza: :pizza:
