import csv

txt = []

with open('data_unparsed.txt','r',encoding='UTF-8') as f:
    for x in f:
        lines = f.readline()
        x = x.replace('\n','')
        lines = lines.replace('\n','')
        txt.append(x)
        txt.append(lines)


with open('output.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(txt)

