# scholar_headgear
NLP course exam:
Protective Headgear: What do people talking about when reviewing products in the context of COVID-19?

## Purpose and overview

This study was set out to investigate costumer experiences with protective headgear during the COVID-19 outbreak. 
Under protective headgear, specifically, we explored reviews of disposable, reusable face masks and face shields. 
The explorative research question was whether we can find topics indicative of barriers and non-barriers to use associated with the three kinds of headgears. 
As reviews were collected from Amazon we had a rich source of metadata accompanying the text (star rating, usefulness, brand, type). 
Thus, we chose the SCHOLAR  (Sparse Contextual Hidden and Observed Language AutoencodeR) neural framework that is built to meaningfully utilize metadata in the process of topic modeling (Card et al., 2017).

## Tools

Data was collected through webscraping using [Scrapy](https://scrapy.org/)
Topic modeling was conducted using [Scholar](https://github.com/dallascard/scholar)

Note: To reproduce this or set up a similar project: follow their installation instructions

## Data collection and description
We chose three brands for each disposable, reusable facemasks, and faceshields from https://www.amazon.com/ (US) among the most popular ones based on the amount of reviews they had.
For each we created a parser (spider) to crawl through the pages and fetch data (9 script in total), see Scraping_example_spider.py for the faceshield brand, Sunzel.
Datasets were merged while adding variables of brand (brand name) and type (disp, reus., shields). This dataset can be found in this repository as DATA_RAW.csv. Description of the chosen brands: chosen_products.pdf
