import streamlit as st
import json
import os

# ================= 1. 核心知识库 (详细总结版) =================
KNOWLEDGE_BASE = """
一、党的重要会议（核心必背）
 
1. 中共二大：通过第一部《中国共产党章程》
​
2. 中共三大：广州召开，确定国共合作方针
​
3. 中共四大：中央执行委员会“委员长”改称总书记
​
4. 中共七大：确立毛泽东思想为党的指导思想；概括三大作风（理论联系实际、密切联系群众、批评与自我批评）
​
5. 中共八大：宣布社会主义改造胜利；我国国内主要矛盾：人民对于建立先进工业国的要求同落后农业国现实之间的矛盾、人民对于经济文化迅速发展的需要同当前经济文化不能满足人民需要的状况之间的矛盾
​
6. 十一届三中全会：1978年，党和国家工作中心转移到经济建设，实行改革开放
​
7. 中共十二大：邓小平在开幕词提出“建设有中国特色的社会主义”
​
8. 中共十三大：“一个中心、两个基本点”，以经济建设为中心
​
9. 中共十四大：经济体制改革目标——社会主义市场经济体制
​
10. 中共十五大：把邓小平理论写入党章
​
11. 中共十六大：首次提出全面建设小康社会
​
12. 中共二十大：向第二个百年奋斗目标进军；大会主题：自信自强、守正创新，踔厉奋发、勇毅前行
 
 
 
二、近代历史与建党初期
 
1. 鸦片战争：中国近代史开端，国门洞开
​
2. 英法联军火烧圆明园：“抢劫可以，纵火不行”
​
3. 甲午战败：根源是清朝封建制度腐朽
​
4. 第一个共产党早期组织：1920年8月，上海
​
5. 十月革命宣传第一人：李大钊
​
6. 最早提出“中国共产党”名称：蔡和森
​
7. 第一次国共合作政治基础：联俄、联共、扶助农工
​
8. 南昌起义：打响武装反抗国民党反动派第一枪
​
9. 三湾改编：确立党对军队绝对领导；支部建在连上
​
10. 九一八事变：1931年，日本侵华开端
​
11. 湘江战役：长征途中最壮烈一战
​
12. 遵义会议：中共第一次独立自主运用马克思主义；选举毛泽东为中央政治局常委
​
13. 长征胜利结束：红军三大主力会宁会师；中央红军跨越12省
​
14. 《西行漫记》：埃德加·斯诺访问陕北后著作
 
 
 
三、抗日战争时期
 
1. 八一宣言：口号停止内战，一致抗日
​
2. 平型关大捷：抗战以来首次大捷
​
3. 新四军军长：叶挺
​
4. 三大法宝：统一战线、武装斗争、党的建设
​
5. 首次提出“毛泽东思想”：王稼祥
​
6. 百团大战：彭德怀指挥
​
7. 皖南事变后：陈毅任新四军代理军长
​
8. 南泥湾大生产：八路军第三五九旅开发
​
9. 毛泽东题词：自己动手，丰衣足食
​
10. 重庆谈判：目的争取和平民主
 
 
 
四、解放战争时期
 
1. 孟良崮战役：全歼国民党整编74师
​
2. 刘邓大军挺进大别山：揭开战略进攻序幕
​
3. 七届二中全会：西柏坡召开；警惕资产阶级“糖衣炮弹”
​
4. 1949年新年献词：毛泽东发出将革命进行到底伟大号召
 
 
 
五、新中国成立与社会主义建设
 
1. 新中国成立：中国人民从此站起来了
​
2. 三大外交方针：另起炉灶、打扫干净屋子再请客、一边倒
​
3. 首个与新中国建交的社会主义国家：苏联
​
4. 首个与新中国建交的西方国家：瑞典
​
5. 新中国第一部法律：《中华人民共和国婚姻法》
​
6. 第一届全国人大：刘少奇当选全国人大常委会委员长
​
7. 十大元帅：不包括粟裕
​
8. 1964年：我国第一颗原子弹爆炸成功
​
9. 1971年：恢复联合国合法席位，关键靠亚非拉国家
​
10. 十一届六中全会：通过《关于建国以来党的若干历史问题的决议》，完成指导思想拨乱反正
 
 
 
六、改革开放新时期
 
1. 两个“春天”：1979年建立经济特区、1992年邓小平南方谈话（解决姓“资”姓“社”问题）
​
2. 停止使用口号：以阶级斗争为纲
​
3. 三步走战略：21世纪中叶达到中等发达国家水平
​
4. 香港回归：1997年7月1日
​
5. 神舟一号：1999年，我国首艘载人航天试验飞船
​
6. “三个代表”重要思想：首次提出于广东高州
​
7. 全面建设小康目标：2020年GDP比2000年翻两番
​
8. 北京奥运会口号：同一个世界、同一个梦想
​
9. 近代三大里程碑：建立中国共产党、成立中华人民共和国、推进改革开放和中国特色社会主义事业
 
 
 
七、新时代（十八大—二十大）核心考点
 
1. 中国共产党人初心和使命：为中国人民谋幸福，为中华民族谋复兴
​
2. 中国特色社会主义最本质特征：中国共产党领导
​
3. “一带一路”：新丝绸之路经济带和21世纪海上丝绸之路
​
4. 精准扶贫：首次在湖南湘西提出
​
5. 国家纪念日：9月3日中国人民抗日战争胜利纪念日；12月13日南京大屠杀死难者国家公祭日
​
6. “五位一体”总体布局：经济建设、政治建设、文化建设、社会建设、生态文明建设
​
7. 新发展理念：创新、协调、绿色、开放、共享
​
8. 总体国家安全观：维护国家主权、安全、发展利益
​
9. 中国式现代化：中国共产党领导的社会主义现代化
​
10. 全面建设社会主义现代化国家首要任务：高质量发展
​
11. 基础性、战略性支撑：教育、科技、人才
​
12. 科技是第一生产力、人才是第一资源、创新是第一动力
​
13. 社会主义民主政治本质属性：全过程人民民主
​
14. 全面依法治国核心：以宪法为核心
​
15. 更基本、更深沉、更持久的力量：文化自信
​
16. 民族复兴的根基：国家安全
​
17. 党对军队的根本原则：绝对领导
​
18. “一国两制”：香港、澳门回归后保持长期繁荣稳定的最佳制度安排
​
19. 中国外交宗旨：推动构建人类命运共同体
​
20. 跳出治乱兴衰历史周期率第二个答案：自我革命
​
21. 三个务必：不忘初心、牢记使命；谦虚谨慎、艰苦奋斗；敢于斗争、善于斗争
​
22. 新时代三件大事：迎来中国共产党成立一百周年；中国特色社会主义进入新时代；完成脱贫攻坚、全面建成小康社会历史任务
​
23. 马克思主义中国化时代化：同中国具体实际、中华优秀传统文化相结合
​
24. 六个必须坚持：人民至上、自信自立、守正创新、问题导向、系统观念、胸怀天下
 
 
 
八、党章与党务基础
 
1. 现行党章：党的二十大修订，除总纲外共11章
​
2. 党的最高理想和最终目标：实现共产主义
​
3. “三会一课”：支部党员大会、党支部委员会、党小组会、党课
​
4. 基层党组织定位：坚强战斗堡垒
​
5. 政治三力：政治判断力、政治领悟力、政治执行力
​
6. 党的群众路线：从群众中来，到群众中去
​
7. 两个永远在路上：全面从严治党永远在路上；党的自我革命永远在路上
​
8. 意识形态工作领导权：党牢牢掌握
 
 
 
九、北京师范大学校情校史（必考）
 
1. 建校时间：1902年
​
2. 校训：学为人师，行为世范
​
3. 校名题写：毛泽东为校长林砺儒题写
​
4. 优师计划：习近平总书记回信勉励北师大师范生
​
5. 黄文秀：北师大校友，广西百色市百坭村驻村第一书记
​
6. 支持港澳融入国家发展大局：党的十九大正式提出
 
 
 
十、高频易混考点速记
 
- 指导思想：七大—毛泽东思想；十五大—邓小平理论；十六大—“三个代表”重要思想；十八大—科学发展观；十九大—习近平新时代中国特色社会主义思想
​
- 军队领导：三湾改编确立党对军队绝对领导，支部建在连上
​
- 历史周期率：第一个答案人民监督；第二个答案自我革命
​
- 民主相关：本质属性全过程人民民主；本质特征人民当家作主
​
- 发展定位：高质量发展是首要任务；发展是党执政兴国第一要务
​
- 根基定位：国家安全是民族复兴根基；文化自信是更基本、更深沉、更持久力量
 
 
 
十一、高频填空/单选核心句
 
1. 党的二大通过了第一部《中国共产党章程》。
​
2. 党的七大确立毛泽东思想为党的指导思想。
​
3. 十一届三中全会作出改革开放历史性决策。
​
4. 中国共产党人的初心和使命是为中国人民谋幸福，为中华民族谋复兴。
​
5. 中国特色社会主义最本质的特征是中国共产党领导。
​
6. 全面建设社会主义现代化国家的首要任务是高质量发展。
​
7. 教育、科技、人才是全面建设社会主义现代化国家的基础性、战略性支撑。
​
8. 全过程人民民主是社会主义民主政治的本质属性。
​
9. 国家安全是民族复兴的根基。
​
10. 北师大校训：学为人师，行为世范。
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
