# token plan playbooks

token plan playbooks 是一套面向开发者、开箱即用的 AI 应用实践模板集合，覆盖编码、内容创作、数据处理、生活娱乐、求职职场五大场景。每个 playbook 均经过实测验证，明确标注所用模型、关键参数、输入输出结构及典型消耗特征，聚焦“怎么用对、怎么用省、怎么避坑”，不抽象讲能力，只交付可复现的操作路径。

## 支持的模型/功能

token plan playbooks 依赖多个专用模型协同完成端到端任务，核心模型及其典型用途如下：

- **`qwen3.8-max`**：深度推理主力，适用于需多步逻辑链、强事实约束与代码生成的场景，如 [文档驱动开发 · 一份文档换一个系统](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md)、[AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)、[交互式教育解题 · 一题变讲解网页](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)。
- **`qwen3.7-plus`**：长上下文理解与视觉理解主力，适用于文档问答、网页提数、合同体检、票据 OCR 等需高精度信息提取与跨段落关联分析的场景，如 [长文 / 论文 / 合同秒读问答](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)、[网页提数 · 指定字段抓成表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)。
- **`qwen3.8-flash`**：低延迟结构化输出主力，适用于命令预检、提交信息、周报汇总、促销图审核等需严格 JSON Schema、快速响应的自动化预检环节，如 [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)、[周报汇总 · 五封邮件汇成四列进度表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)。
- **`wan2.7-image`**：图像生成与编辑主力，支持文生图（`text-to-image`）与参考图编辑（`image-to-image`），用于头像/表情包、证件照换装、商品图变视频等，如 [个人 IP 头像 / 表情包](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)、[老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)。
- **`wan3.0-video`** 和 **`happyhorse-1.1-t2v/i2v`**：视频生成主力，分别适用于长片（30s+）与短片（5s）生成，如 [电影级空镜短片 · 一条提示词出 30 秒 1080P 素材](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)、[商品图变展示视频 · 静图秒变主图短视频](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)。
- **`qwen-audio-3.0-tts-plus`**：语音合成主力，用于睡前故事配音、影像信语音等，如 [睡前故事配音](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)。

> **注意**：文档中多次出现 `qwen3.7-max` 作为编码类任务模型（如 [Qoder 搭个人小工具](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-qoder-tool.md)），但其在 [AI Coding · 给现有系统加功能](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md) 中被明确指定为增量开发主力；而 `qwen3.8-max` 在 [文档驱动开发](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md) 和 [代码安全审计](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md) 中承担更重的推理任务。实践中应按具体 playbook 的实测要求选择模型，避免仅凭名称后缀（如 `-max`）泛化使用。

## 关键参数

playbooks 的稳定产出高度依赖以下关键参数配置，开发者需在调用时显式声明：

- **`enable_thinking: false`**：强制关闭模型思考链路，用于命令预检、提交信息等毫秒级响应场景。例如 [命令预检](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md) 明确要求此参数以保障预检环节的确定性与时效性。
- **`--watermark false`**：全局关闭模型水印，适用于所有视频与图像生成任务。若未设置，`wan2.7-image` 生成的首帧图会自带水印，并被 `wan3.0-video` 原样带入最终成片，导致水印叠加，如 [品牌虚拟代言人](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md) 所强调。
- **分辨率与尺寸约束**：图像任务必须指定 `--size`（如 `1024*1024`）、视频任务必须指定 `duration`（如 `30`）和 `resolution`（如 `1080P`）。错误或缺失将导致默认值偏差，影响产出质量与成本。
- **异步模式 `--async`**：所有视频生成任务（`wan3.0-video`, `happyhorse-1.1-t2v/i2v`）必须启用，因生成耗时在数十秒至数分钟量级，同步请求极易超时。客户端需轮询 task_id 获取结果。

## 使用方式

playbooks 的使用遵循统一的三阶段范式：**准备输入 → 构建指令 → 解析输出**，而非简单 API 调用。

1. **准备输入**：严格按 playbook 要求构造输入素材。例如 [截图变代码](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-screenshot-to-code.md) 要求上传原始看板截图（非压缩图），[表格分析](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md) 要求仅提供表头与前 20 行样本（而非整表），[合同体检](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md) 要求完整粘贴含附件的合同全文。
2. **构建指令**：将输入素材嵌入 playbook 提供的标准化指令模板。模板已固化输出格式（如固定 JSON 字段、Markdown 表格结构）、行为约束（如“只输出最终版 HTML”、“不许编造数据”）和验收标准（如“总时长必须正好 60 秒”）。直接复用模板可规避自由发挥导致的格式错乱。
3. **解析输出**：多数 playbook 输出为结构化数据（JSON/Markdown），可直接接入下游系统。例如 [命令预检](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md) 输出 JSON 数组，可由 CI/CD 流程自动解析 `action` 字段执行 `block` 或 `confirm`；[周报汇总](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md) 输出 Markdown 表格，可一键渲染为内部 Wiki 页面。

