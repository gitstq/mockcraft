"""
MockCraft Network Provider - IP, URL, user-agent.
"""
import random
import uuid


class NetworkProvider:
    """Generates network-related data."""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    ]

    PROTOCOLS = ["http", "https"]
    DOMAINS = [
        "example.com","test.com","api.example.com","www.example.org","app.test.io",
        "api.baidu.com","service.qq.com","cdn.tencent.com","oss.aliyuncs.com","cdn.doge.com",
        "demo.site.com","dev.example.org","staging.test.io","prod.api.com","uat.service.com"
    ]

    Tlds = ["com","org","net","io","cn","co","me","info","biz","edu"]

    def generate(self, type: str = "ipv4", **kwargs) -> str:
        """Generate network data."""
        if type == "ipv4":
            return self._generate_ipv4()
        elif type == "ipv6":
            return self._generate_ipv6()
        elif type == "url":
            return self._generate_url()
        elif type == "user_agent":
            return self._generate_user_agent()
        elif type == "domain":
            return self._generate_domain()
        elif type == "mac":
            return self._generate_mac()
        else:
            return self._generate_ipv4()

    def _generate_ipv4(self) -> str:
        # Weighted: mostly private ranges
        if random.random() < 0.6:
            # Private: 192.168.x.x
            return f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        elif random.random() < 0.5:
            # Private: 10.x.x.x
            return f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        else:
            return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

    def _generate_ipv6(self) -> str:
        groups = [f"{random.randint(0,65535):x}" for _ in range(8)]
        return ":".join(groups)

    def _generate_url(self) -> str:
        protocol = random.choice(self.PROTOCOLS)
        domain = random.choice(self.DOMAINS)
        paths = ["", "/api", f"/v1/{random.choice(['users','data','info','query'])}", "/index.html", f"/data/{random.randint(1000,9999)}"]
        return f"{protocol}://{domain}{random.choice(paths)}"

    def _generate_user_agent(self) -> str:
        return random.choice(self.USER_AGENTS)

    def _generate_domain(self) -> str:
        return random.choice(self.DOMAINS)

    def _generate_mac(self) -> str:
        return ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])

    def ipv4(self, **kwargs) -> str:
        return self._generate_ipv4()

    def ipv6(self, **kwargs) -> str:
        return self._generate_ipv6()

    def url(self, **kwargs) -> str:
        return self._generate_url()

    def user_agent(self, **kwargs) -> str:
        return self._generate_user_agent()
