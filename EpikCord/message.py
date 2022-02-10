from .embed import Embed
class PartialEmoji:
    def __init__(self, data:dict):
        self.data: dict = data
        self.name: str = data.get("name")
        self.id: str = data.get("id")
        self.animated: bool = data.get("animated")
    
class Reaction:
    def __init__(self, data: dict):
        self.count: int = data.get("count")
        self.me: bool = data.get("me")
        self.emoji: PartialEmoji = PartialEmoji(data.get["emoji"])

class Message:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data.get("id")
        self.channel_id: str = data.get("channel_id")
        self.guild_id: Optional[str] = data.get("guild_id") or None
        self.webhook_id: Optional[str] = data.get("webhook_id") or None
        self.author: Optional[User] if not self.webhook_id else WebhookUser = WebhookUser(data.get("author")) if self.webhook_id else User(data["author"])
        self.member: Optional[GuildMember] = GuildMember(data.get("member")) if data.get("member") else None
        self.content: Optional[str] = data.get("content") or None # I forgot Message Intents are gonna stop this.
        self.timestamp: str = data.get("timestamp")
        self.edited_timestamp: Optional[str] = data.get("edited_timestamp") or None
        self.tts: bool = data.get("tts")
        self.mention_everyone: bool = data.get("mention_everyone")
        self.mentions: Optional[List[MentionedUser]] = [MentionedUser(mention) for mention in data.get("mentions")] or None
        self.mention_roles: Optional[List[int]] = data.get("mention_roles") or None
        self.mention_channels: Optional[List[MentionedChannel]] = [MentionedChannel(channel) for channel in data.get("mention_channels")] or None
        self.embeds: Optional[List[Embed]] = [Embed(embed) for embed in data.get("embeds")] or None
        self.reactions: Optional[List[Reaction]] = [Reaction(reaction) for reaction in data.get("reactions")] or None
        self.nonce: Optional[Union[int, str]] = data.get("nonce") or None
        self.pinned: bool = data.get("pinned")
        self.type: int = data.get("type")
        self.activity: MessageActivity = MessageActivity(data.get("activity"))
        self.application: Application = Application(data.get("application")) # Despite there being a PartialApplication, Discord don't specify what attributes it has
        self.flags: int = data.get("flags")
        self.referenced_message: Optional[Message] = Message(data.get("referenced_message")) if data.get("referenced_message") else None
        self.interaction: Optional[MessageInteraction] = MessageInteraction(client, data.get("interaction")) if data.get("interaction") else None
        self.thread: Thread = Thread(data.get("thread")) if data.get("thread") else None
        self.components: Optional[List[Union[MessageSelectMenu, MessageButton]]] = [MessageSelectMenu(component) if component.get("type") == 1 else MessageButton(component) for component in data.get("components")] or None
        self.stickers: Optional[List[StickerItem]] = [StickerItem(sticker) for sticker in data.get("stickers")] or None
        
    async def add_reaction(self, emoji: str):
        emoji = quote(emoji)
        logger.debug(f"Added a reaction to message ({self.id}).")
        response = await self.client.http.put(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        return await response.json()
    
    async def remove_reaction(self, emoji: str, user = None):
        emoji = quote(emoji)
        logger.debug(f"Removed reaction {emoji} from message ({self.id}) for user {user.username}.")
        if not user:
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        else:
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/{user.id}")
        return await response.json()
    
    async def fetch_reactions(self,*, after, limit) -> List[Reaction]:
        logger.debug(f"Fetching reactions from message ({self.id}).")
        response = await self.client.http.get(f"channels/{self.channel_id}/messages/{self.id}/reactions?after={after}&limit={limit}")
        return await response.json()
    
    async def delete_all_reactions(self):
        logger.debug(f"Deleting all reactions from message ({self.id}).")
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions")
        return await response.json()
    
    async def delete_reaction_for_emoji(self, emoji: str):
        logger.debug(f"Deleting a reaction from message ({self.id}) for emoji {emoji}.")
        emoji = quote(emoji)
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}")
        return await response.json()
    
    async def edit(self, message_data: dict):
        logger.debug(f"Editing message {self.id} with message_data {message_data}.")
        response = await self.client.http.patch(f"channels/{self.channel_id}/messages/{self.id}", data=message_data)
        return await response.json()
    
    async def delete(self):
        logger.debug(f"Deleting message {self.id}.")
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}")
        return await response.json()
    
    async def pin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
            logger.debug(f"Pinning message {self.id} with reason {reason}.")
        else:
            logger.debug(f"Pinning message {self.id}.")
        response = await self.client.http.put(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()
    
    async def unpin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
            logger.debug(f"Unpinning message {self.id} with reason {reason}.")
        else:
            logger.debug(f"Unpinning message {self.id}.")
        response = await self.client.http.delete(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()

    async def start_thread(self, name: str, auto_archive_duration: Optional[int], rate_limit_per_user: Optional[int]):
        logger.debug(f"Starting thread for message {self.id} with name {name}, auto archive duration {auto_archive_duration or None}, ratelimit per user {rate_limit_per_user or None}.")
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/threads", data={"name": name, "auto_archive_duration": auto_archive_duration, "rate_limit_per_user": rate_limit_per_user})
        self.client.guilds[self.guild_id].append(Thread(await response.json())) # Cache it
        return Thread(await response.json())
    
    async def crosspost(self):
        logger.debug(f"Crossposting message {self.id}.")
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/crosspost")
        return await response.json()