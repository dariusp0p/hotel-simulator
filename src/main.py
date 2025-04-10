from src.domain.validators import ReservationValidator
from src.repository.text_file_repository import TextFileRepository
from src.service.service import Service

from src.ui.ui import UI


if __name__=="__main__":
    validator = ReservationValidator()
    repository = TextFileRepository()
    service = Service(repository, validator)
    ui = UI(service)
    ui.start()
