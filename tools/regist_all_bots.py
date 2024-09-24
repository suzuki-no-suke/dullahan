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
DB_CONN = os.getenv('DB_CONN')
print(f"db connected -> {DB_CONN}")

dirpath = "./botfirm"
module_base = "botfirm"

def regist_to_db(dbobj, module_filename, classname):
    bottable = TableChatbot(dbobj)

    module_name = f"{module_base}.{module_filename}"
    result = None
    try:
        module_data = importlib.import_module(module_name)
        class_data = getattr(module_data, classname)
    except ImportError as imex:
        result = f"Failed to load : {module_name} / {classname}"
        return result

    # decide message version
    enable_version = []
    versions = {
        Message_v1: "v1",
        Message_v2: "v2"
    }
    for c, v in versions.items():
        if isinstance(class_data, c):
            enable_version.append(v)

    # load class detail
    newbot = ChatBot(
        botname=class_data.botname,
        display_name=class_data.display_name,
        useful_when=class_data.useful_when,
        description=class_data.description,
        enable_version=enable_version,
        module_filename=module_filename,
        classname=classname,
    )
    if len(enable_version) > 0:
        # register
        bottable.upsert_single_bot(newbot)


def find_all_pyfiles(dir):
    """
    フォルダ内のファイルを辞書にして返す
    """
    pass


dbobj = SQLFactory.default_env()
regist_to_db(dbobj, "v1.Echobot", "Echobot")
regist_to_db(dbobj, "v1.Rubberduck", "Rubberduck")
