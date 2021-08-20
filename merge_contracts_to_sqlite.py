#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import sqlite3
import zipfile


def create_contracts_table(DB):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try:
        create_table = '''create table contracts(
                                                        id INTEGER PRIMARY KEY NOT NULL,
                                                        address VARCHAR(50) NOT NULL,
                                                        name VARCHAR(50),
                                                        metadata TEXT,
                                                        version INTEGER DEFAULT 1,
                                                        checkPoints text DEFAULT NULL)'''

        sql_create_address_index = "create index address_index on contracts(address)"
        cursor.execute(create_table)
        cursor.execute(sql_create_address_index)
    except:
        clean_table = "DELETE FROM contracts"
        cursor.execute(clean_table)

    cursor.close()
    conn.commit()
    conn.close()


def get_contract_info(contract_path):
    with open(contract_path, 'r') as f:
        try:
            content = json.loads(f.read())
            content_address = content["address"].lower()
            contract_name = content["name"]
            contract_metadate = json.dumps(content["metadata"])
            contract_version = int(content["version"])
            contract_checkPoints = json.dumps(content["checkPoints"])
        except:
            raise

    return content_address, contract_name, contract_metadate, contract_version, contract_checkPoints


def merge_abis_to_sqlite(DB, contracts_path):

    if not os.path.exists(contracts_path):
        return None

    create_contracts_table(DB)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    fileslist = os.listdir(contracts_path)

    if len(fileslist):
        for file in fileslist:
            if file.endswith(".json"):
                try:
                    address, name, metabase, version, check_points = get_contract_info(contract_path=contracts_path+file)
                except:
                    print("{file} is error......".format(file=file))
                    continue

                sql_insert_info = "insert into contracts (address,name, metadata, version, checkPoints) values (?,?,?,?,?)"
                cursor.execute(sql_insert_info, (address, name, metabase, version, check_points))
                print("{address} is done......".format(address=address))

    cursor.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    path = "./ethereum/"
    if not os.path.exists("./outputs/contracts/ethereum/"):
        os.makedirs("./outputs/contracts/ethereum/")
    merge_abis_to_sqlite(DB="./outputs/contracts/ethereum/contracts.db", contracts_path=path)
