import sys

all = 'all.gff3'
sam = 'sam.txt'

if len(sys.argv) >= 2:
    all = sys.argv[1]
    sam = sys.argv[2]

# print 'All file:', all, '\r\n', 'Sam file:', sam

all_file = open(all, 'r')
sam_file = open(sam, 'r')
lines = sam_file.readlines()
sam_dict = {}
len_sam = 0
for line in lines:
    if line.startswith('@'):
        continue
    items = line.strip().split('\t')
    # print items
    chrn = items[2]
    pos = items[3]
    if chrn.startswith('Chr'):
        # items[2] is Chr*, items[3] is the position of this gene
        if sam_dict.has_key(chrn):
            sam_dict[chrn].append(int(pos))
        else:
            sam_dict[chrn] = [int(pos)]
        len_sam += 1

len_sam = float(len_sam)
# for key in sam_dict.keys():
#      print key, len(sam_dict[key])

result_dict = {}
all_dict = {}

for line in all_file.readlines():
    if line.startswith('@'):
        continue
    items = line.strip().split('\t')
    # print items
    if len(items) < 9:
        continue
    if items[2] == 'gene':
        start = int(items[3])
        id = items[8].split(':')[0]
        if id.find('retrotransposon') >= 0 or id.find('transporter') >= 0:
            continue

        if not result_dict.has_key(id):
            result_dict[id] = [0] * 50

        if all_dict.has_key(items[0]):
            all_dict[items[0]].append((int(start), id))
        else:
            all_dict[items[0]] = [(int(start), id)]

# for key in all_dict.keys():
#     print key, len(all_dict[key])
#print '\r\'

for key in sam_dict.keys():
    #print key

    reads = sam_dict[key]
    group = all_dict[key]
    for pos in reads:
        #print 'Group=', group
        for start, id in group:
            s = start - 1000
            e = start
            #print 'Start=', start, 'id=', id, 's=', s, 'e=', e
            if pos < e and pos >= s:
                #print start, s, e
                # the position in 20bp*50
                div = (pos - s) / 20
                if result_dict.has_key(id):

                    result_dict[id][div] += 1 / len_sam
                    # print id, pos
                    # else:
                    #     result_dict[id]=[0]*50
                    #     result_dict[id][div]=1
                    #     print result_dict
# print result_dict
# OutPut tab separated file
print 'YORF\t',

for i in range(0, 50):
    print i, '\t',
print ''

for key in result_dict.keys():
    print key, '\t',
    a = result_dict[key]
    for i in range(0, 50):
        print a[i], '\t',
    print ''
