from http import HTTPStatus

AUTH_ERROR = 'authorization error'
INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
REQUEST_TIMEOUT = 'request timeout'
NOT_EXPLORED = 'not explored'


class TRFormattedError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}


class AuthorizationError(TRFormattedError):
    def __init__(self, reason=None):
        message = 'Authorization failed'
        if reason:
            message += f': {reason}'
        else:
            message += ' on IsItPhishing side'

        super().__init__(
            AUTH_ERROR,
            message
        )


class InvalidArgumentError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            f'Invalid JSON payload received. {message}'
        )


class IsItPhishingSSLError(TRFormattedError):
    def __init__(self, error):
        error = error.args[0].reason.args[0]
        message = getattr(error, 'verify_message', error.args[0]).capitalize()
        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )


class UnexpectedIsItPhishingError(TRFormattedError):
    def __init__(self, status_code):
        super().__init__(
            HTTPStatus(status_code).phrase.lower(),
            'Unexpected response from IsItPhishing: '
            f'{HTTPStatus(status_code).phrase}'
        )


class IsItPhishingTimeout(TRFormattedError):
    def __init__(self, url):
        super().__init__(
            REQUEST_TIMEOUT,
            f'Timeout was reached while processing URL: "{url}".',
            'warning'
        )


class IsItPhishingNotExplored(TRFormattedError):
    def __init__(self, url):
        super().__init__(
            NOT_EXPLORED,
            f'IsItPhishing API is set not to process such URLs as "{url}". '
            f'This URL may cause collateral damage to the end user.',
            'warning'
        )


class IsItPhishingWatchdogError(TRFormattedError):
    def __init__(self):
        super().__init__(
            code='health check failed',
            message='Invalid Health Check'
        )
