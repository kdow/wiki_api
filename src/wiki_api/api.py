

class APIWrapper:
    def __init__(self) -> None:
        """
        Constructor for APIWrapper
        """

    def _make_request(
            self,
            endpoint: str,
    ) -> str:
        """
        Private method for API call methods
        """

    def get_most_viewed_articles(
            self,
            year: str,
            month: str,
            day='all-days',
    ) -> dict:
        """
        Retrieves a collection of the most viewed articles for a provided
        month or week.
        """

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
        """

    def get_most_viewed_day(
            self,
            article: str,
            year: str,
            month: str,
    ) -> str:
        """
        Returns the date of the provided month which had the most view counts
        for the requested wiki article.
        """


