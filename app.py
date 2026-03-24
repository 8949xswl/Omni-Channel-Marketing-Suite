import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import pymysql
from pymysql.cursors import DictCursor

# ============================================================================
# MySQL 数据库配置
# ============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '170322ASDasd..',
    'database': 'marketing_db'
}

# ============================================================================
# 数据库连接函数
# ============================================================================
def get_db_connection():
    """建立 MySQL 数据库连接"""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        st.warning(f"⚠️ 数据库连接失败：{e}")
        return None


# ============================================================================
# 页面配置
# ============================================================================
st.set_page_config(
    page_title="Omni-Channel Marketing Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 自定义 CSS 样式（专业 SaaS 主题）
# ============================================================================
st.markdown("""
<style>
    /* 侧边栏样式优化 - 浅色主题 */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #f5f5f5 0%, #efefef 100%);
        width: 320px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #333333 !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] .stRadio > label > div:first-child {
        color: #333333 !important;
    }
    
    /* 主容器背景 */
    .main {
        background: linear-gradient(to bottom, #f8f9f9 0%, #e8eef5 100%);
    }
    
    /* KPI 卡片样式 */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #0066cc;
    }
    
    /* 数据表格样式 */
    [data-testid="dataframe"] {
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stMarkdown hr {
        margin: 20px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0066cc, transparent);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 统计工具函数：卡方检验
# ============================================================================
def chi_square_test(control_conv, control_total, variant_conv, variant_total):
    """
    执行卡方检验，用于比较两组的转化率是否有显著差异。
    
    参数：
        control_conv (int): 对照组转化数
        control_total (int): 对照组总样本数
        variant_conv (int): 变体组转化数
        variant_total (int): 变体组总样本数
    
    返回：
        dict: 包含 chi2、p_value、dof 等信息
    """
    if control_total == 0 or variant_total == 0:
        return {'error': '样本量不能为 0'}
    
    # 构建列联表
    contingency_table = np.array([
        [control_conv, control_total - control_conv],
        [variant_conv, variant_total - variant_conv]
    ])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    return {
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'control_conv_rate': control_conv / control_total,
        'variant_conv_rate': variant_conv / variant_total,
        'lift': (variant_conv / variant_total) / (control_conv / control_total) - 1
    }


# ============================================================================
# 统计工具函数：t 检验
# ============================================================================
def t_test(control_vals, variant_vals):
    """
    执行独立样本 t 检验，用于比较两组的平均值是否有显著差异。
    
    参数：
        control_vals (list): 对照组数据（如 ROI、金额等连续数据）
        variant_vals (list): 变体组数据
    
    返回：
        dict: 包含 t_stat、p_value、mean_control、mean_variant 等信息
    """
    if len(control_vals) == 0 or len(variant_vals) == 0:
        return {'error': '数据不能为空'}
    
    control_vals = np.array(control_vals, dtype=float)
    variant_vals = np.array(variant_vals, dtype=float)
    
    t_stat, p_value = stats.ttest_ind(control_vals, variant_vals)
    
    return {
        't_stat': t_stat,
        'p_value': p_value,
        'mean_control': control_vals.mean(),
        'mean_variant': variant_vals.mean(),
        'std_control': control_vals.std(),
        'std_variant': variant_vals.std(),
        'lift': (variant_vals.mean() / control_vals.mean() - 1) * 100 if control_vals.mean() != 0 else 0
    }


# ============================================================================
# 结果解释函数
# ============================================================================
def interpret_pvalue(p_value, alpha=0.05):
    """
    根据 p 值解释统计检验结果。
    
    参数：
        p_value (float): 统计检验的 p 值
        alpha (float): 显著性水平（默认 0.05）
    
    返回：
        dict: 包含显著性水平、结论、建议等信息
    """
    if p_value < alpha:
        conclusion = "✅ 显著差异"
        interpretation = f"两组存在显著差异（p < {alpha}），拒绝零假设"
        recommendation = "🎯 建议采用新方案"
    else:
        conclusion = "❌ 无显著差异"
        interpretation = f"两组无显著差异（p ≥ {alpha}），无法拒绝零假设"
        recommendation = "⏸️ 建议继续观察或调整实验设计"
    
    return {
        'conclusion': conclusion,
        'interpretation': interpretation,
        'recommendation': recommendation,
        'is_significant': p_value < alpha
    }


# ============================================================================
# 备用数据生成函数：KPI 卡片数据
# ============================================================================
def _generate_kpi_data_fallback():
    """
    生成随机的 KPI 数据（模拟真实数据波动）【备用方案】。
    
    返回：
        dict: 包含 GMV、ROI、转化率及其变化值
    """
    gmv = np.random.randint(100000, 500000)
    gmv_delta = np.random.randint(-10000, 30000)
    
    roi = round(np.random.uniform(1.5, 4.5), 2)
    roi_delta = round(np.random.uniform(-0.5, 0.8), 2)
    
    conversion_rate = round(np.random.uniform(2.0, 8.0), 2)
    conversion_delta = round(np.random.uniform(-0.5, 1.2), 2)
    
    return {
        'gmv': gmv,
        'gmv_delta': gmv_delta,
        'roi': roi,
        'roi_delta': roi_delta,
        'conversion_rate': conversion_rate,
        'conversion_delta': conversion_delta
    }


# ============================================================================
# 数据生成函数：KPI 卡片数据 【从数据库读取】
# ============================================================================
def generate_kpi_data():
    """
    生成随机的 KPI 数据（模拟真实数据波动）。
    
    返回：
        dict: 包含 GMV、ROI、转化率及其变化值
    """
    return _generate_kpi_data_fallback()  # 当前仍使用 Mock 数据


# ============================================================================
# 备用函数：概览看板 KPI 指标（Mock 数据）
# ============================================================================
def _generate_dashboard_metrics_fallback():
    """
    生成概览看板的三个 KPI 指标数据【备用方案 - Mock 数据】。
    
    返回：
        dict: 包含今日 ROI、新增用户、平均客单价及其变化值
    """
    daily_roi = round(np.random.uniform(2.5, 4.8), 2)
    daily_roi_delta = round(np.random.uniform(-0.5, 0.8), 2)
    
    new_users = np.random.randint(500, 2000)
    new_users_delta = np.random.randint(-100, 300)
    
    avg_order_value = round(np.random.uniform(150, 500), 2)
    avg_order_value_delta = round(np.random.uniform(-20, 50), 2)
    
    return {
        'daily_roi': daily_roi,
        'daily_roi_delta': daily_roi_delta,
        'new_users': new_users,
        'new_users_delta': new_users_delta,
        'avg_order_value': avg_order_value,
        'avg_order_value_delta': avg_order_value_delta
    }


# ============================================================================
# 数据生成函数：概览看板 KPI 指标【从 MySQL 读取】
# ============================================================================
@st.cache_data(ttl=3600)
def generate_dashboard_metrics():
    """
    生成概览看板的三个 KPI 指标数据【从 MySQL 读取，缓存 1 小时】。
    
    返回：
        dict: 包含今日 ROI、新增用户、平均客单价及其变化值
    """
    try:
        conn = get_db_connection()
        if conn is None:
            st.warning("⚠️ 无法连接数据库，已切换到演示数据")
            return _generate_dashboard_metrics_fallback()
        
        cursor = conn.cursor(DictCursor)
        
        # 查询今日数据（按日期倒序，取最新的一条）
        query = """
        SELECT daily_roi, daily_roi_delta, new_users, new_users_delta, 
               avg_order_value, avg_order_value_delta
        FROM marketing_dashboard_metrics
        WHERE date = CURDATE()
        ORDER BY date DESC
        LIMIT 1
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            cursor.close()
            conn.close()
            return {
                'daily_roi': float(result['daily_roi']),
                'daily_roi_delta': float(result['daily_roi_delta']),
                'new_users': int(result['new_users']),
                'new_users_delta': int(result['new_users_delta']),
                'avg_order_value': float(result['avg_order_value']),
                'avg_order_value_delta': float(result['avg_order_value_delta'])
            }
        else:
            # 如果今日无数据，查询最新的一天
            query = """
            SELECT daily_roi, daily_roi_delta, new_users, new_users_delta, 
                   avg_order_value, avg_order_value_delta
            FROM marketing_dashboard_metrics
            ORDER BY date DESC
            LIMIT 1
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                return {
                    'daily_roi': float(result['daily_roi']),
                    'daily_roi_delta': float(result['daily_roi_delta']),
                    'new_users': int(result['new_users']),
                    'new_users_delta': int(result['new_users_delta']),
                    'avg_order_value': float(result['avg_order_value']),
                    'avg_order_value_delta': float(result['avg_order_value_delta'])
                }
        
        return _generate_dashboard_metrics_fallback()
    
    except Exception as e:
        st.warning(f"⚠️ 数据库查询失败：{e}，已切换到演示数据")
        return _generate_dashboard_metrics_fallback()


# ============================================================================
# 备用函数：投放明细表（Mock 数据）
# ============================================================================
def _generate_campaign_data_fallback():
    """
    生成投放明细表的模拟数据【备用方案 - Mock 数据】。
    
    返回：
        DataFrame: 包含多个投放活动的详细数据
    """
    channels = ['抖音', '小红书', '微博', '微信', '知乎', 'B站', '快手', '头条']
    data = []
    
    for i in range(np.random.randint(8, 12)):
        data.append({
            '投放渠道': np.random.choice(channels),
            '投放日期': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 30)),
            '投放量': np.random.randint(5000, 50000),
            '曝光数': np.random.randint(50000, 500000),
            '点击数': np.random.randint(1000, 20000),
            '成本_¥': np.random.randint(500, 10000),
            '转化数': np.random.randint(10, 200),
            '成交额_¥': np.random.randint(2000, 50000),
            'ROI': round(np.random.uniform(1.5, 5.0), 2),
            '转化率_%': round(np.random.uniform(0.5, 3.0), 2)
        })
    
    df = pd.DataFrame(data)
    df['投放日期'] = df['投放日期'].dt.strftime('%Y-%m-%d')
    return df


# ============================================================================
# 数据生成函数：投放明细表【从 MySQL 读取】
# ============================================================================
@st.cache_data(ttl=3600)
def generate_campaign_data():
    """
    生成投放明细表的数据【从 MySQL 读取，缓存 1 小时】。
    
    返回：
        DataFrame: 包含多个投放活动的详细数据
    """
    try:
        conn = get_db_connection()
        if conn is None:
            st.warning("⚠️ 无法连接数据库，已切换到演示数据")
            return _generate_campaign_data_fallback()
        
        cursor = conn.cursor(DictCursor)
        
        # 查询最近 100 条投放记录
        query = """
        SELECT 投放渠道, 投放日期, 投放量, 曝光数, 点击数, `成本_¥`, 
               转化数, `成交额_¥`, ROI, `转化率_%`
        FROM marketing_campaign_data
        ORDER BY 投放日期 DESC
        LIMIT 100
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if results:
            df = pd.DataFrame(results)
            # 确保日期格式为字符串
            df['投放日期'] = pd.to_datetime(df['投放日期']).dt.strftime('%Y-%m-%d')
            return df
        else:
            return _generate_campaign_data_fallback()
    
    except Exception as e:
        st.warning(f"⚠️ 数据库查询失败：{e}，已切换到演示数据")
        return _generate_campaign_data_fallback()


# ============================================================================
# 页面函数：概览看板
# ============================================================================
def show_dashboard():
    """显示概览看板页面"""
    st.title("📊 概览看板 (Dashboard)")
    st.markdown("---")
    
    # 获取 KPI 数据
    metrics_data = generate_dashboard_metrics()
    
    # 显示三个 KPI 指标
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💹 今日 ROI",
            value=f"{metrics_data['daily_roi']:.2f}x",
            delta=f"{metrics_data['daily_roi_delta']:+.2f}x"
        )
    
    with col2:
        st.metric(
            label="👥 新增用户",
            value=f"{metrics_data['new_users']:,}",
            delta=f"{metrics_data['new_users_delta']:+,}"
        )
    
    with col3:
        st.metric(
            label="💰 平均客单价",
            value=f"¥{metrics_data['avg_order_value']:.2f}",
            delta=f"¥{metrics_data['avg_order_value_delta']:+.2f}"
        )
    
    st.markdown("---")
    
    # 投放明细表
    st.subheader("📊 投放明细表")
    st.markdown("**说明**：支持点击列头进行排序，向左/右滑动查看所有数据")
    
    campaign_df = generate_campaign_data()
    st.dataframe(
        campaign_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    st.markdown("---")
    
    # 数据概览统计
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总投放金额", f"¥{campaign_df['成本_¥'].sum():,}")
    with col2:
        st.metric("总成交额", f"¥{campaign_df['成交额_¥'].sum():,}")
    with col3:
        avg_roi = campaign_df['ROI'].mean()
        st.metric("平均 ROI", f"{avg_roi:.2f}x")
    with col4:
        avg_conversion = campaign_df['转化率_%'].mean()
        st.metric("平均转化率", f"{avg_conversion:.2f}%")


# ============================================================================
# 页面函数：AI 文案助手
# ============================================================================
def show_content():
    """显示 AI 文案助手页面"""
    st.title("✍️ AI 文案助手 (Content)")
    st.markdown("---")
    
    st.markdown("""
    **使用说明**：输入品牌或产品信息，AI 将自动生成高转化文案。
    """)
    
    # 输入框
    prompt = st.text_area(
        "📝 请输入文案创作提示词",
        placeholder="例：我们是一个电商平台，主要销售美妆产品。请生成一条吸引女性用户的营销文案。",
        height=100
    )
    
    # 生成按钮
    if st.button("✨ 生成内容", type="primary", use_container_width=True):
        if prompt.strip():
            st.markdown("---")
            st.success("✅ 内容已生成！")
            
            # Mock 文案响应（预留 API 接口）
            mock_contents = [
                "🌟 **独家福利来袭**：全新美妆精选，专为你定制！使用优惠码 BEAUTY2024 享受首次购买 30% 优惠。立即加入我们的美妆家族，让你的肌肤焕发光彩！",
                "💎 **美妆新世界**：汇聚全球顶级品牌，为你打造专属美丽方案。从护肤到彩妆，一站式解决你的美妆需求。今天下单，明天享受女神级服务！",
                "✨ **限时活动**：精选美妆产品大促销，低至 5 折！我们承诺 100% 正品，假一赔十。加入 2 万+ 满意客户的选择，让美妆成为你的日常！"
            ]
            
            selected_content = np.random.choice(mock_contents)
            
            st.info(f"""
            **生成的文案：**
            
            {selected_content}
            """)
            
            # 编辑和使用选项
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ 编辑文案"):
                    st.session_state.edit_mode = True
            with col2:
                if st.button("🔄 重新生成"):
                    st.rerun()
            with col3:
                if st.button("✅ 接受使用"):
                    st.success("文案已保存到剪贴板！")
        else:
            st.warning("⚠️ 请先输入提示词")
    
    st.markdown("---")
    st.markdown("""
    **💡 提示：** 当前使用 Mock 数据演示。后续将接入 OpenAI / 文心一言 等 API。
    """)


# ============================================================================
# A/B 测试工具 - 首页
# ============================================================================
def show_ab_home():
    """显示 A/B 测试工具首页（KPI 卡片）"""
    st.markdown("### 🏠 首页概览")
    st.markdown("---")
    
    # 生成动态 KPI 数据
    kpi_data = generate_kpi_data()
    
    # 三列布局展示 KPI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 GMV（成交总额）",
            value=f"¥{kpi_data['gmv']:,}",
            delta=f"¥{kpi_data['gmv_delta']:+,}"
        )
    
    with col2:
        st.metric(
            label="📈 ROI（投资回报率）",
            value=f"{kpi_data['roi']:.2f}x",
            delta=f"{kpi_data['roi_delta']:+.2f}x"
        )
    
    with col3:
        st.metric(
            label="🎯 转化率",
            value=f"{kpi_data['conversion_rate']:.2f}%",
            delta=f"{kpi_data['conversion_delta']:+.2f}%"
        )
    
    st.markdown("---")
    
    # 简要说明
    st.markdown("""
    **✨ KPI 指标解读：**
    - **GMV**: 一定时间内的成交总额，反映整体销售规模
    - **ROI**: 投资回报率，表示每投入 1 元获得的收益
    - **转化率**: 用户转化为购买的比例，反映营销效果
    """)


# ============================================================================
# A/B 测试工具 - 显著性计算
# ============================================================================
def show_ab_test():
    """显示 A/B 测试工具页面"""
    st.markdown("""
    **功能说明**：输入两组实验数据，自动计算统计显著性，帮助你快速判断实验结果。
    """)
    
    st.markdown("---")
    
    # 选择检验方法
    test_type = st.radio(
        "选择检验方法",
        ["卡方检验（转化率等比例数据）", "t 检验（ROI、金额等连续数据）"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # 左右分栏：对照组和变体组
    col_control, col_variant = st.columns(2)
    
    if test_type == "卡方检验（转化率等比例数据）":
        # ===== 卡方检验 =====
        with col_control:
            st.subheader("📊 对照组 (Control)")
            control_total = st.number_input(
                "样本总数",
                min_value=1,
                value=1000,
                key="chi_control_total"
            )
            control_conv = st.number_input(
                "转化数",
                min_value=0,
                value=50,
                max_value=control_total,
                key="chi_control_conv"
            )
            control_rate = control_conv / control_total
            st.metric("转化率", f"{control_rate*100:.2f}%")
        
        with col_variant:
            st.subheader("🎯 变体组 (Variant)")
            variant_total = st.number_input(
                "样本总数",
                min_value=1,
                value=1000,
                key="chi_variant_total"
            )
            variant_conv = st.number_input(
                "转化数",
                min_value=0,
                value=65,
                max_value=variant_total,
                key="chi_variant_conv"
            )
            variant_rate = variant_conv / variant_total
            st.metric("转化率", f"{variant_rate*100:.2f}%")
        
        st.markdown("---")
        
        # 计算按钮
        if st.button("📊 计算显著性", type="primary", use_container_width=True):
            result = chi_square_test(control_conv, control_total, variant_conv, variant_total)
            
            if 'error' not in result:
                st.success("✅ 计算完成！")
                st.markdown("---")
                
                # 展示统计结果
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("卡方值（χ²）", f"{result['chi2']:.4f}")
                with col2:
                    st.metric("p 值", f"{result['p_value']:.6f}")
                with col3:
                    lift = result['lift'] * 100
                    st.metric("提升率（Lift）", f"{lift:+.2f}%")
                
                st.markdown("---")
                
                # 解释结果
                interpretation = interpret_pvalue(result['p_value'])
                
                st.markdown(f"""
                ### {interpretation['conclusion']}
                
                **判断标准**：显著性水平 α = 0.05
                
                **统计解释**：{interpretation['interpretation']}
                
                **建议行动**：{interpretation['recommendation']}
                """)
            else:
                st.error(f"❌ 计算失败：{result['error']}")
    
    else:
        # ===== t 检验 =====
        with col_control:
            st.subheader("📊 对照组 (Control)")
            st.markdown("**输入多个数据点（以逗号分隔）：**")
            control_input = st.text_area(
                "数据点",
                value="85,90,88,92,87,89,91,86",
                height=100,
                key="t_control_data"
            )
        
        with col_variant:
            st.subheader("🎯 变体组 (Variant)")
            st.markdown("**输入多个数据点（以逗号分隔）：**")
            variant_input = st.text_area(
                "数据点",
                value="92,95,90,94,93,96,91,95",
                height=100,
                key="t_variant_data"
            )
        
        st.markdown("---")
        
        # 计算按钮
        if st.button("📊 计算显著性", type="primary", use_container_width=True):
            try:
                control_vals = [float(x.strip()) for x in control_input.split(',') if x.strip()]
                variant_vals = [float(x.strip()) for x in variant_input.split(',') if x.strip()]
                
                if len(control_vals) > 1 and len(variant_vals) > 1:
                    result = t_test(control_vals, variant_vals)
                    
                    if 'error' not in result:
                        st.success("✅ 计算完成！")
                        st.markdown("---")
                        
                        # 展示统计结果
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("t 值", f"{result['t_stat']:.4f}")
                        with col2:
                            st.metric("p 值", f"{result['p_value']:.6f}")
                        with col3:
                            st.metric("提升率（Lift）", f"{result['lift']:+.2f}%")
                        
                        # 详细统计信息
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                            **对照组统计**：
                            - 样本量：{len(control_vals)}
                            - 平均值：{result['mean_control']:.2f}
                            - 标准差：{result['std_control']:.2f}
                            """)
                        with col2:
                            st.markdown(f"""
                            **变体组统计**：
                            - 样本量：{len(variant_vals)}
                            - 平均值：{result['mean_variant']:.2f}
                            - 标准差：{result['std_variant']:.2f}
                            """)
                        
                        st.markdown("---")
                        
                        # 解释结果
                        interpretation = interpret_pvalue(result['p_value'])
                        
                        st.markdown(f"""
                        ### {interpretation['conclusion']}
                        
                        **判断标准**：显著性水平 α = 0.05
                        
                        **统计解释**：{interpretation['interpretation']}
                        
                        **建议行动**：{interpretation['recommendation']}
                        """)
                    else:
                        st.error(f"❌ 计算失败：{result['error']}")
                else:
                    st.error("❌ 每组至少需要 2 个数据点")
            except ValueError:
                st.error("❌ 请输入有效的数字数据")


# ============================================================================
# 页面函数：数据实验室
# ============================================================================
def show_labs():
    """显示数据实验室页面"""
    st.title("🔬 数据实验室 (Labs)")
    st.markdown("---")
    st.info("📌 数据实验室功能正在开发中，敬请期待...")


# ============================================================================
# 页面函数：A/B 测试工具（主函数）
# ============================================================================
def show_testing():
    """显示 A/B 测试工具页面"""
    st.title("🧪 A/B 测试工具 (Testing)")
    st.markdown("---")
    
    # 直接显示 A/B 测试功能
    show_ab_test()


# ============================================================================
# 主应用逻辑
# ============================================================================
def main():
    """主应用程序入口"""
    # 侧边栏导航栏
    st.sidebar.markdown("## 🎯 Omni-Channel Marketing Suite")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "选择功能模块",
        [
            "概览看板 (Dashboard)",
            "AI 文案助手 (Content)",
            "A/B 测试工具 (Testing)",
            "数据实验室 (Labs)"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("*© 2026 Omni-Channel Marketing Suite*")
    
    # 根据选择显示对应页面
    if page == "概览看板 (Dashboard)":
        show_dashboard()
    elif page == "AI 文案助手 (Content)":
        show_content()
    elif page == "A/B 测试工具 (Testing)":
        show_testing()
    elif page == "数据实验室 (Labs)":
        show_labs()


# ============================================================================
# 应用入口
# ============================================================================
if __name__ == "__main__":
    main()
