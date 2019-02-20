# title:           	Scraper.py
# description:
# author:          	Roman Tochony
# date:            	20.2.2019
# version:          1.0
# notes:
# python_version:   Python 3.7.2

from bs4 import BeautifulSoup
from urllib.request import urlopen
from WebScrape import Config
from Data.DataManager import Container
import re


class Scraper:
    def __init__(self):
        try:
            html_data = self._get_html_by_url(Config.url)
            self.html_tags = html_data.findAll('tr')
        except Exception as e:
            raise Exception("Something went wrong during url connecting:{}".format(e))

    @staticmethod
    def _get_html_by_url(url):
        """This function download html by url and return it as parsed object"""
        raw_html = urlopen(url).read().decode('utf-8')
        html_doc = BeautifulSoup(raw_html, 'html.parser')
        return html_doc

    def get_data_from_html_to_obj(self):
        heap = []
        for i in self.html_tags:
            heap.append(self._get_elements_in_obj_container(i))
        return heap

    @staticmethod
    def _get_elements_in_obj_container(elements):
        """This function will extract/parse needed data and will arrange it into the objects"""
        data = []
        try:
            for element in elements:
                for content in element:
                    if content != '\n':
                        if str(type(content)) == "<class 'bs4.element.Tag'>":
                            data.append(str(content['data-label']))
                            data.append(str(content['href']))
                        else:
                            reg_cont = re.search('(\d.\d.*) \((.*)\)|\((.*)\),', content)
                            if reg_cont:
                                date = re.search('(\w{3} \d{4})', reg_cont.group(2)) if re.search('(\w{3} \d{4})', reg_cont.group(2)) else 'NA'
                                if date != 'NA':
                                    data.append('{} {}'.format(reg_cont.group(1), reg_cont.group(2).split(',')[0]))
                                    data.append(date.group())
                                else:
                                    data.append('{} {}'.format(reg_cont.group(1), reg_cont.group(2)))
                                    data.append(date)
                            else:
                                data.append(content)

            return Container(data[0], data[1], data[2], data[3], data[4])
        except Exception as e:
            raise Exception("Something went wrong during parsing html file:{}".format(e))

    @staticmethod
    def download_android_images_links(elements):
        """This function simulated file downloading"""
        for element in elements:
            print('File downloading : ' + element.link)
        print('All files downloaded successfully.')

    @staticmethod
    def show_missing_elements(elements):
        """This function will display missing Images"""
        print("Missing Images on web site")
        for element in elements:
            print('Changed to unusable : ' + element.link)
        print('All changed successfully.')
