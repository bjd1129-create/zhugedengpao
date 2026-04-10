"""
CrewAI 核心调度器 (诸葛家班 V4.0 - Full Skills)
"""

from config.agents import (
    create_dahua,
    create_tanzhang,
    create_xiucai,
    create_qiaojiang,
    create_zhanggui
)
from crewai import Crew, Process, Task

SKILLS_BASE = "/Users/bjd/Desktop/ZhugeDengpao-Team/skills"


def create_daily_ops_crew(topic=None):
    """
    日常运营 Crew:
    探长发现信号 (github-ai-trends / arxiv-watcher) 
      → 秀才产出内容 (content-factory / content-repurposer)
        → 掌柜整理日志
          → 大花审批发布
    """
    # Agents
    tanzhang = create_tanzhang()
    xiucai = create_xiucai()
    zhanggui = create_zhanggui()
    dahua = create_dahua()

    # 默认话题
    search_topic = topic or "AI agents automation 2026"

    # Tasks
    task_tanzhang = Task(
        description=f"""
        你是探长，执行以下情报扫描任务：
        
        1. 扫描 GitHub AI 趋势：
           运行: python3 {SKILLS_BASE}/github-ai-trends/scripts/fetch_trends.py --period weekly --limit 15
           提取最火的 AI 项目。
        
        2. 扫描 ArXiv 最新论文：
           运行: bash {SKILLS_BASE}/arxiv-watcher/scripts/search_arxiv.sh '{search_topic}'
           找出最有价值的论文摘要。
        
        3. 扫描 GitHub 热门项目：
           运行: python3 {SKILLS_BASE}/github-trending-cn/scripts/github_trending.py --period daily --limit 10
        
        输出：
        - 3 个值得跟进的"情报点"（标题、热度预测、推荐理由、数据来源）。
        - 附原始数据摘要。
        """,
        expected_output="包含 3 个情报点的 Markdown 简报（含数据支持）。",
        agent=tanzhang
    )

    task_xiucai = Task(
        description="""
        你是秀才，基于探长的情报完成内容生产：
        
        1. 阅读 {SKILLS_BASE}/content-factory/prompts/first-draft.md 的写作模板。
        2. 用探长的情报写一篇短博文/公众号文章。
        3. 要求：口语化，吸引人，标题党但内容真实，说人话。
        4. 写完后，用 content-repurposer 技能生成 Twitter 和 LinkedIn 版本。
           运行: bash {SKILLS_BASE}/content-repurposer/scripts/twitter-thread.sh <文章路径>
           运行: bash {SKILLS_BASE}/content-repurposer/scripts/linkedin-post.sh <文章路径>
        
        输出：
        - 完整博文（含标题）
        - Twitter Thread（6-10 条推文）
        - LinkedIn 帖子
        """.replace("{SKILLS_BASE}", SKILLS_BASE),
        expected_output="一篇完整博文 + Twitter Thread + LinkedIn 帖子。",
        agent=xiucai,
        context=[task_tanzhang]
    )

    task_zhanggui = Task(
        description="""
        你是掌柜，为今天的办公室写一篇"工作日志" (JSON格式)。
        
        记录：
        1. 探长发现了什么情报。
        2. 秀才写了什么内容。
        3. 团队的心情指数 (1-10)。
        4. 当前状态：Busy / Resting / Thinking。
        
        格式示例：
        ```json
        {{
          "date": "YYYY-MM-DD",
          "mood": 8,
          "team_status": "Busy",
          "agents": [
            {{"role": "探长", "status": "Resting", "summary": "Scanned GitHub trends..."}},
            {{"role": "秀才", "status": "Resting", "summary": "Wrote a viral post about AI."}},
            {{"role": "大花", "status": "Thinking", "summary": "Reviewing content pipeline."}}
          ],
          "latest_content": {{
            "title": "...",
            "platforms": ["twitter", "linkedin"]
          }}
        }}
        ```
        """,
        expected_output="包含团队日志的 JSON 代码块。",
        agent=zhanggui,
        context=[task_tanzhang, task_xiucai]
    )

    task_dahua = Task(
        description="""
        你是大花，做最终审批：
        
        1. 审核秀才的文章和社交平台版本。
        2. 批准发布或打回修改（说明理由）。
        3. 签发今日公司指令。
        4. 把掌柜的 JSON 日志输出为最终结果。
        """,
        expected_output="审批意见 + 最终确认的日志 JSON。",
        agent=dahua,
        context=[task_tanzhang, task_xiucai, task_zhanggui]
    )

    crew = Crew(
        agents=[tanzhang, xiucai, zhanggui, dahua],
        tasks=[task_tanzhang, task_xiucai, task_zhanggui, task_dahua],
        process=Process.sequential,
        memory=False,
        cache=False,
    )
    return crew


