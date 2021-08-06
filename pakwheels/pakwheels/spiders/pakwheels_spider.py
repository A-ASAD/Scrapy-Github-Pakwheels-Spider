import scrapy


class PakWheelsSpider(scrapy.Spider):
    name = "pakwheels"

    start_urls = [
        'https://www.pakwheels.com/new-cars/',
    ]

    def start_requests(self):
        urls = [
            'https://www.pakwheels.com/new-cars/',
            'https://www.pakwheels.com/used-cars/',
        ]
        for url in urls:
            if url == 'https://www.pakwheels.com/new-cars/':
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_newly_launched_cars
                    )
            else:
                yield scrapy.Request(url=url, callback=self.parse_used_cars)

    def parse_newly_launched_cars(self, response):
        """
        Extracts and follows links for newly launched cars

        Arguments:
            self: object
            response: Response object

        Yields:
            Request object for car details link
        """

        cars_info = response.css('#newly_launched a.cards')
        yield from response.follow_all(
            cars_info,
            callback=self.parse_new_car_details
            )

    def parse_used_cars(self, response):
        """
        Extracts and follows links for used cars

        Arguments:
            self: object
            response: Response object

        Yields:
            Request object for car details link
        """

        cars_info = response.css('.img-box a')
        yield from response.follow_all(
            cars_info,
            callback=self.parse_old_car_details
            )

    def parse_old_car_details(self, response):
        """
        Yields description of the used car

        Arguments:
            self: object
            response: Response object

        Yields:
            Car details
        """

        car_name = response.css('#scroll_car_info h1::text').get()
        price = response.css('strong.generic-green::text').get()
        # omit 'Lacs' if price not provided
        price = price + ' Lacs' if price.split()[0] == 'PKR' else price
        image_selector = f'[alt="{car_name} Image-1"]::attr(src)'
        image_url = response.css(image_selector).get()
        features = response.css('.car-feature-list li::text').getall()
        features = (
            ', '.join(map(str.strip, features)) or
            'No features provided'
            )

        yield {
            'car_name': car_name,
            'price': price,
            'condition': 'Old',
            'image_url': image_url,
            'features': features
        }

    def parse_new_car_details(self, response):
        """
        Yields description of the newly launched car

        Arguments:
            self: object
            response: Response object

        Yields:
            Car details
        """

        car_name = response.css("h1.nomargin::text").get().split('Price')[0]
        price = response.css('.fs22::text').get()
        image_url = response.css('#image-gallery li')[0].css(
            'img::attr(src)').get()
        features = response.xpath(
            "//div[@class = 'gen_desc_large']/descendant::text()"
            ).getall()
        features = (
            ''.join(map(str.strip, features)) or
            'No features provided'
            )

        yield {
            'car_name': car_name,
            'price': 'PKR ' + price + ' Lacs',
            'condition': 'New',
            'image_url': image_url,
            'features': features
        }
