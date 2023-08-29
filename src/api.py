from calendar import monthrange
from datetime import datetime, timedelta
from requests import get

from models import Result


class APIWrapper:
    def __init__(self) -> None:
        """
        Constructor for APIWrapper
        """
        self.base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        self.headers = {
            'User-Agent': 'WikiAPIProject/0.1 (kedownes@gmail.com)'
        }

    def _make_request(
            self,
            endpoint: str,
    ) -> Result:
        """
        Private method for API call methods

        :param endpoint: URL Endpoint as a string

        :return: a Result object
        """
        response = get(f"{self.base_url}{endpoint}", headers=self.headers)
        data_out = response.json()
        result = Result(
            response.status_code,
            headers=response.headers,
            message=response.reason,
            data=data_out
        )
        return result if response.ok else response.raise_for_status()

    def get_most_viewed_articles(
            self,
            year: str,
            month: str,
            day='all-days',
    ) -> dict:
        """
        Retrieves a collection of the most viewed articles for a provided
        month or week.

        This call defaults to a monthly time period if day is not provided.

        :param year: The four-digit date of the desired year
        :param month: The two-digit date of the desired month
        :param day: Optional; The two-digit date of the first day of the
        desired week

        :return: Dictionary of most viewed articles for the provided date.
        Article titles are the keys, and their associated view counts are the
        values.
        """
        if day != 'all-days':
            week = 7
            start_date = datetime(int(year), int(month), int(day))
            date_list = [
                (start_date + timedelta(days=day)) for day in range(week)
            ]
            most_viewed = {}
            for date in date_list:
                endpoint = f"top/en.wikipedia.org/all-access/{date.year}/{date.strftime('%m')}/{date.strftime('%d')}" # noqa
                response = self._make_request(endpoint)
                most_viewed[date.day] = (response.data['items'][0]['articles'])
            result = {}
            for day in most_viewed:
                for article in most_viewed[day]:
                    result.setdefault(article['article'], 0)
                    result[article['article']] += article['views']
            return result
        else:
            endpoint = f"top/en.wikipedia.org/all-access/{year}/{month}/{day}"
            response = self._make_request(endpoint)
            result = {}
            for article in response.data['items'][0]['articles']:
                result[article['article']] = article['views']
            return result

    def get_article_view_count(
            self,
            article: str,
            year: str,
            month: str,
            day='all-days',
    ) -> int:
        """
        Returns the view count of the requested wiki article for the provided
        month or week.

        This call defaults to a monthly time period if day is not provided.

        :param article: The article title as it appears in the URL slug
        :param year: The four-digit date of the desired year
        :param month: The two-digit date of the desired month
        :param day: Optional; The two-digit date of the first day of the
        desired week

        :return: Integer of the view count of the requested article and
        timespan.
        """
        if day != 'all-days':
            num_days = 6
            start_date = datetime(int(year), int(month), int(day))
            end_date = start_date + timedelta(days=num_days)
            endpoint = f"per-article/en.wikipedia.org/all-access/all-agents/{article}/daily/{start_date.strftime('%Y%m%d%H')}/{end_date.strftime('%Y%m%d%H')}" # noqa
            response = self._make_request(endpoint)
            view_count = 0
            for day in response.data['items']:
                view_count += int(day['views'])
            return view_count
        else:
            num_days = monthrange(int(year), int(month))[1]
            start_date = datetime(int(year), int(month), 1)
            end_date = start_date + timedelta(days=num_days)
            endpoint = f"per-article/en.wikipedia.org/all-access/all-agents/{article}/monthly/{start_date.strftime('%Y%m%d%H')}/{end_date.strftime('%Y%m%d%H')}" # noqa
            response = self._make_request(endpoint)
            return response.data['items'][0]['views']

    def get_most_viewed_day(
            self,
            article: str,
            year: str,
            month: str,
    ) -> str:
        """
        Returns the date of the provided month which had the most view counts
        for the requested wiki article.

        :param article: The article title as it appears in the URL slug
        :param year: The four-digit date of the desired year
        :param month: The two-digit date of the desired month

        :return: String of the day of the provided month which had the most
         views for the wiki article.
        """
        num_days = monthrange(int(year), int(month))[1]
        start_date = datetime(int(year), int(month), 1)
        end_date = start_date + timedelta(days=num_days)
        endpoint = f"per-article/en.wikipedia.org/all-access/all-agents/{article}/daily/{start_date.strftime('%Y%m%d%H')}/{end_date.strftime('%Y%m%d%H')}" # noqa
        response = self._make_request(endpoint)
        response_items = response.data['items']
        max_views = max(response_items, key=lambda item: item['views'])

        return max_views['timestamp'][6:8]
