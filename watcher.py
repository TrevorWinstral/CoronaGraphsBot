import pickle, os, time
from datetime import datetime

fname = 'settings.pkl'
START = 0
old_dict = {}
while True:
    lastmodified = os.stat(fname).st_mtime

    if lastmodified-START > 1:
        print(f'Change at {datetime.fromtimestamp(lastmodified)}')
        with open(fname, 'rb') as inFile:
            new_dict = pickle.load(inFile)
        print(f'\n\n\n\n\n{"="*15}\nChanges Identifed:')

        cleaner = lambda x : [] if x == set() else x
        shared = cleaner( set(new_dict) and set(old_dict) )
        additions = cleaner( set(new_dict) - set(old_dict) )
        deletions = cleaner( set(old_dict) - set(new_dict) )
        
        updates = {k: {'New': new_dict[k], 'Old': old_dict[k]} for k in shared if new_dict[k] != old_dict[k]}
        adds = {k:new_dict[k] for k in additions}
        subs = {k:new_dict[k] for k in deletions}
        print(f'Updates Identified: {updates}\n\n')
        print(f'Additions Identified: {adds}\n\n')
        print(f'Deletions Identified: {subs}\n\n')
        print('='*15)

        old_dict = new_dict

    time.sleep(5)

    START = lastmodified
    