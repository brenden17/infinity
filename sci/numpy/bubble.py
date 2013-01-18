from pylab import *
from scipy import *
import pandas as pd


def load():
    infile = 'crime2005.csv'
    rdata = genfromtxt(infile, dtype='S8,f,f,f,f,f,f,f,i', delimiter=',')

    rdata[0] = zeros(8) # cutting the label's titles
    rdata[1] = zeros(8) # cutting the global statistics

    x = []
    y = []
    color = []
    area = []

    for data in rdata:
        x.append(data[1]) # murder
        y.append(data[5]) # burglary
        color.append(data[6]) # larceny_theft 
        area.append(sqrt(data[8])) # population
        # plotting the first eigth letters of the state's name
        text(data[1], data[5], 
             data[0],size=11,horizontalalignment='center')

    # making the scatter plot
    sct = scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)

    axis([0,11,200,1280])
    xlabel('Murders per 100,000 population')
    ylabel('Burglaries per 100,000 population')
    show()


def load_pd():
    import pandas as pd
    data = pd.read_csv('crime2005.csv')[1:]
    text(data.murder.values, data.burglary.values, 
             size=11,horizontalalignment='center')
    sct = scatter(data.murder.values, 
                    data.burglary.values,
                    c=data.larceny_theft.values,
                    s=data.population.values,
                    linewidths=2, edgecolor='w')

    sct.set_alpha(0.75)
    axis([0,11,200,1280])
    xlabel('Murders per 100,000 population')
    ylabel('Burglaries per 100,000 population')
    show()

if __name__ == '__main__':
    load()
