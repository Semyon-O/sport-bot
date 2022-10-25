import dataclasses
from enum import Enum
from typing import *
import requests

"URL:  " \
"https://classif.gov.spb.ru/api/public/version/3517/structure_version/579/" \
"?page=1&number=&name=&activity=&address=&addressy=&metro=" \
"&area=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9&" \
"phone=&site=&status=&time=&reach=&others=&data_display=&per_page=10"


class BaseClassif:

    def __init__(self, version, structure_version):
        self.version = version
        self.structure_version = structure_version

    @property
    def Url(self):
        url: str = fr"https://classif.gov.spb.ru/api/public/version/{self.version}/structure_version/{self.structure_version}/?"
        return url


class Street(BaseClassif):

    # TODO: Занести эти параметры в @property
    _version = "3517"
    _structure_version = "579"

    def __init__(self):
        BaseClassif.__init__(self, self._version, self._structure_version)

    def make_request(self):
        response = requests.get(self.Url)
        return response.json()

    def __make_request_by(self, activity: str = "", district: str = ""):
        "URL:  " \
        "https://classif.gov.spb.ru/api/public/version/3517/structure_version/579/" \
        "?page=1&number=&name=&activity=&address=&addressy=&metro=" \
        "&area=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9&" \
        "phone=&site=&status=&time=&reach=&others=&data_display=&per_page=10"


        URl = self.Url + f"&area={district}" + f"&activity={activity}"
        response = requests.get(URl)
        return response.json()

    def get_data_by(self, activity: str = "", district: str = ""):
        response = self.__make_request_by(activity=activity, district=district)
        for count in response["results"]:
            print(count["row"])
            DataResponse.number = count["row"]["number"]
            DataResponse.name = count["row"]["name"]
            DataResponse.activity = count["row"]["activity"]
            DataResponse.address = count["row"]["address"]
            DataResponse.addressy = count["row"]["addressy"]
            DataResponse.coordinates = count["row"]["coordinates"]
            DataResponse.metro = count["row"]["metro"]
            DataResponse.phone = count["row"]["phone"]
            DataResponse.site = count["row"]["site"]
            DataResponse.status = count["row"]["status"]
            DataResponse.area = count["row"]["area"]
            DataResponse.time = count["row"]["time"]
            yield DataResponse


@dataclasses.dataclass
class DataResponse():
    number = Any
    name = ...
    activity = ...
    address = ...
    addressy = ...
    coordinates = ...
    metro = ...
    area = ...
    phone = ...
    site = ...
    status = ...
    time = ...
    reach = ...

