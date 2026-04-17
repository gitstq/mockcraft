"""
MockCraft Person Provider - generates names and person-related data.
"""
import random
from typing import Optional


class PersonProvider:
    """Generates person names, titles, and demographics."""

    # Chinese surname and given name pools
    ZH_SURNAMES = [
        "王","李","张","刘","陈","杨","赵","黄","周","吴","徐","孙","胡","朱","高",
        "林","何","郭","马","罗","梁","宋","郑","谢","韩","唐","冯","于","董","萧",
        "程","曹","袁","邓","许","傅","沈","曾","彭","吕","苏","卢","蒋","蔡","贾",
        "丁","魏","薛","叶","阎","余","潘","杜","戴","夏","钟","汪","田","任","姜",
        "范","方","石","姚","谭","廖","邹","熊","金","陆","郝","孔","白","崔","康",
        "毛","邱","秦","江","史","顾","侯","邵","孟","龙","万","段","雷","钱","汤",
        "尹","黎","易","常","武","乔","贺","赖","龚","文","欧阳","司马","诸葛","上官","欧阳"
    ]

    ZH_MALE_NAMES = [
        "伟","强","磊","洋","勇","军","杰","涛","超","明","刚","平","辉","鹏","飞",
        "华","波","斌","宇","浩","凯","亮","俊","峰","健","龙","海","文","博","晨",
        "志","彬","旭","涛","晨","昊","睿","鑫","昊","煜","霖","然","然","博","翔",
        "子轩","浩然","宇轩","天宇","俊杰","子涵","思远","志远","子豪","子俊","天翔",
        "子墨","梓涵","一凡","亦凡","天赐","佳怡","子琪","雨桐","欣怡","思琪","子瑶",
        "思瑶","佳琪","诗琪","雨萱","诗涵","佳欣","思雨","雨涵","欣悦","思悦","佳悦"
    ]

    ZH_FEMALE_NAMES = [
        "芳","娟","敏","静","丽","艳","娜","秀","英","华","慧","巧","美","婷","玲",
        "桂","燕","霞","云","莲","珍","贞","莉","兰","凤","洁","梅","琳","素","雪",
        "萍","雅","欣","蕾","蕊","薇","瑶","琪","涵","婷","雅","诗","思","悦","佳",
        "雨","思雨","雨萱","思瑶","诗涵","欣怡","佳欣","思悦","佳悦","欣悦","怡然",
        "安然","悠然","子墨","子琪","子瑶","思琪","诗琪","佳琪","语桐","语萱","语涵"
    ]

    ZH_PREFIXES = ["", "小"]
    ZH_SUFFIXES = ["", "先生", "女士", "老师"]

    # English name components
    EN_FIRST_NAMES = [
        "James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Barbara",
        "David","Elizabeth","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen",
        "Christopher","Nancy","Daniel","Lisa","Matthew","Betty","Anthony","Margaret","Mark","Sandra",
        "Donald","Ashley","Steven","Kimberly","Paul","Emily","Andrew","Donna","Kenneth","Michelle",
        "Joshua","Dorothy","Kevin","Carol","Brian","Amanda","George","Melissa","Edward","Deborah",
        "Ronald","Stephanie","Timothy","Rebecca","Jason","Sharon","Jeffrey","Laura","Ryan","Cynthia"
    ]

    EN_LAST_NAMES = [
        "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
        "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
        "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
        "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores"
    ]

    def __init__(self, locale: str = "zh_CN"):
        self.locale = locale

    def generate(self, gender: Optional[str] = None, **kwargs) -> str:
        """
        Generate a person name.

        Args:
            gender: 'male', 'female', or None (random)
        """
        if self.locale.startswith("zh"):
            return self._generate_zh(gender)
        else:
            return self._generate_en(gender)

    def _generate_zh(self, gender: Optional[str] = None) -> str:
        surname = random.choice(self.ZH_SURNAMES)
        if gender == "male":
            given = random.choice(self.ZH_MALE_NAMES)
        elif gender == "female":
            given = random.choice(self.ZH_FEMALE_NAMES)
        else:
            given = random.choice(self.ZH_MALE_NAMES + self.ZH_FEMALE_NAMES)
        return surname + given

    def _generate_en(self, gender: Optional[str] = None) -> str:
        first = random.choice(self.EN_FIRST_NAMES)
        last = random.choice(self.EN_LAST_NAMES)
        return f"{first} {last}"

    def fullname(self, gender: Optional[str] = None) -> str:
        """Alias for generate()."""
        return self.generate(gender=gender)
