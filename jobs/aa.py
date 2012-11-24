import json
from mrjob.job import MRJob
import numpy as np

class MRWordCounter(MRJob):
    
    def steps(self):
        return ([self.mr(mapper=self.reader),
                 self.mr(mapper=self.mapper, reducer=self.reducer)]
                )
    
    def reader(self, _, line):
        l = line.split(',')
        s = sum(map(int, l[1:]))
        yield l[0], s
        
    def mapper(self, index, s):
        yield index, s

    def reducer(self, index, s):
        yield index, max(s)

if __name__ == '__main__':
    MRWordCounter.run()
