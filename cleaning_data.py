#%% importing packages
import re #regex
import collections #for storing collections of data
import random #random number generator
import pandas as pd #pandas for dataframes
import numpy as np #numpy for numpy lists

#%% reading the data in
untouched=pd.read_csv('/Users/Blanka/Desktop/NLP/NLP_exam/fm_2/data/DATA_RAW.csv')
df = pd.read_csv('/Users/Blanka/Desktop/NLP/NLP_exam/fm_2/data/DATA_RAW.csv')
df.head()
#removing the unnamed column
df = df.drop('Unnamed: 0',axis=1)

#%%
#---------------Remove all additional alphabetical characters in columns where we don't need them
#star_rating 'X' out of 5 stars -> 'X'
df.star_rating = df.star_rating.replace('(.)(([0-9])([a-z, ]+))+','', regex = True)
#usefulness: One -> 1, 'X' people found this helpful -> 'X'
df.usefulness = df.usefulness.replace('(One)(.*)','1', regex = True)
df.usefulness = df.usefulness.replace('( people found this helpful)','', regex = True)
#date and location: Reviewed in (the) 'X' on 'Y' -> 'X on Y'
df.date_posted = df.date_posted.replace('(Reviewed in)?(the)?','', regex = True)

#%%
#------------------------------Date and location: excluding not from US and before 2020
#splitting the date_posted column into two columns: date and location
location_date=df.date_posted.str.split(pat = "on", expand = True)
location_date.columns = ['location','date']
#merging the two dataframes: original and new with date and location
df = pd.concat([df, location_date], axis = 1, sort = False)
# delete date_posted column - original column with both information
df = df.drop('date_posted',axis=1)

#removing all the data that's not from the US 
df.location
index_countries = df[ df['location'] != "  United States " ].index 
print(index_countries)
df.drop(index_countries, inplace = True)
#now that we have only US data, we delete the location column cause we don't need it.
df = df.drop('location',axis=1)

#%%
# next step: date. we want to cut off at 2020
#splitting the date_posted column into two columns: month & day, year
date=df.date.str.split(pat = ", ", expand = True)
date.columns = ['month_day','year']
#merging the two dataframes
df = pd.concat([df, date], axis = 1, sort = False)
# delete date_posted column
df = df.drop('date',axis=1)

#delete comments that were written before 2020
print(df.year)
index_year = df[ df['year'] != "2020" ].index
print(index_year) #looks like there is none
df.drop(index_year, inplace = True)
#delete the year column cause we don't need it
df = df.drop('year',axis=1)

#%%
###--------------------Changing stars and usefulness from text to number
df['star_rating'] = df['star_rating'].astype(int)
type(df.star_rating[1]) #checking

#checking for the non numeric characters that cause error with usefulness
non_numeric = re.compile(r'[^\d.]+')
df.loc[df['usefulness'].str.contains(non_numeric)]

#cleaning usefulnesss column from commas (identified to cause the errors)
df['usefulness'] = df.usefulness.replace((','), '', regex = True)
#changing strings to integers in usefulness votes
df['usefulness'] = pd.to_numeric(df['usefulness'])

#%%
#---------------Cleaning non english reviews as much as we can
from langdetect import detect #nltk's language detector package

# iterating through each line of the dataset, detecting language in the comment, add the detection to a list and then instert the list to the data in a new column
lang=[]
temp=[]
for index, row in df.iterrows():
    temp = index, row['comment']
    lang.append(detect(str(temp)))
df.insert(7, 'lang', value=lang)

# looking at the comments where non-english language was detected using langdetect's labels
# by looping through each row, looking at the lang variable, if matched then appended to a list that we look at 
vis=[]
for index, row in df.iterrows():
    if row["lang"]== "cy": #'cy' is one of langdetect's language labels (we changed this iteratively to check all)
        temp = (index, row['comment'],row['lang'])
        vis.append(temp)
print(vis)

print(df[,2])
# we need to delete all spanish comments and rows:
# 17 rows will be dropped (that are spanish identified as "welsh" by langdetect)
index_cy = [1105, 4052, 4074, 5356, 5452, 5805, 5833, 5897, 5959, 5999, 7399, 11382, 11540, 11572, 11679, 13425]
df.drop(index_cy, inplace = True)

#removing all the data that's identified and are 'es' (57) (spanish)
index_lang = df[ df['lang'] == "es" ].index
print(index_lang)
df.drop(index_lang, inplace = True)

#deleting language column, as we don't need it any longer
df = df.drop('lang',axis=1)
#df = df.drop('Unnamed: 0.1', axis = 1)

#%%
#----------------------------Merging the titles and the reviews
df["text"] = df["title"] + df["comment"]
#dropping original not merged
df = df.drop('title',axis=1)
df = df.drop('comment', axis = 1)

#%%
#-----------------------------Language detection one more time again to exclude even more spanish reviews that have not been excluded yet
# when doing topic modeling on Kam's computer on the 1st of dec
# we realized that there's still some spanish in there, so let's run the language detect again

df = df.drop('lang', axis = 1)
lang=[]
temp=[]
for index, row in df.iterrows():
    temp = index, row['text']
    lang.append(detect(str(temp)))
df.insert(6, 'lang', value=lang)

vis=[]
for index, row in df.iterrows():
    if row["lang"]== "cy":
        temp = (index, row['text'],row['lang'])
        vis.append(temp)


#after everything we've been through we still found 2 spanish reviews in welsh so we're deleting them now
index_leftover_spanish = [313,7310]
df.drop(index_leftover_spanish, inplace = True)

#after one more round
index_leftover_spanish = [7086]
df.drop(index_leftover_spanish, inplace = True)

#saving data
df.to_csv(path_or_buf='C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\data_cleaned.csv')