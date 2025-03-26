from boosty.types.base import BaseObject


class Counter(BaseObject):
    type: str
    """Type of content in post. """
    count: int
    """Count of content type in post. Teaser field included as image. """
    size: int
    """Size of content each type in post. Teaser size included as image. """
