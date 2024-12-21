class TransactionDoesNotExist(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class IncorrectParameterAmount(Exception):
    pass


class ActionNotFound(Exception):
    pass


class SignCheckFailed(Exception):
    pass


class AlreadyPaid(Exception):
    pass


class TransactionCanceled(Exception):
    pass
