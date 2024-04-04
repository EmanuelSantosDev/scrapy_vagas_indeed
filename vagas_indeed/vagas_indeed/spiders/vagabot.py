import scrapy


class IndeedSpider(scrapy.Spider):

    # identidade do bot
    name = 'indeedbot'

    # request
    def start_requests(self):
        urls = [
            'https://br.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=d8dfc7df48f2446e']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # response
    def parse(self, response):
        for item in response.xpath("//div[@class='job_seen_beacon']"):
            yield {
                'Cargo': item.xpath(".//span[1]/text()").get(),
                'Nome da Empresa': item.xpath(".//span[@data-testid='company-name']/text()").get(),
                'Local': item.xpath(".//div[@data-testid='text-location']/text()").get(),
                'Link para a Vaga': 'https://br.indeed.com' + item.xpath(".//h2/a/@href").get()
            }

        try:
            link_proxima_pagina = response.xpath(
                "//a[@data-testid='pagination-page-next']/@href").get()
            if link_proxima_pagina:
                link_completo = 'https://br.indeed.com' + link_proxima_pagina
                yield scrapy.Request(url=link_completo, callback=self.parse)
        except Exception as error:
            print('CHEGAMOS NA ÚLTIMA PÁGINA')
