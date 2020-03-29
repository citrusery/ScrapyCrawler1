d:
cd D:\@2020\EXPERIMENT\web_crawler\test1
del scraped_data.json
scrapy crawl Book -o scraped_data.json
python __start__.py