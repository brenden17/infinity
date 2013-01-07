import numpy as np
import datetime

def datestr2num(s):
    return datetime.datetime.strptime(s, "%d-%m-%Y").date().weekday()

def loaddata():
    dates, close = np.loadtxt('data.csv', delimiter=',', usecols=(1,6), converters={1: datestr2num}, unpack=True)
    print dates
    print close


PCLASS, SURVIVED, SEX, AGE = (0, 1, 3, 4)
CHILD, ADULT = (0, 1)
MALE, FEMALE = (0, 1)

def filter_age(age):
    try: 
        age = float(age)
        return CHILD if age < 15 else ADULT
    except:
        return -1
        
def filter_survived(servive):
    try: 
        return int (servive)
    except:
        return -1
    
filter_data = {PCLASS : None,
               SURVIVED: filter_survived,
               SEX : lambda sex: MALE if sex=='male' else FEMALE,
               AGE : filter_age,
               }

def raw_load_data(filename, flt=None):
    import csv
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        raw_target = []
        raw_data = []
        raw_row = {}
        features = reader.next()[1:]
        for row in reader:
            for i, ele in enumerate(row[1:]):
                if i == SURVIVED:
                    if filter_data[i]:
                        raw_target.append({features[i]:filter_data[i](ele)})
                    else:
                        raw_target.append({features[i]:ele})
                    continue
                if i in filter_data.keys():
                    if filter_data[i]:
                        raw_row.update({features[i]:filter_data[i](ele)})
                    else:
                        raw_row.update({features[i]:ele})
                    continue

            raw_data.append(raw_row)
            raw_row = {}
    return features, raw_target, raw_data


if __name__ == '__main__':
    features, raw_target, raw_data = raw_load_data('titanic.csv')
    print raw_data
    
    
    