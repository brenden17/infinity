from mrjob.job import MRJob
import logging

class MRWordCounter(MRJob):
	def mapper(self, key, line):
		self.increment_counter('group', 'counter_name', 1)
		for word in line.split():
			yield word, 1

	def reducer(self, word, occurrences):
		yield word, sum(occurrences)


if __name__ == '__main__':
	MRWordCounter.run()