# scholar_headgear
Protective Headgear: What do people talk about when reviewing products in the context of COVID-19?

## Purpose and overview

This study was set out to investigate costumer experiences with protective headgear during the COVID-19 outbreak. 
Under protective headgear, specifically, we explored reviews of disposable, reusable face masks and face shields. 
The explorative research question was whether we can find topics indicative of barriers and non-barriers to use associated with the three kinds of headgears. 
As reviews were collected from Amazon we had a rich source of metadata accompanying the text (star rating, usefulness, brand, type). 
Thus, we chose the SCHOLAR  (Sparse Contextual Hidden and Observed Language AutoencodeR) neural framework that is built to meaningfully utilize metadata in the process of topic modeling (Card et al., 2017).

## Tools

- Data was collected through webscraping using [Scrapy](https://scrapy.org/)
- Topic modeling was conducted using [Scholar](https://github.com/dallascard/scholar)

Note: To reproduce this or set up a similar project: follow their installation instructions

## Data collection and description
We chose three brands for each disposable, reusable facemasks, and faceshields from https://www.amazon.com/ (US) among the most popular ones based on the amount of reviews they had.
For each we created a parser (spider) to crawl through the pages and fetch data (9 script in total), see Scraping_example_spider.py for the faceshield brand, Sunzel.
Datasets were merged while adding variables of brand (brand name) and type (disp, reus., shields). This dataset can be found in this repository as DATA_RAW.csv. Description of the chosen brands:
![data_description](/chosen_products.png)

### Data cleaning
Reviews from outside of the US excluded.
Reviews before 2020 excluded.
Non-english reviews excluded (as much as possible, but not perfect).
Title and main text of the reviews merged into one text column.
Star ratings converted to numbers and stripped from text.
After plotting and considering the meaning of useful votes, they were transformed into a binary factor (if 0 votes = not useful (0), if 1=< = useful (1)).
Training and testing data was split using [sklearn](https://scikit-learn.org/stable/): 80% training, 20% testing
Then train and test dataset transformed into json files for modeling: df_train.json, and df_test.json

### Preprocessing and modeling (file: scholar_facegear.ipynb)
Preprocessing with Scholar: cleaning text from nonalphabetical characters, lowercasing, tokenizing, and stopwords removal (snowball)
- -- min doc count: 4, minimum times a word has to appear across documents to be included
- -- label: type,brand,star_rating,usefulness - metadata, creating a 'postings list' with document indices and binary variable where it belongs
- -- keep alphanum True: keep words with numbers and letters mixed in it
- -- test ft_test.json : precprocessing the test and train sets simulatiosuly
outputs of the preprocessing and background frequency distributions across documents, topics, and words (for both train and test): preproc_output/

2 models were chosen to analyze and compare based on perplexity, coherence, and most importantly qualitative interpretation (whether topics made sense):
- -- model without metadata: exploration of meaningful topics across metadata
- -- model with metadata: type as label, star_rating as a covariate and as an interaction with type --> these specific inclusions of variables were informed by the relationships we saw in the model without metadata:
how topics are distributed across metadata classes and what makes sense in interpretation, e.g. that some types are more liked than others - interaction effect of sentiment (star rating) and type, some topics are more positively than negatively charged, topics are indicative of type of headgear which has also been the goal of our project

Outputs of modeling: output_without_metadata/, output_with_metadata/

Evaluation: perplexity, topic coherence with internal npmi (test set), plotting distribution of topics accross all metadata 
+ with metadata: predictive accuracy of topics on labels (type)

## Highlights of findings
(Non)Barriers found with fairly high topic coherence and straightforward qualitative interpretation:
- visibility through faceshields
- quality of earloops of masks
- fogging of glasses with masks
- melting of faceshields on hot summer days
- size and fit for different people (mostly talked about: kids & men with beards)
- caring for reusable masks or even utilising skrinking for fit (washing, drying, color)
+ additional sub findings: facial expressions and echo (~faceshileds)

"The present study contributes to the field of researching the public discourse around wearing protective headgear in two ways: 1) shedding light on some of the barriers associated with wearing different types of headgear, 2) offering some limited insights into the needs of certain populations and specific social situations that could use some attention."

see the whole analysis, findings and interpretations: NLP2020_Zana_Barrett_Palfi_gr12.pdf

### Thanks to
The present project is built upon this amazing work: 
Dallas Card, Chenhao Tan, and Noah A. Smith. Neural Models for Documents with Metadata. In Proceedings of ACL (2018)

### Cite this
Barrett, K. N., Palfi, B. S., Zana, B. (2020). Protective Headgear: What do people talk about when reviewing products in the context of COVID-19?. [Unpublished]. Department of Linguistics, Cognitive Science and Semiotics, Aarhus University.

