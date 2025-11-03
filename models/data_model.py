"""
数据模型
定义数据结构和处理方法
"""
import os
import pandas as pd
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class AdmissionScore:
    """录取分数数据模型"""
    
    def __init__(self, school_name, year, min_score, max_score, avg_score, student_sources=None):
        """
        初始化录取分数对象
        
        Args:
            school_name (str): 学校名称
            year (int): 年份
            min_score (float): 最低分数
            max_score (float): 最高分数
            avg_score (float): 平均分数
            student_sources (dict): 学生来源分布 {区县名: 人数}
        """
        self.school_name = school_name
        self.year = year
        self.min_score = min_score
        self.max_score = max_score
        self.avg_score = avg_score
        self.student_sources = student_sources or {}
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "school_name": self.school_name,
            "year": self.year,
            "min_score": self.min_score,
            "max_score": self.max_score,
            "avg_score": self.avg_score,
            "student_sources": self.student_sources
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            data["school_name"],
            data["year"],
            data["min_score"],
            data["max_score"],
            data["avg_score"],
            data.get("student_sources", {})
        )

class AdmissionRate:
    """升学率数据模型"""
    
    def __init__(self, school_name, year, c9_rate, rate_985, rate_211):
        """
        初始化升学率对象
        
        Args:
            school_name (str): 学校名称
            year (int): 年份
            c9_rate (float): C9入线率
            rate_985 (float): 985入线率
            rate_211 (float): 211入线率
        """
        self.school_name = school_name
        self.year = year
        self.c9_rate = c9_rate
        self.rate_985 = rate_985
        self.rate_211 = rate_211
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "school_name": self.school_name,
            "year": self.year,
            "c9_rate": self.c9_rate,
            "rate_985": self.rate_985,
            "rate_211": self.rate_211
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            data["school_name"],
            data["year"],
            data["c9_rate"],
            data["rate_985"],
            data["rate_211"]
        )

class DataStorage:
    """数据存储类，负责数据的保存和加载"""
    
    @staticmethod
    def save_admission_scores(scores):
        """
        保存录取分数数据
        
        Args:
            scores (list): AdmissionScore对象列表
        """
        os.makedirs(os.path.dirname(config.SCORE_DATA_FILE), exist_ok=True)
        
        data = [score.to_dict() for score in scores]
        df = pd.DataFrame(data)
        
        # 处理嵌套的student_sources字典
        if 'student_sources' in df.columns:
            # 将student_sources列转换为字符串
            df['student_sources'] = df['student_sources'].apply(str)
        
        df.to_csv(config.SCORE_DATA_FILE, index=False)
    
    @staticmethod
    def load_admission_scores():
        """
        加载录取分数数据
        
        Returns:
            list: AdmissionScore对象列表
        """
        if not os.path.exists(config.SCORE_DATA_FILE):
            return []
        
        df = pd.read_csv(config.SCORE_DATA_FILE)
        scores = []
        
        for _, row in df.iterrows():
            data = row.to_dict()
            
            # 处理student_sources字符串转回字典
            if 'student_sources' in data:
                try:
                    # 尝试将字符串转换回字典
                    import ast
                    data['student_sources'] = ast.literal_eval(data['student_sources'])
                except:
                    data['student_sources'] = {}
            
            scores.append(AdmissionScore.from_dict(data))
        
        return scores
    
    @staticmethod
    def save_admission_rates(rates):
        """
        保存升学率数据
        
        Args:
            rates (list): AdmissionRate对象列表
        """
        os.makedirs(os.path.dirname(config.RATE_DATA_FILE), exist_ok=True)
        
        data = [rate.to_dict() for rate in rates]
        df = pd.DataFrame(data)
        df.to_csv(config.RATE_DATA_FILE, index=False)
    
    @staticmethod
    def load_admission_rates():
        """
        加载升学率数据
        
        Returns:
            list: AdmissionRate对象列表
        """
        if not os.path.exists(config.RATE_DATA_FILE):
            return []
        
        df = pd.read_csv(config.RATE_DATA_FILE)
        rates = []
        
        for _, row in df.iterrows():
            rates.append(AdmissionRate.from_dict(row.to_dict()))
        
        return rates