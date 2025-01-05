class BioValidatorInternalError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self._detail = detail

    @property
    def detail(self) -> str:
        return self._detail

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> Detail: {self._detail}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> detail: {self._detail}"


class BioValidatorExternalError(BioValidatorInternalError):
    def __init__(self, detail: str, status_code: int) -> None:
        super().__init__(detail)

        self._status_code = status_code

    @property
    def status_code(self) -> int:
        return self._status_code

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> detail: {self._detail}, status_code: {self._status_code}"
