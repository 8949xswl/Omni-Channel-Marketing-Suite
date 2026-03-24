import pymysql

# MySQL 连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '170322ASDasd..',
}

try:
    print("正在连接 MySQL...")
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 创建数据库
    print("创建数据库...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS marketing_db")
    
    # 使用数据库
    cursor.execute("USE marketing_db")
    
    # 创建仪表板指标表
    print("创建仪表板指标表...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marketing_dashboard_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL UNIQUE,
        daily_roi DECIMAL(10, 2),
        daily_roi_delta DECIMAL(10, 2),
        new_users INT,
        new_users_delta INT,
        avg_order_value DECIMAL(10, 2),
        avg_order_value_delta DECIMAL(10, 2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    
    # 创建投放明细表
    print("创建投放明细表...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marketing_campaign_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        投放渠道 VARCHAR(50),
        投放日期 DATE,
        投放量 INT,
        曝光数 INT,
        点击数 INT,
        `成本_¥` DECIMAL(12, 2),
        转化数 INT,
        `成交额_¥` DECIMAL(12, 2),
        ROI DECIMAL(10, 2),
        `转化率_%` DECIMAL(10, 2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 插入示例数据到仪表板指标表
    print("插入仪表板示例数据...")
    cursor.execute("""
    INSERT INTO marketing_dashboard_metrics (date, daily_roi, daily_roi_delta, new_users, new_users_delta, avg_order_value, avg_order_value_delta)
    VALUES 
        (CURDATE(), 3.50, 0.25, 1250, 120, 385.50, 25.00),
        (DATE_SUB(CURDATE(), INTERVAL 1 DAY), 3.25, -0.15, 1130, -80, 360.50, -15.00),
        (DATE_SUB(CURDATE(), INTERVAL 2 DAY), 3.40, 0.35, 1210, 150, 375.25, 18.50)
    ON DUPLICATE KEY UPDATE 
        daily_roi = VALUES(daily_roi),
        daily_roi_delta = VALUES(daily_roi_delta),
        new_users = VALUES(new_users),
        new_users_delta = VALUES(new_users_delta),
        avg_order_value = VALUES(avg_order_value),
        avg_order_value_delta = VALUES(avg_order_value_delta)
    """)
    
    # 插入示例数据到投放明细表
    print("插入投放明细示例数据...")
    cursor.execute("""
    INSERT INTO marketing_campaign_data (投放渠道, 投放日期, 投放量, 曝光数, 点击数, `成本_¥`, 转化数, `成交额_¥`, ROI, `转化率_%`)
    VALUES 
        ('抖音', CURDATE(), 25000, 185000, 5200, 3500.00, 156, 28320.00, 7.09, 3.00),
        ('小红书', CURDATE(), 18000, 142000, 4100, 2800.00, 82, 14875.00, 4.31, 2.00),
        ('微博', CURDATE(), 12000, 95000, 2800, 1800.00, 67, 12145.00, 5.75, 2.39),
        ('微信', DATE_SUB(CURDATE(), INTERVAL 1 DAY), 15000, 120000, 3500, 2200.00, 105, 19125.00, 7.69, 3.00),
        ('知乎', DATE_SUB(CURDATE(), INTERVAL 1 DAY), 8000, 65000, 1800, 1200.00, 45, 8175.00, 5.81, 2.50),
        ('B站', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 20000, 160000, 4700, 3200.00, 142, 25830.00, 7.07, 3.02),
        ('快手', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 22000, 175000, 5100, 3600.00, 153, 27765.00, 6.71, 3.00),
        ('头条', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 16000, 128000, 3800, 2400.00, 95, 17275.00, 6.20, 2.50)
    """)
    
    conn.commit()
    print("✅ 数据库初始化完成！")
    
    # 验证数据
    cursor.execute("SELECT COUNT(*) FROM marketing_dashboard_metrics")
    dashboard_count = cursor.fetchone()[0]
    print(f"✅ 仪表板数据: {dashboard_count} 条记录")
    
    cursor.execute("SELECT COUNT(*) FROM marketing_campaign_data")
    campaign_count = cursor.fetchone()[0]
    print(f"✅ 投放明细数据: {campaign_count} 条记录")
    
    cursor.close()
    conn.close()
    print("\n✨ 数据库初始化成功！现在可以启动应用了。")
    
except Exception as e:
    print(f"❌ 出错了: {e}")
    import traceback
    traceback.print_exc()
