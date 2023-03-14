from datetime import datetime

from pydantic import UUID4

from .base import BaseObject
from .comment import CommentsResponse
from .content import Content
from .donator import DonatorsResponse
from .reactions import Reactions
from .teaser import Teaser
from .users import BlogUser


class Currency(BaseObject):
    USD: int | float
    RUB: int | float


class Tag(BaseObject):
    id: int
    title: str
    """Tag name"""


class SubscriptionLevel(BaseObject):
    id: int
    createdAt: datetime
    """Creation timestamp"""
    price: int
    changePrice: int | None
    data: list[Teaser]
    """Could be Conent type"""
    deleted: bool
    isArchived: bool
    name: str
    ownerId: int
    """post.user.id"""

    currencyPrices: Currency


class React(BaseObject):
    actor: str


class Count(BaseObject):
    likes: int
    comments: int
    reactions: Reactions


class Post(BaseObject):
    id: UUID4
    createdAt: datetime
    """Creation timestamp"""
    updatedAt: datetime
    """Last update timestamp"""
    publishTime: datetime
    """Publication timestamp"""
    data: list[Content]
    """TODO List of content, attached to post (text included)"""
    count: Count
    """Count of likes, comments, reactions"""
    comments: CommentsResponse
    hasAccess: bool
    """Is post is available for users"""
    isCommentsDenied: bool
    isLiked: bool
    isPublished: bool
    price: int
    signedQuery: str
    """Query for media fetching"""
    subscriptionLevel: SubscriptionLevel | None
    tags: list[Tag]
    teaser: list[Teaser]
    title: str
    user: BlogUser

    reacted: React | None
    """Unknown"""
    isWaitingVideo: bool
    """Unknown"""
    currencyPrices: Currency
    """Unknown"""
    isRecord: bool
    """Unknown"""
    donators: DonatorsResponse
    """TODO Unknown"""
    donations: int
    """Amount of donations"""
    int_id: int
    """Unknown"""


class PostsResponseExtra(BaseObject):
    isLast: bool
    """Unknown"""
    offset: str
    """Unknown, example value is :code:`1654884900:923396`"""


class PostsResponse(BaseObject):
    data: list[Post]
    extra: PostsResponseExtra
