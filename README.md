# 🎯 Omni-Channel Marketing Suite

一个专业的全渠道营销数据分析和实验平台，集仪表板、AI 文案、A/B 测试、数据分析于一体。

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Streamlit 1.55+](https://img.shields.io/badge/Streamlit-1.55+-red.svg)](https://streamlit.io/)
[![MySQL 8.0+](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 项目概览

Omni-Channel Marketing Suite 是一个为营销团队设计的企业级数据决策平台。帮助运营、策划、分析人员快速进行数据分析、文案优化和实验决策。

**主要目标用户**：
- 📊 电商运营负责人
- ✍️ 营销策划和优化专家  
- 📈 数据分析师
- 🚀 增长黑客

---

## ✨ 核心功能

### 1️⃣ 概览看板 (Dashboard)
- **实时 KPI 指标**：今日 ROI、新增用户、平均客单价
- **变化趋势**：每个指标配置增减幅度，红绿色指示
- **投放明细表**：8 个渠道的投放数据对比
- **统计概览**：总投放金额、总成交额、平均 ROI、平均转化率

### 2️⃣ AI 文案助手 (Content)
- **智能生成**：输入品牌信息，AI 生成高转化营销文案
- **多渠道适配**：针对不同平台的专属文案风格
- **编辑和重生成**：迭代优化，直到创意满意
- **文案库管理**：保存和复用高效文案

### 3️⃣ A/B 测试工具 (Testing)
- **卡方检验**：比较两版本的转化率是否显著不同
- **t 检验**：比较平均值是否显著不同（ROI、客单价等）
- **自动判断**：p < 0.05 为显著差异，自动给出建议

### 4️⃣ 数据实验室 (Labs)
- 🔬 高级分析工具（开发中）

---

## 🛠️ 技术栈

| 组件 | 版本 |
|------|------|
| **Streamlit** | 1.55.0 |
| **Python** | 3.12.3 |
| **MySQL** | 8.0 |
| **Pandas** | 2.3.3 |
| **NumPy** | 2.4.3 |
| **SciPy** | 1.17.1 |
| **pymysql** | 1.0.2+ |
| **python-dotenv** | 1.0.0+ |

---

## 📦 快速开始

### 系统要求
- Python 3.12+
- MySQL 8.0+
- Windows / macOS / Linux

### 安装步骤

#### 1️⃣ 克隆项目
```bash
git clone https://github.com/your-username/omni-channel-marketing-suite.git
cd omni-channel-marketing-suite
```

#### 2️⃣ 创建虚拟环境
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

#### 3️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

#### 4️⃣ 配置数据库
```bash
# 复制环境变量样板
cp .env.example .env

# 编辑 .env，填入你的 MySQL 密码
# DB_PASSWORD=your_mysql_password
```

#### 5️⃣ 初始化数据库
```bash
python init_db.py
```

**输出示例**：
```
正在连接 MySQL...
创建数据库...
创建仪表板指标表...
创建投放明细表...
✅ 数据库初始化完成！
✅ 仪表板数据: 3 条记录
✅ 投放明细数据: 8 条记录
```

#### 6️⃣ 启动应用
```bash
streamlit run app.py
```

浏览器会自动打开：`http://localhost:8501`

---

## 📊 数据库架构

### marketing_dashboard_metrics (仪表板指标表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| date | DATE | 日期（唯一） |
| daily_roi | DECIMAL | 当日 ROI |
| daily_roi_delta | DECIMAL | ROI 变化量 |
| new_users | INT | 新增用户数 |
| new_users_delta | INT | 用户变化量 |
| avg_order_value | DECIMAL | 平均客单价 |
| avg_order_value_delta | DECIMAL | 客单价变化量 |

### marketing_campaign_data (投放明细表)

| 字段 | 类型 | 说明 |
|------|------|------|
| 投放渠道 | VARCHAR | 渠道名称 |
| 投放日期 | DATE | 投放日期 |
| 投放量 | INT | 投放数量 |
| 曝光数 | INT | 曝光次数 |
| 点击数 | INT | 点击次数 |
| 成本_¥ | DECIMAL | 投放成本 |
| 转化数 | INT | 转化数量 |
| 成交额_¥ | DECIMAL | 成交金额 |
| ROI | DECIMAL | 投资回报率 |
| 转化率_% | DECIMAL | 转化率百分比 |

**包含渠道**：抖音、小红书、微博、微信、知乎、B站、快手、头条

---

## 💾 数据管理

### 修改数据的 3 种方式

#### 方式 1️⃣：GUI 工具（推荐）
1. 下载 [MySQL Workbench](https://www.mysql.com/products/workbench/)
2. 连接到 localhost，用户 root
3. 打开 marketing_db 数据库
4. 直接编辑表格数据

#### 方式 2️⃣：命令行
```bash
# 连接数据库
mysql -h localhost -u root -p

# 查看数据
USE marketing_db;
SELECT * FROM marketing_dashboard_metrics;

# 修改今天的 KPI
UPDATE marketing_dashboard_metrics 
SET daily_roi = 4.00, new_users = 1500 
WHERE date = CURDATE();

# 修改抖音渠道
UPDATE marketing_campaign_data 
SET ROI = 8.50, `成本_¥` = 4000 
WHERE 投放渠道 = '抖音' AND 投放日期 = CURDATE();
```

#### 方式 3️⃣：直接编辑 SQL
```bash
# 执行 SQL 文件
mysql -u root -p < init_db.sql
```

---

## 🎯 使用场景

### 场景 1：运营晨会
- 打开 Dashboard
- 快速查看昨天的 ROI、用户增长、客单价变化
- 对比各渠道投放效果

### 场景 2：优化营销文案
- 打开 AI 文案助手
- 输入："美妆品牌，目标 18-35 岁女性，促销 30% 优惠"
- AI 生成 3 个文案版本
- 选中最好的，复制到投放平台

### 场景 3：验证 A/B 测试结果
- 对比新文案 vs 原文案的转化效果
- 输入数据到 A/B 测试工具
- 查看 p 值判断是否采用新方案
- 系统给出建议：显著时采用，否则继续观察

---

## 🔐 安全性

### 密码管理
项目使用环境变量方式管理数据库密码，确保安全性：

```python
# 代码中读取环境变量
password = os.getenv('DB_PASSWORD')

# 实际密码存储在 .env（不上传），样板在 .env.example（可以上传）
```

### .gitignore 配置
已配置以下文件不上传 GitHub：
- `.env` - 本地密码文件
- `.venv/` - 虚拟环境
- `__pycache__/` - Python 缓存
- `.streamlit/` - Streamlit 配置

---

## 📈 性能优化

### 缓存策略
- **数据缓存**：1 小时（TTL=3600）
- **减少查询**：减少数据库查询，提升应用响应速度
- **缓存优先**：首次加载后，同一小时内从缓存读取

### 容错机制
- **自动降级**：数据库连接失败 → 自动切换 Mock 数据
- **永不崩溃**：应用总能显示界面
- **用户提示**：显示警告提示用户数据库状态

---

## ❓ 常见问题

### Q1：为什么修改数据后没有立即显示？
**A**：因为数据缓存了 1 小时。刷新页面可立即显示新数据。

### Q2：A/B 测试的 p 值怎么理解？
**A**：
- `p < 0.05`：两组有显著差异 ✅ 建议采用新方案
- `p ≥ 0.05`：两组无显著差异 ⏸️ 建议继续观察

### Q3：应用显示"无法连接数据库"怎么办？
**A**：MySQL 服务未启动。启动 MySQL 服务即可。应用会自动使用 Mock 数据。

### Q4：怎样修改 MySQL 密码？
**A**：
```bash
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;

# 然后更新 .env 文件中的 DB_PASSWORD
```

### Q5：可以改哪些数据？
**A**：KPI 表和投放表的任何字段都可以改。推荐用 MySQL Workbench 或命令行。

---

## 📚 项目结构

```
omni-channel-marketing-suite/
├── app.py                   # 主应用程序（1000+ 行）
├── init_db.py               # 数据库初始化脚本
├── init_db.sql              # SQL 建表脚本
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量样板
├── .env                     # 本地密码文件（不上传）
├── .gitignore              # Git 忽略配置
├── README.md               # 本文档
└── .venv/                  # 虚拟环境
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request


---

## 🎓 学习资源

- [Streamlit 官方文档](https://docs.streamlit.io/)
- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [SciPy 统计学说明](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [A/B 测试最佳实践](https://www.optimizely.com/optimization-glossary/ab-testing/)

---

