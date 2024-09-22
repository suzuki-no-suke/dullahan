v1 message definition
=====================

## message types

  * `human` : human -> bots
  * `chatbot` : bots -> human

## chat message : user -> bots

```json
{
    'message_id': <uuid>,
    'time': <datetime>,
    'type': 'human',    # fixed values
    'botname': <str>,   # chatbot request to 
    'message': <str>,   # string only
}
```


## chat message : bots -> user

```json
{
    'message_id': <uuid>,
    'time': <datetime>,
    'type': 'chatbot',      # fixed values
    'botname': <str>,       # chatbot response by
    'agent': <str>,         # internal botname
    'message': <str>,       # string only
}
```


