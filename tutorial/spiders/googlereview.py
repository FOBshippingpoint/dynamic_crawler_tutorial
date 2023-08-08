import scrapy
from scrapy_playwright.page import PageMethod

def scroll_actions(times):
    actions = []
    for _ in range(times):
        # 向下滾動評論區塊
        actions.append(
            PageMethod(
                "evaluate",
                'document.querySelector("div.m6QErb:nth-child(2)").scrollBy(0, 10000)',
            )
        )
        # 等待1秒鐘讓評論載入
        actions.append(PageMethod("wait_for_timeout", 1000))
    return actions


class GooglereviewSpider(scrapy.Spider):
    name = "googlereview"
    allowed_domains = ["www.google.com"]

    def start_requests(self):
        yield scrapy.Request(
            "https://www.google.com/maps/place/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/@24.9681606,121.1927239,17z/data=!4m8!3m7!1s0x346823c1ec904dcb:0xcdc129d4455ce456!8m2!3d24.9681558!4d121.1952988!9m1!1b1!16zL20vMDJ2dmx4?entry=ttu",
            meta={
                "playwright": True,
                "playwright_page_methods": scroll_actions(10), # 向下滾動並等待1秒，重複10次
                "playwright_context_kwargs": {
                    "record_video_dir": "./", # 瀏覽過程影片存檔路徑
                },
            },
        )

    def parse(self, response):
        for review in response.css("div.jftiEf"):
            yield {
                # 評論者名字 ::text 代表取得文字
                "reviewer": review.css(".d4r55::text").get(),
                # 評論星級 ::attr(aria-label) 代表取得此元素的aria-label屬性值
                "stars": review.css(".kvMYJc::attr(aria-label)").get(),
                # 評論時間
                "time": review.css(".rsqaWe::text").get(),
                # 評論內容
                "content": review.css(".wiI7pd::text").get(),
            }
