class ValidationError(Exception):
    """
    Exception class for validation errors. This class is used to return
    error messages to fastAPI Response. It has a status_code attribute
    https://http.cat/ and an error_msg attribute.
    """
    def __init__(self, error_msg: str, status_code: int):
        """
        assign error_msg and status_code to attributes.
        :param error_msg: string of error message.
        :param status_code: integer of status code.
        """
        super().__init__(error_msg)
        self.status_code = status_code
        self.error_msg = error_msg
