class BitgetAPIError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"BitgetAPI Error {code}: {message}"
                         f"")


class InvalidProductTypeError(Exception):
    pass


class RequestError(Exception):
    pass
