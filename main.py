from selenium import webdriver
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup
import lxml
import json
import requests

def get_data_selenium():
    try:
        user_agent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        for i in range(1, 23):
            driver.get(f"https://www.medved-holding.com/buy-car/used?page={i}")
            time.sleep(5)
        with open(f"index_{i}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_data():
    for i in range(1, 23):
        with open(f"index_{i}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_card = soup.find_all("tr-car-new-card", class_="tr-hoverable-cta")
        res_list = []
        for item in all_card:
            try:
                name_brand = item.find("div", class_="tr-heading tr-h4").find("span", class_="tr-title-brand").text
                name_model = item.find("div", class_="tr-heading tr-h4").find("span", class_="tr-title-model").text
                full_name_car = name_brand + name_model
                href_car = "https://www.medved-holding.com/" + item.find("a").get("href")
                year_car = item.find("div", class_="tr-necklace-text").text.replace('\xa0', '')
                description_car = item.find("div", class_="tr-description").text.replace('\xa0', '')
                price_car = item.find("div", class_="tr-price-primary tr-nowrap").text.replace('\xa0', '')
                res_list.append(
                    {
                        "Автомобиль": full_name_car,
                        "Год · Пробег": year_car,
                        "Описание": description_car,
                        "Цена": price_car,
                        "Ссылка": href_car
                    }
                )


                print(full_name_car)
                print(href_car)
                print(year_car)
                print(description_car)
                print(price_car)
                print("#"*10)
            except Exception as ex:
                print(ex)
        with open("result.json", "a", encoding="utf-8") as file:
            json.dump(res_list, file, indent=4, ensure_ascii=False)

#get_data_selenium()
get_data()
