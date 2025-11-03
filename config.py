# 上海高中数据收集系统配置文件

# 学校分类
SCHOOL_CATEGORIES = {
    "上海四校": ["上海中学", "华师大二附中", "复旦附中", "交大附中"],
    "八大金刚": ["南洋模范", "格致中学", "大同中学", "控江中学", "七宝中学", "延安中学", "建平中学", "复兴高级中学"],
    "市重点": ["上海市实验学校", "位育中学", "向明中学", "市西中学", "上海中学东校", "上海市平和双语学校", 
             "华东师大一附中", "上海外国语大学附属中学", "上海市曹杨第二中学", "上海市晋元高级中学"],
    "闵行区重点": ["闵行中学", "莘庄中学", "北桥高级中学", "闵行区实验中学"],
    "浦东新区重点": ["浦东中学", "建平中学浦东校区", "进才中学", "上海中学东校", "华东师大二附中紫竹校区", "上海市实验学校东校"]
}

# 查询模式
QUERY_MODES = {
    "录取分数": "{year}年上海{school}录取分数及学生来源",
    "升学率": "{year}年上海{school}C9、985、211入线率"
}

# 数据年份范围
DATA_YEARS = list(range(2021, 2026))  # 2021-2025年
PREDICTION_YEAR = 2026

# 豆包API配置
DOUBAN_API_URL = "https://www.doubao.com/api/chat/completions"
DOUBAN_API_KEY = ""  # 需要用户自行填写

# 数据存储路径
DATA_OUTPUT_DIR = "data/output"
SCORE_DATA_FILE = f"{DATA_OUTPUT_DIR}/admission_scores.csv"
RATE_DATA_FILE = f"{DATA_OUTPUT_DIR}/admission_rates.csv"
PREDICTION_FILE = f"{DATA_OUTPUT_DIR}/predictions_2026.csv"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "sh_high_school.log"