class ApplicationException(Exception):
    pass

class ValidationError(ApplicationException):
    pass



class RepositoryError(ApplicationException):
    pass

class ReservationAlreadyExistsError(RepositoryError):
    pass

class ReservationNotFoundError(RepositoryError):
    pass

class DatabaseUnavailableError(RepositoryError):
    pass



class ServiceError(ApplicationException):
    pass

class ActionError(ApplicationException):
    pass

class InputError(ApplicationException):
    pass

class ConfiguratorError(ApplicationException):
    pass