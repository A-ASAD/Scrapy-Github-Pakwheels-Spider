import scrapy
from scrapy.http import FormRequest


class GithubSpider(scrapy.Spider):
    name = "github"

    start_urls = [
        'https://github.com/login',
    ]

    def parse(self, response):
        """
        Logs into the github

        Arguments:
            self
            response:
                Response object

        Returns:
            Form request for login
        """

        authenticity_token = response.css(
            '[name=authenticity_token]::attr(value)'
            ).get()

        return [FormRequest.from_response(
            response,
            url='https://github.com/session',
            method="POST",
            formdata={
                'authenticity_token': authenticity_token,

                # your login here (email/username)
                'login': '',

                # your password here
                'password': ''

            },
            callback=self.parse_github
        )]

    def parse_github(self, response):
        """
        Navigates to repositories page

        Arguments:
            self
            response:
                Response object
        """

        yield response.follow(
            'https://github.com/A-ASAD?tab=repositories',
            callback=self.parse_menu
            )

    def parse_menu(self, response):
        """
        Parses profile opafe and yields data

        Arguments:
            self
            response:
                Response object

        Yields:
            User data (name, nickname, followers, following, stars,
            repositories)
        """

        name = response.css('.p-name::text').get().strip()
        nickname = response.css('.p-nickname::text').get().strip()
        followers, following, stars = response.css(
            'span.text-bold.color-text-primary::text'
            ).getall()
        repositories = response.css(
            '#user-repositories-list a[itemprop="name codeRepository"]::text'
            ).getall()
        repositories = ', '.join(map(str.strip, repositories))

        yield {
            'name': name,
            'nickname': nickname,
            'followers': followers,
            'following': following,
            'stars': stars,
            'repositories': repositories
        }
