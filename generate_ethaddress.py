import inquirer
import os
import platform
import sys
from eth_account import Account
from loguru import logger
from questionary import Choice, select
from termcolor import cprint

def get_address_by_key(key):
    account = Account.from_key(key)
    return account.address

def get_file_content(file_name):
    with open(file_name, 'r') as f:
        data = [line.strip() for line in f.readlines()]

    return data

def get_data_for_key(name):
    # print("name: ",name)
    if name == '':
        file = f'generate/wallets.txt'
    else:
        file = f'generate/wallets-{name}.txt'
    datas = get_file_content(file)
    return datas

def set_data_for_key(name, address, privatekey):
    # print("name: ",name)
    if name == '':
        file = f'generate/wallets.txt'
    else:
        file = f'generate/wallets-{name}.txt'
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            line = line.replace(privatekey, f"{address},{privatekey}")
            file_data += line
    with open(file, "w") as f:
        f.write(file_data)

def set_data_add_key(name, privatekey):
    # print("name: ",name)
    if name == '':
        file = f'generate/wallets.txt'
    else:
        file = f'generate/wallets-{name}.txt'
    with open(file, "a") as f:
        f.writelines(privatekey + '\n')

def generate_privkey(name):
    while True:
        try:
            enter_count = [
                inquirer.Text('count', message="👉 输入账户数量")
            ]
            count = int(inquirer.prompt(enter_count, raise_keyboard_interrupt=True)['count'])
            if count > 0:
                break
            else:
                logger.info("❌  请输入正数.\n")
        except ValueError:
            logger.info("❌  请输入一个数字.\n")
    for id in range(count):
        acct = Account.create()
        privatekey = acct.key.hex()
        set_data_add_key(name, privatekey)
        print(id, privatekey)
    logger.success(f"批量生成 {count} 钱包私钥 -> generate/wallets{name}.txt")

def generate_address(name):
    datas = get_data_for_key(name)
    count = len(datas)
    while True:
        if not datas:
            print("nokey")
            break
        else:
            data = datas.pop(0)
            id = count-len(datas)
        if len(data.split(',')) == 2:
            continue
        privatekey=data.split(',')[0]
        address = get_address_by_key(privatekey)
        set_data_for_key(name, address, privatekey)
        print(id, address, privatekey)
    logger.success(f"批量计算 {count} 钱包地址 -> generate/wallets{name}.txt")

def choose_name() -> str:
    enter_name = [
        inquirer.Text('name', message="👉 输入名字")
    ]
    name = inquirer.prompt(enter_name, raise_keyboard_interrupt=True)['name']
    return name

def main():
    try:
        while True:
            if platform.system().lower() == 'windows':
                os.system("title main")
            answer = select(
                '选择',
                choices=[
                    Choice("🔥 批量生成ETH私钥", 'generate_privkey', shortcut_key="1"),
                    Choice("🚀 批量计算ETH地址", 'generate_address', shortcut_key="2"),
                    Choice('❌ Exit', "exit", shortcut_key="0")
                ],
                use_shortcuts=True,
                use_arrow_keys=True,
            ).ask()
            if answer == 'generate_privkey':
                name = choose_name()
                generate_privkey(name)
            elif answer == 'generate_address':
                name = choose_name()
                generate_address(name)
            elif answer == 'exit':
                sys.exit()
    except KeyboardInterrupt:
        cprint(f'\n 退出，请按<Ctrl + C>', color='light_yellow')
        sys.exit()


if __name__ == '__main__':
    main()
