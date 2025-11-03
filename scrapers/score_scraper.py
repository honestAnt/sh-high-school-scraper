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
        prompt = f"{year}年{school_name}录取分数及学生来源"
        
        # 发送查询
        response = self.query(prompt)
        
        # 直接从mock_query中获取数据
        if 'error' in response:
            # 如果API密钥未设置，直接使用mock_query
            response = self.mock_query(prompt)
            
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
        if min_score == 0:  # 如果没有找到，尝试带"分"字的格式
            min_score = self._extract_number(text, r'最低分[：:]\s*(\d+)分')
            
        max_score = self._extract_number(text, r'最高分[：:]\s*(\d+)')
        if max_score == 0:
            max_score = self._extract_number(text, r'最高分[：:]\s*(\d+)分')
            
        avg_score = self._extract_number(text, r'平均分[：:]\s*(\d+)')
        if avg_score == 0:
            avg_score = self._extract_number(text, r'平均分[：:]\s*(\d+)分')
        
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
                # 打印匹配结果用于调试
                print(f"匹配到: {match.group(0)}, 捕获组: {match.groups()}")
                return float(match.group(1))
            except (ValueError, IndexError):
                # 尝试使用第二个捕获组
                try:
                    if len(match.groups()) > 1:
                        return float(match.group(2))
                except (ValueError, IndexError):
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