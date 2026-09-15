# 玩法攻略

Token Plan 40 个实测玩法攻略索引，覆盖 AI Coding、内容创作、资料与数据处理、生活娱乐、求职职场五大场景，每个玩法提供完整的提示词示例和实测产出。

订阅 Token Plan 后，可参见以下 40 个玩法快速上手。每个玩法提供完整的提示词示例和实测产出，具体产出效果与 Credits 消耗以控制台「用量详情」为准。

## 分类速览

分类

玩法数

能力定位

AI Coding / 开发

11

一套 AI 能力打通从架构调研到系统交付全链路。改旧码、建新应用、审安全，开启智能编程新体验。

自媒体 / 内容创作

8

一套 AI 能力打通从图文策划到动态呈现全流程。会写稿、能配音、可动图，开启高效内容生产新体验。

资料与数据处理

10

一组多模态能力解决从文档/表格/数据库到业务洞察转化难题。文转表、图读数、语查库，定义新一代数据引擎。

生活娱乐

6

一套 AI 能力打通从记忆修复到日常守护全流程。会规划、能陪伴、懂关怀，开启有温度的智能生活新体验。

求职职场

5

一套 AI 能力打通从简历优化到教学互动全流程。改简历、练面试、出图纸、做日报、讲题目，开启高效自我发展新体验。

## 玩法总表

分类

场景

说明

攻略

AI Coding / 开发

AI Coding · 给现有系统加功能

一句话描述需求，AI 读入现有代码增量加功能不动老逻辑。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md)

AI Coding / 开发

Qoder 搭个人小工具

在 Qoder 里对话式搭记账、单词卡等个人小应用，零基础也能上手。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-qoder-tool.md)

AI Coding / 开发

一句话生成可玩小游戏

一句话描述玩法，模型直接生成可运行的单文件小游戏，打开即玩。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-mini-game.md)

AI Coding / 开发

AI 代码安全审计 · 定位到修复

把代码交给模型做安全审计，逐条给出漏洞、风险等级与可替换的修复代码。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)

AI Coding / 开发

文档驱动开发 · 一份文档换一个系统

写一份《技术文档》讲清功能与验收标准，模型一次性交付可运行系统，门槛从会写代码变成会写需求。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md)

AI Coding / 开发

代码调研 · 摸清陌生项目架构

两轮法读懂大型仓库：先喂骨架出架构地图，再按点名文件补全文出调用链。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)

AI Coding / 开发

界面体检 · 截图挑毛病

把界面截图交给视觉理解模型，按四个维度逐项挑刺并打分；页面报错、图片加载不出来也可截图配代码一起定位。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md)

AI Coding / 开发

截图变代码 · 数据看板照结构还原

上传数据看板截图，Qwen3.8-flash 视觉理解照结构还原，图表用纯 CSS 绘制、数字照抄，产出零外部依赖的单文件 HTML。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-screenshot-to-code.md)

AI Coding / 开发

命令预检 · 执行前先过一道风险检查

输入待执行的命令清单，模型逐条判风险等级、给放行或拦截建议与更安全的替代写法，输出固定 5 字段 JSON。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)

AI Coding / 开发

提交信息 · 一上午的改动自动拆 commit

输入未提交的 git diff，模型自动拆成多条 commit，写出符合 Conventional Commits 的标题正文并标注破坏性改动。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-commit-writer.md)

AI Coding / 开发

代码评审 · PR 合并前先过一遍 diff

输入本次 PR diff，模型给出能不能合的结论与 blocking / suggestion / nit 三级意见，每条附具体后果与改法。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)

自媒体 / 内容创作

儿童趣味动物视频生成

一个动物词生成儿童童话与三拍脚本，再文生视频出 5 秒动画。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-kids-animal-video.md)

自媒体 / 内容创作

睡前故事配音

语音合成模型把童话文本念成温柔人声，输出睡前故事音频。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)

自媒体 / 内容创作

个人 IP 头像 / 表情包

一句话描述形象，文生图出头像，再用参考图编辑出角色一致的表情包。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)

自媒体 / 内容创作

小红书封面图 / 文案一次出

文本模型写标题正文与标签，文生图出竖版封面并把标题渲染进画面。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-redbook-cover.md)

自媒体 / 内容创作

