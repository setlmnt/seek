import scrapy
import json

class Spider(scrapy.Spider):
    name = "zap_imoveis"
    uf = "ba"
    cidade = "vitoria-da-conquista"
    tipo = "aluguel"
    start_urls = [f'http://www.zapimoveis.com.br/{tipo}/imoveis/{uf}+{cidade}/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }

    def parse(self, response):
        imoveis = []

        addresses = response.xpath('*//h2/text()').getall()
        values = response.xpath('*//p[@class="simple-card__price js-price color-darker heading-regular heading-regular__bolder align-left"]/strong/text()').getall()
        size = response.xpath('*//span[@itemprop="floorSize"]/text()').getall()

        for i in range(len(addresses)):
            endereco = addresses[i].strip() if i < len(addresses) else None
            valor = values[i].strip() if i < len(values) else None
            tamanho = size[i].strip() if i < len(size) else None

            imovel = {
                'endereco': endereco,
                'valor': valor,
                'size': tamanho,
            }
            imoveis.append(imovel)

        with open(f'imoveis_{self.cidade}-{self.uf}.json', 'w', encoding='utf-8') as file:
            json.dump(imoveis, file, ensure_ascii=False, indent=4)
