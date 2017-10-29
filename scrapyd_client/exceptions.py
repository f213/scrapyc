class ScrapydClientException(BaseException):
    """Generic client exception"""
    pass


class ScrapydClientResponseNotOKException(ScrapydClientException):
    """Non-ok JSON response from the server"""
    pass


class ScrapyClientProjectDoesNotExist(ScrapydClientException):
    pass


class ScrapydClientHTTPException(ScrapydClientException):
    """Basic HTTP exception"""
    pass


class ScrapydUnAuthorizedException(ScrapydClientHTTPException):
    """Bad auth credentials exception"""
    pass
