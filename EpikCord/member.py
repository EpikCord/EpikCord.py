class ThreadMember:
    def __init__(self, data: dict):
        self.thread_id: str = data["thread_id"]
        self.user_id: str = data["user_id"]
        self.join_timestamp: str = data["join_timestamp"]
        self.flags: int = data["flags"]