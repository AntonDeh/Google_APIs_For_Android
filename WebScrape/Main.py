# title:           	Main.py
# description:
# author:          	Roman Tochony
# date:            	20.2.2019
# version:          1.0
# notes:
# python_version:   Python 3.7.2


from WebScrape.Scrape import *
from Data.DB_Worker import *


def main():
    try:
        db = MongoDB()
        container = Container()
        scraper = Scraper()

        #TODO Check if it is first connection

        html_collections_converted_to_obj = scraper.get_data_from_html_to_obj()
        db_collections_converted_obj = container.json_collections_to_obj(db.read_collections_from_db())
        db.set_true_for_valid_incoming_Images(container.turn_valid_collections(db.find_invalid_collections_from_db(),
                                                                               html_collections_converted_to_obj))

        dic_of_collections = container.get_object_lists_differences(db_collections_converted_obj,
                                                                    html_collections_converted_to_obj)

        if len(dic_of_collections['from_db']) > 0:
            db.set_false_for_not_listed_collections(container.objects_list_to_json(dic_of_collections['from_db']))
            scraper.show_missing_elements(dic_of_collections['from_db'])
        if len(dic_of_collections['from_html']) > 0:
            db.fill_collections_to_db(container.objects_list_to_json(dic_of_collections['from_html']))
            scraper.download_android_images_links(dic_of_collections['from_html'])

    except Exception as e:
        print("Some issue was happen: {}".format(e))


if __name__ == '__main__':
    print('----------------------Running GoogleAPIsForAndroid Scraper ----------------------')
    main()
    print('-------------------------All Done!!!-------------------------------')

