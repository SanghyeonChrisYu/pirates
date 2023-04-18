from library.logging_pack import *
from library import cf
import re
import datetime
from datetime import datetime, timedelta, timezone

import pandas as pd
import numpy as np

import pymysql
import sqlalchemy as sa
from sqlalchemy import create_engine, event
pymysql.install_as_MySQLdb()

def escape_percentage(conn, clauseelement, multiparams, params):
    # execute로 실행한 sql문이 들어왔을 때 %를 %%로 replace
    if isinstance(clauseelement, str) and '%' in clauseelement and multiparams is not None:
        while True:
            replaced = re.sub(r'([^%])%([^%s])', r'\1%%\2', clauseelement)
            if replaced == clauseelement:
                break
            clauseelement = replaced

    return clauseelement, multiparams, params

class Data_Loader():
    def __init__(self):
        logger.debug("data_loader_init")
        self.db_name_setting()

    def db_name_setting(self):
        self.engine_bridge_main = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/bridge_main",
            encoding='utf-8')
        self.engine_bridge_data = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/bridge_data",
            encoding='utf-8')

        # event.listen(self.engine_bridge_main, 'before_execute', escape_percentage, retval=True)
        # event.listen(self.engine_bridge_data, 'before_execute', escape_percentage, retval=True)

if __name__ == "__main__":
    data_loader = Data_Loader()
    data_loader.db_name_setting()


    # conn.cursor().execute('create database bridge_data')

    # data_loader.engine_bridge_data.execute("create table ")

    # print(data)
    print("미국은 갈건데?")
