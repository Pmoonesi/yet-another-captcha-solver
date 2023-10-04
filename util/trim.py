import os

import glob

label_paths = glob.glob('new_label/*.txt')

label_paths = sorted(label_paths)

for i, label_path in enumerate(label_paths):

    with open(label_path, 'r') as f:
        temp = f.readline().replace(' ','').strip()

    output_path = label_path.replace('new_label', 'new_label_ns')
    with open(output_path, 'w') as f:
        f.write(temp)
    
print('done')
    
