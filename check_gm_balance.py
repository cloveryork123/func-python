import datetime
import inquirer
import os
import platform
import sqlite3
import sys
import time
from loguru import logger
from questionary import Choice, select
from termcolor import cprint

def get_balance(name):
    if len(name) > 0:
        conn = sqlite3.connect(f'accounts-{name}.db')
    else:
        conn = sqlite3.connect(f'accounts.db')
    cursor = conn.cursor()

    today = datetime.date.today().strftime('%Y%m%d')

    ## 查看余额
    cursor.execute("SELECT id,address,checkin,balance FROM accounts WHERE id > ?", (0,))
    accounts = cursor.fetchall()
    count_all = len(accounts)
    count_fail = 0
    count_success = 0
    for account in accounts:
        # print("account:", account)
        checkin_timestamp = int(account[2])
        checkin_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(checkin_timestamp))
        checkin_day = time.strftime("%Y%m%d", time.localtime(checkin_timestamp))
        # logger.debug(f"today: {today} checkin_day: {checkin_day} calc: {int(today) - int(checkin_day)}")
        if int(today) - int(checkin_day) > 1:
            count_fail+=1
            logger.error(f"id: {account[0]} address: {account[1]} checkin: {checkin_date} balance: {account[3]}")
        elif int(today) - int(checkin_day) == 1:
            count_fail+=1
            logger.info(f"id: {account[0]} address: {account[1]} checkin: {checkin_date} balance: {account[3]}")
        else:
            count_success+=1
            logger.success(f"id: {account[0]} address: {account[1]} checkin: {checkin_date} balance: {account[3]}")
    logger.success(f"all: {count_all} success: {count_success} fail: {count_fail} ")

    cursor.close()
    conn.close()

def update_id(name):
    if len(name) > 0:
        conn = sqlite3.connect(f'accounts-{name}.db')
    else:
        conn = sqlite3.connect(f'accounts.db')
    cursor = conn.cursor()

    # 更新数据
    cursor.execute("SELECT * FROM accounts WHERE id > ?", (0,))
    accounts = cursor.fetchall()
    for account in accounts:
        # print("account:", account)
        cursor.execute("UPDATE accounts SET id = ? WHERE id = ?", (account[0], account[0]))
        conn.commit()

    cursor.close()
    conn.close()

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
                    Choice("🔥 获取余额", 'get_balance', shortcut_key="1"),
                    Choice("🚀 更新ID", 'update_id', shortcut_key="2"),
                    Choice('❌ Exit', "exit", shortcut_key="0")
                ],
                use_shortcuts=True,
                use_arrow_keys=True,
            ).ask()
            if answer == 'get_balance':
                name = choose_name()
                get_balance(name)
            elif answer == 'update_id':
                name = choose_name()
                update_id(name)
            elif answer == 'exit':
                sys.exit()
    except KeyboardInterrupt:
        cprint(f'\n 退出，请按<Ctrl + C>', color='light_yellow')
        sys.exit()


if __name__ == '__main__':
    main()
