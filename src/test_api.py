import pytest
from requests import HTTPError

from api import APIWrapper
from models import Result
from pageview_data import *


@pytest.fixture
def wiki_wrapper():
    """
    Fixture to return instance of API Wrapper class.
    """
    return APIWrapper()


def test___make_request_valid_returns_ok_result(wiki_wrapper):
    """
    Function to test _make_request returns data from wikimedia's API
    """
    result = wiki_wrapper._make_request(
        "top/en.wikipedia.org/all-access/2022/11/all-days"
    )
    assert type(result) is Result
    assert result.status_code == 200
    assert result.data == top_articles_month


def test___make_request_invalid_returns_ok_result(wiki_wrapper):
    """
    Function to test _make_request raises HTTPError if invalid date is provided
    """
    bad_url =  'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/2024/11/all-days' # noqa
    with pytest.raises(HTTPError) as exc_info:
        wiki_wrapper._make_request(
            "top/en.wikipedia.org/all-access/2024/11/all-days"
        )
        raise HTTPError('404 Client Error: Not Found for url: ')
    assert exc_info.type is HTTPError
    assert exc_info.value.args[0] == f"404 Client Error: Not Found for url: " \
                                     f"{bad_url}"


def test_get_most_viewed_articles_returns_collection_for_month(
        wiki_wrapper
):
    """
    Function to test get_most_viewed_articles for a month
    """
    response = wiki_wrapper.get_most_viewed_articles('2022', '11')
    assert type(response) is dict
    assert response == top_articles_month_formatted


def test_get_most_viewed_articles_returns_collection_for_week(
    wiki_wrapper,
):
    """
    Function to test get_most_viewed_articles for a week
    """
    response = wiki_wrapper.get_most_viewed_articles('2022', '11', "01")
    assert type(response) is dict
    assert response == top_articles_week_formatted


def test_get_article_view_count_returns_view_count_for_month(
    wiki_wrapper
):
    """
    Function to test get_article_view_count for a month
    """
    response = wiki_wrapper.get_article_view_count(
        'Danny_Elfman',
        '2021',
        '02'
    )

    assert type(response) is int
    assert response == 89711


def test_get_article_view_count_returns_view_count_for_week(
    wiki_wrapper
):
    """
    Function to test get_article_view_count for a week
    """
    response = wiki_wrapper.get_article_view_count(
        'Uruguay',
        '2018',
        '02',
        '01'
    )

    assert type(response) is int
    assert response == 24122


def test_get_most_viewed_day_returns_date(wiki_wrapper):
    """
    Function to test get_most_viewed_day
    """
    response = wiki_wrapper.get_most_viewed_day('Robot', '2020', '12')

    assert type(response) is str
    assert response == "10"
