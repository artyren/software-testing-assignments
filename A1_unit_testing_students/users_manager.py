import os, json
def rollback_json():
    os.remove("users.json")
    os.system('cp users_backup.json users.json')


def get_json(path):
    with open(path, "r") as users:
        return json.load(users)

