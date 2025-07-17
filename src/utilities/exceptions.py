class ApplicationException(Exception):
    pass

class ValidationError(ApplicationException):
    pass



class RepositoryError(ApplicationException):
    pass

class ReservationAlreadyExistsError(RepositoryError):
    """Raised when trying to add a reservation with a duplicate ID."""
    pass

class ReservationNotFoundError(RepositoryError):
    """Raised when trying to delete or update a reservation that doesn't exist."""
    pass

class DatabaseUnavailableError(RepositoryError):
    """Raised when the database connection fails or SQL is broken."""
    pass



class ServiceError(ApplicationException):
    pass

class ActionError(ApplicationException):
    pass

class InputError(ApplicationException):
    pass

class ConfiguratorError(ApplicationException):
    pass