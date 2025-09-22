class ApplicationException(Exception):
    pass

class ValidationError(ApplicationException):
    pass


class DatabaseError(ApplicationException):
    pass
class DatabaseUnavailableError(DatabaseError):
    pass

class RepositoryError(ApplicationException):
    pass

class ReservationAlreadyExistsError(RepositoryError):
    pass
class ReservationNotFoundError(RepositoryError):
    pass

class FloorAlreadyExistsError(RepositoryError):
    pass
class FloorNotFoundError(RepositoryError):
    pass

class ElementAlreadyExistsError(RepositoryError):
    pass
class ElementNotFoundError(RepositoryError):
    pass





class ServiceError(ApplicationException):
    pass

class ActionError(ApplicationException):
    pass

class ControllerError(ApplicationException):
    pass

class InputError(ApplicationException):
    pass

class ConfiguratorError(ApplicationException):
    pass