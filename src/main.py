from src.service.controller import Controller

from db import reservation_model
from src.ui.ui import UI



if __name__=="__main__":
    reservation_model.create_reservation_table()
    repository = TextFileRepository()
    service = Controller(repository)
    ui = UI(service)
    ui.start()
