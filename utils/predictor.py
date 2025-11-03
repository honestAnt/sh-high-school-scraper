"""
预测工具
提供2026年录取分数线预测功能
"""
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.data_model import AdmissionScore, DataStorage
import config

class ScorePredictor:
    """分数预测类"""
    
    @staticmethod
    def predict_scores(school_name, prediction_year=2026):
        """
        预测指定学校未来年份的录取分数
        
        Args:
            school_name (str): 学校名称
            prediction_year (int): 预测年份
            
        Returns:
            dict: 预测结果
        """
        # 加载历史数据
        scores = DataStorage.load_admission_scores()
        
        # 过滤指定学校的数据
        school_scores = [score for score in scores if score.school_name == school_name]
        
        if len(school_scores) < 2:
            return {
                "school_name": school_name,
                "year": prediction_year,
                "min_score": None,
                "max_score": None,
                "avg_score": None,
                "confidence": 0,
                "error": "历史数据不足，无法进行预测"
            }
        
        # 准备训练数据
        X = np.array([[score.year] for score in school_scores])
        y_min = np.array([score.min_score for score in school_scores])
        y_max = np.array([score.max_score for score in school_scores])
        y_avg = np.array([score.avg_score for score in school_scores])
        
        # 创建并训练线性回归模型
        model_min = LinearRegression()
        model_max = LinearRegression()
        model_avg = LinearRegression()
        
        model_min.fit(X, y_min)
        model_max.fit(X, y_max)
        model_avg.fit(X, y_avg)
        
        # 预测未来年份的分数
        future_year = np.array([[prediction_year]])
        predicted_min = model_min.predict(future_year)[0]
        predicted_max = model_max.predict(future_year)[0]
        predicted_avg = model_avg.predict(future_year)[0]
        
        # 计算预测置信度（基于历史数据的数量和拟合度）
        confidence = min(len(school_scores) / 5, 1) * 0.7  # 数据量因子
        
        # 计算R²作为拟合度指标
        r2_min = model_min.score(X, y_min)
        r2_max = model_max.score(X, y_max)
        r2_avg = model_avg.score(X, y_avg)
        avg_r2 = (r2_min + r2_max + r2_avg) / 3
        
        # 综合置信度
        confidence = confidence * (0.3 + 0.7 * avg_r2)
        
        return {
            "school_name": school_name,
            "year": prediction_year,
            "min_score": round(predicted_min, 1),
            "max_score": round(predicted_max, 1),
            "avg_score": round(predicted_avg, 1),
            "confidence": round(confidence * 100, 1),  # 转换为百分比
            "r2_score": round(avg_r2, 3)
        }
    
    @staticmethod
    def batch_predict_scores(school_names, prediction_year=2026):
        """
        批量预测多个学校的录取分数
        
        Args:
            school_names (list): 学校名称列表
            prediction_year (int): 预测年份
            
        Returns:
            list: 预测结果列表
        """
        predictions = []
        
        for school in school_names:
            prediction = ScorePredictor.predict_scores(school, prediction_year)
            predictions.append(prediction)
        
        return predictions
    
    @staticmethod
    def save_predictions(predictions, output_file=None):
        """
        保存预测结果
        
        Args:
            predictions (list): 预测结果列表
            output_file (str, optional): 输出文件路径
            
        Returns:
            bool: 是否保存成功
        """
        if not predictions:
            return False
        
        if output_file is None:
            output_file = config.PREDICTION_FILE
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 转换为DataFrame并保存
        df = pd.DataFrame(predictions)
        df.to_csv(output_file, index=False)
        
        return True