# token plan playbooks

`token plan playbooks` 是一套面向开发者的结构化实践指南，覆盖 AI 编程、内容生成、数据处理、生活应用等 5 大场景，提供可复用的提示词模板、模型选型建议与参数配置。所有 playbook 均基于真实调用链验证，强调输入可控、输出可验、消耗可预期，不依赖黑盒 Agent 自主决策。

## 支持的模型/功能

Playbook 的能力边界由底层模型决定，需严格匹配任务类型：

- **代码增量开发与文档驱动开发**：必须使用 `qwen3.8-max`（如 [AI Coding · 给现有系统加功能](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md) 和 [文档驱动开发 · 一份文档换一个系统](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md) 所示），因其具备长上下文理解与复杂逻辑编排能力；`qwen3.7-max` 在部分简单增量场景可降级使用，但实测在多文件依赖推理中失败率显著升高。
- **视觉理解类任务（UI 体检、截图转代码、票据 OCR）**：统一使用 `qwen3.7-plus`，其视觉编码器对界面元素、文字位置、色彩语义识别稳定；`qwen3.8-flash` 虽支持图像输入，但在“数颜色”“认字体”等细节任务中易出错，[界面体检 · 截图挑毛病与定位报错](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md) 明确指出其“在需要精确清点的细节上会看走眼”。
- **视频生成与高精度图生视频**：`wan3.0-video` 用于电影级空镜（30 秒/1080P），`happyhorse-1.1-t2v` 用于短动画（5 秒/720P），`happyhorse-1.1-i2v` 专用于首帧锁定的运动控制；三者不可互换，`wan3.0-video` 不支持首帧输入，`i2v` 模型无法生成无参考的原创视频。
- **命令安全预检与 PR 评审**：必须关闭思考模式（`enable_thinking: false`），使用 `qwen3.8-flash`，以保障毫秒级响应与确定性 JSON 输出格式；开启思考会导致输出不稳定，违反自动化流程要求。

> **注意**：文档 12 中 `wan3.0-video` 的调用链描述为 `qwen3.8-flash → wan3.0-video`，但实际 `wan3.0-video` 是独立文生视频模型，不接受文本模型的中间提示词加工；该处为流程示意错误，正确做法是直接将电影感提示词（经 `qwen3.8-flash` 扩写后）喂给 `wan3.0-video`。

## 关键参数

所有 playbook 的稳定性高度依赖以下参数配置：

- **输入长度控制**：代码调研类任务（如 [代码调研 · 摸清陌生项目架构](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)）严禁全量上传代码，必须先用 `ast` 提取签名骨架（仅保留类/函数名与 docstring 首行），将输入压缩至原体积 10% 以内，否则触发上下文截断或模型拒绝响应。
- **输出格式强制**：安全审计、提交信息、PR 评审等结构化任务，指令中必须声明“只返回一个 JSON 对象，不要输出任何其他文字”，并明确定义字段（如 `commits`, `verdict`, `issues`）。未强制格式时，模型可能混入解释性文字，导致下游解析失败。
- **视觉任务分辨率约束**：UI 体检、截图转代码等任务，截图应使用标准网页尺寸（如 1920×1080），避免超大图；[界面体检 · 截图挑毛病与定位报错](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md) 明确说明“截图越大越清晰、输入消耗越高”，且超大图会降低模型对关键区域的聚焦精度。
- **视频任务异步标识**：所有视频生成（`wan3.0-video`, `happyhorse-1.1-t2v`, `i2v`）必须启用 `--async` 参数获取 `task_id`，再轮询结果；直接同步等待将因超时导致请求失败。

## 使用方式

Playbook 的执行遵循“指令即契约”原则，开发者需严格按三段式组织输入：

1. **角色定义**：明确模型身份（如“资深应用安全工程师”“UI/UX 设计师”），避免模糊表述（如“帮我看看”）；
2. **输入交付**：代码、截图、视频、合同全文等原始素材，必须通过 `<image_url: base64>` 或 `<video_url: base64>` 等标准协议嵌入，或在指令末尾用 `【现有代码】` `【合同全文】` 等标记包裹；
3. **输出约束**：除格式外，必须指定行为边界，例如：
   - “所有数字、商品名、货号一律照抄图上的，看不清就在 `missing_info` 里说明，不许猜、不许编”（见 [长图变数据 · 促销图抽字段 + 文案风险初筛](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)）；
   - “只根据 diff 的实际内容判断，不要靠函数名或文件名猜”（见 [代码评审 · PR 合并前先过一遍 diff](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)）；
   - “身份锁定写在提示词最前面，并明确‘是同一个人、不要改变长相’”（见 [人物一致性换装组照](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)）。

