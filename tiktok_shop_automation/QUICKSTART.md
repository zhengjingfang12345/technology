# 快速入门指南

## 5分钟快速上手

### 步骤1：安装依赖（2分钟）

```bash
cd tiktok_shop_automation

# 安装Python依赖
pip install -r requirements.txt

# 安装浏览器驱动（推荐使用Playwright）
playwright install chromium
```

### 步骤2：配置账号（1分钟）

**方式一：使用环境变量（推荐）**

```bash
# Linux/Mac
export TIKTOK_USERNAME="your_email@example.com"
export TIKTOK_PASSWORD="your_password"

# Windows PowerShell
$env:TIKTOK_USERNAME="your_email@example.com"
$env:TIKTOK_PASSWORD="your_password"

# Windows CMD
set TIKTOK_USERNAME=your_email@example.com
set TIKTOK_PASSWORD=your_password
```

**方式二：修改配置文件**

编辑 `config/config.yaml`，修改以下内容：

```yaml
tiktok_shop:
  username: "your_email@example.com"
  password: "your_password"
```

### 步骤3：运行程序（2分钟）

```bash
python main.py
```

程序会：
1. 自动打开浏览器
2. 导航到TikTok店铺登录页面
3. 等待您手动完成登录（包括验证码等）
4. 登录后按回车键
5. 自动抓取热门商品数据
6. 保存到 `data/` 目录

## 常用命令

```bash
# 基本运行
python main.py

# 使用自定义配置
python main.py -c config/my_config.yaml

# 查看帮助
python main.py --help
```

## 配置调整

### 调整抓取范围

编辑 `config/config.yaml`：

```yaml
scraping:
  max_pages: 10           # 限制抓取10页，0表示不限制
  scrolls_per_page: 5     # 每页滚动5次
```

### 更改输出格式

```yaml
storage:
  format: "excel"         # 可选: excel, csv, json
  output_dir: "./data"
```

### 切换自动化框架

```yaml
browser:
  type: "playwright"      # 可选: playwright, selenium, yingdao
  headless: false        # true=无头模式（后台运行）
```

## 输出结果

数据保存在 `data/` 目录，文件名格式：

```
tiktok_popular_products_20260117_153045.xlsx
```

## 遇到问题？

1. **查看日志**: `logs/tiktok_automation.log`
2. **查看截图**: `logs/screenshots/`
3. **阅读完整文档**: `README.md`

## 下一步

- 📖 阅读完整的 [README.md](README.md)
- 🔧 学习高级配置选项
- 🎯 根据需求自定义数据提取逻辑

---

祝使用愉快！ 🚀
