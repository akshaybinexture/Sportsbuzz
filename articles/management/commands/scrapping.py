import time
from django.apps import apps
Article = apps.get_model('articles', 'Article')
Article_detail = apps.get_model('articles', 'Article_detail')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

from datetime import datetime, timedelta


GOOGLE_CHROME_PATH = "/app/.apt/usr/bin/google-chrome"
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)

def iso_time_cal(z):
    datetime_object = datetime.strptime(z, "%Y-%m-%dT%H:%M:%S%z")
    return datetime_object


def time_cal(string):
    ini_time_for_now = datetime.now()
    hr = min = day = 0
    if string.find('hr ago') != -1:
        # hr = int(string[string.find('hr')-2])
        # print(hr)
        hr = int(''.join(filter(str.isdigit, string)))
        print(hr)

        print('found hr')
    elif string.find('min ago') != -1:
        min = int(''.join(filter(str.isdigit, string)))
        print(min)
        print('found min')
    elif string.find('d ago') != -1:
        day = int(''.join(filter(str.isdigit, string)))
        print(day)
        print('found d')
    date_posted = ini_time_for_now - timedelta(days=day, minutes=min, hours=hr)
    print('date_posted: ', str(date_posted))
    print(type(date_posted))
    return date_posted


arti_list = []
arti_detail_list = []
links = []
pages = 1
sports = ['cricket', 'football', 'wwe', 'tennis', 'basketball']
# chrome_options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=chrome_options)
def articles():
    for sport in sports:
        for page in range(1, pages + 1):
            driver.get(f'https://www.sportskeeda.com/{sport}?page={page}')
            # section = driver.find_elements_by_css_selector('.story-wrapper')
            for sec in driver.find_elements_by_css_selector('.story-wrapper'):
                try:
                    article_id = WebDriverWait(sec, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "story-link-overlay"))
                        ).get_attribute('id').split('-')[3]
                    article_id = int(article_id)
                    # article_id = sec.find_element_by_class_name("story-link-overlay").get_attribute('id').split('-')[3]
                    print(f'article-id = {article_id}')
                    heading = sec.find_element_by_class_name("story-link-overlay").text
                    print(f'heading = {heading}')
                    # time = sec.find_element_by_class_name('block-story-date').text
                    # print(f'time = {time}')
                    # date = time_cal(time)
                    # print(f'time = {date}')
                    link = sec.find_element_by_class_name("story-link-overlay").get_attribute('href')
                    print(f'link = {link}')
                    links.append(link)
                    # we have yo scroll the page to get in img url as it wil load css then find the tag or element
                    # img_url = WebDriverWait(sec, 20).until(EC.visibility_of_element_located(
                    #     (By.CLASS_NAME, "in-block-img"))).value_of_css_property("background-image")
                    # img_url = img_url.split('"')[1]
                    # print(f'img_url= {img_url}')
                    # category = link.split('/')[3]

                    category = sport
                    print(f'category = {category}')
                    # date, img_url = article_detail(link, driver)
                    arti = {
                        'article_id': article_id, 'heading': heading, 'link': link, 'category': category
                    }
                    arti_list.append(arti)
                except ValueError:
                    continue
                except NoSuchElementException:
                    continue
    return arti_list


        # print(links)
        # print(len(links))


def article_detail(link):
    # chrome_options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options=chrome_options)
    para_list = []
    tweet_list = []
    driver.get(link)
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    print(link)
    heading = driver.find_element_by_id('heading').text
    print(heading)
    try:
        img_url = driver.find_element_by_css_selector('.intro img').get_attribute('src')
    except:
        NoSuchElementException
        img_url = None
    print(f'img_url = {img_url}')
    # time = driver.find_element_by_css_selector('.article-modified-date').text.split(" ")
    # if len(time)>4:
    #     time.pop(0)
    #     time.pop(-1)
    # else:
    #     time.pop(0)
    # datetime = " ".join(time)
    # print(f'time:{datetime}')
    try:
        time = driver.find_element_by_css_selector('.article-modified-date').get_attribute('data-iso-string')
        print(f'time =@ {time}')
        cal_time = iso_time_cal(time)
        print(f'time = {cal_time}')
    except:
        NoSuchElementException


    section = driver.find_element_by_css_selector('#article-content')
    # paras = section.find_elements_by_css_selector('p')
    # for para in paras:
    #     try:
    #         p = para.text
    #         para_list.append(p)
    #     except:
    #         StaleElementReferenceException
    section1 = soup.find('div', attrs={"id": "article-content"}).find_all(["p", "blockquote"])
    for sec in section1:
        text = sec.text
        para_list.append(text)
    print(para_list)
    description = {
        'description': para_list
    }
    print(description)

    try:
        tweet_urls = section.find_elements_by_css_selector('.sportskeeda-embed')
        for i in tweet_urls:
            tweet = WebDriverWait(i, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))).get_attribute('src')
            tweet_list.append(tweet)
    except:
        tweet_list = []
    tweets = {
        'tweets': tweet_list
    }
    print(f'{tweets}: tweets')


    # try:
    #     tweet_url = section.find_element_by_css_selector('#twitter-widget-0').get_attribute('src')
    #
    # except:
    #     NoSuchElementException
    #     tweet_url = None
    # print(f'tweet_url: {tweet_url}')
    article_id_detail = section.get_attribute('data-slug-id')
    print(f'article_id_detail = {article_id_detail}')
    arti_detail = {
        'article_id_detail': article_id_detail, 'heading': heading, 'img_url': img_url, 'time': cal_time, 'description': description, 'tweet_url': tweets
    }
    arti_detail_list.append(arti_detail)
    # driver.close()
    return cal_time, img_url



