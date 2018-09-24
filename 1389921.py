# 	Name: Alessandro Gallo
# 	Student ID: 1389921
# 	Previous Department: Aerospace Engineering
# 	Kaggle Nickname: Alex Punkallo
# 	Kaggle score: 2.56196

#	In the read_me file the description of every point

import csv
import random
import math
import pandas as pd
from sklearn import preprocessing
from collections import Counter

# 1)

train=pd.read_csv('train.csv', nrows=200, parse_dates = ['Dates'])
test=pd.read_csv('test.csv', nrows=200, parse_dates = ['Dates'])

numb = preprocessing.LabelEncoder()
crime = numb.fit_transform(train.Category)

hour = train.Dates.dt.hour
hour=hour.tolist()
   
days = numb.fit_transform(train.DayOfWeek)
for k in range(len(days)):
    days[k]=days[k]+24

district = numb.fit_transform(train.PdDistrict)
for k in range(len(district)):
    district[k]=district[k]+31

train_data = {'hour' : hour, 'days' : days, 'district' : district, 'crime' : crime}
list_of_field=["hour","days","district"]
train_data=pd.DataFrame(train_data)

cols = train_data.columns.tolist()
cols = cols[-3:] + cols[:-3]
dataset = train_data[cols] 
dataset.to_csv('out.csv',header=None,index=False)

# 2)

dataset = dataset.values.tolist()
dic={}
maxc=max(crime)
for k in range((maxc)+1):
    dic[k]=[]
for k in dataset:
    dic[k[-1]].extend([k[i] for i in range(3)])

for key,val in dic.iteritems():
    dic[key]=Counter(dic[key])

P_C={cl:0 for cl in range(max(crime)+1)}
for item in dataset:
    P_C[item[-1]] += 1

for key in P_C.keys():
    P_C[key]=P_C[key]/float(sum(P_C.values()))

# 3)

for key in dic.keys():
    for key2 in range(41):
        if not(key2 in dic[key]): 
            dic[key][key2]=0
    for key2 in range(41):
        dic [key][key2]+=1

P_I_C={I:{} for I in range(max(crime)+1)}
for key in dic.keys():
    for key2 in dic[key].keys():
        P_I_C[key][key2]=dic[key][key2]/float(sum(dic[key].values()))

# 4)

numb = preprocessing.LabelEncoder()

hour = test.Dates.dt.hour
hour=hour.tolist()
   
days = numb.fit_transform(test.DayOfWeek)
for k in range(len(days)):
    days[k]=days[k]+24

district = numb.fit_transform(test.PdDistrict)
for k in range(len(district)):
    district[k]=district[k]+31

test_data = {'hour' : hour, 'days' : days, 'district' : district}
list_of_field=["hour","days","district"]
test_data=pd.DataFrame(test_data)

cols = test_data.columns.tolist()
cols = cols[-3:] + cols[:-3]
dataset = test_data[cols] 
dataset.to_csv('out2.csv',header=None,index=False)

dataset = dataset.values.tolist()
result=pd.read_csv('submiss.csv')

numb = preprocessing.LabelEncoder()
crime = numb.fit_transform(train.Category)

# 5)

i=0
submit = []
for k in dataset:
    submit.append({"Id": i})
    j=0
    for crime in P_C.keys():
        prob=P_C[crime]
        for f in range(len(k)):
            prob*=P_I_C[crime][f]
        submit[i][numb.classes_[j]]=prob
        j+=1
    i+=1

keys = submit[0].keys()
with open('submiss.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(submit)

