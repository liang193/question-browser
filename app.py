import streamlit as st
import json
import os

# ================= 1. 核心知识库静态文本 (详细升级版) =================
KNOWLEDGE_BASE = """
### 🌟 入党积极分子结业考试详细知识点总结（全覆盖）

#### 一、 党的创立与大革命时期
* **早期组织与建党**：1920年8月，最先在上海建立了中国第一个共产党早期组织[cite: 2]。第一个提出党的名称为“中国共产党”的是蔡和森[cite: 2]。在中国公开颂扬俄国十月革命的第一人是李大钊[cite: 2]。
* **重要会议**：
    * **党的一大**：确定党的名称是“中国共产党”[cite: 2]。
    * **党的二大**：依据马克思列宁建党学说，通过了《中国共产党章程》，对党员、党组织等六个方面作了规定[cite: 2]。
    * **党的三大**：1923年6月在广州召开，确定了国共合作的方针[cite: 2]。
    * **党的四大**：将党的中央执行委员会的“委员长”职务改称为“总书记”[cite: 2]。
* **国共合作**：第一次国共合作的政治基础是新三民主义，其三大政策为“联俄、联共、扶助农工”[cite: 2]。

#### 二、 土地革命与抗日战争时期
* **武装反抗与军队建设**：南昌起义打响了武装反抗国民党反动派第一枪[cite: 2]。“三湾改编”把支部建在连上，确立了党对军队的绝对领导[cite: 2]。
* **伟大长征**：遵义会议是中共第一次独立自主地运用马克思主义原理解决自己的路线、方针、政策的会议[cite: 2]。湘江战役是中央红军长征途中最壮烈的一战[cite: 2]。长征胜利跨越了12个省[cite: 2]。标志红军长征胜利结束的是红军三大主力在会宁会师[cite: 2]。
* **抗日战争**：
    * **政策与宣传**：1935年发表“八一宣言”，提出“停止内战，一致抗日”口号[cite: 2]。埃德加·斯诺撰成《西行漫记》，首次向外界详细介绍红军[cite: 2]。我党在敌后根据地实行的土地政策是地主减租减息[cite: 2]。
    * **重大战役**：平型关伏击战取得抗战以来首次大捷[cite: 2]；忻口会战是抗战初期华北战场规模最大、最激烈，国共配合最好的一次战役[cite: 2]；百团大战给予日军沉重打击[cite: 2]。
* **理论与作风建设**：王稼祥第一次提出“毛泽东思想”概念[cite: 2]。党的七大确立毛泽东思想为全党的指导思想[cite: 2]。党的三大优良作风是：理论和实践相结合、和人民群众紧密联系在一起、批评与自我批评[cite: 2]。战胜敌人的三个法宝是：统一战线、武装斗争、党的建设[cite: 2]。

#### 三、 解放战争与新中国成立
* **解放战争进程**：刘邓大军强渡黄河挺进大别山，揭开了战略进攻序幕[cite: 2]。孟良崮战役全歼国民党整编74师[cite: 2]。毛泽东指出人民解放军转入战略反攻是历史的转折点[cite: 2]。1948年底发出“将革命进行到底”的号召[cite: 2]。
* **七届二中全会**：在西柏坡召开，决定了取得全国胜利后的基本政策，告诫全党警惕资产阶级“糖衣炮弹”，因为共产党即将成为执政党[cite: 2]。
* **新中国初期**：
    * **外交方针**：“另起炉灶”、“打扫干净屋子再请客”、“一边倒”[cite: 2]。
    * **第一建交国**：第一个建交的社会主义国家是苏联，西方国家是瑞典[cite: 2]。
    * **法制建设**：1950年颁布的新中国第一部法律是《中华人民共和国婚姻法》[cite: 2]。

#### 四、 改革开放与现代化建设
* **伟大转折**：1978年十一届三中全会果断停止使用“以阶级斗争为纲”口号，把中心转移到经济建设上来，实行改革开放[cite: 2]。
* **特色理论发展**：
    * **十二大**：邓小平明确提出“建设有中国特色的社会主义”[cite: 2]。
    * **十三大**：阐述“一个中心（经济建设为中心）、两个基本点”基本路线[cite: 2]。
    * **十四大**：明确经济体制改革目标是建立社会主义市场经济体制[cite: 2]。
    * **十五大**：把邓小平理论确立为指导思想[cite: 2]。
    * **十六大**：第一次提出全面建设小康社会的奋斗目标[cite: 2]。
* **发展战略**：“三步走”战略第三步是到21世纪中叶，达到中等发达国家水平[cite: 2]。

#### 五、 新时代中国特色社会主义
* **历史方位与本质**：中国特色社会主义进入新时代[cite: 2]。最本质的特征是中国共产党领导[cite: 2]。
* **三大里程碑**：建立中国共产党、成立中华人民共和国、推进改革开放和中国特色社会主义事业[cite: 2]。
* **初心与使命**：为中国人民谋幸福，为中华民族谋复兴[cite: 2]。
* **五位一体**：经济、政治、文化、社会、生态文明建设[cite: 2]。
* **新时代发展方略**：
    * **高质量发展**：全面建设社会主义现代化国家的首要任务[cite: 2]。
    * **三大支撑**：教育、科技、人才是基础性、战略性支撑[cite: 2]。科技是第一生产力、人才是第一资源、创新是第一动力[cite: 2]。
    * **民主与法治**：全过程人民民主是社会主义民主政治的本质属性[cite: 2]。全面依法治国是国家治理的一场深刻革命[cite: 2]。
    * **国家安全**：贯彻总体国家安全观，国家安全是民族复兴的根基[cite: 2]。
    * **祖国统一**：坚持“一国两制”是新时代党解决台湾问题总体方略的根本保证[cite: 2]。

#### 六、 北京师范大学校史专区
* **建校时间**：成立于1902年[cite: 2]。
* **校训**：学为人师、行为世范[cite: 2]。
* **校名题字**：1950年，毛泽东主席应校长林砺儒函请题写校名[cite: 2]。
* **时代楷模**：2013级学生黄文秀，毕业后在广西百色市百坭村担任驻村第一书记，获“七一勋章”[cite: 2]。
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
        st.error(f"找不到文件：{file_path}，请确保它已经上传到了 GitHub。")
        return []

QUESTIONS_DATA = load_questions()

# ================= 3. 会话状态初始化 =================
# 记录错题 ID
if 'wrong_questions' not in st.session_state:
    st.session_state['wrong_questions'] = set()

# 记录刷题模式当前的题目索引 
if 'current_q_index' not in st.session_state:
    st.session_state['current_q_index'] = 0

# 记录当前题目的答题状态，用于显示解析 
if 'show_feedback' not in st.session_state:
    st.session_state['show_feedback'] = False
if 'is_correct' not in st.session_state:
    st.session_state['is_correct'] = False

# ================= 4. 网页全局配置与侧边栏 =================
st.set_page_config(page_title="入党积极分子刷题系统", page_icon="📚", layout="centered")

st.sidebar.title("🚩 学习导航")
page = st.sidebar.radio(
    "请选择功能模块：", 
    ["📖 知识点总结", "📝 刷题模式", "🔍 总题库浏览", "❌ 错题专栏"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：在『刷题模式』中做错的题目会自动加入『错题专栏』。")

# ================= 5. 各页面功能实现 =================

if not QUESTIONS_DATA:
    st.stop()

# 模块 1: 知识点总结
if page == "📖 知识点总结":
    st.title("📖 核心知识点专栏")
    st.markdown(KNOWLEDGE_BASE)

# 模块 2: 刷题模式 (自动下一题版)
elif page == "📝 刷题模式":
    st.title("📝 模拟刷题")
    
    total_q = len(QUESTIONS_DATA)
    current_index = st.session_state['current_q_index']
    
    # 进度提示
    st.progress((current_index + 1) / total_q, text=f"当前进度: {current_index + 1} / {total_q}")
    
    if current_index >= total_q:
        st.success("🎉 恭喜您，已经刷完了所有题目！")
        if st.button("重新开始"):
            st.session_state['current_q_index'] = 0
            st.session_state['show_feedback'] = False
            st.rerun()
    else:
        current_q = QUESTIONS_DATA[current_index]
        
        st.markdown(f"### 第 {current_q['id']} 题")
        st.write(current_q['question'])
        
        # 答题表单
        with st.form(key=f"form_main_{current_q['id']}"):
            user_choice = st.radio("请选择你的答案：", current_q['options'], index=None)
            
            # 如果正在显示反馈，按钮变成“下一题”，否则是“提交答案”
            if st.session_state['show_feedback']:
                submit_btn = st.form_submit_button("下一题 ➡️")
            else:
                submit_btn = st.form_submit_button("提交答案")
            
            if submit_btn:
                # 状态 1：用户点击了“下一题”
                if st.session_state['show_feedback']:
                    st.session_state['current_q_index'] += 1
                    st.session_state['show_feedback'] = False 
                    st.rerun() 
                    
                # 状态 2：用户点击了“提交答案”
                else:
                    if user_choice is None:
                        st.warning("⚠️ 请先选择一个选项！")
                    else:
                        st.session_state['show_feedback'] = True
                        if user_choice == current_q['answer']:
                            st.session_state['is_correct'] = True
                            if current_q['id'] in st.session_state['wrong_questions']:
                                st.session_state['wrong_questions'].remove(current_q['id'])
                        else:
                            st.session_state['is_correct'] = False
                            st.session_state['wrong_questions'].add(current_q['id'])
                        st.rerun() 

        # 显示反馈信息
        if st.session_state['show_feedback']:
            if st.session_state['is_correct']:
                st.success("✅ 回答正确！")
            else:
                st.error("❌ 回答错误！")
                st.info(f"**正确答案是：** {current_q['answer']}")
                st.warning(current_q['explanation'])
            st.write("请点击上方的 **下一题 ➡️** 按钮继续。")

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
        
        wrong_qs = [q for q in QUESTIONS_DATA if q['id'] in st.session_state['wrong_questions']]
        
        for current_q in wrong_qs:
            st.markdown("---")
            st.markdown(f"#### 第 {current_q['id']} 题: {current_q['question']}")
            
            with st.form(key=f"form_wrong_{current_q['id']}"):
                user_choice = st.radio("重新选择：", current_q['options'], index=None, key=f"radio_wrong_{current_q['id']}")
                submit_btn = st.form_submit_button("验证答案")
                
                if submit_btn:
                    if user_choice is None:
                        st.warning("⚠️ 请先选择一个选项！")
                    elif user_choice == current_q['answer']:
                        st.success("✅ 这次选对了！刷新页面或切换模块后，它将从错题本中移除。")
                        st.session_state['wrong_questions'].remove(current_q['id'])
                    else:
                        st.error("❌ 还是选错了，请查看解析加强记忆！")
                        st.info(f"**正确答案是：** {current_q['answer']}")
                        st.warning(current_q['explanation'])
