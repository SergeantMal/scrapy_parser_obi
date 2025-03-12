import scrapy


class ObisvetnewparsSpider(scrapy.Spider):
    name = "obisvetnewpars"
    allowed_domains = ["obi.ru", "www.obi.ru"]
    start_urls = ["https://obi.ru/osveschenie"]

    def parse(self, response):
        svetilniki = response.css('div.FuS7R')
        for svetilnik in svetilniki:
            name = svetilnik.css('p._1UlGi::text').get()
            price = svetilnik.css('div._1YQve span::text').get()
            link = svetilnik.css('a').attrib['href']

            # Убираем неразрывные пробелы в цене
            if price:
                price = price.replace("\xa0", "")

            yield {
                'name': name,
                'price': price,
                'link': 'https://obi.ru' + link,
            }