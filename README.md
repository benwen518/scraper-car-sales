
下面提供一份完整的 README 文档，包含中文和英文版本，详细介绍代码功能、环境要求、安装方法、运行方法等内容。你可以将其保存为 `README.md` 文件。

---

# EV Sales Data Scraper / 电动车销量数据爬虫

## Overview / 项目概述

**English:**

This project is a web scraping tool that collects electric vehicle (EV) sales data from the website [xl.16888.com](https://xl.16888.com/). The script uses Selenium for browser automation (in headless mode) and BeautifulSoup for parsing HTML content. The collected data is saved into a CSV file, including fields such as serial number, vehicle model, sales figures, manufacturer, price, parameter link, and month.

**中文：**

本项目是一个爬虫工具，用于从 [xl.16888.com](https://xl.16888.com/) 网站收集电动车销量数据。该脚本使用 Selenium 进行浏览器自动化操作（无界面模式）以及 BeautifulSoup 进行 HTML 内容解析。爬取的数据将保存为 CSV 文件，包含字段有：序号、车型、销量、厂商、价格、参数链接和月份。

---

## Features / 功能特点

* Automated ChromeDriver setup using `webdriver_manager`.

  使用 `webdriver_manager` 自动配置 ChromeDriver。
* Headless browsing to enable background execution.

  支持无界面浏览，可在后台运行爬虫。
* Dynamic page navigation with retry mechanism.

  带有重试机制的动态页面访问，多次尝试加载数据。
* Data extraction from HTML tables using BeautifulSoup.

  使用 BeautifulSoup 从 HTML 表格中提取数据。
* Logging and progress tracking with Python’s `logging` and `tqdm`.

  通过 Python 的 `logging` 模块记录日志，并使用 `tqdm` 展示进度条。
* Saves collected data as CSV.

  将爬取的数据保存为 CSV 文件。

---

## Requirements / 环境要求

* Python 3.6 及以上版本
* 以下 Python 库：
  * `re`
  * `numpy`
  * `pandas`
  * `beautifulsoup4` (bs4)
  * `selenium`
  * `webdriver_manager`
  * `tqdm`
  * 以及标准库模块：`time`、`logging`、`sys`、`datetime`

**安装依赖（推荐使用 pip）：**

```bash
pip install numpy pandas beautifulsoup4 selenium webdriver-manager tqdm
```

---

## Usage / 使用方法

1. **Clone or Download the Code / 下载代码：**
   **English:**

   Clone the repository or simply download the source code file (e.g., `ev_scraper.py`).
   **中文：**

   克隆本仓库或下载源码文件（例如 `ev_scraper.py`）。
2. **Run the Script / 运行脚本：**
   **English:**

   Open a terminal in the project directory and execute:

   ```bash
   python ev_scraper.py
   ```

   The script will automatically initialize the Chrome driver in headless mode, scrape the sales data for the specified months, and then store the data as a CSV file (e.g., `ev_sales_202212.csv`).

   **中文：**

   在项目目录下打开终端，执行以下命令：

   ```bash
   python ev_scraper.py
   ```

   脚本将自动以无界面模式初始化 Chrome 驱动，爬取指定月份的销量数据，并将数据保存为 CSV 文件（例如 `ev_sales_202212.csv`）。
3. **Configuration / 配置说明：**

   * 代码中的 `get_ev_data` 函数默认爬取的月份为 `"202212"`，并且构建了一个月份列表从 2022 年开始至指定月份。你可以根据需要修改此参数或调整月份列表的生成方式。
   * 日志文件将以 `ev_scraper_YYYYMMDD_HHMMSS.log` 的格式生成，并保存在代码运行的目录下，方便调试和问题排查。
4. **Troubleshooting / 常见问题排查：**

   * **Chrome Driver 相关问题：**

     如果遇到 ChromeDriver 初始化失败，确保本机已安装 Chrome 浏览器，并且 Chrome 版本与 webdriver_manager 下载的驱动版本兼容。
   * **网络访问问题：**

     若访问某个 URL 重试多次均失败，请检查网络连接或网站是否有反爬虫设置。
   * **数据提取问题：**

     若页面结构发生变化或提取不到数据，请根据页面新结构调整 BeautifulSoup 中的选择器。

---

## Code Structure / 代码结构

* **setup_driver():**

  Initializes the Chrome driver in headless mode with desired options and returns the driver instance.
* **get_url_with_retry(url, driver, max_retries=3):**

  Attempts to fetch the URL content with a retry mechanism. Returns the page source HTML.
* **extract_data_from_table(soup):**

  Parses the HTML (via BeautifulSoup) to extract table data. The function processes rows and cells to extract text and link information.
* **get_month_pages(month, driver):**

  Determines the total number of pages for a specified month by parsing pagination details on the page.
* **get_ev_data(month="202212"):**

  The main function which:

  * Initializes the driver.
  * Constructs a list of months for which data needs to be scraped.
  * Iterates through each month and its pages to extract data.
  * Combines and saves the extracted data to a CSV file.
  * Closes the browser driver at the end.

---

## Logging and Debugging / 日志与调试

* Logging is configured to output both to the console and to a log file, with timestamps and log levels.

  日志配置为同时输出到控制台和日志文件中，包含时间戳和日志级别，便于实时监控和调试。
* Progress bars are displayed using the `tqdm` library for long-running loops (months and pages).

  使用 `tqdm` 库显示进度条，方便监控月份和页面爬取进度。

---

## License / 许可

**English:**

This project is open source and available under the MIT License.

**中文：**

本项目开源，遵循 MIT 许可协议。

---

## Contact / 联系方式

For any questions or issues, please open an issue on the repository or contact the author.

如有疑问或问题，请在仓库中提交 Issue 或联系作者。

---

以上即为项目的完整说明文档。希望这份 README 能帮助你快速了解、配置及使用该电动车销量数据爬虫工具！
