import streamlit as st
import json
import os

# ================= 1. 核心知识库 (详细总结版) =================
KNOWLEDGE_BASE = """
### 🌟 入党积极分子结业考试核心知识点
#### 一、 建党与大革命时期
* **上海建党**：1920年8月，陈独秀在上海建立第一个早期组织。
* **二大章程**：通过第一部《中国共产党章程》。
* **三大合作**：确立国共合作，政治基础是新三民主义。
#### 二、 革命战争时期
* **三湾改编**：确立“支部建在连上”，党对军队的绝对领导。
* **遵义会议**：生死攸关的转折点，标志党在政治上走向成熟。
* **七大思想**：确立毛泽东思想为党的指导思想。
#### 三、 新时代与校史
* **本质特征**：中国特色社会主义最本质的特征是中国共产党领导。
* **北师大校训**：学为人师、行为世范。
* **黄文秀**：北师大校友，“七一勋章”获得者，脱贫攻坚楷模。
"""

# ================= 2. 数据读取逻辑 =================
@st.cache_data
def load_questions():
    file_path = "questions.json" 
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                st.error("JSON 文件格式有误，请检查。")
                return []
    else:
        st.error(f"找不到文件：{file_path}")
        return []

QUESTIONS_DATA = load_questions()

# ================= 3. 会话状态初始化 =================
if 'wrong_questions' not in st.session_state:
    st.session_state['wrong_questions'] = set()
if 'current_q_index' not in st.session_state:
    st.session_state['current_q_index'] = 0
if 'show_feedback' not in st.session_state:
    st.session_state['show_feedback'] = False
if 'combo_count' not in st.session_state:
    st.session_state['combo_count'] = 0
if 'max_combo' not in st.session_state:
    st.session_state['max_combo'] = 0

# ================= 4. 网页配置 =================
st.set_page_config(page_title="入党积极分子刷题系统", page_icon="🚩")

st.sidebar.title("🚩 学习导航")
page = st.sidebar.radio("功能模块", ["📖 知识点总结", "📝 刷题模式", "🔍 总题库浏览", "❌ 错题专栏"])

# ================= 5. 功能模块实现 =================

if not QUESTIONS_DATA:
    st.stop()

# --- 模块 1: 知识点总结 ---
if page == "📖 知识点总结":
    st.title("📖 核心知识点专栏")
    st.markdown(KNOWLEDGE_BASE)

# --- 模块 2: 刷题模式 (升级：自主选进度 + 连击) ---
elif page == "📝 刷题模式":
    st.title("📝 模拟刷题")
    
    total_q = len(QUESTIONS_DATA)
    
    # --- 新增：跳转功能 ---
    with st.expander("跳题/设置起始点"):
        jump_idx = st.number_input(f"输入题号 (1-{total_q})", min_value=1, max_value=total_q, value=st.session_state['current_q_index']+1)
        if st.button("确认跳转"):
            st.session_state['current_q_index'] = jump_idx - 1
            st.session_state['show_feedback'] = False # 重置反馈状态
            st.rerun()

    # 数据看板
    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔥 当前连击", f"{st.session_state['combo_count']} Combo")
    with c2:
        st.metric("🏆 最高连击", f"{st.session_state['max_combo']} Max")

    current_index = st.session_state['current_q_index']
    
    if current_index >= total_q:
        st.balloons()
        st.success("🎉 恭喜刷完所有题目！")
        if st.button("从头开始"):
            st.session_state['current_q_index'] = 0
            st.rerun()
    else:
        current_q = QUESTIONS_DATA[current_index]
        st.progress((current_index + 1) / total_q, text=f"进度: {current_index + 1} / {total_q}")
        
        st.markdown(f"#### 第 {current_q['id']} 题")
        st.write(current_q['question'])
        
        # 答题区
        # 注意：这里不用 st.form 封装，为了更好的交互体验
        user_choice = st.radio("选择答案：", current_q['options'], index=None, key=f"q_{current_index}")
        
        if not st.session_state['show_feedback']:
            if st.button("提交答案"):
                if user_choice:
                    st.session_state['show_feedback'] = True
                    if user_choice == current_q['answer']:
                        st.session_state['is_correct'] = True
                        st.session_state['combo_count'] += 1
                        if st.session_state['combo_count'] > st.session_state['max_combo']:
                            st.session_state['max_combo'] = st.session_state['combo_count']
                    else:
                        st.session_state['is_correct'] = False
                        st.session_state['combo_count'] = 0 # 连击中断，但不会跳回第一题
                        st.session_state['wrong_questions'].add(current_q['id'])
                    st.rerun()
                else:
                    st.warning("请先选择一个选项")
        else:
            # 显示判定结果
            if st.session_state['is_correct']:
                st.success(f"✅ 正确！Combo x {st.session_state['combo_count']}")
            else:
                st.error(f"❌ 错误！正确答案：{current_q['answer']}")
                st.warning(f"**解析：** {current_q['explanation']}")
            
            if st.button("下一题 ➡️"):
                st.session_state['current_q_index'] += 1
                st.session_state['show_feedback'] = False
                st.rerun()

# --- 模块 3: 总题库浏览 ---
elif page == "🔍 总题库浏览":
    st.title("🔍 总题库全览")
    search = st.text_input("搜索题目关键字")
    for q in QUESTIONS_DATA:
        if search in q['question']:
            with st.expander(f"第 {q['id']} 题"):
                st.write(q['question'])
                st.success(f"答案：{q['answer']}")
                st.caption(f"解析：{q['explanation']}")

# --- 模块 4: 错题专栏 ---
elif page == "❌ 错题专栏":
    st.title("❌ 错题专栏")
    if not st.session_state['wrong_questions']:
        st.info("暂无错题记录")
    else:
        st.write(f"共 {len(st.session_state['wrong_questions'])} 道错题")
        wrong_ids = list(st.session_state['wrong_questions'])
        for q_id in wrong_ids:
            # 找到原题
            q = next((x for x in QUESTIONS_DATA if x['id'] == q_id), None)
            if q:
                with st.expander(f"错题 {q['id']}"):
                    st.write(q['question'])
                    st.write(f"正确答案：{q['answer']}")
                    if st.button(f"移除此错题 {q['id']}"):
                        st.session_state['wrong_questions'].remove(q_id)
                        st.rerun()
