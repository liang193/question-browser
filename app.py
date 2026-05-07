import streamlit as st
import json
import os

# ================= 1. 核心知识库静态文本 (详细版) =================
KNOWLEDGE_BASE = """
### 🌟 入党积极分子结业考试详细知识点总结

#### 一、 党的创立与大革命时期
* **早期组织**：1920年8月，上海建立了中国第一个共产党早期组织。
* **核心人物**：第一个提出“中国共产党”名称的是蔡和森。李大钊是公开颂扬俄国十月革命的第一人。
* **重要会议**：
    * **二大**：通过第一部《中国共产党章程》。
    * **三大**：确定国共合作方针。
    * **四大**：将“委员长”职务改称为“总书记”。
* **三大政策**：联俄、联共、扶助农工。

#### 二、 土地革命与抗日战争时期
* **三湾改编**：确立“支部建在连上”，党对军队的绝对领导。
* **遵义会议**：生死攸关的转折点，中共第一次独立自主解决党内问题。
* **抗战贡献**：平型关大捷（首次大捷）、百团大战（沉重打击日军）。
* **理论确立**：王稼祥首提“毛泽东思想”；党的七大确立其为指导思想。
* **三大作风**：理论联系实际、密切联系群众、批评与自我批评。

#### 三、 改革开放与新时代
* **伟大转折**：1978年十一届三中全会，将重心转移到经济建设，实行改革开放。
* **新时代特征**：中国特色社会主义最本质的特征是中国共产党领导。
* **中心任务**：高质量发展是全面建设社会主义现代化国家的首要任务。
* **北师大专属**：校训“学为人师、行为世范”；“七一勋章”获得者黄文秀（2013级校友）。
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
        st.error(f"找不到文件：{file_path}，请确保它已经上传到同一目录下。")
        return []

QUESTIONS_DATA = load_questions()

# ================= 3. 会话状态初始化 =================
# 错题本
if 'wrong_questions' not in st.session_state:
    st.session_state['wrong_questions'] = set()

# 刷题进度与反馈状态
if 'current_q_index' not in st.session_state:
    st.session_state['current_q_index'] = 0
if 'show_feedback' not in st.session_state:
    st.session_state['show_feedback'] = False
if 'is_correct' not in st.session_state:
    st.session_state['is_correct'] = False

# 连击系统逻辑
if 'combo_count' not in st.session_state:
    st.session_state['combo_count'] = 0
if 'max_combo' not in st.session_state:
    st.session_state['max_combo'] = 0

# ================= 4. 网页全局配置与侧边栏 =================
st.set_page_config(page_title="入党积极分子刷题系统", page_icon="🚩", layout="centered")

st.sidebar.title("🚩 学习导航")
page = st.sidebar.radio(
    "请选择功能模块：", 
    ["📖 知识点总结", "📝 刷题模式", "🔍 总题库浏览", "❌ 错题专栏"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：提交答案后会自动显示解析。答对增加连击，答错连击归零。")

# ================= 5. 各页面功能实现 =================

if not QUESTIONS_DATA:
    st.stop()

# --- 模块 1: 知识点总结 ---
if page == "📖 知识点总结":
    st.title("📖 核心知识点专栏")
    st.markdown(KNOWLEDGE_BASE)

# --- 模块 2: 刷题模式 (带连击系统) ---
elif page == "📝 刷题模式":
    st.title("📝 模拟刷题")
    
    # 连击看板展示
    col1, col2 = st.columns(2)
    with col1:
        combo = st.session_state['combo_count']
        if combo >= 15: status = "🔥 登峰造极！"
        elif combo >= 10: status = "🚀 势不可挡！"
        elif combo >= 5: status = "✨ 渐入佳境！"
        elif combo > 0: status = "👍 连续正确"
        else: status = "🎯 开始挑战"
        st.metric("当前连击", f"{combo} Combo", delta=status if combo > 0 else None)
    with col2:
        st.metric("历史最高连击", f"{st.session_state['max_combo']} Max")

    total_q = len(QUESTIONS_DATA)
    current_index = st.session_state['current_q_index']
    
    # 进度条
    st.progress((current_index + 1) / total_q, text=f"进度: {current_index + 1} / {total_q}")
    
    if current_index >= total_q:
        st.balloons()
        st.success(f"🎉 恭喜完成所有题目！本次最高连击数：{st.session_state['max_combo']}")
        if st.button("重新开始"):
            st.session_state['current_q_index'] = 0
            st.session_state['combo_count'] = 0
            st.rerun()
    else:
        current_q = QUESTIONS_DATA[current_index]
        st.markdown(f"#### 第 {current_q['id']} 题")
        st.write(current_q['question'])
        
        # 答题表单
        with st.form(key=f"form_main_{current_q['id']}"):
            user_choice = st.radio("选择答案：", current_q['options'], index=None)
            
            # 按钮切换逻辑
            if st.session_state['show_feedback']:
                btn_label = "下一题 ➡️"
            else:
                btn_label = "提交答案"
            
            submit_btn = st.form_submit_button(btn_label)
            
            if submit_btn:
                # 触发下一题逻辑
                if st.session_state['show_feedback']:
                    st.session_state['current_q_index'] += 1
                    st.session_state['show_feedback'] = False 
                    st.rerun() 
                # 触发判定逻辑
                else:
                    if user_choice is None:
                        st.warning("⚠️ 请先选择一个选项！")
                    else:
                        st.session_state['show_feedback'] = True
                        if user_choice == current_q['answer']:
                            st.session_state['is_correct'] = True
                            st.session_state['combo_count'] += 1
                            if st.session_state['combo_count'] > st.session_state['max_combo']:
                                st.session_state['max_combo'] = st.session_state['combo_count']
                            if current_q['id'] in st.session_state['wrong_questions']:
                                st.session_state['wrong_questions'].remove(current_q['id'])
                        else:
                            st.session_state['is_correct'] = False
                            st.session_state['combo_count'] = 0 # 连击中断
                            st.session_state['wrong_questions'].add(current_q['id'])
                        st.rerun()

        # 显示解析
        if st.session_state['show_feedback']:
            if st.session_state['is_correct']:
                st.success(f"✅ 回答正确！Combo x {st.session_state['combo_count']}")
                if st.session_state['combo_count'] == 10:
                    st.toast("达成 10 连击！太棒了！")
            else:
                st.error(f"❌ 连击中断！正确答案：{current_q['answer']}")
                st.warning(f"**解析：** {current_q['explanation']}")
            st.info("💡 请点击上方的按钮进入『下一题』")

# --- 模块 3: 总题库浏览 ---
elif page == "🔍 总题库浏览":
    st.title("🔍 总题库全览")
    for q in QUESTIONS_DATA:
        with st.expander(f"第 {q['id']} 题"):
            st.write(q['question'])
            for opt in q['options']:
                st.write(opt)
            st.success(f"答案：{q['answer']}")
            st.caption(f"解析：{q['explanation']}")

# --- 模块 4: 错题专栏 ---
elif page == "❌ 错题专栏":
    st.title("❌ 错题二次攻坚")
    if not st.session_state['wrong_questions']:
        st.balloons()
        st.success("目前没有错题记录，请继续保持！")
    else:
        st.write(f"待复习错题：{len(st.session_state['wrong_questions'])} 道")
        wrong_qs = [q for q in QUESTIONS_DATA if q['id'] in st.session_state['wrong_questions']]
        
        for q in wrong_qs:
            with st.form(key=f"wrong_f_{q['id']}"):
                st.write(f"**{q['question']}**")
                ans = st.radio("重新作答：", q['options'], index=None, key=f"ans_{q['id']}")
                if st.form_submit_button("验证"):
                    if ans == q['answer']:
                        st.success("✅ 这次对了！点击下方按钮移出记录。")
                        if st.button(f"从错题本移除题目 {q['id']}"):
                            st.session_state['wrong_questions'].remove(q['id'])
                            st.rerun()
                    else:
                        st.error(f"❌ 还是错了，正确答案是：{q['answer']}")
