import pymongo
import charts

client = pymongo.MongoClient('localhost',27017)
doubantop250 = client['doubantop250']
detail = doubantop250['detail']

list =[]
for item in detail.find().limit(50):
    list.append(item['评分'])

name_list = []
for item in detail.find():
    name_list.append(item['片名'])

intlist =[float(x) for x in list]

def data_gen (types):
    length = 0
    if length < len(name_list):
        for name,score in zip(name_list,intlist):
            data ={
                'name':name,
                'data':[score],
                'type':types
            }
            yield data
            length += 1


series = [data for data in data_gen('column')]
charts.plot(series, show='inline', options=dict(title=dict(text='电影评分')))