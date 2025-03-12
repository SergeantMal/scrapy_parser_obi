import scrapy


class ObisvetnewparsSpider(scrapy.Spider):
    name = "obisvetnewpars"
    allowed_domains = ["obi.ru", "www.obi.ru"]
    start_urls = ["https://obi.ru/osveschenie"]

    def parse(self, response):
        # Ограничиваем область парсинга товарами ДО блока с популярными товарами
        product_section = response.css('div._3yNpa div.FuS7R')



        for svetilnik in product_section:
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

        # Пагинация: проверяем, есть ли следующая страница
        current_page = response.url.split("page=")[-1] if "page=" in response.url else "1"
        current_page = int(current_page)

        if current_page < 69:  # Лимит страниц
            next_page = f"https://obi.ru/osveschenie?page={current_page + 1}"
            yield response.follow(next_page, callback=self.parse)

