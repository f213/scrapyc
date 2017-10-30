class ScrapydClientException(BaseException):
    """Generic client exception"""
    pass


class ResponseNotOKException(ScrapydClientException):
    """Non-ok JSON response from the server"""
    pass


class ProjectDoesNotExist(ScrapydClientException):
    pass


class HTTPException(ScrapydClientException):
    """Basic HTTP exception"""
    pass


class UnAuthorizedException(HTTPException):
    """Bad auth credentials exception"""
    pass