短剧脚本 · 把干货稿改成能拍的分镜

深度思考模型把干货稿改成 60 秒口播脚本，按 JSON 逐镜输出。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-drama-script.md)

自媒体 / 内容创作

商品图变展示视频 · 静图秒变主图短视频

一张商品图，让产品不动、只有光影流转，生成主图展示短视频。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)

自媒体 / 内容创作

让人物动起来 · 图生视频精准控运动

把运动写成可测量的数字，让图生视频真正走位而不原地踏步。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)

自媒体 / 内容创作

人物一致性换装组照

把身份锁定写在第一句，只让模型改服装场景，批量出同一个人的不同造型。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)

资料与数据处理

表格分析 · 脏数据出结论

不把整表塞给模型，只发表头与样本让它写清洗分析脚本，数据留在本地跑。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)

资料与数据处理

网页提数 · 指定字段抓成表

网页抓取工具拿正文全文，按指定字段对齐成表，比联网搜索更老实。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)

资料与数据处理

合同体检 · 挑出对我不利的条款

让模型把关联条款串起来看，挑出对己方不利的组合型风险。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)

资料与数据处理

票据 / 文档识别归档

视觉理解读图，OCR 提取字段成 JSON 并给出归档文件名。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md)

资料与数据处理

跨境选品 · 识图定价

识图认商品，再算利润、做合规质检，识图与推理串成一条链。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-cross-border.md)

资料与数据处理

长文 / 论文 / 合同秒读问答

长上下文吃下整篇文档，先出中文速读再逐条追问回原文。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)

资料与数据处理

个人知识库问答 · RAG 三段式

把公司制度、个人笔记做成能问的知识库，用大白话就能问出正确那一条。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-knowledge-rag.md)

资料与数据处理

周报汇总 · 五封邮件汇成四列进度表

输入五封成员汇报邮件，模型按成员、任务、进度、风险四列汇总成一张进度表，并挑出原文没明说的阻塞。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)

资料与数据处理

长图变数据 · 促销图抽字段 + 文案风险初筛

上传促销长图，模型视觉理解抽出商品、价格、券与规则字段，输出固定字段 JSON，并对图上文案做一遍投放前的风险初筛。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)

资料与数据处理

视频摘要 · 按时间线拆片段

上传视频，模型视觉理解按时间线拆成片段并逐段摘要，附时间戳、总体摘要与片段数量统计。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-video-digest.md)

生活娱乐

老照片修复上色 / 证件照换装

用参考图编辑去划痕、上色、换装，人物长相保持不变。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)

生活娱乐

OpenClaw 个人任务管家

一句话交办，OpenClaw 自动编排文本、图片生成与联网搜索，端到端办成一件事。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)

生活娱乐

一句话规划周末出游 · 多步 Agent

一句话交办，模型一次调用里自主编排联网、算账、排程，跑完多步出游规划。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)

生活娱乐

父母用药管家 · 服药 / 开药双提醒

把真实困境连同界面要求一起写进提示词，模型产出一个能长期用的用药管家网页。

[查看攻略](https://help.aliyun.com/zh/model-studio/token-plan-playbook-med-reminder)

生活娱乐

居家安全 · 拍张照排查隐患

给家里拍张照交给视觉理解模型，连空间关系一起看，三段式排查隐患。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md)

生活娱乐

时光影像信

把零散心里话润色成信、念成语音、配上会动的分镜，合成一支短片。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-photo-letter.md)

求职职场

简历诊断 · 按 JD 改写

对着 JD 先诊断简历差距，再用 STAR 法则重写经历。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)

求职职场

AI 面试教练 · 出题追问打分

模型扮演面试官出题、追问、打分，帮你逐轮复盘提分。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-interview-coach.md)

求职职场

三维 CAD 建模 · 出 STEP/STL 文件

一句话描述零件，模型生成建模脚本，本地 CAD 内核执行后产出 STEP/STL 文件。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md)

求职职场

教育社群故事化群日报

文本模型把群聊素材转成 story.json，本地离线渲染成 HTML 与 PNG 长图。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-group-daily-report.md)

求职职场

交互式教育解题 · 一题变讲解网页

一道题变成分步讲解 + 可拖动验证的单文件交互网页。

[查看攻略](raw/model-user-guide/token-plan-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)
