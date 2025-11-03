"""
升学率爬虫
负责获取高中升学率数据
"""
import re
import sys
import os
from tqdm import tqdm

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper
from models.data_model import AdmissionRate
import config

class RateScraper(BaseScraper):
    """升学率爬虫类"""
    
    def __init__(self, api_key=None):
        """初始化升学率爬虫"""
        super().__init__(api_key)
    
    def get_admission_rate(self, school_name, year):
        """
        获取指定学校和年份的升学率
        
        Args:
            school_name (str): 学校名称
            year (int): 年份
            
        Returns:
            AdmissionRate: 升学率对象
        """
        # 构建查询提示词
        prompt = config.QUERY_MODES["升学率"].format(year=year, school=school_name)
        
        # 发送查询
        response = self.query(prompt)
        text = self.extract_text_from_response(response)
        
        # 解析结果
        return self._parse_rate_text(text, school_name, year)
    
    def _parse_rate_text(self, text, school_name, year):
        """
        解析文本中的升学率信息
        
        Args:
            text (str): 响应文本
            school_name (str): 学校名称
            year (int): 年份
            
        Returns:
            AdmissionRate: 升学率对象
        """
        # 提取升学率信息
        c9_rate = self._extract_percentage(text, r'C9[入线率]{2,4}[：:]\s*(\d+\.?\d*)[%％]')
        rate_985 = self._extract_percentage(text, r'985[入线率]{2,4}[：:]\s*(\d+\.?\d*)[%％]')
        rate_211 = self._extract_percentage(text, r'211[入线率]{2,4}[：:]\s*(\d+\.?\d*)[%％]')
        
        return AdmissionRate(school_name, year, c9_rate, rate_985, rate_211)
    
    def _extract_percentage(self, text, pattern, default=0):
        """
        从文本中提取百分比
        
        Args:
            text (str): 文本
            pattern (str): 正则表达式模式
            default (float): 默认值
            
        Returns:
            float: 提取的百分比值
        """
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return default
        return default
    
    def batch_collect_rates(self, school_names, years):
        """
        批量收集多个学校多年的升学率
        
        Args:
            school_names (list): 学校名称列表
            years (list): 年份列表
            
        Returns:
            list: AdmissionRate对象列表
        """
        results = []
        total = len(school_names) * len(years)
        
        with tqdm(total=total, desc="收集升学率") as pbar:
            for school in school_names:
                for year in years:
                    rate = self.get_admission_rate(school, year)
                    results.append(rate)
                    pbar.update(1)
        
        return results