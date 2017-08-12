import re
import os
import numpy as np

a = np.loadtxt(open('note_dict.csv'), dtype = str, delimiter = ',')
a = a.swapaxes(0,1)
raw_name_dict = dict(a.tolist())
name_dict = {str(k)[2:-1]:str(v)[2:-1] for k,v in raw_name_dict.items()}

old_pattern = re.compile(r'(\d\d)')
for file_name in os.listdir('.'):
    try:
        number = old_pattern.match(file_name).group(0)
    except:
        continue
    new_name = name_dict[str(number)] + '.ogg'
    os.rename(file_name, new_name)
    