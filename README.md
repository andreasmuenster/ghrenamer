# ghrenamer
Rename Github-ABAP-Repositiories to customer namespace

## About The Project

This scrip can be handy if you want to convert github abap-projects to your customer namespace (e.g. to roll them out in your template).

Here's why:
* you avoid name colissions 
* you don't violate your development-rules (namespaces etc.)
* you save time - so you can pull new versions practically as often as you like :)
* the script is handy and takes care of potential duplicates due to the max length of ddic or repo objects

## Getting Started

There's not quite much you need to do.

* download your required (main) repository from Github (eg. https://github.com/abap2xlsx/abap2xlsx ) > Code > Download ZIP
* extract the zip file in a new folder 
* adopt the ghrenamer "Settings" part at least 
    - top dir
    - name_prefix_old (typically Z)
    - name_prefix_new (your required namespace, Y or /NSP/ or whatever you like)
* run the script     
* (optional) check the adopted files and contents
* zip the directory again
* create an offline repo with abapgit and this zip file
* pull everything in to your system and
* check if it works







