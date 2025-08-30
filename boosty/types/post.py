from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4, HttpUrl

from boosty.types.base import BaseObject
from boosty.types.comment import CommentsResponse
from boosty.types.common import PostCommon
from boosty.types.content import Content
from boosty.types.counters import Counter
from boosty.types.donator import DonatorsResponse
from boosty.types.poll import Poll
from boosty.types.reaction_counters import ReactionCounters
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
    isHidden: bool
    isLimited: bool


class React(BaseObject):
    actor: str


class Count(BaseObject):
    likes: int
    comments: int
    reactions: Reactions
    views: int | None = None


class Post(PostCommon):
    int_id: int
    """Unknown, probably post.id to int"""

    user: BlogUser
    """Blogger user object"""
    title: str
    """Post title"""
    data: list[Content]
    """List of contents, attached to post (text included)"""
    isPublished: bool
    """Is post published to users"""
    publishTime: datetime
    """Publication timestamp"""
    contentCounters: list[Counter]
    """List of counters and sizes, attached to post (text included)"""
    tags: list[Tag]

    hasAccess: bool
    """Is post available for you"""
    teaser: list[TeaserContent]
    """Post teaser for users which haven't access to post"""
    subscriptionLevel: SubscriptionLevel | None = None
    """Subscription level for non-free posts"""
    price: int
    """Price to open post"""
    donators: DonatorsResponse
    """List of sponsors of the post"""
    donations: float | dict  # TODO dict is appearing sometimes
    """Amount of donations"""
    currencyPrices: Currency
    """Unknown"""

    isCommentsDenied: bool
    comments: CommentsResponse

    isLiked: bool
    count: Count
    """Count of likes, comments, reactions"""
    reactionsDisabled: bool
    """Is reactions disabled for post"""
    reacted: React | None = None

    signedQuery: str
    """Query for media fetching"""
    poll: Poll | None = None
    advertiserInfo: str | None = None
    """Unknown"""
    isWaitingVideo: bool
    """Unknown, probably an indicator, which shows if video is processing"""
    isRecord: bool
    """Is post a stream record"""
    showViewsCounter: bool | None = None
    """TODO"""
    isPinned: bool
    """TODO"""
    sortOrder: int
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
