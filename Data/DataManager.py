# title:           	DataManager.py
# description:
# author:          	Roman Tochony
# date:            	20.2.2019
# version:          1.0
# notes:
# python_version:   Python 3.7.2

import json


class Container:
    """Object initiator function"""
    def __init__(self, version='', date='', description='', link='', sha='', is_valid=True):
        self.version = version
        self.date = date
        self.description = description
        self.link = link
        self.sha = sha
        self.is_valid = is_valid

    @staticmethod
    def _obj_compare(data, html_element):
        """This function get two objects and compare between them by [Version,date,description,link,sha],
        the function will return true in case two objects are equals else will return false"""
        if(data.version != html_element.version or
            data.date != html_element.date or
            data.description != html_element.description or
            data.link != html_element.link or
            data.sha != html_element.sha or
                data.is_valid != html_element.is_valid):
            return False
        return True

    @staticmethod
    def _sort_objects_list(obj_list):
        """This function will sort objects list by the link"""
        sorted_list = sorted([x for x in obj_list], key=lambda x: x.sha) if len(obj_list) > 0 else []
        return sorted_list

    def get_object_lists_differences(self, data, html_doc):
        """This function will get two lists contains objects, will check if those lists are equals,greater or smaller
         the differences will be returned by dictionary that contain html or/and file missing objects"""
        missing_sw_versions = {}

        data = self._sort_objects_list(data)
        html_doc = self._sort_objects_list(html_doc)

        extracted_sha = [x.sha for x in html_doc]
        differences_file = [item for item in data if item.sha not in extracted_sha
                                and self._is_valid_obj(item)]

        extracted_sha = [x.sha for x in data]
        differences_html_doc = [item for item in html_doc if item.sha not in extracted_sha]

        missing_sw_versions['from_html'] = differences_html_doc
        missing_sw_versions['from_db'] = differences_file
        return missing_sw_versions

    @staticmethod
    def objects_list_to_json(obj_list):
        """This function will get list of objects and write into file in JSON format"""
        temp = []
        try:
            for obj in obj_list:
                temp.append(json.dumps(obj.__dict__))
            temp = [json.loads(x) for x in temp]
            return temp
        except Exception as e:
            raise Exception("Something went wrong during converting object to json:{}".format(e))

    @staticmethod
    def json_collections_to_obj(collection_list):
        """This function will get list of collection and turned them out to list of objects"""
        try:
            temp = []
            for x in collection_list:
                temp.append(Container(
                    x['version'],
                    x['date'],
                    x['description'],
                    x['link'],
                    x['sha'],
                    x['is_valid']
                ))
            return temp

        except Exception as e:
            raise Exception("Something went wrong during converting collection to object:{}".format(e))

    @staticmethod
    def _is_valid_obj(single_collection):
        """This helper function will check validation bit of object"""
        if single_collection.is_valid:
            return True
        return False

    @staticmethod
    def is_valid_collection(single_collection):
        """This helper function will check collection validity"""
        if single_collection['is_valid']:
            return True
        return False

    @staticmethod
    def turn_valid_collections(invalid_collections_list, html_valid_collections):
        """This function will check if there is collection that
        should returned to valid bit and return list of those collections"""
        extracted_sha = [x.sha for x in html_valid_collections]
        true_change_collections = [item for item in invalid_collections_list if item['sha'] in extracted_sha]
        return true_change_collections
