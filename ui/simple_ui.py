"""
简单的命令行用户界面
提供与用户交互的功能
"""
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.school import SchoolManager, SchoolCategory
from scrapers.score_scraper import ScoreScraper
from scrapers.rate_scraper import RateScraper
from utils.data_processor import DataProcessor
from utils.predictor import ScorePredictor
import config

class SimpleUI:
    """简单的命令行用户界面"""
    
    def __init__(self):
        """初始化用户界面"""
        self.school_manager = SchoolManager()
        self.score_scraper = ScoreScraper()
        self.rate_scraper = RateScraper()
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("欢迎使用上海高中数据收集系统")
        print("=" * 60)
        print("本系统基于豆包爬虫框架，提供上海各重点高中的数据收集和分析功能")
        print("=" * 60)
    
    def display_menu(self):
        """显示主菜单"""
        print("\n请选择功能：")
        print("1. 录取分数查询")
        print("2. 升学率查询")
        print("3. 2026年录取分数预测")
        print("4. 批量数据收集")
        print("0. 退出系统")
        
        choice = input("\n请输入选项编号: ")
        return choice
    
    def display_school_categories(self):
        """显示学校分类"""
        print("\n请选择学校分类：")
        
        categories = self.school_manager.get_all_categories()
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.value}")
        
        choice = input("\n请输入分类编号: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(categories):
                return categories[index]
        except ValueError:
            pass
        
        print("无效的选择，请重新选择")
        return self.display_school_categories()
    
    def display_schools_by_category(self, category):
        """显示指定分类的学校"""
        print(f"\n{category.value}包含的学校：")
        
        schools = self.school_manager.get_schools_by_category(category)
        for i, school in enumerate(schools, 1):
            print(f"{i}. {school.name}")
        
        choice = input("\n请输入学校编号: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(schools):
                return schools[index]
        except ValueError:
            pass
        
        print("无效的选择，请重新选择")
        return self.display_schools_by_category(category)
    
    def display_years(self):
        """显示可选年份"""
        print("\n请选择年份：")
        
        for i, year in enumerate(config.DATA_YEARS, 1):
            print(f"{i}. {year}年")
        
        choice = input("\n请输入年份编号: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(config.DATA_YEARS):
                return config.DATA_YEARS[index]
        except ValueError:
            pass
        
        print("无效的选择，请重新选择")
        return self.display_years()
    
    def query_admission_score(self):
        """录取分数查询"""
        print("\n===== 录取分数查询 =====")
        
        # 选择学校分类
        category = self.display_school_categories()
        
        # 选择学校
        school = self.display_schools_by_category(category)
        
        # 选择年份
        year = self.display_years()
        
        print(f"\n正在查询 {year}年 {school.name} 的录取分数...")
        
        # 获取录取分数
        score = self.score_scraper.get_admission_score(school.name, year)
        
        # 显示结果
        print("\n查询结果：")
        print(f"学校: {score.school_name}")
        print(f"年份: {score.year}")
        print(f"最低分: {score.min_score}")
        print(f"最高分: {score.max_score}")
        print(f"平均分: {score.avg_score}")
        
        if score.student_sources:
            print("\n学生来源分布:")
            for source, percentage in score.student_sources.items():
                print(f"{source}: {percentage}%")
        
        input("\n按回车键返回主菜单...")
    
    def query_admission_rate(self):
        """升学率查询"""
        print("\n===== 升学率查询 =====")
        
        # 选择学校分类
        category = self.display_school_categories()
        
        # 选择学校
        school = self.display_schools_by_category(category)
        
        # 选择年份
        year = self.display_years()
        
        print(f"\n正在查询 {year}年 {school.name} 的升学率...")
        
        # 获取升学率
        rate = self.rate_scraper.get_admission_rate(school.name, year)
        
        # 显示结果
        print("\n查询结果：")
        print(f"学校: {rate.school_name}")
        print(f"年份: {rate.year}")
        print(f"C9入线率: {rate.c9_rate}%")
        print(f"985入线率: {rate.rate_985}%")
        print(f"211入线率: {rate.rate_211}%")
        
        input("\n按回车键返回主菜单...")
    
    def predict_scores(self):
        """2026年录取分数预测"""
        print("\n===== 2026年录取分数预测 =====")
        
        # 选择学校分类
        category = self.display_school_categories()
        
        # 选择学校
        school = self.display_schools_by_category(category)
        
        print(f"\n正在预测 {school.name} 2026年的录取分数...")
        
        # 预测分数
        prediction = ScorePredictor.predict_scores(school.name)
        
        # 显示结果
        print("\n预测结果：")
        print(f"学校: {prediction['school_name']}")
        print(f"预测年份: {prediction['year']}")
        
        if prediction.get('error'):
            print(f"预测失败: {prediction['error']}")
        else:
            print(f"预测最低分: {prediction['min_score']}")
            print(f"预测最高分: {prediction['max_score']}")
            print(f"预测平均分: {prediction['avg_score']}")
            print(f"预测置信度: {prediction['confidence']}%")
        
        input("\n按回车键返回主菜单...")
    
    def batch_collect_data(self):
        """批量数据收集"""
        print("\n===== 批量数据收集 =====")
        
        # 选择学校分类
        category = self.display_school_categories()
        
        print(f"\n正在为 {category.value} 批量收集数据...")
        
        # 获取该分类的所有学校
        schools = self.school_manager.get_schools_by_category(category)
        school_names = [school.name for school in schools]
        
        # 批量收集录取分数
        print("\n收集录取分数数据...")
        scores = self.score_scraper.batch_collect_scores(school_names, config.DATA_YEARS)
        
        # 批量收集升学率
        print("\n收集升学率数据...")
        rates = self.rate_scraper.batch_collect_rates(school_names, config.DATA_YEARS)
        
        # 保存数据
        from models.data_model import DataStorage
        DataStorage.save_admission_scores(scores)
        DataStorage.save_admission_rates(rates)
        
        print(f"\n数据收集完成，共收集了 {len(scores)} 条录取分数数据和 {len(rates)} 条升学率数据")
        
        input("\n按回车键返回主菜单...")
    
    def run(self):
        """运行用户界面"""
        self.display_welcome()
        
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.query_admission_score()
            elif choice == '2':
                self.query_admission_rate()
            elif choice == '3':
                self.predict_scores()
            elif choice == '4':
                self.batch_collect_data()
            elif choice == '0':
                print("\n感谢使用上海高中数据收集系统，再见！")
                break
            else:
                print("\n无效的选择，请重新选择")

if __name__ == "__main__":
    ui = SimpleUI()
    ui.run()