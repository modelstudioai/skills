# token plan playbooks

`token plan playbooks` 是一套面向开发者、基于具体任务场景的端到端实践指南集合，覆盖 AI Coding、内容创作、数据处理、生活娱乐、求职职场等 5 大类共 47 个可复用的“玩法”（playbook）。每个 playbook 明确定义输入（如截图、diff、合同全文）、调用模型、关键参数、输出格式及典型消耗模式，强调“不塞全量数据、只喂必要信息”的高效 token 使用原则。所有 playbook 均经实测验证，产出可直接运行或上线。

## 支持的模型/功能

`token plan playbooks` 适配多模态与多能力模型，按任务类型严格选型：

- **文本生成与深度推理**：`qwen3.8-max`（用于文档驱动开发、合同体检、三维 CAD 建模等需长上下文与强逻辑的任务）；`qwen3.7-plus`（用于表格分析、网页提数、RAG 查询改写等中等复杂度任务）；`qwen3.8-flash`（用于命令预检、提交信息、PR 评审等低延迟、高吞吐场景，[原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md) 明确要求 `enable_thinking: false`）。
- **视觉理解**：`qwen3.7-plus`（用于界面体检、票据 OCR、居家安全排查等需图文联合分析的场景）；`qwen3.8-flash`（用于促销图字段抽取、视频摘要等对结构化输出稳定性要求高的视觉任务，[原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md) 要求关闭思考以保障 JSON 字段准确率）。
- **文生图与图生图**：`wan2.7-image`（用于 IP 头像生成、证件照换装、商品图生成等，[原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md) 强调参考图编辑时“身份锁定”必须置于提示词首句）。
- **文生视频与图生视频**：`wan3.0-video`（用于电影级空镜、虚拟代言人等长视频生成）；`happyhorse-1.1-i2v`（用于商品图变视频、人物走位控制等需精准运动约束的场景）。
- **语音合成**：`qwen-audio-3.0-tts-plus`（用于睡前故事配音、影像信语音等，需先创建音色 ID）。

> **注意**：文档 14 中提及 `wan3.0-video`，但文档 33 的虚拟代言人流程实际调用的是 `wan3.0-video`（first_frame 模式），而文档 34 的儿童动画使用的是 `happyhorse-1.1-t2v`。三者模型名、形态与适用场景不同，不可混用。

## 关键参数

Playbook 的有效性高度依赖参数配置，核心参数如下：

- **`enable_thinking`**：对 `qwen3.8-flash` 类低延迟模型，**必须显式设为 `false`**（如 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md) 所示），否则响应时间显著增加，破坏预检环节的实时性。
- **分辨率与尺寸**：图像/视频任务中，**优先使用最小必要尺寸**。例如界面体检用常规网页截图（非超大图），商品图变视频推荐 720P/5 秒起步，避免无谓 token 消耗。
- **输出格式约束**：所有结构化输出（JSON）必须严格限定字段。例如命令预检要求固定 5 字段（`cmd`, `level`, `action`, `reason`, `safer`），PR 评审要求 `blocking/suggestion/nit` 三级 severity，任何偏差将导致下游自动化流程失败。
- **水印控制**：视频与图像生成默认带“AI 生成”水印，生产环境必须添加 `--watermark false` 参数（见 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md) 和 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)）。

## 使用方式

所有 playbook 遵循统一的三步法，强调“最小输入、最大产出”：

1. **准备最小必要输入**：绝不上传原始敏感数据。代码审计前需脱敏密钥；合同评审前应移除真实客户名称；票据 OCR 应遮挡税号等字段。对于大文件（如 1.5 万行代码），采用骨架法（仅传函数签名与 docstring）先行定位关键文件，再补全文（见 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)）。
2. **构造精确指令**：指令需包含明确的输出格式（如 JSON Schema）、行为边界（如“主体全静，只让光影动”、“身份锁定写在第一句”）和禁止项（如“不要编造数字”、“不要臆造类名”）。模糊描述（如“优化一下”）会导致不可控输出。
3. **本地后处理与验证**：Playbook 输出常需本地校验。例如 RAG 脚本需 `assert` 自检召回正确性；CAD 建模脚本需本地执行并比对体积；视频摘要的时间戳仅适用于粗略定位，不可替代专业剪辑点。