def save_function(arti_list):
    print('starting arti_list')
    new_count = 0

    for art in arti_list:
        try:
            Article.objects.get_or_create(
                article_id=art['article_id'],
                heading=art['heading'],
                article_link=art['link'],
                date_posted=art['datetime'],
                category=art['category'],
                img_url=art['img_url']
            )
            new_count += 1
        except Exception as e:
            print('failed at article list data')
            print(e)
            continue
    print('Starting arti_detail_list')
    for i in range(len(arti_detail_list)):
        try:
            # user = User.objects.only('id').get(id=data['user_id'])
            # obj = ModelA.objects.create(phone=data['phone'], user=user)
            article = Article.objects.only('article_id').get(article_id=arti_list[i]['article_id'])
            # obj = Article_detail.objects.create(phone=data['phone'], user=user)
            Article_detail.objects.get_or_create(
                article_detail_id=article,
                heading=arti_detail_list[i]['heading'],
                img_url=arti_detail_list[i]['img_url'],
                date_posted=arti_detail_list[i]['time'],
                description=arti_detail_list[i]['description'],
                tweet_url=arti_detail_list[i]['tweet_url']
            )
            new_count += 1
        except Exception as e:
            print('failed at article_detail data')
            print(e)
            continue
    print(f'length 0f article list{len(arti_list)}')
    print(f'length 0f article detail list{len(arti_detail_list)}')
    return print('finished')


# list1 = articles()
def main_scrapping():
    list1 = articles()
    for i in range(len(list1)):
        link = list1[i]['link']
        dtime, img_url = article_detail(link)
        list1[i]['datetime'] = dtime
        list1[i]['img_url'] = img_url
    save_function(arti_list)

# driver.close()



# for link in links:
#     para_list = []
#     driver.get(link)
#     source = requests.get(link).text
#     soup = BeautifulSoup(source, 'lxml')
#     print(link)
#     heading = driver.find_element_by_id('heading').text
#     print(heading)
#     img_url = driver.find_element_by_css_selector('.intro img').get_attribute('src')
#     print(f'img_url = {img_url}')
#     time = driver.find_element_by_css_selector('.article-modified-date').text.split(" ")
#     time.pop(0)
#     time.pop(-1)
#     datetime = "".join(time)
#     print(f'time:{datetime}')
#     section = driver.find_element_by_css_selector('#article-content')
#     # paras = section.find_elements_by_css_selector('p')
#     # for para in paras:
#     #     try:
#     #         p = para.text
#     #         para_list.append(p)
#     #     except:
#     #         StaleElementReferenceException
#     section1 = soup.find('div', attrs={"id": "article-content"}).find_all(["p", "blockquote"])
#     for sec in section1:
#         text = sec.text
#         para_list.append(text)
#     print(para_list)
#     description = {
#         'description': para_list
#     }
#     print(description)
#     try:
#         tweet_url = section.find_element_by_css_selector('#twitter-widget-0').get_attribute('src')
#
#     except:
#         NoSuchElementException
#         tweet_url = None
#     print(f'tweet_url: {tweet_url}')
#     article_id_detail = section.get_attribute('data-slug-id')
#     print(f'article_id_detail = {article_id_detail}')
#     arti_detail = {
#         'article_id_detail': article_id_detail,'heading': heading, 'img_url': img_url, 'time': time, 'description': description, 'tweet_url': tweet_url
#     }
#     arti_detail_list.append(arti_detail)



print(f'arti_list = {arti_list}')
print(f'arti_detail_list = {arti_detail_list}')

# for i in range(len(arti_list)):
#     query = "INSERT OR IGNORE  INTO Article VALUES(?,?,?,?,?,?);", (arti_list[i]['article_id'],
#                                                                      (arti_list[i]['heading'],
#                                                                      (arti_list[i]['link'],
#                                                                      (arti_list[i]['datetime'],
#                                                                      (arti_list[i]['category'],
#                                                                      (arti_list[i]['img_url'],)
#     obj = Database(query)
#     obj.execute()




# save_function(arti_list)