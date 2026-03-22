import os
import shutil


def copy_files_recursive(source, destination):
    if not os.path.exists(source):
        raise Exception('Source given not a valid dir.')
    if not os.path.exists(destination):
        os.mkdir(destination)
        print (f'Copy directory: {source} -> {destination}')
    source_contents = os.listdir(source)
    for item in source_contents:
        item_path = os.path.join(source,item)
        copy_item = os.path.join(destination,item)
        if os.path.isfile(item_path):
            print(f'Copy file: {item_path} -> {copy_item}')
            shutil.copy(item_path,copy_item)
        elif os.path.isdir(item_path):
            copy_files_recursive(item_path,copy_item)
            

