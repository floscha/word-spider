import re

import scrapy


def clean_translation(translation):
    """Clean the translation string from unwanted substrings."""
    illegal_substrings = ['; french.languagedaily.com',
                          ';\u00a0french.languagedaily.com',
                          ' french.languagedaily.co']
    for iss in illegal_substrings:
        translation = translation.replace(iss, '')
    return translation


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

            # Ignore empty cells.
            if not cells:
                continue

            # Extract rank or ignore cell otherwise.
            match = re.search(r'(\d+).', cells[0])
            if not match:
                continue
            rank = int(match.group(1))

            # Exctract word and respective translation.
            # Respect that most of the last words (#759+) have no translation.
            if len(cells) == 3:
                word = cells[-2]
                translation = None
            else:
                word = cells[-3]
                translation = cells[-2]
                # Remove unwanted text from translation.
                translation = clean_translation(translation)

            # Extract part-of-speech attributes.
            pos = cells[-1]

            # Assemble vocab dictionary.
            vocab_dict = {'rank': rank,
                          'word': word,
                          'translation': translation,
                          'pos': pos}

            yield vocab_dict