## 限制和注意事项

- **敏感数据隔离**：所有含密钥、内网地址、客户数据的代码/合同/票据，必须脱敏后再提交；[AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md) 强调“真实密钥、内网地址、客户数据请把值替换成占位符再提交”，模型仍能识别“此处硬编码凭据”的模式。
- **模型能力边界**：`qwen3.7-plus` 的视觉理解不替代专业 OCR 或人脸识别，[票据 / 文档识别归档](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md) 明确说明“图片本身会转成 tokens 计入输入”，且对遮挡、低对比度文本识别率下降；[人物一致性换装组照](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md) 也提醒“这是让视觉模型做的交叉比对，不是权威人脸识别，重要用途请自己再核”。
- **成本不可省略项**：带参考图编辑（如老照片修复、换装）的消耗远高于纯文生图，因参考图输入是 token 消耗大头；[老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md) 指出“原图分辨率越高越贵”。视频生成消耗呈指数增长，5 秒视频成本约为同分辨率图片的 3–5 倍，务必先用 5 秒/720P 验证再加量。
- **法律与合规免责**：AI 合同体检、医疗提醒等涉及专业领域的产出，仅作自查辅助，[合同体检 · 挑出对我不利的条款](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md) 和 [父母用药管家 · 服药 / 开药双提醒](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-med-reminder.md) 均明确声明“不构成法律意见”“不提供任何用药建议”，最终决策须由持证专业人士完成。

## 来源文档

- [AI Coding / 开发](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding.md)
- [AI Coding · 给现有系统加功能](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md)
- [Qoder 搭个人小工具](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-qoder-tool.md)
- [一句话生成可玩小游戏](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-mini-game.md)
- [AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)
- [代码调研 · 摸清陌生项目架构](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)
- [界面体检 · 截图挑毛病与定位报错](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md)
- [截图变代码 · 数据看板照结构还原](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-screenshot-to-code.md)
- [提交信息 · 一上午的改动自动拆 commit](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-commit-writer.md)
- [代码评审 · PR 合并前先过一遍 diff](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)
- [自媒体 / 内容创作](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content.md)
- [电影级空镜短片 · 一条提示词出 30 秒 1080P 素材](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)
- [文档驱动开发 · 一份文档换一个系统](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md)
- [睡前故事配音](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)
- [个人 IP 头像 / 表情包](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)
- [小红书封面图 / 文案一次出](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-redbook-cover.md)
- [短剧脚本 · 把干货稿改成能拍的分镜](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-drama-script.md)
- [商品图变展示视频 · 静图秒变主图短视频](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)
- [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)
- [人物一致性换装组照 · 锁住这张脸，只换衣服和场景](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)
- [资料与数据处理](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data.md)
- [表格分析 · 脏数据出结论](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)
- [网页提数 · 指定字段抓成表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)
- [合同体检 · 挑出对我不利的条款](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)
- [儿童趣味动物视频生成](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-kids-animal-video.md)
- [票据 / 文档识别归档](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md)
- [跨境选品 · 识图定价](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-cross-border.md)
- [长文 / 论文 / 合同秒读问答](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)
- [个人知识库问答 · RAG 三段式](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-knowledge-rag.md)
- [周报汇总 · 五封邮件汇成四列进度表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)
- [长图变数据 · 促销图抽字段 + 文案风险初筛](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)
- [视频摘要 · 按时间线拆片段](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-video-digest.md)
- [生活娱乐](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life.md)
- [老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)
- [品牌虚拟代言人 · 一张形象图出 15 秒口播成片](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)
- [OpenClaw 个人任务管家](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)
- [父母用药管家 · 服药 / 开药双提醒](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-med-reminder.md)
- [居家安全 · 拍张照排查隐患](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md)
- [时光影像信 · 把想说的话做成会动、能听的一封信](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-photo-letter.md)
- [让人物动起来 · 图生视频精准控运动](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)
- [求职职场](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career.md)
- [AI 面试教练 · 出题追问打分](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-interview-coach.md)
- [三维 CAD 建模 · 出 STEP/STL 文件](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md)
- [一句话规划周末出游 · 多步 Agent](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)
- [教育社群故事化群日报](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-group-daily-report.md)
- [简历诊断 · 按 JD 改写](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)
- [交互式教育解题 · 一题变讲解网页](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)


