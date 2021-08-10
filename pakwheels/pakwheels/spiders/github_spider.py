import scrapy
from scrapy.http import FormRequest
import os
from dotenv import load_dotenv

load_dotenv()

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

        authenticity_token = response.xpath(
            '//input[@name="authenticity_token"]/@value'
            ).get()

        return [FormRequest.from_response(
            response,
            url='https://github.com/session',
            method="POST",
            formdata={
                'authenticity_token': authenticity_token,

                # your login here (email/username)
                'login': os.getenv('LOGIN'),

                # your password here
                'password': os.getenv('PASSWORD')

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
            callback=self.parse_user_data
            )

    def parse_user_data(self, response):
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

        name = response.xpath(
            '//span[contains(@class, "p-name")]/text()'
            ).get().strip()
        nickname = response.xpath(
            '//span[contains(@class, "p-nickname")]/text()'
            ).get().strip()
        followers, following, stars = response.xpath(
            '//span[@class="text-bold color-text-primary"]/text()'
            ).getall()
        repositories = response.xpath(
            '//div[@id="user-repositories-list"]//'
            'a[@itemprop="name codeRepository"]/text()'
            ).getall()
        repositories = ', '.join(map(str.strip, repositories))

        print( {
            'name': name,
            'nickname': nickname,
            'followers': followers,
            'following': following,
            'stars': stars,
            'repositories': repositories
        })
