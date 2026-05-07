import streamlit as st
import json
import os

# ================= 1. 核心知识库静态文本 =================
KNOWLEDGE_BASE = """
### 🌟 入党积极分子结业考试核心知识点总结
*(节选整理，常看常新)*

#### 一、 建党初期与大革命时期
* **早期组织**：1920年8月，最先在上海建立了中国第一个共产党早期组织。
* **党名提出**：第一个提出党的名称为“中国共产党”的是蔡和森。中国一大通过了中国共产党的第一纲领，正式确定党名。
* **组织建设**：党的二大通过了《中国共产党章程》。党的三大在广州召开，确定了国共合作方针。
* **国共合作**：第一次国共合作的政治基础是新三民主义，其三大政策为联俄、联共、扶助农工。

#### 二、 土地革命与抗日战争时期
* **武装斗争**：打响了武装反抗国民党反动派第一枪的是南昌起义。“三湾改编”把支部建在连上，确立了党对军队的绝对领导。
* **生死攸关的转折**：遵义会议是中共第一次独立自主地运用马克思主义原理解决自己的路线、方针、政策会议。
* **指导思想**：党的七大确立毛泽东思想为全党的指导思想。
* **三大作风**：理论和实践相结合的作风、和人民群众紧密联系在一起的作风、批评与自我批评的作风。

#### 三、 改革开放与现代化建设新时期
* **伟大转折**：1978年12月，党的十一届三中全会作出了实行改革开放的历史性决策。
* **特色道路**：1982年党的十二大明确提出“建设有中国特色的社会主义”。
* **奋斗目标**：党的十六大第一次提出全面建设小康社会的奋斗目标。

#### 四、 新时代中国特色社会主义
* **最本质特征**：中国特色社会主义最本质的特征是中国共产党领导。
* **三大里程碑**：建立中国共产党、成立中华人民共和国、推进改革开放和中国特色社会主义事业。
* **首要任务**：高质量发展是全面建设社会主义现代化国家的首要任务。
* **总体国家安全观**：必须坚定不移贯彻总体国家安全观。
"""

# ================= 2. 数据读取逻辑 =================
# 使用缓存机制，避免每次操作网页都重新读取文件，提升网页流畅度
@st.cache_data
def load_questions():
    file_path = "questions.json" # 确保 json 文件和 app.py 在同一目录下
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                st.error("JSON 文件格式有误，请检查。")
                return []
    else:
        st.error(f"找不到文件：{file_path}，请确保它已经上传到了 GitHub。")
        return []

QUESTIONS_DATA = load_questions()

# ================= 3. 会话状态初始化 =================
# 用于记录用户的错题 ID，刷新页面或切换模块时不会丢失
if 'wrong_questions' not in st.session_state:
    st.session_state['wrong_questions'] = set()

# ================= 4. 网页全局配置与侧边栏 =================
st.set_page_config(page_title="入党积极分子刷题系统", page_icon="📚", layout="centered")

st.sidebar.title("🚩 学习导航")
page = st.sidebar.radio(
    "请选择功能模块：", 
    ["📖 知识点总结", "📝 刷题模式", "🔍 总题库浏览", "❌ 错题专栏"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：在『刷题模式』中做错的题目会自动加入『错题专栏』供您二次攻坚。")

# ================= 5. 各页面功能实现 =================

# 阻止在数据未加载成功时渲染后续页面
if not QUESTIONS_DATA:
    st.stop()

# 模块 1: 知识点总结
if page == "📖 知识点总结":
    st.title("📖 核心知识点专栏")
    st.markdown(KNOWLEDGE_BASE)

# 模块 2: 刷题模式
elif page == "📝 刷题模式":
    st.title("📝 模拟刷题")
    
    # 提取所有题目的标题供下拉框使用
    q_titles = [f"第 {q['id']} 题" for q in QUESTIONS_DATA]
    
    # 题目选择器
    selected_idx = st.selectbox("请选择要练习的题目：", range(len(q_titles)), format_func=lambda x: q_titles[x])
    current_q = QUESTIONS_DATA[selected_idx]
    
    st.markdown(f"### {current_q['question']}")
    
    # 答题表单
    with st.form(key=f"form_main_{current_q['id']}"):
        user_choice = st.radio("请选择你的答案：", current_q['options'], index=None)
        submit_btn = st.form_submit_button("提交答案")
        
        if submit_btn:
            if user_choice is None:
                st.warning("⚠️ 请先选择一个选项！")
            elif user_choice == current_q['answer']:
                st.success("✅ 回答正确！")
                # 如果回答正确且在错题本中，将其移除
                if current_q['id'] in st.session_state['wrong_questions']:
                    st.session_state['wrong_questions'].remove(current_q['id'])
            else:
                st.error("❌ 回答错误！")
                st.session_state['wrong_questions'].add(current_q['id'])
                st.info(f"**正确答案是：** {current_q['answer']}")
                st.warning(current_q['explanation'])

# 模块 3: 总题库浏览
elif page == "🔍 总题库浏览":
    st.title("🔍 总题库 (全览)")
    st.write(f"当前题库共收录 **{len(QUESTIONS_DATA)}** 道题目。点击下方题目可查看详情与答案。")
    
    for q in QUESTIONS_DATA:
        with st.expander(f"第 {q['id']} 题: {q['question']}"):
            for opt in q['options']:
                st.write(opt)
            st.markdown("---")
            st.success(f"**正确答案：** {q['answer']}")
            st.caption(q['explanation'])

# 模块 4: 错题专栏
elif page == "❌ 错题专栏":
    st.title("❌ 错题二次攻坚")
    
    if not st.session_state['wrong_questions']:
        st.balloons()
        st.success("🎉 太棒了！当前没有错题记录，知识掌握得很牢固！")
    else:
        st.write(f"您当前共有 **{len(st.session_state['wrong_questions'])}** 道错题待复习。")
        
        # 筛选出租错题
        wrong_qs = [q for q in QUESTIONS_DATA if q['id'] in st.session_state['wrong_questions']]
        
        for current_q in wrong_qs:
            st.markdown("---")
            st.markdown(f"#### 第 {current_q['id']} 题: {current_q['question']}")
            
            # 使用唯一的 key 避免表单冲突
            with st.form(key=f"form_wrong_{current_q['id']}"):
                user_choice = st.radio("重新选择：", current_q['options'], index=None, key=f"radio_wrong_{current_q['id']}")
                submit_btn = st.form_submit_button("验证答案")
                
                if submit_btn:
                    if user_choice is None:
                        st.warning("⚠️ 请先选择一个选项！")
                    elif user_choice == current_q['answer']:
                        st.success("✅ 这次选对了！")
                        st.info("提示：您可以切换到其他页面再回来，此题将从错题本中移除。")
                        st.session_state['wrong_questions'].remove(current_q['id'])
                    else:
                        st.error("❌ 还是选错了，请查看解析加强记忆！")
                        st.info(f"**正确答案是：** {current_q['answer']}")
                        st.warning(current_q['explanation'])
