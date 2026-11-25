# token plan playbooks

`token plan playbooks` 是一套面向开发者的结构化 AI 应用实践指南，涵盖 42 个经实测验证的端到端玩法（playbook），按场景分类提供可复用的提示词模式、模型选型建议与输出规范。每个 playbook 均基于真实 Token Plan 订阅能力设计，输出效果与 Credits 消耗以控制台“用量详情”为准。所有玩法均已在 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks.md) 中完整索引并附实测产出示例。

## 支持的模型/功能

Playbooks 调用底层多模态模型能力，具体模型绑定由场景决定，**不支持用户手动指定模型**。关键能力映射如下：

- **代码类玩法**：主要依赖 `Qwen3.8-flash`（视觉理解）、`Qwen3.5-coder`（代码生成/评审）及 `Qoder` Agent 框架；例如“截图变代码”明确使用 `Qwen3.8-flash` 视觉理解还原 HTML [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks.md)。
- **视频生成类**：统一调用 `wan3.0-video`，如“电影级空镜短片”和“品牌虚拟代言人”均基于该模型原生运镜与口型同步能力 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks.md)。
- **长文档处理类**：依赖 `Qwen3.5-turbo` 或更高上下文窗口模型，如“长文秒读问答”“合同体检”需完整加载原文进行跨条款推理。
- **Agent 类玩法**：如 `OpenClaw` 任务管家、“一句话规划周末出游”，由平台自动编排文本、图像、联网等多步调用，开发者无需管理子任务调度。

> **注意**：文档中“三维 CAD 建模”玩法描述为“生成建模脚本，本地 CAD 内核执行”，但当前 Token Plan 不开放本地内核调用权限；实际输出为可导入主流 CAD 工具（如 Fusion 360）的 STEP/STL 文件，该细节与 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks.md) 中“产出 STEP/STL 文件”的表述一致，但“本地内核执行”属过时描述，应忽略。

## 关键参数

Playbooks 本身不暴露 API 级参数，但以下字段在调用链中起决定性作用：

- `input`：严格按 playbook 要求组织输入格式（如 `git diff` 文本、网页 HTML 片段、Base64 图片字符串），非结构化输入将导致失败。
- `output_format`：多数玩法强制 JSON 输出（如 `命令预检` 固定 5 字段 JSON），部分要求 `text/plain`（如 `睡前故事配音` 输入纯文本）。
- `context_window_hint`：对长文档类玩法（如“论文秒读问答”），需在提示词中显式声明文档长度（如“全文约12,000字”），否则模型可能截断处理。
- `reference_image`：涉及图生图/图生视频的玩法（如“人物一致性换装组照”），必须提供首张参考图作为 identity anchor。

## 使用方式

1. **确认订阅状态**：仅 Token Plan 订阅用户可访问全部 42 个 playbook，未订阅时部分攻略页返回 403。
2. **定位具体 playbook**：通过 [原文标题](../../raw/token-plan-user-guide/token-plan-playbooks.md) 中的“玩法总表”跳转至对应子攻略页（如 `token-plan-playbook-code-review.md`），获取完整提示词模板与输入样例。
3. **构造请求体**：按子攻略页明确的 `input` 格式准备数据，**禁止添加额外说明性文字**（如“请帮我…”），所有指令已内置于 playbook 提示词中。
4. **提交并解析响应**：直接调用 `/v1/playbook/{id}` 接口（ID 见子攻略页 URL），响应体结构与文档中“实测产出”栏完全一致，可直接用于下游消费。

## 限制和注意事项

- **Credits 消耗不可预测**：同一 playbook 在不同输入规模下 Credits 波动显著（如“周报汇总”处理 5 封邮件 vs 20 封邮件），务必通过控制台“用量详情”实时监控。
- **无状态设计**：所有 playbook 均为 stateless 请求，不保留历史上下文。如需多轮交互（如面试教练的追问），必须由客户端维护对话 ID 并在每次请求中传入完整历史。
- **文件上传限制**：视觉类玩法（截图、长图、视频）支持单文件 ≤ 20MB，超出将被拒绝；PDF 需先转为图片再上传。
- **输出强约束**：违反 `output_format`（如要求 JSON 却返回 Markdown）视为失败，不会重试或降级。务必校验子攻略页的“输出示例”结构。
- **地域合规性**：`wan3.0-video` 生成内容受中国境内内容安全策略约束，含敏感元素的提示词将触发拦截，无 fallback 机制。

## 来源文档

- [玩法攻略](../../raw/token-plan-user-guide/token-plan-playbooks.md)


