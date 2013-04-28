from collections import deque, Iterable
import sys

def check_valid_fastq(lines):
    return (lines[0].startswith('@') and
            lines[2].startswith('+') and
            len(lines[1])==len(lines[3]))

def slide(s, maxlen=4):
    if isinstance(s, Iterable):
        iter_s = iter(s)
    else:
        raise StopIteration

    window = deque([next(iter_s) for _ in range(3)], maxlen=maxlen)

    for c in iter_s:
        window.append(c)
        yield window

if __name__ == '__main__':
    for lines in slide(sys.stdin):
        if check_valid_fastq(lines):
            sys.stdout.write(''.join(lines))
