class ScrapydClientHTTPException(BaseException):
    pass


class ScrapydUnAuthorizedException(ScrapydClientHTTPException):
    pass
