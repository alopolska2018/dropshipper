import json

def open_json_file():
    with open('removebg_accounts.json', 'r') as file:
        accounts_dict = json.load(file)
        return accounts_dict

def save_json_file(data):
    with open('removebg_accounts.json', 'w') as file:
        json.dump(data, file)

def run():
    index = 0
    accounts_dict = open_json_file()
    for account in accounts_dict['accounts']:
        if 'api_key' in account:
            index += 1
        else:
            print(f'login: {account["login"]}, password: {account["password"]}')
            api_key = input('Podaj klucz api: ')
            if api_key:
                accounts_dict['accounts'][index]['api_key'] = api_key
                index += 1
    save_json_file(accounts_dict)

if __name__ == '__main__':
    run()