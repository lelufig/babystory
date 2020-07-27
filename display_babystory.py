from selenium import webdriver
from getpass import getpass
import time
from datetime import datetime


def get_target_urls(file_name):
    with open(file_name) as f:
        target_urls = f.read().split()
    return target_urls


def login(chrome, username, password):
    chrome.get('https://www.instagram.com/?hl=ja')
    time.sleep(3)

    chrome.find_element_by_name('username').send_keys(username)
    chrome.find_element_by_name('password').send_keys(password)
    chrome.find_element_by_tag_name("form").find_elements_by_tag_name("button")[1].click()
    time.sleep(5)

    chrome.find_element_by_xpath('//button[text()="後で"]').click()
    time.sleep(1)

    chrome.find_element_by_xpath('//button[text()="後で"]').click()
    time.sleep(1)


def get_posts_by_keyword(chrome, target_urls, filter_date):
    print('=' * 80)
    for target_url in target_urls:
        try:
            chrome.get(target_url)
            time.sleep(2)

            # ターゲットとなるユーザの投稿件数を取得
            poster_name = chrome.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').text
            post_body = chrome.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
            post_date_str = chrome.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[2]/a/time').get_attribute('datetime')
            post_date = datetime(year=int(post_date_str[0:4]), month=int(post_date_str[5:7]), day=int(post_date_str[8:10]))

            # ここから表示
            if post_date >= filter_date:
                print('🌟', poster_name, 'さんの投稿', post_date)
                print(target_url)
                print(post_body)
                print('=' * 80)

        except KeyboardInterrupt:
            print()
            if 'n' ==input('Continue?[y/n]: '):
                break

        except:
            print('エラーが発生しました')
            print(target_url)
            print('=' * 80)


def main():
    # 初期設定
    username = input('Username: ')
    password = getpass('Password: ')
    filter_date = datetime.strptime(input('Date after: '), '%Y-%m-%d')
    print('Collect posts after - ', filter_date)
    target_urls = get_target_urls('post_urls.txt')
    chrome = webdriver.Chrome()

    # 処理
    login(chrome, username, password)
    get_posts_by_keyword(chrome, target_urls, filter_date)


if __name__=='__main__':
    main()
