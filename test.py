import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'ev_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_driver():
    """设置并返回Chrome驱动"""
    print("正在初始化Chrome驱动...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        print("正在安装ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("正在创建Chrome实例...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome驱动初始化成功！")
        return driver
    except Exception as e:
        print(f"Chrome驱动初始化失败: {str(e)}")
        logging.error(f"Chrome驱动初始化失败: {str(e)}")
        raise

def get_url_with_retry(url, driver, max_retries=3):
    """获取URL内容，带重试机制"""
    print(f"正在访问URL: {url}")
    for attempt in range(max_retries):
        try:
            driver.get(url)
            # 等待表格加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            print(f"成功获取页面内容: {url}")
            return driver.page_source
        except Exception as e:
            print(f"第{attempt + 1}次尝试失败: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print(f"无法访问URL {url}，已达到最大重试次数")
                logging.error(f"访问URL失败: {url}, 错误: {str(e)}")
                return None

def extract_data_from_table(soup):
    """从表格中提取数据"""
    data = []
    try:
        # 找到表格
        table = soup.find('table')
        if not table:
            print("未找到数据表格")
            return []

        # 获取所有行
        rows = table.find_all('tr')
        print(f"找到 {len(rows)} 行数据")

        for row in rows:
            # 获取行中的所有单元格
            cells = row.find_all('td')
            if len(cells) >= 5:  # 确保至少有5个单元格
                row_data = []
                # 收集前5个单元格的文本
                for i, cell in enumerate(cells[:5]):
                    text = cell.get_text().strip()
                    row_data.append(text)
                
                # 获取链接（如果存在）
                link_cell = cells[2].find('a')
                if link_cell and link_cell.get('href'):
                    row_data.append(link_cell.get('href'))
                else:
                    row_data.append("")
                
                data.append(row_data)

        print(f"成功提取 {len(data)} 行数据")
        return data
    except Exception as e:
        print(f"提取数据时出错: {str(e)}")
        return []

def get_month_pages(month, driver):
    """获取指定月份的所有页面URL"""
    print(f"正在获取 {month} 月份的页面数量...")
    url = f'https://xl.16888.com/ev-{month}-{month}-1.html'
    source = get_url_with_retry(url, driver)
    if not source:
        return []
        
    soup = BeautifulSoup(source, "lxml")
    
    # 打印页面内容以供调试
    print("页面内容片段：")
    print(soup.prettify()[:500])  # 打印前500个字符
    
    # 尝试不同的选择器
    page_info = None
    for selector in [
        'div.xl-data-page-r > div > span',
        'div.xl-page > span',  # 新的选择器
        '.page-box',  # 另一个可能的选择器
    ]:
        page_info = soup.select_one(selector)
        if page_info:
            print(f"找到页面信息，使用选择器: {selector}")
            break
    
    if not page_info:
        # 如果找不到页面信息，默认返回至少一页
        print(f"无法找到页面信息，默认使用1页")
        return [url]
        
    # 提取页数信息
    total = re.findall(r"\d+", page_info.get_text())
    if not total:
        print(f"无法解析页面数量，默认使用1页")
        return [url]
        
    total = int(total[0])
    pages = (total + 49) // 50
    print(f"{month} 月份共有 {pages} 页数据")
    return [f'https://xl.16888.com/ev-{month}-{month}-{i+1}.html' for i in range(pages)]

def get_ev_data(month="202212"):
    """主函数"""
    print(f"开始抓取 {month} 月份的数据...")
    try:
        driver = setup_driver()
        print("成功初始化驱动")
        
        months = [
            f"{year}{str(m).zfill(2)}"
            for year in range(2022, 2025)
            for m in range(1, 12)
            if f"{year}{str(m).zfill(2)}" <= month
        ]
        
        all_data = []
        for current_month in tqdm(months, desc="处理月份"):
            print(f"\n开始处理 {current_month} 月份的数据")
            urls = get_month_pages(current_month, driver)
            
            for url in tqdm(urls, desc=f"处理{current_month}月份的页面"):
                source = get_url_with_retry(url, driver)
                if not source:
                    continue
                
                soup = BeautifulSoup(source, "lxml")
                month_data = extract_data_from_table(soup)
                
                if month_data:
                    # 添加月份信息
                    for row in month_data:
                        row.append(current_month)
                    all_data.extend(month_data)
                    print(f"当前数据总行数: {len(all_data)}")
        
        if all_data:
            # 转换为DataFrame
            columns = ["序号", "车型", "销量", "厂商", "价格", "参数链接", "月份"]
            df = pd.DataFrame(all_data, columns=columns)
            print(f"最终数据形状: {df.shape}")
            print("数据示例：")
            print(df.head())
            
            # 保存数据
            output_file = f"ev_sales_{month}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"数据已保存到 {output_file}")
        else:
            print("警告：没有收集到任何数据！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        logging.error(f"程序执行错误: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("已关闭浏览器驱动")

if __name__ == '__main__':
    try:
        print("开始执行爬虫程序...")
        get_ev_data()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行失败: {str(e)}")
    finally:
        print("程序结束")