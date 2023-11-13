#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import sqlite3
import shutil
from functools import reduce
from Crypto.Hash import keccak

CHAIN_ID_MAP = {
    "ethereum": 1,
    "arbitrum": 42161,
    "avalanche": 43114,
    "bsc": 56,
    "celo": 42220,
    "fantom": 250,
    "flare": 14,
    "harmony": 1666600000,
    "moonriver": 1285,
    "optimism": 69,
    "polygon": 137,
    "songbird": 19,
}

def printProgressBar(
    iteration,
    total,
    prefix="Progress:",
    suffix="Complete",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

connection_pool = {};

def create_db_table(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    try:
        create_table = """create table contracts
                (
                    id INTEGER PRIMARY KEY NOT NULL,
                    address VARCHAR(50) NOT NULL,
                    name VARCHAR(50),
                    selectorId VARCHAR(50),
                    functionABI TEXT,
                    version INTEGER DEFAULT 1,
                    checkPoints text DEFAULT NULL
                )"""

        sql_create_address_index = "create index address_index on contracts(address)"
        cursor.execute(create_table)
        cursor.execute(sql_create_address_index)
    except:
        clean_table = "DELETE FROM contracts"
        cursor.execute(clean_table)

    cursor.close()
    conn.commit()
    conn.close()


def get_or_create_db_table(path):
    if not os.path.exists(path):
        create_db_table(path)
        conn = sqlite3.connect(path)
        connection_pool[f"{path}"] = conn
        return conn
    else:
        return connection_pool[f"{path}"]

def caclulate_selector_id(function_name_with_type):
    bytes_for_function = bytes(function_name_with_type, 'utf-8')
    sha = keccak.new(digest_bits=256)
    sha.update(bytes_for_function)
    return sha.hexdigest()[0:8]

def insert_record_into_db(db_path):
    pass

def process_function_abi_object(func_obj):
    if(len(func_obj["inputs"])>0):
        type_list = [each['type'] for each in func_obj["inputs"]]
        return ','.join(type_list)
    else:
        return ""

def parse_contract_json(json_contract):
    abi_list = json_contract["metadata"]["output"]["abi"]

    abi_func_list = [ each for each in abi_list if each["type"] == "function"]
    functions = [];
    for each in abi_func_list:
        function_signature = f"{each['name']}({process_function_abi_object(each)})"
        selector = caclulate_selector_id(function_signature)
        functions.append({
            'abi': each,
            'selector': selector
        })

    return functions

def get_contract_info(contract_path):
    with open(contract_path, 'r') as f:
        try:
            content = json.loads(f.read())
            content_address = content["address"].lower()
            contract_name = content["name"]
            contract_metadate = json.dumps(content["metadata"])
            contract_version = 1
            contract_checkPoints = json.dumps(content.get("checkPoints",[]))
            abi_details = parse_contract_json(content)
        except:
            raise

    return content_address, contract_name, contract_metadate, contract_version, contract_checkPoints, abi_details


def merge_abis_to_sqlite(chain_name, db_target_path, contracts_path):
    
    if not os.path.exists(contracts_path):
        return None

    
    fileslist = os.listdir(contracts_path)

    if len(fileslist):
        sum_of_file = len(fileslist) - 1
        location = 0
        for file in fileslist:
            if file.endswith(".json"):
                db_sharding_index = file[2]
                path = f"{db_target_path}/{CHAIN_ID_MAP[chain_name]}_{db_sharding_index.lower()}_contracts.db"
                conn = get_or_create_db_table(path)
                cursor = conn.cursor()

                try:
                    address, name, metabase, version, check_points, abi_details = get_contract_info(contract_path=contracts_path+file)
                except Exception as e:
                    print(e)
                    print("{file} is error......".format(file=file))
                    raise e
                
                for each in abi_details:
                    selectorId = each['selector']
                    functionABI = each['abi']
                    sql_insert_info = "insert into contracts (address,name,selectorId,functionABI,version, checkPoints) values (?,?,?,?,?,?)"
                    cursor.execute(sql_insert_info, (address, name, selectorId, json.dumps(functionABI),version, check_points))
                location += 1
                printProgressBar(location, sum_of_file, prefix=f"processing: {contracts_path}")
            
                cursor.close()
                conn.commit()


if __name__ == "__main__":
    ignored = [".github", ".git", "outputs", "v3"]
    targets = [ name for name in os.listdir('.') if os.path.isdir(os.path.join('.', name)) and name not in ignored]
    if os.path.exists("./outputs"):
        shutil.rmtree("./outputs", ignore_errors=True)
    if not os.path.exists("./outputs/contracts"):
        os.makedirs("./outputs/contracts")
    db_target_path = "./outputs/contracts"
    for each_target in targets:
        path = f"./{each_target}/"
        merge_abis_to_sqlite(each_target, db_target_path, contracts_path=path)
        [each.close() for each in connection_pool.values()]
    shutil.make_archive('contracts_g3', 'zip', root_dir='./outputs', base_dir='contracts')
