class UniqueConstraint(Exception):
    def __init__(self, field: str) -> None:
        super().__init__()
        self.field = field
