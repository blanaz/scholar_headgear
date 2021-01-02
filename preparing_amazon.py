import re
import collections
import requests
import random
import pandas as pd
import numpy as np
import io

df = pd.read_csv('C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\DATA_ALL.csv')
df(head)


#removing the unnamed column
df = df.drop('Unnamed: 0',axis=1)

#remove all characters from stars column, except for the rating
df.star_rating = df.star_rating.replace('(.)(([0-9])([a-z, ]+))+','', regex = True)
df.date_posted = df.date_posted.replace('(Reviewed in)?(the)?','', regex = True)


#splitting the date_posted column into two columns: date and location
location_date=df.date_posted.str.split(pat = "on", expand = True)
location_date.columns = ['location','date']

#merging the two dataframes
df = pd.concat([df, location_date], axis = 1, sort = False)

# delete date_posted column
df = df.drop('date_posted',axis=1)

#removing all the data that's not from the US 
df.location
index_countries = df[ df['location'] != "  United States " ].index 
print(index_countries)
df.drop(index_countries, inplace = True)

#now that we have only US data, we delete the location column cause we don't need it.
df = df.drop('location',axis=1)

# next step: date. we want to cut off at 2020
print(df.date[1])

#splitting the date_posted column into two columns: date and location
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

#usefulness
print(df.usefulness[10])

df.usefulness = df.usefulness.replace('(One)(.*)','1', regex = True)
df.usefulness = df.usefulness.replace('( people found this helpful)','', regex = True)

#saving data
#df.to_csv(path_or_buf='C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df.csv')

#read df
#df = pd.read_csv('C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df.csv')
#deleting extra indexing column
#df = df.drop('Unnamed: 0',axis=1)

###Changing stars and usefulness from string to number
df['star_rating'] = df['star_rating'].astype(int)
type(df['star_rating'])

#checking for the non numeric characters that cause error
non_numeric = re.compile(r'[^\d.]+')
df.loc[df['usefulness'].str.contains(non_numeric)]

#cleaning usefulnesss column from commas
df['usefulness'] = df.usefulness.replace((','), '', regex = True)

df['usefulness'] = pd.to_numeric(df['usefulness'])

#cleaning non english things
#check for spelling mistakes

from langdetect import detect

# iterating through each line of the dataset, detecting language in the
# comment, add the detection to a list and then instert the list to the data
# in a new column


lang=[]
temp=[]
for index, row in df.iterrows():
    temp = index, row['comment']
    lang.append(detect(str(temp)))
df.insert(7, 'lang', value=lang)



# #saving data
# #df.to_csv(path_or_buf='C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df_index_problem.csv')
# #read df
# df = pd.read_csv('C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df_index_problem.csv')
# # looking at the comments where non-english language was detected



# by looping through each row, looking at the lang variable, if matched
# then appended to a list that we look at 


vis=[]
for index, row in df.iterrows():
    if row["lang"]== "cy":
        temp = (index, row['comment'],row['lang'])
        vis.append(temp)

print(vis)

print(df[,2])
# we need to delete all es comments and rows:
# 17 rows will be dropped (that are spanish, not "welsh")
index_cy = [1105, 4052, 4074, 5356, 5452, 5805, 5833, 5897, 5959, 5999, 7399, 11382, 11540, 11572, 11679, 13425]
df.drop(index_cy, inplace = True)

#removing all the data that's es (57)
index_lang = df[ df['lang'] == "es" ].index
print(index_lang)
df.drop(index_lang, inplace = True)


#now that we have only US data, we delete the location column cause we don't need it.
df = df.drop('lang',axis=1)
df = df.drop('Unnamed: 0.1', axis = 1)

#merging the titles and the reviews
df["text"] = df["title"] + df["comment"]

df = df.drop('title',axis=1)
df = df.drop('comment', axis = 1)


#saving data
#df.to_csv(path_or_buf='C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df_fixed_language.csv')


# we realized that there's still some spanish in there, so let's run the language detect again
#df = pd.read_csv('C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\df.csv')

from langdetect import detect

# iterating through each line of the dataset, detecting language in the
# comment, add the detection to a list and then instert the list to the data
# in a new column
df = df.drop('lang', axis = 1)
lang=[]
temp=[]
for index, row in df.iterrows():
    temp = index, row['text']
    lang.append(detect(str(temp)))
df.insert(6, 'lang', value=lang)

# by looping through each row, looking at the lang variable, if matched
# then appended to a list that we look at 

vis=[]
for index, row in df.iterrows():
    if row["lang"]== "cy":
        temp = (index, row['text'],row['lang'])
        vis.append(temp)


#after everything we've been through we still found 1 spanish and 1 spanish in welsh so we're deleting them now
index_leftover_spanish = [313,7310]
df.drop(index_leftover_spanish, inplace = True)

#after one more round
index_leftover_spanish = [7086]
df.drop(index_leftover_spanish, inplace = True)



#saving data
df.to_csv(path_or_buf='C:\\Users\\blank\\OneDrive\\Dokumentumok\\CogsciMaster\\NLP\\Exam\\scraping\\theone\\data\\cleaned_data.csv')
