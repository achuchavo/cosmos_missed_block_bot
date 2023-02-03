# COSMOS MISSED BLOCK TELEGRAM BOT
Telegram Alarm Bot for Cosmos Missed Blocks 

- After cloning rename config_dummy.py to config_dummy.py
- In config.py paste your Telegram Bot TOKEN

# Run using just one Script [mb_cosmos.py]

Run Using the following command :

```
   python3 mb_cosmos.py [coin_name] [rpc_endpoint] [sleep_time] [uptime_count_threshhold] [validator_addr]
```

#### Parameters 

| #    | Type                               | Description                                                  |
| ---- | ---------------------------------- | ------------------------------------------------------------ |
| 1    | [coin_name]                 | coin name e.g EVMOS                               |
| 2    | [rpc_endpoint] | Public RPC Endpoint |
| 3    | [sleep_time] | Sleep time timer interval |
| 4    | [uptime_count_threshhold]| Level at which when dropped will signal alarm bot |
| 4    | [validator_addr]| Validator Address |


#### EXAMPLE (EVMOS)

```
   python3 mb_cosmos.py EVMOS https://evmos-rpc.polkachu.com 0.2 90 C52CF80E872A4F2CC3A114A733D301A421C857F0
```

#### TO GET VALIDATOR ADDRESS RUN

```
   curl -X GET "http://localhost:26657/status" | jq
```


