import scrapy
from scrapy import Request

from moviecrawler.items import MoviecrawlerItem


class movieScoreSpider(scrapy.Spider):
    name = "moiveSpider"
    # allowed_domains = ["https://www.imdb.cn/"]
    start_urls = [
        "https://www.imdb.cn/movies/?page=1"
    ]
    page = 1

    def parse(self, response):

        item = MoviecrawlerItem()
        item["form"] = response.css('div#genre_list.vsb_main  a::text').extract()[1:]  # 类型
        item["movieName"] = response.css("div.hot_box a img::attr(alt)").extract()   # 电影名
        item["image_urls"] = response.css("div.hot_box a img::attr(src)").extract()  # 图片url
        item["score"] = response.css(".hot_list .img_score::attr(title)").extract()   # 分数

        # yield item
        item["realContentLink"] = response.css(".hot_list .img_box::attr(href)").extract()    # 详情页url
        for i, m, s in zip(item["realContentLink"], item["movieName"], item["score"]):
            newLink = "https://www.imdb.cn" + i   # 拼接详情页

            yield Request(newLink, callback=self.parseRealContent, meta={"mn": m, "score": s})

            # print("==="+newLink)
        prepareLink = response.xpath("//div[@class='hot_page userPage']")[0].xpath("//li")[-1].css("a::attr(href)")[
            0].extract()    # 获取下一页链接

        if prepareLink is not None:   # 判断下一页是否存在
            preNextLink = "https://www.imdb.cn" + prepareLink
            fullNextLink = preNextLink.split("=")[0] + "=" + str(self.page)
            print(fullNextLink)
            self.page += 1
            yield Request(fullNextLink, callback=self.parse)

    def parseRealContent(self, response):
        item = MoviecrawlerItem()
        # movieName = response.meta["mn"]
        movieName = response.meta["mn"]   # 接收电影名
        score = response.meta["score"]  # 接收分数
        item["movieName"] = movieName
        item["score"] = score
        item["daoyan"] = response.xpath("//div[@class='txt_bottom_r txt_bottom_r_overflow']")[0].css(
            "a::text").extract()[0]   # 获取导演
        item["daoyan"] = "".join(item["daoyan"])  # 因为获取是个列表，需要通过字符串拼接
        item["bianju"] = response.xpath("//div[@class='txt_bottom_r txt_bottom_r_overflow']")[1].css(
            "a::text").extract()    # 获取编剧
        item["bianju"] = ",".join(item["bianju"])   # 拼接
        item["zhuyan"] = response.xpath("//div[@class='txt_bottom_r txt_bottom_r_overflow']")[2].css(
            "a::text").extract()   # 获取主演信息
        item["zhuyan"] = ",".join(item["zhuyan"])   # 拼接
        item["type"] = \
            response.xpath("//div[@class='txt_bottom_item']")[3:].xpath("//div[@class='txt_bottom_r']/text()")[
                0].extract().strip()   # 获取类型
        item["country"] = \
            response.xpath("//div[@class='txt_bottom_item']")[3:].xpath("//div[@class='txt_bottom_r']/text()")[
                1].extract().strip()   # 获取国家
        item["language"] = \
            response.xpath("//div[@class='txt_bottom_item']")[3:].xpath("//div[@class='txt_bottom_r']/text()")[
                2].extract().strip()   # 获取电影语言
        item["time"] = \
            response.xpath("//div[@class='txt_bottom_item']")[3:].xpath("//div[@class='txt_bottom_r']/text()")[
                3].extract().strip()   # 获取时间
        item["duration"] = \
            response.xpath("//div[@class='txt_bottom_item']")[3:].xpath("//div[@class='txt_bottom_r']/text()")[
                4].extract().strip()   # 获取电影时长
        # print("item: ==========" + str(item))
        yield item  # 返回到pipeline中，进行数据库操作
