bots information
=================

## get bot list

endpoint

  * `/bots/list`

request -> None

response

```jsoh
[
    {
        'botname': <str>,
        'useful_whe': <str>,    # description only written in text
        'descrption': <str>,    # detailed descrition written in markdown 
        'supported_message_version': List[<str>]
    },
    ...
]
```

## get signle bot

method : get

  * `/bots/detail/<botname:str>`
    * botname : 存在するボット名

request -> None

```json
{
    'botname': <str>,
    'useful_whe': <str>,    # description only written in text
    'descrption': <str>,    # detailed descrition written in markdown 
    'supported_message_version': List[<str>]
}
```


## (authentication required) single bot configuration

method : get

  * `/bots/edit/<botname:str>`
    * botname

```json
{
    'botname': <str>,
    'useful_when': <str>,    # description only written in text
    'descrption': <str>,    # detailed descrition written in markdown 
    'supported_message_version': List[<str>],
    'module_filename': <str>,
    'classname': <str>,
}
```

## (authentication required) single bot configuration upsert

method : post

  * `/bots/edit/<botname:str>`
    * botname

```json
{
    'botname': <str>,
    'useful_when': <str>,   # description only written in text
    'descrption': <str>,    # detailed descrition written in markdown 
    'supported_message_version': List[<str>],
    'module_filename': <str>,
    'classname': <str>,
}
```



