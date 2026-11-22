# Qwen API 与世界模型 API 对比

本对比旨在帮助开发者在百炼平台技术选型阶段，清晰区分 **Qwen 系列通用大模型 API** 与 **世界模型（World Model）专用叙事生成 API** 的定位、能力边界与工程适配性。随着 AI 应用向深度交互、[多模态](../concepts/multi-modal.md)理解与结构化内容创作演进，两类 API 分别服务于“通用智能底座”与“垂直创作引擎”两大范式。本文不预设优劣，而是基于协议设计、输入输出语义、模型能力粒度及落地约束，提供客观、可操作的技术决策依据。

## 关键维度对比

| 维度 | Qwen API | 世界模型 API |
|------|----------|--------------|
| **核心定位** | 通用大语言/[多模态](../concepts/multi-modal.md)模型服务接口，支持对话、推理、代码、视觉理解等广泛任务 | 面向叙事性内容生成的专用引擎，聚焦世界观构建、镜头编排、角色行为建模等影视/游戏级创作流程 |
| **输入格式** | 多协议兼容：<br>• OpenAI Chat：`messages` 数组（含 `role`/`content`/`image_url`）<br>• Responses：`string` 或结构化 `EasyInputMessage` 数组 + `tools`<br>• Anthropic：`messages` 数组（支持 `text`/`image`/`video`/`document` 混合 content）<br>• DashScope 原生：`input: { messages: [...] }` 封装 | 统一 JSON 结构体，`input` 字段为模型特有对象：<br>• Adventure：需 `world_seed` + `narrative_constraints`<br>• Directing：需 `shot_sequence` + `scene_context`<br>• Acting（邀测）：需 `character_state` + `emotion_bias` 等细粒度参数 |
| **输出格式** | 协议一致性强：<br>• OpenAI 兼容：标准 `choices[0].message.content` + `usage`<br>• Responses：含 `response_id`、`tool_calls`、`store_id` 等 Agent 上下文字段<br>• Anthropic：`content` 数组（含 `text`/`tool_use`/`thinking` 块）<br>• DashScope：`output.text` + `output.choices[0].finish_reason` | 固定结构化响应：<br>• `output.result`（字符串或嵌套 JSON 对象）<br>• `output.metadata`（含生成耗时、token 使用量、版本信息）<br>• 不返回原始 token 流或工具调用链，无 `usage` 字段（计费按请求次/模型类型） |
| **支持模型** | • 文本/代码：`qwen4-max`、`qwen3.8-plus`、`qwen3.7-flash`、`qwen-coder`<br>• [多模态](../concepts/multi-modal.md)：`qwen3-vl-plus`、`qwen3.8-vl`、`qwen-audio`（仅 DashScope 协议）<br>• 第三方模型：DeepSeek、Qwen-VL 等（部分协议受限） | • `happyoyster-adventure-v1`（世界观生成）<br>• `happyoyster-directing-v1`（镜头与节奏编排）<br>• `happyoyster-acting-v1`（邀测中，不开放公测）<br>• **不支持任何 Qwen 系列通用模型调用** |
| **API 端点** | • OpenAI 兼容：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Responses：`.../compatible-mode/v1/responses`<br>• Anthropic：`.../apps/anthropic/v1/messages`<br>• DashScope 原生：`.../api/v1/services/aigc/{text-generation\|multimodal-generation}/generation` | 统一入口：<br>`https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`<br>• **不支持业务空间专属域名**，强制使用公共 `dashscope.aliyuncs.com` 域名<br>• 无协议变体，仅 RESTful POST |
| **计费方式** | • 按 **[Token](../concepts/token.md) 使用量** 计费（输入 + 输出 tokens）<br>• 不同模型单价不同（如 `qwen4-max` > `qwen3.8-flash`）<br>• 多模态输入（图像/视频）按像素/帧数折算额外 token 成本<br>• Responses API 中 `store=true` 产生持久化存储费用 | • 按 **单次请求** 计费（固定单价）<br>• Adventure/Directing 模块单价相同，Acting（若开放）单独定价<br>• **无 token 粒度计费**，输入长度上限 8192 tokens，超限直接报错不计费<br>• 无流式响应附加费用（`stream=true` 仍按 1 次计） |
| **典型场景** | • 智能客服、知识问答、文档摘要<br>• 多轮 Agent 应用（联网搜索、代码执行、RAG）<br>• 图文/音视频理解与生成（如财报分析+图表生成）<br>• 快速迁移现有 OpenAI/Anthropic 生态应用 | • 游戏剧情系统初始化（动态生成世界观、角色关系图谱）<br>• 虚拟制片预演（自动生成分镜脚本、镜头运动序列）<br>• 互动小说引擎（实时分支剧情推演与一致性维护）<br>• 影视 AI 辅助导演（节奏控制、情绪张力建模） |
| **会话与状态管理** | • Responses API 支持 `previous_response_id` 串联 + `x-dashscope-session-cache: enable` 自动缓存<br>• OpenAI Chat 依赖客户端维护 `messages` 历史<br>• DashScope 原生无内置会话机制，需自行管理 | • **无原生会话状态**：每次请求完全独立<br>• Adventure 输出可作为 Directing 输入（如 `world_graph` 传递），但需应用层显式编排<br>• 不支持 `store/retrieve` 类持久化上下文机制 |

