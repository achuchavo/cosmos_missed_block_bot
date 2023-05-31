import requests
import time
import config
# import cosmos
import sys
import json
import datetime

TOKEN = config.TOKEN
the_chat_id = config.the_chat_id
the_block = 0
block_arr = []
the_block_dict = {}
block_arr_dict = {}
sleep_time = 0.5
now_time = {}
then_time = {}
# sleep_time = float(sys.argv[3])
# coin_name = sys.argv[1]
# rpc_endpoint = sys.argv[2]
# uptime_limit = int(sys.argv[4])
# uptime_limit_fixed = int(sys.argv[4])
# the_validator = sys.argv[5]
config = {}
# below gets chat id
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json()


def set_the_block(api_json):
    for atoken in api_json:
        the_block_dict[atoken] = 0


def set_the_block_arr(api_json):
    for atoken in api_json:
        block_arr_dict[atoken] = []


def set_now_time(api_json):
    for atoken in api_json:
        now_time[atoken] = datetime.datetime.now()


def set_then_time(api_json):
    for atoken in api_json:
        then_time[atoken] = datetime.datetime.now()


def load_api_vals():
    global config
    with open("config.json", "r") as infile:
        config = json.load(infile)
    print(config["api"])


def get_latest_block(an_endpoint, acoin_name, aval_name):
    url_status = f""+an_endpoint+"/status"
    json_status = requests.get(url_status)
    recent_block = json_status.json(
    )['result']['sync_info']['latest_block_height']
    process_block = int(recent_block)-1
    return process_block

# missed blocks functions


def check_missed_block(an_endpoint, acoin_name, aval_name):
    global the_block_dict
    global now_time
    global then_time
    uptime = 100
    try:
        now_time[acoin_name] = datetime.datetime.now()
        time_diff = (now_time[acoin_name] -
                     then_time[acoin_name]).total_seconds() / 60
        if the_block_dict[acoin_name] == 0:
            the_block_dict[acoin_name] = get_latest_block(
                an_endpoint, acoin_name, aval_name)
        url = f""+an_endpoint+"/commit?height="+str(the_block_dict[acoin_name])
        ajson = requests.get(url)
        _validator = aval_name
        ablock = get_latest_block(an_endpoint, acoin_name, aval_name)
        if the_block_dict[acoin_name] < ablock:
            for commits in ajson.json()['result']['signed_header']['commit']['signatures']:
                if commits['validator_address'] == _validator:
                    time_stamp = commits['timestamp']
                    signature = commits['signature']
                    block_arr_dict[acoin_name].insert(0, (str(ablock), '0'))
                    break
            else:
                # block has been missed so update block arr to value 1
                block_arr_dict[acoin_name].insert(0, (str(ablock), '1'))

            # check for uptime condition and send uptime alarm
            if len(block_arr_dict[acoin_name]) >= 100:
                print('--------------')
                uptime = get_uptime(block_arr_dict[acoin_name], acoin_name)
                print(f"UPTIME {acoin_name} - {ablock}  : {str(uptime)}")
                if time_diff >= 60:
                    send_alarm(uptime, acoin_name)
                    then_time[acoin_name] = datetime.datetime.now()
                    load_api_vals()
                block_arr_dict[acoin_name].pop()

            if the_block_dict[acoin_name] < ablock:
                the_block_dict[acoin_name] = the_block_dict[acoin_name] + 1
            else:
                the_block_dict[acoin_name] = the_block_dict[acoin_name]-1
            uptime = get_uptime(block_arr_dict[acoin_name], acoin_name)
            print(acoin_name + ' Missed Blocks : ' + str(100-uptime))
            print(
                f"{acoin_name} Blocks[{the_block_dict[acoin_name]}] : {len(block_arr_dict[acoin_name])}")
            print('--------------')
    except Exception as e:
        print('Exception : ' + acoin_name + "-" +str(e))
        if len(block_arr_dict[acoin_name]) >= 100:
            block_arr_dict[acoin_name].pop()
    return


def get_uptime(a_arr, acoin_name):
    cnt = 0
    for x, y in a_arr:
        if y == '1':
            cnt = cnt + 1
    cnt = 100-cnt
    return cnt


def send_alarm(auptime, acoin_name):
    message = acoin_name+" uptime 주기 : " + str(auptime)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={the_chat_id}&text={message}"
    print(requests.get(url).json())


if __name__ == "__main__":
    load_api_vals()
    if len(config["api"]) > 0:
        set_the_block(config["api"])
        set_the_block_arr(config["api"])
        set_now_time(config["api"])
        set_then_time(config["api"])
    while True:
        if len(config["api"]) > 0:
            apis = config["api"]
            vals = config["vals"]
            for atoken in apis:
                an_api = apis[atoken]
                a_val = vals[atoken]
                check_missed_block(an_api, atoken, a_val)
        time.sleep(0.5)
