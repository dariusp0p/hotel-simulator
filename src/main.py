from src.repository.reservation_repository_textfile import TextFileRepository
from src.service.service import Service

from src.ui.ui import UI


if __name__=="__main__":
    repository = TextFileRepository()
    service = Service(repository)
    ui = UI(service)
    ui.start()
