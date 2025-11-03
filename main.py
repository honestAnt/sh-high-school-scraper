#!/usr/bin/env python3
"""
上海高中数据收集系统
主程序入口
"""
import os
import sys
import logging
from ui.simple_ui import SimpleUI
import config

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=config.LOG_FILE,
    filemode='a'
)
logger = logging.getLogger('main')

def main():
    """主程序入口"""
    # 确保数据输出目录存在
    os.makedirs(config.DATA_OUTPUT_DIR, exist_ok=True)
    
    # 启动用户界面
    try:
        ui = SimpleUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序运行异常: {str(e)}")
        print(f"\n程序运行异常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()