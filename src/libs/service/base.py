from pydantic import BaseModel
from typing import ClassVar


class Service(BaseModel):
    """
    Service class is responsible to fasilates the
     connection between the API and the bussiness logic via one feature :
    implement a class to use the pydantic full features
    """

    def run(self):
        return self.dict()
