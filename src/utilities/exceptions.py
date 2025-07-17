class ApplicationException(Exception):
    pass

class ValidationError(ApplicationException):
    pass

class RepositoryError(ApplicationException):
    pass

class ServiceError(ApplicationException):
    pass

class ActionError(ApplicationException):
    pass

class InputError(ApplicationException):
    pass

class ConfiguratorError(ApplicationException):
    pass