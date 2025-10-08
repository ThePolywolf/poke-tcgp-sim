from tools.validation import validate_type

class SetHook:
    __str_buf_name = 26
    __str_buf_code = 5
    __str_buf_cards = 5

    def __init__(self, name: str, code: str, url: str, cards: int):
        validate_type(name, str)
        validate_type(code, str)
        validate_type(url, str)
        validate_type(cards, int)

        self.name: str = name
        self.code: str = code
        self.url: str = url
        self.cards: int = cards

    @staticmethod
    def display_header() -> str:
        return f"{"code":<{SetHook.__str_buf_code}} {"name":<{SetHook.__str_buf_name}} | {"cards":>{SetHook.__str_buf_cards}} | url"

    def __str__(self):
        return f"{f"({self.code})":<{SetHook.__str_buf_code}} {self.name:<{SetHook.__str_buf_name}} | {f"{self.cards}":>{SetHook.__str_buf_cards}} | {self.url}"