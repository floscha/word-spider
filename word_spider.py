import re

import scrapy


class WordSpider(scrapy.Spider):
    name = 'wordspider'

    # Set up messy page names.
    base_url = 'http://french.languagedaily.com/wordsandphrases/'
    start_urls = [base_url + 'most-common-words',
                  base_url + 'common-french-words']
    for i in range(3, 13):
        if i == 4:
            start_urls.append(base_url + 'most-common-french-words')
        else:
            start_urls.append('%s-%d' % (start_urls[0], i))

    def parse(self, response):
        rows = response.xpath('//table[@class="vocabulary"]/tbody/tr')

        for row in rows:
            cells = row.xpath('td/text()').extract()
            if not cells:
                continue
            match = re.search(r'(\d+).', cells[0])
            if not match:
                continue
            rank = int(match.group(1))

            # Cut off useless leading cells.
            cells = cells[-3:]

            word = cells[0]
            translation = cells[1]
            pos = cells[2]
            yield {'rank': rank,
                   'word': word,
                   'translation': translation,
                   'pos': pos}
