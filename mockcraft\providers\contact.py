"""
MockCraft Contact Provider - emails, phones, addresses.
"""
import random
import re


class ContactProvider:
    """Generates contact information: email, phone, address."""

    # Email domains
    EMAIL_DOMAINS_COMMON = [
        "gmail.com","qq.com","163.com","126.com","outlook.com","hotmail.com",
        "yahoo.com","sina.com","sohu.com","139.com","icloud.com","foxmail.com",
        "proton.me","live.com","mail.com","yeah.net","tom.com","263.net"
    ]

    # Chinese mobile prefixes (mainland)
    CN_PHONE_PREFIXES = [
        "130","131","132","133","134","135","136","137","138","139",
        "147","150","151","152","153","155","156","157","158","159",
        "166","170","171","172","173","175","176","177","178","179",
        "180","181","182","183","184","185","186","187","188","189",
        "190","191","193","195","196","197","198","199"
    ]

    # Chinese address components
    CN_PROVINCES = [
        "北京市","上海市","天津市","重庆市",
        "河北省","山西省","辽宁省","吉林省","黑龙江省",
        "江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省",
        "湖北省","湖南省","广东省","海南省","四川省","贵州省","云南省","陕西省",
        "甘肃省","青海省","台湾省",
        "内蒙古自治区","广西壮族自治区","西藏自治区","宁夏回族自治区","新疆维吾尔自治区"
    ]

    CN_CITIES = [
        "北京","上海","深圳","广州","杭州","南京","武汉","成都","重庆","西安",
        "苏州","天津","长沙","郑州","东莞","青岛","沈阳","宁波","昆明","大连",
        "厦门","福州","济南","温州","长春","哈尔滨","石家庄","佛山","泉州","南昌",
        "合肥","贵阳","太原","兰州","呼和浩特","乌鲁木齐","银川","海口","三亚","珠海"
    ]

    CN_STREETS = [
        "人民路","中山路","建设路","解放路","和平路","文化路","新华路","长江路","黄河路",
        "北京路","上海路","南京路","西湖路","东华路","西华路","南华路","北华路",
        "科技路","创新路","学院路","大学路","公园路","广场路","商业街","工业路",
        "机场路","车站路","市场路","金融街","软件园","工业园"
    ]

    CN_DISTRICTS = [
        "朝阳区","海淀区","东城区","西城区","浦东新区","徐汇区","黄浦区","静安区",
        "天河区","越秀区","白云区","南山区","福田区","罗湖区","龙岗区","宝安区",
        "江岸区","武昌区","江汉区","锦江区","青羊区","雁塔区","碑林区","渝中区"
    ]

    def __init__(self, locale: str = "zh_CN", default_type: str = "email"):
        self.locale = locale
        self._default_type = default_type

    def generate(self, type: str = None, name: str = None, domain: str = None, **kwargs) -> str:
        """
        Generate contact data.

        Args:
            type: 'email', 'phone', or 'address'
            name: optional name to derive email from
            domain: optional custom email domain
        """
        if type is None:
            type = getattr(self, "_default_type", "email")
        if type == "email":
            return self._generate_email(name, domain)
        elif type == "phone":
            return self._generate_phone()
        elif type == "address":
            return self._generate_address()
        elif type == "mobile":
            return self._generate_phone()
        else:
            return self._generate_email(name, domain)

    def _generate_email(self, name: str = None, domain: str = None) -> str:
        if name is None:
            from .person import PersonProvider
            person = PersonProvider(self.locale)
            name = person.generate().replace(" ", "")
        else:
            name = str(name).lower().replace(" ", "").replace("\n", "")

        domain = domain or random.choice(self.EMAIL_DOMAINS_COMMON)

        # Various email patterns
        patterns = [
            lambda n: n,
            lambda n: f"{n}{random.randint(1,999)}",
            lambda n: f"{n}_{random.randint(1,99)}",
            lambda n: f"{n}.{random.choice(['a','b','c','x','y'])}",
            lambda n: f"dev_{n}",
            lambda n: f"{n}{random.choice(['_','.'])}{random.choice(['1988','1990','2020','01'])}",
        ]
        local = random.choice(patterns)(name)
        return f"{local}@{domain}"

    def _generate_phone(self) -> str:
        prefix = random.choice(self.CN_PHONE_PREFIXES)
        suffix = f"{random.randint(100,999)}{random.randint(1000,9999)}"
        return f"+86{prefix}{suffix}"

    def _generate_address(self) -> str:
        province = random.choice(self.CN_PROVINCES)
        city = random.choice(self.CN_CITIES)
        district = random.choice(self.CN_DISTRICTS)
        street = random.choice(self.CN_STREETS)
        number = random.randint(1, 999)
        return f"{province}{city}{district}{street}{number}号"

    def email(self, **kwargs) -> str:
        return self.generate(type="email", **kwargs)

    def phone(self, **kwargs) -> str:
        return self.generate(type="phone", **kwargs)

    def address(self, **kwargs) -> str:
        return self.generate(type="address", **kwargs)
