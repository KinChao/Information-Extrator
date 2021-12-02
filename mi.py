from typedb.client import TransactionType
import csv
import re

from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from Helpers.batchLoader import write_batch


def migrate_uniprot(session, num, num_threads, batch_size):
    if num != 0:
        print('  ')
        print('Opening Uniprot dataset...')
        print('  ')


        uniprotdb = get_uniprotdb(num_threads)

        insert_organism(uniprotdb, session, num_threads, batch_size)


        print('.....')
        print('Finished migrating Uniprot file.')
        print('.....')

def get_uniprotdb(split_size):
    with open('output.tsv', 'rt', encoding='ANSI') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        raw_file = []
        n = 0

        for row in csvreader:
            raw_file.append(row)

        return raw_file[0]


def insert_organism(uniprotdb, session, num_threads, batch_size):
    batch = []
    batches = []


    pattern = "(?<=\[).+?(?=\])"


    typeql = ''
    is1 = 1
    iseven = 0
    id = 0
    for q in uniprotdb:



        count = 0

        if (iseven%2 == 0):


            typeql += f"insert $De isa description, has des '{uniprotdb[id+1]}'; "

            for m in re.finditer(pattern, q):
                m_group = m.group()
                count = count +1
                typeql += f"$En isa entity1, has en-name '{m_group}'; $2 (associated-entity: $En, associated-des: $De) isa entity-des-association;"

            batch.append(typeql)
            typeql=''
            is1 = 0
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []
        iseven = iseven + 1
        id = id+1
    batches.append(batch)
    pool = ThreadPool(num_threads)
    pool.map(partial(write_batch, session), batches)
    pool.close()
    pool.join()
    print('organisms committed!')
