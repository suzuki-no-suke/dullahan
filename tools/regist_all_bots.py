from dotenv import load_dotenv

import sys
sys.path.append("..")

import importlib
import os

from src.orm.Base import SQLFactory
from src.orm.models.chatbot import ChatBot
from src.orm.tables.table_chatbot import TableChatbot

from src.datadef.chat_message import Message_v1, Message_v2

load_dotenv('../.env')
os.environ['DB_CONN'] = os.environ['DB_CONN'].replace('sqlite:///.', 'sqlite:///..')
DB_CONN = os.getenv('DB_CONN')
print(f"db connected -> {DB_CONN}")

def regist_to_db(dbobj, module_filename, classname):
    bottable = TableChatbot(dbobj)

    module_name = f"{module_base}.{module_filename}"
    result = None
    try:
        module_data = importlib.import_module(module_name)
        class_data = getattr(module_data, classname)
    except ImportError as imex:
        print(f"import failed -> {imex}")
        result = f"Failed to load : {module_name} / {classname}"
        return result

    result = f"{module_filename} / {classname} -> import succeed "

    # load class detail
    newbot = ChatBot(
        botname=class_data.botname,
        display_name=class_data.display_name,
        useful_when=class_data.useful_when,
        description=class_data.description,
        enable_version=class_data.enable_version,
        module_filename=module_filename,
        classname=classname,
    )

    result += f"-> botname {newbot.botname}"

    if len(newbot.enable_version) > 0:
        # register
        bottable.upsert_single_bot(newbot)
        return result + f" -> register succeed"
    return result + f" -> version not declared. not registered"


def find_all_pyfiles(dir):
    files = {}
    abspath = os.path.abspath(dir)
    #print(f"target dir => {abspath}")
    for entry in os.listdir(abspath):
        entrypath = os.path.join(abspath, entry)
        if entry[:2] == "__":
            continue
        elif entry == "helper":
            continue
        elif os.path.isdir(entrypath):
            dircont = find_all_pyfiles(entrypath)
            files[entry] = dircont
        elif os.path.isfile(entrypath):
            splited = os.path.splitext(entry)
            if splited[1] == ".py":
                files[splited[0]] = None
    return files

def flatten_filename(dirdict):
    flatten_dict = {}
    for e, d in dirdict.items():
        if d is None:
            flatten_dict[e] = e
        else:
            subdir = flatten_filename(d)
            for sube, c in subdir.items():
                flatten_dict[e + "." + sube] = c
    return flatten_dict





dirpath = "../botfirm"
module_base = "botfirm"

dbobj = SQLFactory.default_env()

listed_dir = find_all_pyfiles(dirpath)
flatten_dir = flatten_filename(listed_dir)

print(f"flatten -> {flatten_dir}")

#print(regist_to_db(dbobj, "v1.Echobot", "Echobot"))
#print(regist_to_db(dbobj, "v1.Rubberduck", "Rubberduck"))

for m, c in flatten_dir.items():
    print(regist_to_db(dbobj, m, c))
