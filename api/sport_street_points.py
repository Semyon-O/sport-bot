import dataclasses
from typing import *
import requests


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

    def make_request_url(self):
        response = requests.get(self.Url)
        return response.json()

    def __make_request_by(self, activity: str = "", district: str = ""):

        URl = self.Url + f"&area={district}" + f"&activity={activity}"
        response = requests.get(URl)
        return response.json()

    def get_data_by(self, activity: str = "", district: str = "") -> "Iterable[DataResponse]":
        response = self.__make_request_by(activity=activity, district=district)
        for count in response["results"]:
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


