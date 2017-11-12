fpath=$1

# Delete old data.
rm $fpath

# Scrape 1000 most common words and save to JSON file.
scrapy runspider word_spider.py -o $fpath

# Sort the words by rank.
python sort_json.py $fpath

# Validate that all ranks from 1 to 1000 exist.
python validate.py $fpath
