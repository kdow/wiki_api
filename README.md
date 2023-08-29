# Wikimedia Pageview API

This is a wrapper API for the 
[Wikimedia Pageview API](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews). Three APIs are provided which 
will allow users to do the following:
- `get_most_viewed_articles`: Get a list of the most viewed articles for a week or a month.
- `get_article_view_count`: Get the view count for an article for a week or a month.
- `get_most_viewed_day`: Get the date of a month when an article had the most page views.

## Setup Instructions
### Installation Requirements
This code should be run using Python 3. Python 3.11 was the version used to write and run this code, but any 
Python 3.x version should work.

To check any python versions currently installed:
```shell
python --version
python2 --version
python3 --version
```

If python or python3 do not show a 3.x version, it will need to be installed. 

To install on macOS:
```shell
brew install python
```
Or find other installation options at [python.org](https://www.python.org/downloads/)

Python commands will be run with either `python` as shown in the examples below, `python3`, or `py`  depending on your
operating system and how python was set up.


Necessary packages are listed in `requirements.txt` and can be installed with pip. To install them all, run:
```shell
python -m pip install -r requirements.txt
```
If pip is not installed, you can follow the instructions [here](https://pip.pypa.io/en/stable/installation/), and then
run the above command.


### How to run

The API calls can be made using the python interpreter. To open run:
```shell
python
```

Import the `api.py` file:
```shell
import api
```

Create an instance of the API wrapper class:
```shell
wiki_api = api.APIWrapper()
```

To call the APIs, see examples below and replace arguments as desired:

#### get_most_viewed_articles
To run `get_most_viewed_articles`, use the following command (replacing year/month/day as desired; see examples below): 
`wiki_api.get_most_viewed_articles({year}{month}{*day})'`

Example `get_most_viewed_articles` call for a **month**:
```shell
wiki_api.get_most_viewed_articles('2022','11')
```

Example `get_most_viewed_articles` call for a **week**:
```shell
wiki_api.get_most_viewed_articles('2022','11','01')
```


#### get_article_view_count

Example `get_article_view_count` call for a **month**:
```shell
wiki_api.get_article_view_count('Uruguay','2018','02')
```

Example `get_article_view_count` call for a **week**:
```shell
wiki_api.get_article_view_count('Ryan_Gosling','2022','07', day='01')
```


#### get_most_viewed_day

Example `get_most_viewed_day` call:
```shell
wiki_api.get_most_viewed_day('Robot','2020','12')
```

To exit the python interpreter:
```shell
exit()
```

### Testing
Unit tests can be run using pytest from the command line within the `src/` directory:
```shell
cd src
pytest --cov
```