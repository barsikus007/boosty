from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4, HttpUrl

from boosty.types.base import BaseObject
from boosty.types.comment import CommentsResponse
from boosty.types.content import Content
from boosty.types.counters import Counter
from boosty.types.donator import DonatorsResponse
from boosty.types.poll import Poll
from boosty.types.reactions import Reactions
from boosty.types.teaser import TeaserContent
from boosty.types.users import BlogUser
from boosty.utils.post import Entity, render_text

if TYPE_CHECKING:
    from boosty.api.api import API


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
    changePrice: int | None = None
    data: list[TeaserContent]
    """Could be Content type"""
    deleted: bool
    isArchived: bool
    name: str
    ownerId: int
    """post.user.id"""

    currencyPrices: Currency

    promos: dict | list  # TODO


class React(BaseObject):
    actor: str


class Count(BaseObject):
    likes: int
    comments: int
    reactions: Reactions
    views: int | None = None


class Post(BaseObject):
    id: UUID4
    createdAt: datetime
    """Creation timestamp"""
    updatedAt: datetime
    """Last update timestamp"""
    publishTime: datetime
    """Publication timestamp"""
    isPublished: bool
    """Is post published to users"""
    user: BlogUser
    """Blogger user object"""

    title: str
    """Post title"""
    data: list[Content]
    """List of contents, attached to post (text included)"""
    contentCounters: list[Counter]
    """List of counters and sizes, attached to post (text included)"""
    tags: list[Tag]

    hasAccess: bool
    """Is post available for you"""
    teaser: list[TeaserContent]
    """Post teaser for users which haven't access to post"""

    count: Count
    """Count of likes, comments, reactions"""
    comments: CommentsResponse
    isCommentsDenied: bool
    isLiked: bool
    price: int
    """Price to open post"""
    signedQuery: str
    """Query for media fetching"""
    subscriptionLevel: SubscriptionLevel | None = None
    """Subscription level for non-free posts"""

    poll: Poll | None = None
    advertiserInfo: str | None = None
    reacted: React | None = None
    """Unknown"""
    isWaitingVideo: bool
    """Unknown, probably an indicator, which shows if video is incomplete"""
    currencyPrices: Currency
    """Unknown"""
    isRecord: bool
    """Is post a stream record"""
    donators: DonatorsResponse
    """List of sponsors of the post"""
    donations: float | dict  # TODO dict is appearing sometimes
    """Amount of donations"""
    int_id: int
    """Unknown, probably post.id to int"""

    isBlocked: bool
    """New option is Post Blocked by platform or some reason"""
    isDeleted: bool
    """TODO"""
    showViewsCounter: bool | None = None
    """TODO"""

    @property
    def url(self) -> HttpUrl:
        return HttpUrl(f"https://boosty.to/{self.user.blogUrl}/posts/{self.id}")

    @property
    def text(self) -> tuple[str, list[Entity]]:
        return render_text(self.data)

    async def get_comments(
        self,
        boosty_api: "API",
        offset: str | None = None,
        limit: int | None = None,
        reply_limit: int | None = None,
        order: str | None = None,
    ) -> CommentsResponse:
        return await boosty_api.get_post_comments(
            self.user.blogUrl, self.id, offset=offset, limit=limit, reply_limit=reply_limit, order=order
        )


class PostsResponseExtra(BaseObject):
    isLast: bool
    """Is last page"""
    offset: str
    """Value for pagination. Example: :code:`1654884900:923396`"""


class PostsResponse(BaseObject):
    data: list[Post]
    extra: PostsResponseExtra


class EditedPost(BaseObject):
    title: str = ""
    """Post title"""
    data: list[Content]
    """List of contents, attached to post (text included)"""
    price: int = 300
    """Price to open post"""
    teaser_data: list[TeaserContent]  # TODO [] as mutable default if needed
    """Post teaser for users which haven't access to post"""
    tags: str = ""
    deny_comments: bool = False
    wait_video: bool = False
    """TODO"""
    publish_time: int | None = None
    """Timestamp to publish post. If None - post will be published immediately"""
    advertiser_info: str


class NewPost(EditedPost):
    has_chat: bool = False
    """TODO"""
