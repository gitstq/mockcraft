"""
MockCraft Text Provider - sentences, paragraphs, words.
"""
import random


class TextProvider:
    """Generates text content: words, sentences, paragraphs."""

    ZH_WORDS = [
        "数据","系统","网络","用户","管理","分析","服务","信息","应用","技术",
        "开发","设计","测试","性能","安全","平台","功能","接口","模块","流程",
        "项目","产品","业务","市场","运营","策略","目标","资源","成本","质量",
        "团队","客户","合作","创新","效率","价值","体验","智能","自动","标准",
        "优化","集成","部署","监控","日志","配置","版本","发布","构建","调试",
        "算法","模型","训练","预测","识别","处理","存储","计算","传输","加密",
        "认证","授权","权限","角色","审计","备份","恢复","迁移","扩容","容错"
    ]

    ZH_SENTENCES = [
        "本系统采用分布式架构，支持高并发访问和横向扩展。",
        "通过数据清洗和特征工程，显著提升了模型预测准确率。",
        "优化了数据库查询策略，查询响应时间降低60%以上。",
        "引入微服务架构，实现了服务的独立部署和快速迭代。",
        "采用异步消息队列，有效解耦了系统各组件的依赖关系。",
        "实现了基于角色的访问控制，确保了数据访问的安全性。",
        "通过容器化部署，极大地简化了环境配置和运维工作。",
        "构建了完整的监控告警体系，问题发现和响应时间大幅缩短。",
        "采用缓存策略，有效减轻了数据库的访问压力。",
        "实现了自动化测试覆盖，代码质量和交付速度同步提升。",
        "通过负载均衡和熔断机制，系统可用性达到99.9%以上。",
        "引入日志聚合分析平台，实现了全链路追踪和问题定位。",
        "采用配置中心统一管理，实现了配置的动态更新和热加载。",
        "通过灰度发布策略，降低了新版本上线的业务风险。",
        "构建了完善的权限管理体系，保障了系统的安全合规。",
        "采用消息确认机制，确保了关键业务消息的可靠投递。",
        "通过接口限流和防重放设计，提升了系统的防护能力。",
        "实现了数据全量备份和增量备份相结合的备份策略。",
        "采用连接池复用技术，优化了数据库连接的资源消耗。",
        "通过统一异常处理和标准化响应，提升了接口的健壮性。"
    ]

    ZH_PARAGRAPHS = [
        "为了满足业务快速增长的需求，系统架构进行了全面的升级改造。新的架构采用前后端分离设计，前端通过RESTful API与后端服务进行通信，后端服务基于微服务架构构建，各服务之间通过消息总线进行异步通信，有效降低了系统耦合度，提升了整体的可扩展性和可维护性。",
        "在数据处理层面，我们引入了流式计算框架，实现了实时数据的采集、清洗和分析。通过构建数据仓库和数据湖，实现了历史数据的存储和分析挖掘。数据团队基于这些数据资产，开发了多套业务分析模型，为产品优化和运营决策提供了强有力的数据支撑。",
        "安全是系统的生命线。在安全建设方面，我们构建了纵深防御体系，从网络层、应用层、数据层多个维度进行安全防护。采用OAuth2.0和JWT实现统一身份认证和授权管理，通过入侵检测和安全审计系统实时监控安全威胁，定期进行渗透测试和安全评估，确保系统安全合规运行。"
    ]

    EN_WORDS = [
        "data","system","network","user","management","analysis","service","information",
        "application","technology","development","design","testing","performance","security",
        "platform","function","interface","module","process","project","product","business",
        "market","operation","strategy","goal","resource","cost","quality","team","client",
        "cooperation","innovation","efficiency","value","experience","intelligence","automation",
        "standard","optimization","integration","deployment","monitoring","log","configuration",
        "version","release","build","debug","algorithm","model","training","prediction",
        "recognition","processing","storage","computing","transmission","encryption"
    ]

    EN_SENTENCES = [
        "The system architecture has been upgraded to support horizontal scaling.",
        "Through data cleaning and feature engineering, model accuracy improved significantly.",
        "Optimized database query strategies reduced response time by over 60 percent.",
        "Microservices architecture enables independent deployment and rapid iteration.",
        "Asynchronous message queues effectively decouple system components.",
        "Role-based access control ensures data security and compliance.",
        "Containerized deployment greatly simplifies environment configuration.",
        "Complete monitoring and alerting system shortens incident response time.",
        "Caching strategy effectively reduces database access pressure.",
        "Automated testing coverage improves code quality and delivery speed."
    ]

    EN_PARAGRAPHS = [
        "To meet rapidly growing business needs, the system architecture underwent a comprehensive upgrade. The new architecture follows a frontend-backend separation design, where the frontend communicates with backend services through RESTful APIs. Built on microservices architecture, each service communicates asynchronously via message bus, effectively reducing coupling and improving scalability.",
        "At the data processing layer, we introduced a stream computing framework for real-time data collection, cleaning, and analysis. By building a data warehouse and data lake, we enable historical data storage and analytical mining. Data teams developed multiple business analysis models based on these assets, providing strong data support for product optimization."
    ]

    def __init__(self, locale: str = "zh_CN"):
        self.locale = locale

    def generate(self, count: int = None, min_length: int = None, max_length: int = None, **kwargs) -> str:
        """
        Generate text content.

        Args:
            count: Number of sentences/words (context-dependent)
            min_length: Minimum character count
            max_length: Maximum character count
        """
        if self.locale.startswith("zh"):
            return self._generate_zh(count, min_length, max_length)
        else:
            return self._generate_en(count, min_length, max_length)

    def _generate_zh(self, count: int = None, min_length: int = None, max_length: int = None) -> str:
        if min_length or max_length:
            return self._generate_by_length_zh(min_length or 10, max_length or 100)
        parts = []
        n = count if count else random.randint(2, 5)
        for _ in range(n):
            parts.append(random.choice(self.ZH_SENTENCES))
        return "".join(parts)

    def _generate_by_length_zh(self, min_len: int, max_len: int) -> str:
        result = ""
        while len(result) < max_len:
            result += random.choice(self.ZH_SENTENCES)
        return result[:max_len]

    def _generate_en(self, count: int = None, min_length: int = None, max_length: int = None) -> str:
        if min_length or max_length:
            return self._generate_by_length_en(min_length or 20, max_length or 200)
        parts = []
        n = count if count else random.randint(3, 7)
        for _ in range(n):
            parts.append(random.choice(self.EN_SENTENCES))
        return " ".join(parts)

    def _generate_by_length_en(self, min_len: int, max_len: int) -> str:
        result = ""
        while len(result) < max_len:
            result += random.choice(self.EN_SENTENCES) + " "
        return result[:max_len].strip()

    def word(self, **kwargs) -> str:
        if self.locale.startswith("zh"):
            return random.choice(self.ZH_WORDS)
        return random.choice(self.EN_WORDS)

    def sentence(self, **kwargs) -> str:
        return self.generate(count=1, **kwargs)

    def paragraph(self, **kwargs) -> str:
        return self.generate(count=3, **kwargs)
