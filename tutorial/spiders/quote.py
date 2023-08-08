import scrapy


class QuoteSpider(scrapy.Spider):
    name = "quote"

    def start_requests(self):
        yield scrapy.Request(
            "http://quotes.toscrape.com/js/",
            meta={"playwright": True},
        )

    def parse(self, response):
        for quote in response.css(".text::text"):
            yield {"quote": quote.get()}

        next_page_url = response.css(".next a::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(
                "http://quotes.toscrape.com" + next_page_url, meta={"playwright": True}
            )
