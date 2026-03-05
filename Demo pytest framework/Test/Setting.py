import json
import os
import requests
import yaml
from Unit.Common.Open_File import open_file_yaml

# Biến toàn cục
CURRENT_DIR = os.path.dirname(__file__)

path_dir_log = os.path.abspath(os.path.join(CURRENT_DIR,"Unit","Evm","Log"))
path_dir_parametrize = os.path.abspath(os.path.join(CURRENT_DIR,"Unit","Evm","Module","Parametrize"))

with open(os.path.join(CURRENT_DIR, "Config.yaml"), "r") as file: config = yaml.safe_load(file)

url_browser = config["Contract"].get("url_browser")
headers = config["Contract"].get("headers")
comment_bytecode = config["Contract"].get("comment_bytecode")

src_addr_list = list(map(lambda x: x["AddrCoin"],filter(lambda x: "AddrCoin" in x, (requests.request("POST", url_browser, headers=headers, data=json.dumps({"method": "listaccounts","params": {"page_size": 500}})).json()).get("result"))))

duration_time_expect = config["Contract"].get("duration_time_expect")
param_transfer=open_file_yaml(path_dir_parametrize+"\\Transfer.yaml")
param_approve=open_file_yaml(path_dir_parametrize+"\\Approve.yaml")
param_transfer_from=open_file_yaml(path_dir_parametrize+"\\TransferFrom.yaml")














