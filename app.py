import httpx
import asyncio
import random
from colorama import Fore, Style, init
import os
import time

init()

REFRESH_CLICK = 120  # Refresh click in 120 seconds

async def getState(session, query):
    url = "https://app2.firecoin.app/api/loadState"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"tma {query}",
        "origin": "https://app2.firecoin.app",
        "priority": "u=1, i",
        "referer": "https://app2.firecoin.app/",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Content-Type": "text/plain; charset=utf-8"
    }

    while True:
        try:
            resp = await session.post(url, headers=headers, data="{}")
            resp.raise_for_status()  
            return resp.json()
        except httpx.HTTPError as e:
            print(f"HTTP Error fetching state, retrying... {e}")
            await asyncio.sleep(5) 

async def Clicker(session, query, current_clicks):
    url = "https://app2.firecoin.app/api/click"
    number_click = current_clicks + random.randint(100000, 10000000)
    payload = f"{{\"clicks\":{number_click}}}" 
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"tma {query}",
        "origin": "https://app2.firecoin.app",
        "priority": "u=1, i",
        "referer": "https://app2.firecoin.app/",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Content-Type": "text/plain; charset=utf-8"
    }

    while True:
        try:
            resp = await session.post(url, headers=headers, data=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            print(f"HTTP Error sending click, retrying... {e}")
            await asyncio.sleep(5) 

async def earnTasks(session, query, task_name):
    url = f"https://app2.firecoin.app/api/{task_name}"
    headers = {
        "accept": "*/*",
        "accept-language": "en,en-US;q=0.9,id;q=0.8",
        "authorization": f"tma {query}",
        "content-length": "0", 
        "dnt": "1",
        "origin": "https://app2.firecoin.app",
        "priority": "u=1, i",
        "referer": "https://app2.firecoin.app/earn",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    while True:
        try:
            resp = await session.post(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            print(f"HTTP Error with task '{task_name}', retrying... {e}")
            await asyncio.sleep(5) 

async def boosterUp(session, query, item_name):
    url = "https://app2.firecoin.app/api/buyBooster"
    payload = f"{{\"code\":\"{item_name}\"}}"
    headers = {
        "accept": "*/*",
        "accept-language": "en,en-US;q=0.9,id;q=0.8",
        "authorization": f"tma {query}",
        "dnt": "1",
        "origin": "https://app2.firecoin.app",
        "priority": "u=1, i",
        "referer": "https://app2.firecoin.app/boosts",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Content-Type": "text/plain; charset=utf-8"
    }

    while True:
        try:
            resp = await session.post(url, headers=headers, data=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            print(f"HTTP Error activating booster '{item_name}', retrying... {e}")
            await asyncio.sleep(5)

async def runAll(query):
    async with httpx.AsyncClient() as session:
        load = await getState(session, query)

        userid = load['user_id']
        balance = load['clicks']
        wood_count = load['wood']['count']
        wood_max = load['wood']['max_value']

        next_info = await Clicker(session, query, balance)
        next_user = next_info.get('nextUser', {}).get('name', 'N/A')
        next_balance = next_info.get('nextUser', {}).get('clicks', 'N/A')

        twitter_task = load['task_twitter']
        telegram_task = load['task_telegram']
        status_task = f"{Fore.GREEN}Completed{Style.RESET_ALL}"
        if twitter_task == 0 or telegram_task == 0: 
            for task_name in ['followTwitterBonus', 'joinChannelBonus']:
                task_result = await earnTasks(session, query, task_name)
                if not task_result.get('success', False):
                    status_task = f"{Fore.RED}Failed{Style.RESET_ALL}"
                    break 

        AUTO_BOOSTER = True #True for activate auto booster
        status_autoboost = f"{Fore.GREEN}On{Style.RESET_ALL}" if AUTO_BOOSTER else f"{Fore.RED}Off{Style.RESET_ALL}"
        
        if AUTO_BOOSTER:
            for booster in ['bot', 'tapmul', 'regen', 'max']:
                await boosterUp(session, query, booster)

        print(f"[{userid}] | Balance: {Fore.GREEN}{balance}{Style.RESET_ALL} | Wood: {Fore.YELLOW}{wood_count}/{wood_max}{Style.RESET_ALL} | Next: {next_user} - {next_balance} | Tasks: {status_task} | Auto Boosters: {status_autoboost}")

async def main():
    os.system("cls" if os.name == "nt" else "clear") 

    while True:
        print("""
  __ _                    _         _           _   
 / _(_)_ __ ___  ___ ___ (_)_ __   | |__   ___ | |_ 
| |_| | '__/ _ \/ __/ _ \| | '_ \  | '_ \ / _ \| __|
|  _| | | |  __/ (_| (_) | | | | | | |_) | (_) | |_ 
|_| |_|_|  \___|\___\___/|_|_| |_| |_.__/ \___/ \__|
        """)
        start = time.time()
        tasks = []
        try:
            with open('query.txt', 'r') as qf:
                for line in qf:
                    query = line.strip()
                    tasks.append(asyncio.create_task(runAll(query)))
            await asyncio.gather(*tasks) 

        except FileNotFoundError:
            with open('query.txt', 'w') as qf:
                qf.write("query1\nquery2\nquery3\n...")
                print("query.txt not found, created a sample file. Please add your queries!")
                await asyncio.sleep(5) 
                continue 

        finish = time.time() - start
        time_delay = REFRESH_CLICK 
        while time_delay > 0:
            mins, secs = divmod(time_delay, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"Execution Time: {Fore.YELLOW}{round(finish, 2)}{Style.RESET_ALL}s | Refresh: {Fore.YELLOW}{timer}{Style.RESET_ALL}s", end="\r")
            time.sleep(1)
            time_delay -= 1
        os.system("cls" if os.name == "nt" else "clear") 

if __name__ == "__main__":
    asyncio.run(main()) 