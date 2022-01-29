class Route:
    def __init__(self, client,url: str):
        self.client = client
        self.base_url = "https://discord.com/api/v9/"
        self.url = f"{self.base_url}{url}"
    
    async def request(self, method: str, *args, **kwargs):
        return await self.client.http.request(method, self.url, *args, **kwargs)