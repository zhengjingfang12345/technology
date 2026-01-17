# TikTok店铺自动化工具

一个基于Python的TikTok店铺自动化工具，支持自动登录、热门商品数据抓取等功能。支持影刀RPA、Playwright、Selenium多种自动化框架。

## 功能特性

✨ **核心功能**
- 🔐 自动登录TikTok店铺（支持手动辅助登录）
- 📊 自动抓取热门商品列表（瀑布流加载）
- 💾 多格式数据存储（Excel、CSV、JSON）
- 🔄 支持多页数据采集和自动去重
- 📸 自动截图记录关键步骤

🛠️ **技术特性**
- 支持影刀RPA、Playwright、Selenium三种自动化框架
- 灵活的配置系统（YAML配置文件）
- 完善的日志记录
- 错误重试机制
- 数据缓冲和批量保存

## 项目结构

```
tiktok_shop_automation/
├── config/
│   └── config.yaml          # 配置文件
├── data/                    # 数据输出目录
├── logs/                    # 日志目录
│   └── screenshots/         # 截图目录
├── utils/                   # 工具模块
│   ├── __init__.py
│   ├── browser.py          # 浏览器自动化
│   ├── config_loader.py    # 配置加载
│   ├── data_storage.py     # 数据存储
│   └── logger.py           # 日志配置
├── main.py                 # 主程序
└── requirements.txt        # 依赖包
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd tiktok_shop_automation

# 安装依赖
pip install -r requirements.txt

# 如果使用 Playwright（推荐）
playwright install chromium

# 如果使用影刀RPA，请从官网下载SDK并安装
```

### 2. 配置设置

编辑 `config/config.yaml` 文件，配置您的TikTok店铺信息：

```yaml
tiktok_shop:
  username: "your_email@example.com"
  password: "your_password"

browser:
  type: "playwright"  # 可选: playwright, selenium, yingdao
  headless: false     # 是否无头模式
```

**安全提示**：建议使用环境变量存储敏感信息：

```bash
export TIKTOK_USERNAME="your_email@example.com"
export TIKTOK_PASSWORD="your_password"
```

### 3. 运行程序

```bash
# 使用默认配置
python main.py

# 使用自定义配置文件
python main.py -c /path/to/config.yaml
```

### 4. 使用流程

1. 程序启动后会自动打开浏览器并导航到登录页面
2. **手动完成登录**（包括验证码、二次验证等）
3. 登录完成后按回车键，程序将自动继续执行
4. 自动导航到"商品 → 商品机会 → 热门商品"页面
5. 自动滚动页面，抓取所有商品数据
6. 数据自动保存到 `data/` 目录

## 配置说明

### 浏览器配置

```yaml
browser:
  type: "playwright"        # 浏览器类型
  headless: false          # 是否无头模式
  timeout: 30              # 超时时间（秒）
  page_load_wait: 3        # 页面加载等待时间
  scroll_wait: 2           # 滚动等待时间
```

### 抓取配置

```yaml
scraping:
  scrolls_per_page: 5      # 每页滚动次数
  max_pages: 0             # 最大页数（0=无限制）
  scroll_pixels: 800       # 每次滚动像素
  deduplicate: true        # 是否去重
```

### 存储配置

```yaml
storage:
  format: "excel"          # 存储格式: json, csv, excel
  output_dir: "./data"     # 输出目录
  file_prefix: "tiktok_popular_products"
  append: false            # 是否追加到现有文件
```

## 支持的自动化框架

### 1. Playwright（推荐）

```bash
pip install playwright
playwright install chromium
```

优点：速度快、稳定性好、API现代化

### 2. Selenium

```bash
pip install selenium webdriver-manager
```

优点：成熟稳定、社区支持好

### 3. 影刀RPA

从[影刀官网](https://www.yingdao.com/)下载SDK并安装

优点：可视化操作、中文支持好、适合非技术人员

## 数据输出

程序会将抓取的商品数据保存为以下格式之一：

- **Excel** (.xlsx)：推荐，适合数据分析
- **CSV** (.csv)：通用格式，易于导入其他系统
- **JSON** (.json)：程序化处理

数据字段包括：
- `product_id`: 商品ID
- `product_name`: 商品名称
- `price`: 价格
- `sales`: 销量
- `image_url`: 图片URL
- `product_url`: 商品链接
- `category`: 分类
- `rating`: 评分

## 高级功能

### 自动截图

程序会在关键步骤自动截图，保存在 `logs/screenshots/` 目录：
- 登录页面
- 登录后页面
- 热门商品页面
- 每5页截图一次

### 错误重试

配置重试机制：

```yaml
advanced:
  retry_times: 3           # 失败重试次数
  retry_interval: 5        # 重试间隔（秒）
```

### 代理支持

```yaml
advanced:
  use_proxy: true
  proxy_url: "http://proxy.example.com:8080"
```

## 常见问题

### Q: 程序无法登录怎么办？

A: 程序设计为手动辅助登录。在浏览器打开后，手动完成登录（包括验证码），然后按回车继续。

### Q: 为什么没有抓取到数据？

A: 可能原因：
1. 页面元素选择器需要更新（TikTok可能更新了页面结构）
2. 登录未成功
3. 网络问题

查看日志文件获取详细错误信息。

### Q: 如何自定义数据提取逻辑？

A: 编辑 `main.py` 中的 `_extract_with_playwright()` 等方法，根据实际页面结构调整CSS选择器。

### Q: 支持多店铺吗？

A: 可以通过多个配置文件实现：

```bash
python main.py -c config/shop1.yaml
python main.py -c config/shop2.yaml
```

## 技术支持

如需技术支持或功能定制，请通过以下方式联系：

- 提交 Issue
- 发送邮件至项目维护者

## 注意事项

⚠️ **重要提示**：

1. 本工具仅供学习和个人使用
2. 请遵守TikTok的服务条款和robots.txt
3. 合理控制抓取频率，避免对服务器造成压力
4. 妥善保管账号密码等敏感信息
5. 建议使用环境变量而非配置文件存储密码

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-01-17)

- ✨ 初始版本发布
- 🔐 支持TikTok店铺自动登录
- 📊 支持热门商品数据抓取
- 💾 支持多格式数据导出
- 🛠️ 支持Playwright、Selenium、影刀RPA三种框架

---

**祝您使用愉快！** 🎉
