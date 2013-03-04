import argparse

#creating a parser
parser = argparse.ArgumentParser(description='test arg')

#adding arguments
parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an inter for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
const=sum, default=max, help='sum the integers')

args = parser.parse_args()
print args.
print args.accumulate(args.integers)