## 各方案适用场景建议

### ✅ 选择 Qwen API 当：
- 你需要一个**通用、灵活、可扩展的 AI 底座**，支撑从简单问答到复杂 Agent 的全栈能力；
- 项目已集成 OpenAI/Anthropic SDK，追求**最小改造成本迁移**；
- 任务涉及**多模态输入（图像/视频/音频）或长文本推理**，且需精细控制 `max_tokens`、`temperature`、`reasoning.effort` 等参数；
- 你正在构建需要**工具调用（function calling）、联网搜索、代码解释器**的智能体；
- 成本敏感，希望按实际 token 消耗精细化计费，而非固定请求单价。

### ✅ 选择世界模型 API 当：
- 你的核心需求是**结构化叙事生成**，而非通用文本生成——例如自动构建游戏世界观、生成分镜脚本、驱动虚拟角色行为；
- 你接受**领域专用接口设计**，愿意为更高抽象层级（如 `shot_sequence`、`world_seed`）付出学习成本；
- 你追求**输出结果的强结构化与领域语义一致性**（如 Adventure 输出必含 `character_relations` 和 `conflict_nodes` 字段）；
- 你处于影视、游戏、互动娱乐等垂直行业，已有专业创作流程（如分镜表、角色设定档），需 API 与之对齐；
- 你倾向**确定性计费模型**（单次请求固定价格），且输入规模可控（≤8192 tokens），无需 token 级优化。

### ⚠️ 不建议混用或强行替代的场景：
- **不要用 Qwen API 替代 World Model 的 Adventure 功能**：虽可用 `qwen4-max` 写一段世界观描述，但无法保证角色关系图谱的拓扑完整性、分支剧情的逻辑闭环性，也缺乏 `narrative_constraints` 等约束注入能力。
- **不要用 World Model API 替代 Qwen 的通用对话能力**：它不支持 `system` 角色设定、不提供 `messages` 历史管理、无工具调用机制，无法构建客服或助手类应用。
- **避免在 World Model 中尝试多模态输入**：该 API 当前仅接受纯文本 `input`，不支持图像/视频 URL 或 base64 编码。

## 技术选型参考（面向开发者）

| 选型考量项 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **快速原型验证（MVP）** | Qwen API（OpenAI Chat） | SDK 兼容性高，5 行代码即可调通；支持 `messages` 历史回传，适合快速迭代对话逻辑。 |
| **企业级 Agent 平台** | Qwen API（Responses） | 内置工具链（file_search、code_interpreter）、自动会话缓存、`response_id` 追踪，大幅降低 Agent 工程复杂度。 |
| **游戏剧情引擎开发** | 世界模型 API（Adventure + Directing） | 提供 `world_seed` 初始化、`narrative_constraints` 约束、`shot_sequence` 编排等原生语义，避免在通用模型上做脆弱 prompt 工程。 |
| **虚拟制片工作流集成** | 世界模型 API（Directing） | 直接映射影视工业术语（如 `camera_movement`、`cut_timing`），输出可导入 DaVinci Resolve 或 Unreal Engine 的结构化分镜数据。 |
| **多模态内容理解应用** | Qwen API（DashScope 原生） | 唯一完整支持 `video` + `fps` + `max_frames` 控制的协议，且 `detail`/`min_pixels` 参数层级明确，适合精准控制视觉理解粒度。 |
| **成本敏感型 SaaS 产品** | Qwen API（qwen3.8-flash） | Flash 系列模型单位 token 成本最低，兼顾响应速度与基础能力，适合高频轻量请求场景。 |
| **需要长期上下文记忆的叙事应用** | Qwen API（Responses + store） | 利用 `store=true` 持久化用户世界设定，后续请求通过 `retrieve` 加载，实现跨会话叙事连贯性——World Model 无此能力。 |

> **最后提醒**：世界模型 API 当前为邀测开放，需在百炼控制台提交权限申请；Qwen API 则开箱即用（需配置 WorkspaceId 域名）。建议在技术评审阶段同步确认访问权限状态，避免开发阻塞。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)


