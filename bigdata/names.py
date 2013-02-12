import pandas as pd
import matplotlib.pyplot as plt

def get_names():
    '''
    name_dir = '/media/main/data/source/pydata-book-master/ch02/names/'
    names1880 = pd.read_csv(name_dir+'yob1880.txt', names=['names', 'sex',
'births'])
    print names1880
    print names1880.groupby('sex').births.sum()
    '''
    years = range(1880, 2011)
    pieces = []
    columns = ['name', 'sex', 'births']

    name_dir = '/media/main/data/source/pydata-book-master/ch02/names/yob%d.txt'
    for year in years:
        path = name_dir % year
        frame = pd.read_csv(path, names=columns)
        frame['year'] = year
        pieces.append(frame)
    names = pd.concat(pieces, ignore_index=True)
    return names
    '''
    total_births = names.pivot_table('births', rows='year', cols='sex',
aggfunc=sum)

    total_births.plot(title='Total births by sex and year')
    plt.show()
    '''

    '''
    def add_prop(group):
        births = group.births.astype(float)
        group['prop'] = births / births.sum()
        return group

    names = names.groupby(['year', 'sex']).apply(add_prop)
    print names
    '''

def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]

def get_top():
    names = get_names()
    grouped = names.groupby(['year', 'sex'])
    top1000 = grouped.apply(get_top1000)
    boys = top1000[top1000.sex=='M']
    total_births = top1000.pivot_table('births', rows='year', cols='name',
aggfunc=sum)
    subset = total_births[['Brenden', 'Jessica', 'Dayna','Kate']]
    print subset
    subset.plot(subplots=True, figsize=(12,10), grid=False, title="nm")
    plt.show()
if __name__=='__main__':
    get_top()
