# token plan playbooks

`token plan playbooks` 是一套面向开发者、开箱即用的 AI 应用实践模式集合，覆盖编码、内容创作、数据处理、生活娱乐、求职职场等场景。每个 playbook 提供明确的目标、可复现的步骤、对应模型与关键参数，并经过实测验证。它不替代工程规范，而是聚焦“如何用最少的上下文、最稳的模型组合，把一个具体任务一次跑通”。

## 支持的模型/功能

Playbook 覆盖多模态能力，按任务类型匹配专用模型：

- **文本生成与推理**：`qwen3.7-plus`（通用、高性价比）、`qwen3.8-max`（深度思考、长上下文、复杂逻辑）、`qwen3.8-flash`（低延迟、高吞吐，适合预检/汇总类任务）  
- **视觉理解**：`qwen3.7-plus`（图文混合理解，如界面体检、票据 OCR）、`qwen3.8-flash`（高速视觉解析，如促销图抽字段、视频摘要）  
- **文生图**：`wan2.7-image`（高质量、强可控性，支持参考图编辑）  
- **文生视频 / 图生视频**：`wan3.0-video`（电影级长片）、`happyhorse-1.1-t2v`（儿童动画）、`happyhorse-1.1-i2v`（商品光影/人物走位）  
- **语音合成**：`qwen-audio-3.0-tts-plus`（情感化人声）、`cosyvoice-v3-flash`（系统音色直出）  
- **代码与结构化输出**：所有文本模型均支持 JSON Schema 输出，但需在指令中**显式声明结构**并关闭思考（如 `enable_thinking: false`）以保障字段稳定性，详见 [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)。

> **注意**：文档 13 中提及 `wan3.0-video` 用于电影级空镜，但文档 34 中同一模型被用于品牌口播成片（first_frame 模式）。二者调用方式与参数差异显著：前者为纯文生视频（无首帧），后者依赖首帧图驱动。实际使用时必须严格区分输入形态，不可混用提示词模板。

## 关键参数

Playbook 的稳定性高度依赖参数控制，核心参数如下：

- `enable_thinking: false`：对预检、命令审核、PR 评审等需确定性输出的场景**必须关闭思考**，否则 JSON 字段可能缺失或错乱。该参数在 OpenAI 兼容模式下置于请求体顶层，见 [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md) 示例。  
- `--watermark false`：对 `wan2.7-image` 和 `wan3.0-video` 等图像/视频模型，**必须显式关闭水印**，否则首帧图带水印将导致视频成片叠加双水印，见 [品牌虚拟代言人 · 一张形象图出 15 秒口播成片](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)。  
- `duration` 与 `resolution`：视频类任务（如 `wan3.0-video`, `happyhorse-1.1-t2v`）必须明确指定 `duration`（秒）和 `resolution`（如 `1080P`, `720P`），未指定时默认值可能导致成本激增或产出不符预期。  
- `web_extractor` 与 `code_interpreter`：多步 Agent 类任务（如 [一句话规划周末出游 · 多步 Agent](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)）需在工具链中**显式启用对应插件**，否则联网或计算能力不可用。

## 使用方式

Playbook 遵循“最小可行输入”原则，典型流程为三步：

1. **准备输入素材**：仅提供必要信息。例如代码调研只需签名骨架而非全量代码；合同体检直接传入全文而非摘要；促销图分析上传原始 base64 图片而非截图描述。  
2. **构建结构化指令**：明确指定输出格式（如 JSON Schema）、约束条件（如“只输出最终版”、“不要解释”）和关键要求（如“身份锁定写在第一句”、“主体全静、只让光影动”）。指令质量直接决定产出稳定性。  
3. **执行与验证**：优先用小规格试跑（如 5 秒视频、720P 分辨率、单文件代码），确认逻辑成立后再扩展。对关键输出（如 CAD 体积、JSON 字段）应进行本地校验，见 [三维 CAD 建模 · 出 STEP/STL 文件](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md) 中的体积零误差验证。

## 限制和注意事项

- **输入侧消耗主导成本**：视觉（图片/视频 base64）、长文本（论文/合同）、大代码库（全量 diff）会显著增加输入 tokens，是主要计费来源。推荐策略：代码调研用 AST 骨架（文档 7）、数据处理只传样本（文档 22）、视频任务先用 5 秒验证。  
- **模型能力边界明确**：`qwen3.7-plus` 可完成 OCR 与基础视觉理解，但复杂运动控制（如人物走位）必须用 `happyhorse-1.1-i2v` 并配合数字约束（文档 20）；`qwen3.8-flash` 不适合需要深度推理的任务（如文档驱动开发需 `qwen3.8-max`，见文档 6）。  
- **隐私与合规红线**：真实密钥、内网地址、客户数据**严禁直接提交**，须替换为占位符（文档 5）；真人照片换装需获本人授权（文档 21）；医疗/金融等专业领域产出**仅作提醒，不替代专业判断**（文档 37、38）。  
- **输出非绝对可靠**：所有 playbook 均标注“免责声明”，产出效果与 Credits 消耗以控制台“用量详情”为准。例如合同条款分析需法务复核（文档 24），CAD 模型需本地导出后做几何校验（文档 42）。

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
- [代码评审 · PR 合并前先过一遍 diff](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)
- [自媒体 / 内容创作](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content.md)
- [电影级空镜短片 · 一条提示词出 30 秒 1080P 素材](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)
- [儿童趣味动物视频生成](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-kids-animal-video.md)
- [睡前故事配音](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)
- [个人 IP 头像 / 表情包](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)
- [小红书封面图 / 文案一次出](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-redbook-cover.md)
- [短剧脚本 · 把干货稿改成能拍的分镜](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-drama-script.md)
- [商品图变展示视频 · 静图秒变主图短视频](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)
- [让人物动起来 · 图生视频精准控运动](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)
- [人物一致性换装组照 · 锁住这张脸，只换衣服和场景](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)
- [表格分析 · 脏数据出结论](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)
- [资料与数据处理](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data.md)
- [合同体检 · 挑出对我不利的条款](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)
- [网页提数 · 指定字段抓成表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)
- [跨境选品 · 识图定价](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-cross-border.md)
- [票据 / 文档识别归档](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md)
- [个人知识库问答 · RAG 三段式](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-knowledge-rag.md)
- [长文 / 论文 / 合同秒读问答](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)
- [周报汇总 · 五封邮件汇成四列进度表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)
- [长图变数据 · 促销图抽字段 + 文案风险初筛](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)
- [视频摘要 · 按时间线拆片段](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-video-digest.md)
- [生活娱乐](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life.md)
- [品牌虚拟代言人 · 一张形象图出 15 秒口播成片](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)
- [一句话规划周末出游 · 多步 Agent](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)
- [老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)
- [父母用药管家 · 服药 / 开药双提醒](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-med-reminder.md)
- [居家安全 · 拍张照排查隐患](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md)
- [求职职场](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career.md)
- [简历诊断 · 按 JD 改写](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)
- [AI 面试教练 · 出题追问打分](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-interview-coach.md)
- [三维 CAD 建模 · 出 STEP/STL 文件](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md)
- [教育社群故事化群日报](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-group-daily-report.md)
- [OpenClaw 个人任务管家](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)
- [时光影像信 · 把想说的话做成会动、能听的一封信](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-photo-letter.md)
- [交互式教育解题 · 一题变讲解网页](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)
- [提交信息 · 一上午的改动自动拆 commit](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-commit-writer.md)


