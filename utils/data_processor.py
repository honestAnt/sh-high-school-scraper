"""
数据处理工具
提供数据分析和处理功能
"""
import pandas as pd
import numpy as np
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.data_model import AdmissionScore, AdmissionRate, DataStorage
import config

class DataProcessor:
    """数据处理类"""
    
    @staticmethod
    def get_school_scores(school_name, years=None):
        """
        获取指定学校的录取分数数据
        
        Args:
            school_name (str): 学校名称
            years (list, optional): 年份列表，如果不提供则获取所有年份
            
        Returns:
            list: AdmissionScore对象列表
        """
        scores = DataStorage.load_admission_scores()
        
        if not scores:
            return []
        
        # 过滤指定学校
        school_scores = [score for score in scores if score.school_name == school_name]
        
        # 如果指定了年份，进一步过滤
        if years:
            school_scores = [score for score in school_scores if score.year in years]
        
        return school_scores
    
    @staticmethod
    def get_school_rates(school_name, years=None):
        """
        获取指定学校的升学率数据
        
        Args:
            school_name (str): 学校名称
            years (list, optional): 年份列表，如果不提供则获取所有年份
            
        Returns:
            list: AdmissionRate对象列表
        """
        rates = DataStorage.load_admission_rates()
        
        if not rates:
            return []
        
        # 过滤指定学校
        school_rates = [rate for rate in rates if rate.school_name == school_name]
        
        # 如果指定了年份，进一步过滤
        if years:
            school_rates = [rate for rate in school_rates if rate.year in years]
        
        return school_rates
    
    @staticmethod
    def get_category_scores(category, year):
        """
        获取指定分类学校在特定年份的录取分数
        
        Args:
            category (str): 学校分类
            year (int): 年份
            
        Returns:
            dict: {学校名: AdmissionScore对象}
        """
        scores = DataStorage.load_admission_scores()
        
        if not scores:
            return {}
        
        # 获取该分类的学校列表
        schools = config.SCHOOL_CATEGORIES.get(category, [])
        
        # 过滤指定分类和年份的分数
        category_scores = {}
        for score in scores:
            if score.school_name in schools and score.year == year:
                category_scores[score.school_name] = score
        
        return category_scores
    
    @staticmethod
    def get_category_rates(category, year):
        """
        获取指定分类学校在特定年份的升学率
        
        Args:
            category (str): 学校分类
            year (int): 年份
            
        Returns:
            dict: {学校名: AdmissionRate对象}
        """
        rates = DataStorage.load_admission_rates()
        
        if not rates:
            return {}
        
        # 获取该分类的学校列表
        schools = config.SCHOOL_CATEGORIES.get(category, [])
        
        # 过滤指定分类和年份的升学率
        category_rates = {}
        for rate in rates:
            if rate.school_name in schools and rate.year == year:
                category_rates[rate.school_name] = rate
        
        return category_rates
    
    @staticmethod
    def calculate_score_statistics(scores):
        """
        计算分数统计信息
        
        Args:
            scores (list): AdmissionScore对象列表
            
        Returns:
            dict: 统计信息
        """
        if not scores:
            return {
                "min": 0,
                "max": 0,
                "avg": 0,
                "median": 0,
                "std": 0
            }
        
        avg_scores = [score.avg_score for score in scores]
        
        return {
            "min": min(avg_scores),
            "max": max(avg_scores),
            "avg": sum(avg_scores) / len(avg_scores),
            "median": np.median(avg_scores),
            "std": np.std(avg_scores)
        }
    
    @staticmethod
    def calculate_rate_statistics(rates):
        """
        计算升学率统计信息
        
        Args:
            rates (list): AdmissionRate对象列表
            
        Returns:
            dict: 统计信息
        """
        if not rates:
            return {
                "c9": {"min": 0, "max": 0, "avg": 0},
                "985": {"min": 0, "max": 0, "avg": 0},
                "211": {"min": 0, "max": 0, "avg": 0}
            }
        
        c9_rates = [rate.c9_rate for rate in rates]
        rates_985 = [rate.rate_985 for rate in rates]
        rates_211 = [rate.rate_211 for rate in rates]
        
        return {
            "c9": {
                "min": min(c9_rates),
                "max": max(c9_rates),
                "avg": sum(c9_rates) / len(c9_rates)
            },
            "985": {
                "min": min(rates_985),
                "max": max(rates_985),
                "avg": sum(rates_985) / len(rates_985)
            },
            "211": {
                "min": min(rates_211),
                "max": max(rates_211),
                "avg": sum(rates_211) / len(rates_211)
            }
        }