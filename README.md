# 上海高中数据收集系统

基于豆包爬虫框架的上海高中数据自动化收集系统，用于获取上海各重点高中的录取分数线和升学率数据。

## 免责声明

本项目仅供学习和研究使用，不得用于商业目的。使用本系统收集的数据请遵守相关法律法规，不得用于非法用途。本项目开发者不对使用本系统产生的任何后果负责。

## 功能特点

- 支持多种学校分类（上海四校、八大金刚、市重点、闵行区重点、浦东新区重点）
- 自动收集2021-2025年历史数据
- 提供2026年录取分数线预测
- 两种查询模式：
  - 录取分数查询：获取指定年份和学校的录取分数及学生来源
  - 升学率查询：获取指定年份和学校的C9、985、211入线率

## 使用方法

1. 安装依赖：
```
pip install -r requirements.txt
```

2. 运行程序：
```
python main.py
```

3. 按照提示输入查询条件，获取相关数据。

## 项目结构

```
sh-high-school/
├── README.md
├── LICENSE
├── requirements.txt
├── main.py
├── config.py
├── data/
│   └── output/
├── models/
│   ├── school.py
│   └── data_model.py
├── scrapers/
│   ├── base_scraper.py
│   ├── score_scraper.py
│   └── rate_scraper.py
├── utils/
│   ├── data_processor.py
│   └── predictor.py
└── ui/
    └── simple_ui.py
```

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。