## 限制和注意事项

- **输入侧 [Token](../concepts/token.md) 消耗主导成本**：对于视觉理解（`qwen3.7-plus`, `qwen3.8-flash`）和视频生成任务，输入的图片/视频文件本身经 base64 编码后计入 tokens，是主要成本来源。截图/长图尺寸越大、视频时长越长，消耗越高。建议使用标准网页截图尺寸（非超大图）和 5–30 秒视频长度进行初验。
- **参考图编辑成本显著更高**：`wan2.7-image` 的参考图编辑（`image-to-image`）比纯文生图（`text-to-image`）消耗更高，因其需同时处理参考图 tokens 与文本 prompt。例如 [人物一致性换装组照](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md) 和 [老照片修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md) 均明确指出“参考图输入是消耗大头”。
- **隐私与合规边界**：所有涉及真实用户数据、密钥、内网地址的输入，必须脱敏后再提交。例如 [代码安全审计](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md) 要求将密钥替换为占位符；[居家安全](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md) 强调演示图由 AI 生成，真实排查需自行评估隐私风险。
- **模型能力边界**：`qwen3.8-flash` 不具备深度推理能力，仅适合结构化输出；`wan3.0-video` 的运动控制稳定性弱于 `happyhorse-1.1-i2v`，后者更适合精准走位（如 [让人物动起来](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)）。务必依据 playbook 实测结论选择模型，而非主观假设。

## 来源文档

- [AI Coding / 开发](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding.md)
- [Qoder 搭个人小工具](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-qoder-tool.md)
- [一句话生成可玩小游戏](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-mini-game.md)
- [文档驱动开发 · 一份文档换一个系统](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-doc-driven-dev.md)
- [代码调研 · 摸清陌生项目架构](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-survey.md)
- [界面体检 · 截图挑毛病与定位报错](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ui-review.md)
- [截图变代码 · 数据看板照结构还原](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-screenshot-to-code.md)
- [命令预检 · 执行前先过一道风险检查](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-cmd-guard.md)
- [提交信息 · 一上午的改动自动拆 commit](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-commit-writer.md)
- [代码评审 · PR 合并前先过一遍 diff](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-review.md)
- [自媒体 / 内容创作](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content.md)
- [电影级空镜短片 · 一条提示词出 30 秒 1080P 素材](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)
- [儿童趣味动物视频生成](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-kids-animal-video.md)
- [睡前故事配音](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-bedtime-story-tts.md)
- [个人 IP 头像 / 表情包](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-ip-avatar-sticker.md)
- [小红书封面图 / 文案一次出](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-redbook-cover.md)
- [AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)
- [短剧脚本 · 把干货稿改成能拍的分镜](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-drama-script.md)
- [AI Coding · 给现有系统加功能](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md)
- [商品图变展示视频 · 静图秒变主图短视频](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-product-video.md)
- [让人物动起来 · 图生视频精准控运动](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-motion-control.md)
- [人物一致性换装组照 · 锁住这张脸，只换衣服和场景](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-outfit-change.md)
- [资料与数据处理](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data.md)
- [表格分析 · 脏数据出结论](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)
- [网页提数 · 指定字段抓成表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-web-extract.md)
- [合同体检 · 挑出对我不利的条款](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-contract-review.md)
- [长文 / 论文 / 合同秒读问答](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-doc-qa.md)
- [个人知识库问答 · RAG 三段式](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-knowledge-rag.md)
- [跨境选品 · 识图定价](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-cross-border.md)
- [长图变数据 · 促销图抽字段 + 文案风险初筛](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-poster-audit.md)
- [视频摘要 · 按时间线拆片段](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-video-digest.md)
- [生活娱乐](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life.md)
- [品牌虚拟代言人 · 一张形象图出 15 秒口播成片](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)
- [老照片修复上色 / 证件照换装](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-old-photo.md)
- [OpenClaw 个人任务管家](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)
- [一句话规划周末出游 · 多步 Agent](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)
- [父母用药管家 · 服药 / 开药双提醒](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-med-reminder.md)
- [居家安全 · 拍张照排查隐患](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-home-hazard.md)
- [时光影像信 · 把想说的话做成会动、能听的一封信](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-photo-letter.md)
- [求职职场](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career.md)
- [简历诊断 · 按 JD 改写](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)
- [AI 面试教练 · 出题追问打分](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-interview-coach.md)
- [三维 CAD 建模 · 出 STEP/STL 文件](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-cad-3d.md)
- [教育社群故事化群日报](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-group-daily-report.md)
- [交互式教育解题 · 一题变讲解网页](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-edu-solver.md)
- [票据 / 文档识别归档](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-invoice-ocr.md)
- [周报汇总 · 五封邮件汇成四列进度表](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-weekly-report.md)


