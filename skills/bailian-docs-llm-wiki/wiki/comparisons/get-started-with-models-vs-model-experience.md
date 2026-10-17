# 模型快速入门与模型体验实践对比

为帮助开发者高效启动大模型集成工作，百炼平台提供两条核心技术路径：**模型快速入门（Get Started with Models）** 侧重标准化、生产就绪的 API 接入，面向工程化部署；**模型体验实践（Model Experience）** 侧重统一入口、[多模态](../concepts/multimodal.md)实验与控制台交互，面向探索性验证与快速原型开发。本文档从技术实现、使用约束与适用阶段三个维度进行系统性对比，旨在为开发者在项目不同生命周期中做出精准的技术选型提供依据。

## 关键维度对比

| 维度 | 模型快速入门（Get Started with Models） | 模型体验实践（Model Experience） |
|------|----------------------------------------|--------------------------------|
| **设计定位** | 生产级 API 接入框架，强调兼容性、稳定性与运维可控性 | 统一模型实验平台，强调易用性、[多模态](../concepts/multimodal.md)覆盖与低门槛调试能力 |
| **输入格式** | 严格遵循 OpenAI 兼容协议：<br>• `messages` 数组（角色+内容）<br>• 支持 `functions` / `tool_choice`（部分模型）<br>• 不支持原生图像/音频二进制嵌入（需预编码为 base64 URL） | 模型自描述式结构：<br>• `input` 字段为 JSON 对象，格式随模型类型动态变化（如 `{"prompt": "..."}`、`{"image_url": "data:image/png;base64,..."}`、`{"video_bytes": "..."}`）<br>• 原生支持[多模态](../concepts/multimodal.md)数据直传（含图像、视频、音频、3D 等二进制或 URI） |
| **输出格式** | OpenAI 标准响应体：<br>• `choices[0].message.content`（文本）<br>• `choices[0].delta.content`（流式）<br>• `usage.input_tokens` / `output_tokens`（[Token](../concepts/token.md) 计量） | 百炼统一响应体：<br>• `output.text`（文本生成）<br>• `output.image_url` / `output.video_url`（生成类）<br>• `output.results`（结构化结果，如 OCR 表格、目标检测框）<br>• `usage.total_tokens`（仅文本类模型返回，非全模态一致） |
| **支持模型** | • 聚焦主流文本大模型（Qwen3.7-plus / 3.8-max / 3.8-flash）<br>• 明确支持 DeepSeek、Kimi、GLM、MiniMax 等第三方模型（按地域可用）<br>• **不支持**视觉/语音/3D/世界模型等专用能力模型 | • 全模态覆盖：<br> ✓ 文本（Qwen 系列）、代码（CodeQwen）<br> ✓ 视觉（Qwen-VL、OCR、目标检测）<br> ✓ 图像/视频生成（Wanx-Image、Wanx-Video）<br> ✓ 语音（TTS、ASR、S2S）<br> ✓ 3D（TriPo）、世界模型（HappyOyster）、嵌入（Qwen-Embedding）<br>• **不支持**第三方模型（DeepSeek/Kimi/GLM 等） |
| **API 端点** | `/v1/chat/completions`（OpenAI 兼容路径）<br>• 必须指定 `base_url`（含 WorkspaceId 或 DashScope 域名）<br>• 依赖 `model` 字段路由至后端实例 | `/v1/models/{model}/invoke`（百炼原生路径）<br>• `base_url` 固定为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）<br>• `model` 作为路径参数，强绑定模型能力语义 |
| **鉴权方式** | `Authorization: Bearer <API_KEY>`（标准 Header）<br>• API Key 需按地域单独创建<br>• 支持模型级权限粒度控制（“自定义权限”） | `Authorization: Bearer <API_KEY>`（标准 Header）<br>• API Key 与“模型快速入门”共用同一套密钥体系<br>• **不支持**模型级权限隔离，所有已开通模型均可调用 |
| **计费方式** | • 支持三种计费方案：<br> ✓ 按量付费（Pay-as-you-go）<br> ✓ [Token](../concepts/token.md) Plan（包年/包月 [Token](../concepts/token.md) 预购）<br> ✓ Coding Plan（开发者专属套餐）<br>• 各方案对应独立 Base URL 与配额策略 | • **仅支持按量付费**一种计费模式<br>• Token Plan 与 Coding Plan 用户无法通过此路径调用模型<br>• 所有调用均计入主账号按量账单，无专属优惠叠加 |
| **限流机制** | • 双维度硬限流：<br> ✓ RPM（每分钟请求数）<br> ✓ TPM（每分钟 Token 总消耗，含输入+输出）<br>• 动态 TPM：qwen3.8-max 等旗舰模型额度随月消费金额分档提升 | • 单维度软限流：<br> ✓ RPS（每秒请求数）为主控指标<br> ✓ 并发数限制（Concurrent Requests）<br>• **无 TPM 限制**，但单次请求输入长度受模型类型硬约束（如文本 ≤32k tokens，图像 ≤1536×1536） |
| **典型场景** | • SaaS 产品后端服务集成<br>• 高并发对话机器人（客服/教育）<br>• 企业知识库问答系统（需稳定 SLA）<br>• 第三方模型混合编排（如 Qwen + GLM 协同） | • 控制台模型效果验证与 Prompt 工程调试<br>• 多模态应用原型开发（图文理解→生成→编辑闭环）<br>• 内部 AI 工具链快速搭建（如自动化报告生成、视频摘要）<br>• 教学演示与开发者 workshop 实验环境 |

