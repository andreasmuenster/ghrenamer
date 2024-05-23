# --------------------------------------------------------------------
# GHRenamer - Github Renamer
# --------------------------------------------------------------------
# Tool to rename repositories from Github to customer-namespaces
# Source: https://github.com/andreasmuenster/ghrenamer
# --------------------------------------------------------------------
 
import operator
import os
import sys
import re
import ctypes
import string
 
# SETTINGS - CHANGE HERE ------------------------------------------------ 
top_dir = "c:/temp/myrepository/"
name_prefix_old = str.upper("Z")
name_prefix_new = str.upper("/NSP/")

c_ignore_files = ['pdf', 'png', 'DS_Store', 'zip']
c_max_length_unknown_object = 10
c_repo_max_length = dict(tabl=30, ttyp=30, xslt=30, view=30, dtel=30, doma=30, prog=40, clas=30, intf=30, msag=20)
# SETTINGS - END HERE ----------------------------------------------------

source_dir = top_dir + "src"
search_pattern = "(^" + name_prefix_old + "[^\\.]*)([^\\.]*)"
file_renaming = {}
 
def get_unique_id(long_id: str, max_length: int, file_name: str, hashmap: ctypes.Array) -> str:
    # Cut everything down and create new id
 
    if len(long_id) < max_length:  # cut length to max length
        id = long_id
    else:
        id = long_id[:max_length]
 
    if any(e in id[-1] for e in ["-", "_"]):  # replace invalid last characters
        size: int = len(id)
        id = id[:-1] + '0'
 
    try:
        check_key = hashmap[id]
        match = re.search(r"\d+", id)
        if match:
            number_found = match.group(0)
            match_add_1 = str(int(number_found) + 1)
            new_id = id[:len(id) - len(match_add_1)] + str(match_add_1)
            new_id = get_unique_id(new_id, max_length, file_name, hashmap)
        else:
            new_id = get_unique_id(id[:len(id) - 1] + "0", max_length, file_name, hashmap)
        return new_id
 
    except KeyError:
        return id
 
 
def do_replace(top_dir: str, hashmap: ctypes.Array):
    # unspecific (longest items) need to be replaced at first
    hashmap_downsorted = sorted(hashmap.items(), key=operator.itemgetter(1), reverse=True)
 
    for dirpath, dirnames, files in os.walk(source_dir, topdown=False):
 
        if '.git' in dirpath:
            continue
 
        for file_name in files:
 
            if any(s in file_name for s in (c_ignore_files)):
                continue
 
            file_name_complete = os.path.join(dirpath, file_name)
 
            f = open(file_name_complete, 'r', encoding='UTF8')
            file_data = f.read()
            f.close()
 
            file_data_new = file_data
 
            for new_value, old_value in hashmap_downsorted:
                # if file_name.endswith('xml'):
                file_data_new = re.sub(str.lower(old_value), str.lower(new_value), file_data_new)
                file_data_new = re.sub(str.upper(old_value), str.upper(new_value), file_data_new)
                file_data_new = re.sub(old_value, str.upper(new_value), file_data_new, flags=re.IGNORECASE)
 
            f = open(file_name_complete, 'w', encoding='utf_8')
            f.write(file_data_new)
            f.close()
 
            print("Processed: " + file_name_complete)
 
 
def do_rename(top_dir: str, hashmap: ctypes.Array):
    for source, target in file_renaming.items():
        os.rename(source, target)
 
 
def construct_renaming_patterns(top_dir: str, name_prefix_old: str, name_prefix_new: str) -> ctypes.Array:
    r_renaming = {}
    file_name_wo_extension = {}
 
    for dirpath, dirnames, files in os.walk(source_dir, topdown=False):
 
        if '.git' in dirpath:
            continue
 
        for file_name in files:
 
            # Check if file needs to be processed
 
            found = re.search(search_pattern, file_name, flags=re.IGNORECASE)
            if not found:
                continue
 
            if any(s in file_name for s in (c_ignore_files)):
                continue
 
            # Get File-Id, Extension ...
 
            patterns = re.split("\\.", file_name)
            file_id = patterns[0]
            file_type = patterns[1]
            file_rest = '.'.join(patterns[2:])
 
            # Check if file-name was already mapped
            id_new = ""
            for key, value in r_renaming.items():
                if value == file_id:
                    id_new = key
                    break
 
            # If not mapped, try to generate a unique key -> id_new
            if not id_new:
                try:
                    id_max_length = c_repo_max_length[file_type]
                except KeyError:
                    id_max_length = c_max_length_unknown_object
 
                try:
                    id_new = file_name_wo_extension[os.path.splitext(file_name)[0]]
                except KeyError:
                    id_changed = re.sub("^" + name_prefix_old, name_prefix_new, file_id, flags=re.IGNORECASE)
                    id_new = get_unique_id(id_changed, id_max_length, file_name, r_renaming)
                    file_name_wo_extension[os.path.splitext(file_name)[0]] = id_new
 
                # remember variable rename hash
                r_renaming[id_new] = file_id
 
            # remember file to rename (AND / becomes #)
            file_name_new = re.sub("/", "#", id_new)
            file_renaming[os.path.join(dirpath, file_name)] = os.path.join(dirpath,
                                                                           file_name_new + '.' + file_type + '.' + file_rest)
 
    return r_renaming
 
renaming_patterns = construct_renaming_patterns(top_dir, name_prefix_old, name_prefix_new)
do_replace(top_dir, renaming_patterns)
do_rename(top_dir, renaming_patterns)