from abc import ABC, abstractmethod

class PortalScraper(ABC):
    """
    所有平台爬虫的基类，定义统一接口。
    """
    @abstractmethod
    def fetch_assignments(self):
        """
        抓取当前平台的作业信息。
        Returns:
            List[Dict]: 包含 title, description, due_date, source 等字段的作业信息列表。
        """
        pass