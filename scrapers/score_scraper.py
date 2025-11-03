"""
录取分数爬虫
负责获取高中录取分数数据
"""
import re
import sys
import os
from tqdm import tqdm

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper
from models.data_model import AdmissionScore
import config

class ScoreScraper(BaseScraper):
    """录取分数爬虫类"""
    
    def __init__(self, api_key=None):
        """初始化录取分数爬虫"""
        super().__init__(api_key)
    
    def get_admission_score(self, school_name, year):
        """
        获取指定学校和年份的录取分数
        
        Args:
            school_name (str): 学校名称
            year (int): 年份
            
        Returns:
            AdmissionScore: 录取分数对象
        """
        # 构建查询提示词
        prompt = config.QUERY_MODES["录取分数"].format(year=year, school=school_name)
        
        # 发送查询
        response = self.query(prompt)
        text = self.extract_text_from_response(response)
        
        # 解析结果
        return self._parse_score_text(text, school_name, year)
    
    def _parse_score_text(self, text, school_name, year):
        """
        解析文本中的分数信息
        
        Args:
            text (str): 响应文本
            school_name (str): 学校名称
            year (int): 年份
            
        Returns:
            AdmissionScore: 录取分数对象
        """
        # 提取分数信息
        min_score = self._extract_number(text, r'最低分[：:]\s*(\d+)')
        max_score = self._extract_number(text, r'最高分[：:]\s*(\d+)')
        avg_score = self._extract_number(text, r'平均分[：:]\s*(\d+)')
        
        # 提取学生来源信息
        student_sources = {}
        source_pattern = r'([^：:,，、\n]+)[：:]\s*(\d+)[%％]'
        source_matches = re.findall(source_pattern, text)
        
        for source, percentage in source_matches:
            source = source.strip()
            if '区' in source or '县' in source:
                student_sources[source] = float(percentage)
        
        return AdmissionScore(school_name, year, min_score, max_score, avg_score, student_sources)
    
    def _extract_number(self, text, pattern, default=0):
        """
        从文本中提取数字
        
        Args:
            text (str): 文本
            pattern (str): 正则表达式模式
            default (float): 默认值
            
        Returns:
            float: 提取的数字
        """
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return default
        return default
    
    def batch_collect_scores(self, school_names, years):
        """
        批量收集多个学校多年的录取分数
        
        Args:
            school_names (list): 学校名称列表
            years (list): 年份列表
            
        Returns:
            list: AdmissionScore对象列表
        """
        results = []
        total = len(school_names) * len(years)
        
        with tqdm(total=total, desc="收集录取分数") as pbar:
            for school in school_names:
                for year in years:
                    score = self.get_admission_score(school, year)
                    results.append(score)
                    pbar.update(1)
        
        return results