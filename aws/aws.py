from boto import ec2
import sys

tokyo = 'ap-northeast-1'

aws = sys.argv[0].split('/')[-1].split('.')[0]
arg = sys.argv[1]

if arg not in ['stop', 'start']:
    print('Wrong arguments')
    sys.exit()

conn = ec2.connect_to_region(tokyo)
insts = conn.get_all_instances()
for inst in insts:
    for ins in inst.instances:
        if ins.tags.get('Name') == aws:
            print('Current status: %s' % ins.state)
            if arg == 'stop' and ins.state == 'running':
                ins.stop()
                print('aws stops')
            elif arg == 'start' and ins.state == 'stopped':
                ins.start()
                print('aws starts')
            else:
                print('Something Wrong~~')