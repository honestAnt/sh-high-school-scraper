"""
学校分类模型
定义上海高中的分类和相关属性
"""
from enum import Enum
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class SchoolCategory(Enum):
    """学校分类枚举"""
    SHANGHAI_FOUR = "上海四校"
    EIGHT_GIANTS = "八大金刚"
    CITY_KEY = "市重点"
    MINHANG_KEY = "闵行区重点"
    PUDONG_KEY = "浦东新区重点"

class School:
    """学校类，表示一所高中及其属性"""
    
    def __init__(self, name, category):
        """
        初始化学校对象
        
        Args:
            name (str): 学校名称
            category (SchoolCategory): 学校分类
        """
        self.name = name
        self.category = category
        self.admission_scores = {}  # 按年份存储录取分数 {year: score}
        self.admission_rates = {}   # 按年份存储升学率 {year: {"C9": rate, "985": rate, "211": rate}}
    
    def __str__(self):
        return f"{self.name} ({self.category.value})"
    
    def add_admission_score(self, year, score):
        """添加某年的录取分数"""
        self.admission_scores[year] = score
    
    def add_admission_rate(self, year, c9_rate, rate_985, rate_211):
        """添加某年的升学率"""
        self.admission_rates[year] = {
            "C9": c9_rate,
            "985": rate_985,
            "211": rate_211
        }
    
    def get_admission_score(self, year):
        """获取某年的录取分数"""
        return self.admission_scores.get(year)
    
    def get_admission_rate(self, year):
        """获取某年的升学率"""
        return self.admission_rates.get(year)

class SchoolManager:
    """学校管理类，管理所有学校实例"""
    
    def __init__(self):
        """初始化学校管理器"""
        self.schools = {}
        self._load_schools_from_config()
    
    def _load_schools_from_config(self):
        """从配置文件加载学校信息"""
        for category_name, schools in config.SCHOOL_CATEGORIES.items():
            category = None
            for cat in SchoolCategory:
                if cat.value == category_name:
                    category = cat
                    break
            
            if category:
                for school_name in schools:
                    school = School(school_name, category)
                    self.schools[school_name] = school
    
    def get_school(self, name):
        """根据名称获取学校"""
        return self.schools.get(name)
    
    def get_schools_by_category(self, category):
        """根据分类获取学校列表"""
        return [school for school in self.schools.values() if school.category == category]
    
    def get_all_schools(self):
        """获取所有学校"""
        return list(self.schools.values())
    
    def get_all_categories(self):
        """获取所有学校分类"""
        return [category for category in SchoolCategory]