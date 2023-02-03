import requests
import time
import config
# import cosmos
import sys
TOKEN =  config.TOKEN
the_chat_id = config.the_chat_id
the_block = 0
block_arr = []
coin_name =  sys.argv[1]
rpc_endpoint = sys.argv[2]
sleep_time = float(sys.argv[3])
uptime_limit =  int(sys.argv[4])
uptime_limit_fixed =  int(sys.argv[4])
the_validator = sys.argv[5]
#below gets chat id 
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

def get_latest_block():
    #get latest block
    url_status = f""+rpc_endpoint+"/status"
    json_status = requests.get(url_status)
    recent_block = json_status.json()['result']['sync_info']['latest_block_height']
    print('latest : '+recent_block)
    process_block = int(recent_block)-1
    return process_block


#missed blocks
def check_missed_block():
    global the_block
    global uptime_limit
    uptime = 100
    try:
        if the_block == 0 :
            the_block = get_latest_block()    
        url = f""+rpc_endpoint+"/commit?height="+str(the_block)
        ajson = requests.get(url)
        _validator = the_validator
        ablock = get_latest_block()  
        if  the_block < ablock:
            for commits in ajson.json()['result']['signed_header']['commit']['signatures']:
                if commits['validator_address'] == _validator:
                    time_stamp = commits['timestamp']
                    signature = commits['signature']
                    #print(str(the_block),'-',time_stamp, '-', signature)
                    block_arr.insert(0,(str(ablock),'0'))
                    break
            else:
                #block has been missed so update block arr to value 1
                block_arr.insert(0,(str(ablock),'1')) 
                
            #check for uptime condition and send uptime alarm
            if len(block_arr) >= 100:
                print('--------------')
                print('latest  :' + str(ablock) + ' process : ' + str(the_block))
                uptime = get_uptime(block_arr)
                print('UPTIME  :' + str(uptime))
                if uptime < uptime_limit:
                    send_alarm(uptime)  
                    uptime_limit = uptime_limit-5 
                elif uptime > uptime_limit_fixed :
                    uptime_limit  = uptime_limit_fixed
                block_arr.pop()               
                print('--------------')        
                
            if  the_block < ablock:
                the_block = the_block +1  
            else:
                the_block = the_block-1   
            
            print(the_block)
            uptime = get_uptime(block_arr)
            print(len(block_arr))
    except Exception as e:
        print('Exception : ' +  str(e))
        if len(block_arr) >= 100:
            block_arr.pop() 
    return

def get_uptime(a_arr):
    cnt = 0
    for x,y in a_arr:
        if y == '1':
            cnt = cnt +1
    print(coin_name +' Missed Blocks : ' +str(cnt))
    cnt = 100-cnt
    return cnt

def send_alarm(auptime):
    global coin_name
    message = coin_name+" uptime : " +str(auptime)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={the_chat_id}&text={message}"
    print(requests.get(url).json()) 
    
        
if __name__ == "__main__": 
    # check_missed_block()
    while True:
        check_missed_block()
        time.sleep(sleep_time)