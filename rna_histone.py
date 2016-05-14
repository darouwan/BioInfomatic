import sys
import xlrd

all = 'gene.xls'
sam = 'sam.txt'

if len(sys.argv) >= 2:
    all = sys.argv[1]
    sam = sys.argv[2]

data = xlrd.open_workbook(all)
table0 = data.sheet_by_name(u'0')
table20 = data.sheet_by_name(u'20%')
table40 = data.sheet_by_name(u'40%')
table60 = data.sheet_by_name(u'60%')
table80 = data.sheet_by_name(u'80%')
table100 = data.sheet_by_name(u'100%')

all_dict_0 = {}
all_dict_20 = {}
all_dict_40 = {}
all_dict_60 = {}
all_dict_80 = {}
all_dict_100 = {}


def generate_dict(table, dict, id_pos):
    result_dict_plus = {}
    result_dict_minus = {}
    for i in range(table.nrows):
        row = table.row_values(i)
        id = row[id_pos]
        chr = row[id_pos + 1]
        start = int(row[id_pos + 2])
        end = int(row[id_pos + 3])
        sign = row[id_pos + 4]
        if not result_dict_plus.has_key(id) and sign == u'+':
            result_dict_plus[id] = [0] * 40
        if not result_dict_minus.has_key(id) and sign == u'-':
            result_dict_minus[id] = [0] * 40

        if dict.has_key(chr):
            dict[chr].append((id, chr, start, end, sign))
        else:
            dict[chr] = [(id, chr, start, end, sign)]
    return dict, result_dict_plus, result_dict_minus


def accumulate(all_dict, items, result_dict_plus, result_dict_minus):
    chrn = items[2]
    pos = int(items[3])
    if chrn.startswith('Chr'):
        gene = all_dict[chrn]
        # print chrn, pos
        for id, chr, start, end, sign in gene:

            if sign == u'+':

                s = start - 1000
                e = start + 1000
                if pos < e and pos >= s:
                    # print start, s, e
                    # the position in 20bp*50
                    div = (pos - s) / 50
                    if result_dict_plus.has_key(id):
                        result_dict_plus[id][div] += 1
            if sign == u'-':
                s = end - 1000
                e = end + 1000
                if pos < e and pos >= s:
                    # print start, s, e
                    # the position in 20bp*50
                    div = (pos - s) / 50
                    if result_dict_minus.has_key(id):
                        result_dict_minus[id][div] += 1


def reverse_plus(result_dict_plus, result_dict_minus):
    row = [0] * 40
    for key in result_dict_plus:
        r = result_dict_plus[key]
        if len(r) == 40:
            for i in range(len(r)):
                row[i] += r[i]
    for key in result_dict_minus:
        r = result_dict_minus[key]
        if len(r) == 40:
            for i in range(len(r)):
                row[i] += r[39 - i]
    return row


all_dict_0, result_dict_plus_0, result_dict_minus_0 = generate_dict(table0, all_dict_0, 3)
all_dict_20, result_dict_plus_20, result_dict_minus_20 = generate_dict(table20, all_dict_20, 5)
all_dict_40, result_dict_plus_40, result_dict_minus_40 = generate_dict(table40, all_dict_40, 12)
all_dict_60, result_dict_plus_60, result_dict_minus_60 = generate_dict(table60, all_dict_60, 12)
all_dict_80, result_dict_plus_80, result_dict_minus_80 = generate_dict(table80, all_dict_80, 12)
all_dict_100, result_dict_plus_100, result_dict_minus_100 = generate_dict(table100, all_dict_100, 12)

sam_file = open(sam, 'r')
lines = sam_file.readlines()
sam_dict = {}
len_sam = 0

for line in lines:
    if line.startswith('@'):
        continue
    items = line.strip().split('\t')
    # print items
    len_sam += 1
    accumulate(all_dict_0, items, result_dict_plus_0, result_dict_minus_0)
    accumulate(all_dict_20, items, result_dict_plus_20, result_dict_minus_20)
    accumulate(all_dict_40, items, result_dict_plus_40, result_dict_minus_40)
    accumulate(all_dict_60, items, result_dict_plus_60, result_dict_minus_60)
    accumulate(all_dict_80, items, result_dict_plus_80, result_dict_minus_80)
    accumulate(all_dict_100, items, result_dict_plus_100, result_dict_minus_100)

    row_0 = reverse_plus(result_dict_plus_0, result_dict_minus_0)
    row_20 = reverse_plus(result_dict_plus_20, result_dict_minus_20)
    row_40 = reverse_plus(result_dict_plus_40, result_dict_minus_40)
    row_60 = reverse_plus(result_dict_plus_60, result_dict_minus_60)
    row_80 = reverse_plus(result_dict_plus_80, result_dict_minus_80)
    row_100 = reverse_plus(result_dict_plus_100, result_dict_minus_100)

print '0%', row_0
print '20%', row_20
print '40%', row_40
print '60%', row_60
print '80%', row_80
print '100%', row_100
