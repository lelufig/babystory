from selenium import webdriver
from getpass import getpass
import time


def get_target_urls(file_name):
    with open(file_name) as f:
        target_urls = f.read().split()
    return target_urls


def login(chrome, username, password):
    chrome.get('https://www.instagram.com/?hl=ja')
    time.sleep(1)

    chrome.find_element_by_name('username').send_keys(username)
    chrome.find_element_by_name('password').send_keys(password)
    chrome.find_element_by_tag_name("form").find_elements_by_tag_name("button")[1].click()
    time.sleep(3)

    chrome.find_element_by_xpath('//button[text()="後で"]').click()
    time.sleep(3)

    chrome.find_element_by_xpath('//button[text()="後で"]').click()
    time.sleep(3)


def get_posts_by_keyword(chrome, target_urls, keyword):
    for target_url in target_urls:
        print('投稿者:', target_url)

        try:
            chrome.get(target_url)

            # ターゲットとなるユーザの投稿件数を取得
            post_count = chrome.find_element_by_xpath('//span[text()="投稿"]').text
            post_count = post_count.replace('件', '').replace('投稿', '').replace(',', '')
            print('投稿件数:', post_count)
            post_count = int(post_count)

            # 投稿件数に応じて全スクロール
            if post_count > 12:
                scroll_count = int(post_count / 12) + 1
                for _ in range(scroll_count):
                    chrome.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(2)
                images = chrome.find_elements_by_xpath('//img//ancestor::a')
                images = filter(lambda x: x.find_element_by_tag_name('img').get_attribute('alt').find(keyword) >= 0, images)

                print('=' * 80)
                for image in images:
                    print('🌟', image.get_attribute('href'))
                    print(image.find_element_by_tag_name('img').get_attribute('alt'))
                    print('=' * 80)
            print()
        except:
            print('エラーが発生しました')
            print()


def main():
    # 初期設定
    username = input('Username: ')
    password = getpass('Password: ')
    keyword = input('Keyword: ')
    target_urls = get_target_urls('urls.txt')
    chrome = webdriver.Chrome()

    # 処理
    login(chrome, username, password)
    get_posts_by_keyword(chrome, target_urls, keyword)


if __name__=='__main__':
    main()