## 限制和注意事项

- **[Token](../concepts/token.md) 消耗主因**：输入侧消耗远高于输出侧。图片/视频转为 `image_tokens` 占比最高；长文本（如 6,800 字合同）进上下文是主要成本来源；而纯文本生成（如 commit 信息）消耗相对可控。
- **模型能力边界**：
  - 视觉模型在精确计数（如“画面中有几种颜色”）和文字识别（尤其带 logo 的包装）上易出错，其输出应作为线索而非结论（见 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md)）。
  - `qwen3.8-flash` 在需要深度推理的任务（如合同组合风险分析）上表现弱于 `qwen3.8-max`，应按任务复杂度分级选用（见 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)）。
- **安全与合规**：
  - **绝不上传生产密钥、内网地址、客户 PII 数据**。所有示例均强调“脱敏后再提交”，真实密钥请替换为占位符（如 `API_KEY=sk-xxx` → `API_KEY=<REDACTED>`）。
  - 人物一致性换装、老照片修复等涉及真人图像的场景，**必须获得本人明确授权**，且不得用于伪造身份或误导性宣传（见 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)）。
- **效果免责**：所有 playbook 文档均含标准免责声明——“本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台‘用量详情’为准”。

## 来源文档

- [AI Coding / 开发](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding.md)
- [AI Coding · 给现有系统加功能](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md)
- [Qoder 搭个人小工具](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-qoder-tool.md)
- [一句话生成可玩小游戏](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-mini-game.md)
- [AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)
- [文档驱动开发 · 一份文档换一个系统](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md)
- [代码调研 · 摸清陌生项目架构](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)
- [界面体检 · 截图挑毛病与定位报错](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md)
- [截图变代码 · 数据看板照结构还原](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-screenshot-to-code.md)
- [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)
- [提交信息 · 一上午的改动自动拆 commit](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-commit-writer.md)
- [代码评审 · PR 合并前先过一遍 diff](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)
- [自媒体 / 内容创作](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content.md)
- [电影级空镜短片 · 一条提示词出 30 秒 1080P 素材](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)
- [睡前故事配音](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)
- [个人 IP 头像 / 表情包](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)
- [小红书封面图 / 文案一次出](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-redbook-cover.md)
- [短剧脚本 · 把干货稿改成能拍的分镜](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-drama-script.md)
- [商品图变展示视频 · 静图秒变主图短视频](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)
- [让人物动起来 · 图生视频精准控运动](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)
- [人物一致性换装组照 · 锁住这张脸，只换衣服和场景](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)
- [资料与数据处理](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data.md)
- [表格分析 · 脏数据出结论](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)
- [网页提数 · 指定字段抓成表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)
- [票据 / 文档识别归档](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md)
- [合同体检 · 挑出对我不利的条款](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)
- [跨境选品 · 识图定价](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-cross-border.md)
- [长文 / 论文 / 合同秒读问答](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)
- [个人知识库问答 · RAG 三段式](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-knowledge-rag.md)
- [长图变数据 · 促销图抽字段 + 文案风险初筛](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)
- [视频摘要 · 按时间线拆片段](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-video-digest.md)
- [生活娱乐](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life.md)
- [品牌虚拟代言人 · 一张形象图出 15 秒口播成片](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)
- [儿童趣味动物视频生成](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-kids-animal-video.md)
- [老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)
- [OpenClaw 个人任务管家](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)
- [一句话规划周末出游 · 多步 Agent](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)
- [父母用药管家 · 服药 / 开药双提醒](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-med-reminder.md)
- [时光影像信 · 把想说的话做成会动、能听的一封信](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-photo-letter.md)
- [求职职场](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career.md)
- [周报汇总 · 五封邮件汇成四列进度表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)
- [简历诊断 · 按 JD 改写](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)
- [AI 面试教练 · 出题追问打分](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-interview-coach.md)
- [三维 CAD 建模 · 出 STEP/STL 文件](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md)
- [教育社群故事化群日报](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-group-daily-report.md)
- [居家安全 · 拍张照排查隐患](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md)
- [交互式教育解题 · 一题变讲解网页](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)