def create_developer_crew(requirement=None):
    """
    开发 Crew:
    需求 → 巧匠写代码 (frontend-dev / bailian-image-gen / canvas-design)
         → 掌柜记录
    """
    qiaojiang = create_qiaojiang()
    zhanggui = create_zhanggui()

    dev_req = requirement or "根据用户需求编写完整代码。"

    task_qiaojiang = Task(
        description=f"""
        你是巧匠，完成以下开发任务：
        
        {dev_req}
        
        技能调用指南：
        - 前端页面：参考 {SKILLS_BASE}/frontend-dev/SKILL.md，按 Phase 1-6 流程执行。
        - 图片生成：运行 python3 {SKILLS_BASE}/bailian-image-gen/scripts/bailian_image_gen.py --mode t2i --prompt "..." --output xxx.png
        - 设计海报：参考 {SKILLS_BASE}/canvas-design/SKILL.md，先写设计哲学 .md，再生成 PDF/PNG。
        
        核心要求：
        1. 代码完整可运行，不要片段。
        2. 真实资产，不用占位符 URL。
        3. 中文注释，清晰易懂。
        """,
        expected_output="完整的代码文件路径 + 代码内容 + 使用说明。",
        agent=qiaojiang
    )

    task_zhanggui = Task(
        description="将巧匠的开发成果记录到办公室日志中。输出 JSON 格式。",
        expected_output="日志记录 (JSON)。",
        agent=zhanggui,
        context=[task_qiaojiang]
    )

    crew = Crew(
        agents=[qiaojiang, zhanggui],
        tasks=[task_qiaojiang, task_zhanggui],
        process=Process.sequential,
    )
    return crew


def create_content_factory_crew(source_content=None):
    """
    内容工厂 Crew（专门使用 content-factory + content-repurposer）：
    Writer → Editor → Remixer → Headline Machine
    """
    xiucai = create_xiucai()
    zhanggui = create_zhanggui()

    source = source_content or "用户提供的内容或话题。"

    task_writer = Task(
        description=f"""
        使用 Content Factory 技能完成内容生产：
        
        1. 阅读 {SKILLS_BASE}/content-factory/prompts/first-draft.md
        2. 基于话题写初稿
        3. 阅读 {SKILLS_BASE}/content-factory/prompts/polish-pass.md 做润色
        4. 阅读 {SKILLS_BASE}/content-factory/prompts/headlines.md 生成 20 个标题
        5. 运行 content-repurposer 生成多平台版本
        
        源内容：{source}
        """,
        expected_output="完整文章 + 20 个标题 + 多平台适配版本。",
        agent=xiucai
    )

    task_zhanggui = Task(
        description="记录内容产出到日志。",
        expected_output="JSON 日志。",
        agent=zhanggui,
        context=[task_writer]
    )

    crew = Crew(
        agents=[xiucai, zhanggui],
        tasks=[task_writer, task_zhanggui],
        process=Process.sequential,
    )
    return crew


def create_crew(crew_type: str, **kwargs):
    """
    任务路由: 兼容 main.py 的 create_crew(task_type, **params)
    """
    if crew_type in ["content", "daily_ops", "research"]:
        topic = kwargs.get("topic", kwargs.get("query", kwargs.get("task_description", None)))
        return create_daily_ops_crew(topic=topic)
    elif crew_type in ["developer", "code"]:
        requirement = kwargs.get("requirement", kwargs.get("prompt", kwargs.get("task_description", None)))
        return create_developer_crew(requirement=requirement)
    elif crew_type in ["content_factory", "repurpose"]:
        source = kwargs.get("source", kwargs.get("content", None))
        return create_content_factory_crew(source_content=source)
    else:
        raise ValueError(f"不支持的 Crew 类型: {crew_type}")
