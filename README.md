# Ansible dynamic inventory for MongoDB

Helps to get ansible dynamic inventory from MongoDB

## How to use
### 1. Set environment variables
`INV_MONGO_URI` - Mongo uri with all required credentials.

`INV_MONGO_DB` - Mongo inventory database.

`INV_INCLUDE_META` - [optional] Set to include hosts _meta to inventory. Otherwise ansible will request host data one by one.


### 2. Create collections `groups` and `hosts`
Group object example:
```json
{
    "name": "group_name",
    "children": [
        "child_group_1",
        "child_group_2"
    ],
    "hosts": [
        "192.168.28.71",
        "192.168.28.72"
    ],
    "vars": {
        "ansible_ssh_user": "no_root",
        "ansible_ssh_private_key_file": "~/.ssh/root_key",
        "is_foo": True,
        "bar_qty": 123
    }
}
```

Host object example:
```json
{
    "name": "dns.google.com",
    "ansible_host": "8.8.8.8",
    "foo": "bar"
}
```

### 3. Is it default inventory?
To replace default inventory you don't need everytime add your groups to `all`

Just add groups `all` and `ungrouped` to groups in your database:
```json
{
    "name" : "all",
    "children" : ["ungrouped"],
    "vars" : {}
}
```
```json
{
    "name" : "ungrouped",
    "children" : [],
    "hosts" : [
        # names of all ungrouped hosts
    ]
}
```

### 4. Enable script
Add [mongo.py](https://gitlab.com/true-web-app/ci-cd/mongodb-inventory/-/blob/master/mongo.py) file in your `hosts` directory or set it as a inventory directly via `ansible-playbook your_playbook.yml -i mongo.py`

#### Done :)
