from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time


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


def get_posts(chrome):
    chrome.get('https://www.instagram.com/explore/tags/%E5%A6%8A%E5%A8%A08%E9%80%B1/')
    time.sleep(5)

    # ターゲットとなるユーザの投稿件数を取得
    post_count = chrome.find_element_by_xpath('//span[text()="投稿"]').text
    post_count = post_count.replace('件', '').replace('投稿', '').replace(',', '')
    print('投稿件数:', post_count)
    post_count = int(post_count)
    post_urls = set()

    try:
        # 投稿件数に応じて全スクロール
        if post_count > 12:
            scroll_count = int(post_count / 12) + 1
            for _ in range(scroll_count):
                chrome.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)

                # 後でファイルに書き出すために投稿URLを集めておく
                posts = chrome.find_elements_by_xpath('//a[not(@class)]')
                for post in posts:
                    url = post.get_attribute('href')
                    if '/p/' in url:
                        post_urls.add(url)
    except:
        print('エラーが発生しました')
        print()

    # ファイルに書き出し
    post_urls = map(lambda x: x + '\n', post_urls)
    with open('post_urls.txt', 'w') as f:
        f.writelines(post_urls)

def main():
    # 初期設定
    username = input('Username: ')
    password = getpass('Password: ')
    chrome = webdriver.Chrome()

    # 処理
    login(chrome, username, password)
    get_posts(chrome)


if __name__=='__main__':
    main()