## 各方案的适用场景建议

| 场景阶段 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **首次接触百炼，想快速验证模型效果** | ✅ 模型体验实践 | 控制台即开即用，无需配置 Base URL 或 SDK，支持拖拽上传图片/视频，5 分钟内完成图文理解、文生图等跨模态实验；避免因地域/Key/URL 配置错误导致的 401/429 问题。 |
| **构建生产级文本服务（如智能客服、内容生成 API）** | ✅ 模型快速入门 | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)可直接复用现有 SDK 和中间件（如 LangChain、LlamaIndex），支持细粒度限流控制、Token Plan 成本优化、多地域灾备部署，且具备明确 SLA 保障。 |
| **需要调用视觉/语音/3D/世界模型等专用能力** | ✅ 模型体验实践 | “模型快速入门”路径未开放这些模型的 OpenAI 兼容封装；而“模型体验”提供原生 `input` 结构与专用响应字段（如 `output.image_url`, `output.results`），是唯一官方支持路径。 |
| **团队已采购 Token Plan 或 Coding Plan 套餐** | ✅ 模型快速入门 | Token Plan/Coding Plan 仅对 `/v1/chat/completions` 等兼容接口生效；若使用“模型体验”路径，将自动回退至按量计费，无法享受套餐权益。 |
| **需对不同模型实施差异化访问控制（如子账号仅能调用 qwen3.7-plus）** | ✅ 模型快速入门 | 仅在此路径支持 API Key 的“自定义权限”功能，可精确限定 Key 可访问的模型列表；“模型体验”路径下所有模型对有效 Key 全开放。 |
| **开发多模态 Agent（如接收用户拍照→OCR→推理→生成报告）** | ⚠️ 混合使用 | 建议：OCR/视觉理解 → 使用“模型体验”路径（原生支持图像输入）；后续文本推理 → 切换至“模型快速入门”路径（利用其高吞吐与成本优势）。二者可通过同一 WorkspaceId 和 API Key 无缝协同。 |

## 面向开发者的技术选型参考

- **优先选择“模型快速入门”的情况**：  
  你正在构建一个需要长期稳定运行、有明确性能与成本要求的线上服务；你的技术栈已深度集成 OpenAI SDK；你使用的是 Qwen 系列文本模型或第三方模型；你已采购 Token Plan 或需精细化配额管理。

- **优先选择“模型体验实践”的情况**：  
  你处于需求探索或 MVP 阶段，需高频切换模型类型（如从文生图试到视频生成）；你需要处理非文本模态（图像、音频、视频、3D）；你依赖控制台可视化调试能力降低学习成本；你仅使用按量付费且不追求极致吞吐。

- **重要提醒**：  
  - 两条路径**并非互斥**，而是互补。百炼推荐“体验先行、接入落地”——先用“模型体验”验证效果与流程，再用“模型快速入门”完成生产集成。  
  - 所有调用均计入**同一主账号维度**的限流与账单，切勿因路径不同而误判资源水位。  
  - DashScope 兼容域名将于 2026 年 9 月 30 日停更新特性，请新项目一律使用业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`）。  
  - 模型名称存在版本演进（如 `qwen3.7-plus` vs `qwen3.8-plus`），实际可用模型请以[控制台模型市场](https://bailian.console.aliyun.com/model/market)实时列表为准，避免依赖文档静态命名。

## 被对比主题页

- [get started with models](../guides/get-started-with-models.md)
- [model experience](../guides/model-experience.md)


