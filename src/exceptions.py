class ApplicationException(Exception):
    pass

class RepositoryError(ApplicationException):
    pass

class ValidationError(ApplicationException):
    pass

class InputError(ApplicationException):
    pass

class ConfiguratorError(ApplicationException):
    pass