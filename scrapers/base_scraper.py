"""
豆包爬虫基础类
提供与豆包API交互的基本功能
"""
import requests
import json
import time
import logging
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=config.LOG_FILE,
    filemode='a'
)
logger = logging.getLogger('base_scraper')

class BaseScraper:
    """豆包爬虫基础类"""
    
    def __init__(self, api_key=None):
        """
        初始化爬虫
        
        Args:
            api_key (str, optional): 豆包API密钥，如果不提供则使用配置文件中的密钥
        """
        self.api_key = api_key or config.DOUBAN_API_KEY
        self.api_url = config.DOUBAN_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def query(self, prompt, max_retries=3, retry_delay=2):
        """
        向豆包API发送查询
        
        Args:
            prompt (str): 查询提示词
            max_retries (int): 最大重试次数
            retry_delay (int): 重试延迟（秒）
            
        Returns:
            dict: API响应结果
        """
        if not self.api_key:
            logger.error("API密钥未设置，请在config.py中设置DOUBAN_API_KEY或初始化时提供")
            return {"error": "API密钥未设置"}
        
        payload = {
            "model": "doubao-pro",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        for attempt in range(max_retries):
            try:
                logger.info(f"发送查询: {prompt[:50]}...")
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("查询成功")
                    return result
                else:
                    logger.warning(f"查询失败，状态码: {response.status_code}, 响应: {response.text}")
                    
                    if attempt < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"达到最大重试次数 {max_retries}")
                        return {"error": f"API请求失败: {response.status_code}", "details": response.text}
            
            except Exception as e:
                logger.error(f"查询异常: {str(e)}")
                
                if attempt < max_retries - 1:
                    logger.info(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"达到最大重试次数 {max_retries}")
                    return {"error": f"查询异常: {str(e)}"}
    
    def extract_text_from_response(self, response):
        """
        从API响应中提取文本内容
        
        Args:
            response (dict): API响应结果
            
        Returns:
            str: 提取的文本内容
        """
        try:
            if "error" in response:
                return f"错误: {response['error']}"
            
            if "choices" in response and len(response["choices"]) > 0:
                message = response["choices"][0].get("message", {})
                return message.get("content", "")
            
            return "无法从响应中提取文本"
        
        except Exception as e:
            logger.error(f"提取文本异常: {str(e)}")
            return f"提取文本异常: {str(e)}"
    
    def mock_query(self, prompt):
        """
        模拟查询（用于测试）
        
        Args:
            prompt (str): 查询提示词
            
        Returns:
            dict: 模拟的API响应结果
        """
        logger.info(f"模拟查询: {prompt[:50]}...")
        
        # 根据提示词类型返回不同的模拟数据
        if "录取分数" in prompt:
            return {
                "choices": [
                    {
                        "message": {
                            "content": "2023年上海中学录取分数情况如下：\n最低分：555分\n最高分：578分\n平均分：565分\n\n学生来源分布：\n徐汇区：35%\n浦东新区：25%\n静安区：15%\n黄浦区：10%\n其他区县：15%"
                        }
                    }
                ]
            }
        elif "升学率" in prompt:
            return {
                "choices": [
                    {
                        "message": {
                            "content": "2023年上海中学升学率情况：\nC9入线率：45%\n985入线率：68%\n211入线率：92%"
                        }
                    }
                ]
            }
        else:
            return {
                "choices": [
                    {
                        "message": {
                            "content": "无法识别的查询类型"
                        }
                    }
                ]
            }