import csv

import os
rootdir = 'groups'
print("source,target,timestamp")
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if 'update1' in file or 'update2' in file:
            continue
        file_path = os.path.join(subdir, file)
        posted_by_set = set()
        if str(file_path).endswith("comments.tab"):
            with open(file_path, encoding="utf-8") as tsv:
                for line in csv.DictReader(tsv, dialect="excel-tab"):
                    group = file.split("_")[1]
                    posted_by = line['post_by'] 
                    posted_time = line['post_published']
                    if not posted_by in posted_by_set:
                        row = "{0},{1},{2}".format(posted_by,group,posted_time)
                        print(row)
                        posted_by_set.add(posted_by) 
                    comment_by = line['comment_by'] 
                    comment_time = line['comment_published'] 
                    
                    row = "{0},{1},{2}".format(comment_by,group,comment_time)
                    print(row)
