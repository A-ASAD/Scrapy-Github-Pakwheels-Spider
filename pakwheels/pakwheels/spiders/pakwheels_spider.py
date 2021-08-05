import scrapy


class PakWheelsSpider(scrapy.Spider):
    name = "pakwheels"

    start_urls = [
        'https://www.pakwheels.com/new-cars/',
    ]

    def parse(self, response):
        """
        Extracts and follows links for car details

        Arguments:
            self: object
            response: Response object
        """

        cars_info = response.css('#newly_launched a.cards')
        yield from response.follow_all(
            cars_info,
            callback=self.parse_car_description
            )

    def parse_car_description(self, response):
        """
        Prints description of the car

        Arguments:
            self: object
            response: Response object
        """

        car_name = response.css("h1.nomargin::text").get()
        price = response.css('.fs22::text').get()
        car_description = response.xpath(
            "//div[@class = 'gen_desc_large']/descendant::text()"
            ).getall()
        print('Name:', car_name.split('Price')[0])
        print('Price: PKR', price, 'LACS')
        print(''.join(map(str.strip, car_description)) or
              'No description provided', '\n\n'
              )
