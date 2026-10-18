# Qwen 系列模型与世界模型对比

本页旨在为百炼平台开发者提供清晰、实用的技术选型参考，系统对比 **Qwen 系列大语言/[多模态](../concepts/multi-modal.md)模型**（通用AI能力底座）与 **世界模型（World Model）**（面向交互式叙事与游戏场景的专用建模系统）在架构定位、能力边界、接口设计及工程实践层面的关键差异。二者并非替代关系，而是互补协同：Qwen 擅长通用理解、生成与工具协同；世界模型专注结构化世界状态演化、角色行为决策与剧情因果推演。正确区分适用场景，可避免过度工程化或能力错配。

---

## 关键维度对比

| 维度 | Qwen 系列模型 | 世界模型 |
|------|----------------|------------|
| **核心定位** | 通用大语言/[多模态](../concepts/multi-modal.md)基础模型（LLM/VLM/AML），面向广泛AI任务（问答、创作、代码、[多模态](../concepts/multi-modal.md)理解与生成） | 领域专用建模引擎，聚焦“动态世界”模拟——支持剧情分支生成、角色行为决策、环境状态演化、镜头调度等强因果性、时序性交互任务 |
| **输入格式** | 多协议适配：<br>• OpenAI Chat：`messages: [{role, content}]`（content 支持 text/image/video/file）<br>• OpenAI Responses：`input: string \| array`（更灵活的原始输入）<br>• Anthropic Messages：`content: [{type, text/image/video}]`（细粒度媒体分片） | 统一 RESTful JSON 结构：<br>• 必填 `scene_state`（严格 schema 化的对象，描述当前世界状态，如角色位置、物品持有、情绪值、剧情节点ID等）<br>• 可选 `user_input`（玩家/导演指令文本）<br>• `max_steps` 控制推演深度（Adventure≤5，Directing≤3） |
| **输出格式** | 协议一致但语义丰富：<br>• 标准文本响应（含 tool_calls、function_call 字段）<br>• 流式 SSE 响应（`stream: true`）<br>• 结构化 JSON 输出（Anthropic Messages + JSON Schema 约束）<br>• 多模态输出元数据（如图像 base64、视频 URL、音频时长） | 类型强绑定：<br>• Adventure/Directing：同步返回 `200 OK` + JSON，含 `next_scene_state`、`narrative_output`、`directing_actions` 等字段<br>• Acting（邀测中）：仅支持 WebSocket SSE 流式响应，输出微动作帧序列（含时间戳、表情强度、语音基频等） |
| **支持模型** | • 主力：`qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3-coder-flash`、`qwen3.6-*` 等全系 Qwen 版本<br>• 多模态扩展：`qwen3-vl-plus`（图文）、`qwen3-vl`（视频）、`qwen3-audio`（音频）、`qwen3-omni`（音视频+文档）<br>• 第三方模型：DeepSeek、GLM、Kimi（部分协议兼容） | • `happyoyster-adventure`：剧情演化与玩家意图推理<br>• `happyoyster-directing`：多角色协同与镜头语言编排<br>• `happyoyster-acting`（邀测）：角色级动作、微表情、语音韵律建模（需白名单） |
| **API 端点** | 统一业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com`<br>• Chat：`/compatible-mode/v1/chat/completions`<br>• Responses（推荐）：`/compatible-mode/v1/responses`<br>• Anthropic：`/apps/anthropic/v1/messages` | 全局固定域名：<br>`https://dashscope.aliyuncs.com`（REST）<br>`wss://dashscope.aliyuncs.com`（Acting WebSocket）<br>• Adventure：`POST /api/v1/world-model/adventure`<br>• Directing：`POST /api/v1/world-model/directing`<br>• Acting：`wss://.../api/v1/world-model/acting` |
| **计费方式** | 按 token 计费（输入+输出 tokens）：<br>• 不同模型单价不同（如 `qwen3.8-max` > `qwen3.7-plus`）<br>• 多模态输入按等效文本 token 折算（图像≈500 tokens/1024×1024）<br>• 工具调用、缓存等高级功能不额外计费 | 按调用次数（Call）计费：<br>• Adventure/Directing：单次请求计 1 Call（无论 `max_steps=1` 或 `=5`）<br>• Acting：按连接时长与帧率计费（非 token），WebSocket 连接建立即开始计费<br>• 所有模型共享 Key 级 QPS 限额（10 QPS），Acting 连接数单独管控 |
| **典型场景** | • 智能客服、知识问答、内容创作（文案/脚本/诗歌）<br>• 多模态分析（PDF解析、图表理解、视频摘要）<br>• Agent 应用（联网搜索、代码执行、多步骤工具编排）<br>• 通用对话系统、教育辅导、编程助手 | • 开放世界 RPG 的实时剧情生成与状态管理<br>• 互动影视/虚拟制片中的导演调度与镜头规划<br>• 数字人/虚拟偶像的拟真表演驱动（动作+表情+语音协同）<br>• 游戏 NPC 行为树增强与上下文感知响应 |

---

## 各方案适用场景建议

### ✅ 推荐选用 **Qwen 系列模型** 当：
- 任务本质是「理解 → 推理 → 生成」的通用认知过程（如回答用户问题、总结长文档、编写 Python 脚本、分析截图中的表格）；
- 需要灵活接入外部工具链（搜索、数据库、API），构建自主 Agent；
- 输入/输出以文本为主，辅以图像、视频、音频、PDF 等多模态内容；
- 要求高兼容性（已集成 OpenAI/Anthropic SDK 的项目可零改造迁移）；
- 场景对「世界状态持久性」无强依赖（如无需跨多轮对话维持复杂对象关系图）。

### ✅ 推荐选用 **世界模型** 当：
- 核心需求是「状态驱动的因果推演」：例如“玩家进入森林后，触发隐藏BOSS战，同时天气由晴转雨，NPC A 因恐惧躲进帐篷”；
- 构建强交互叙事产品（文字冒险、互动剧、沙盒游戏），需保证剧情逻辑自洽、角色行为一致、世界变化可追溯；
- 需要专业级导演级控制（如“给主角特写+慢镜头+背景音乐渐强”）或表演级细节（如“右眉微抬0.3秒，嘴角左倾，语速降低15%”）；
- 客户端可承担状态管理责任（主动传递完整 `scene_state`，不依赖服务端会话缓存）；
- 对中文剧情连贯性、角色性格稳定性有极致要求（世界模型针对中文叙事做过专项优化）。

### ⚠️ 不建议混用或强行替代的场景：
- ❌ 用 Qwen 替代 Adventure 模型做剧情分支决策：Qwen 缺乏内置的世界状态 schema 和因果约束机制，易产生逻辑断层或状态遗忘；
- ❌ 用世界模型替代 Qwen 做通用问答或代码生成：世界模型无 tokenizer、无代码训练数据、不支持 function calling，能力严重受限；
- ❌ 在世界模型 API 中传入自由文本代替 `scene_state`：将直接导致 400 错误（schema 校验失败），必须使用预定义 JSON 结构。

---

## 面向开发者的选型参考

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| 构建一个支持上传 PDF 并自动提取关键条款的合同审查助手 | **Qwen（`qwen3-vl-plus` + OpenAI Responses）** | 原生支持 `input_file` 文档解析，可结合 `tool_calls` 调用规则引擎校验条款 | 使用 `qwen3.7-plus` 或更低版本可能丢失长文档结构理解能力 |
| 开发一款玩家可自由探索、剧情实时演化的武侠文字 MUD | **世界模型（Adventure） + Qwen 辅助** | Adventure 提供状态演化与分支保障；Qwen 可用于生成旁白文案、NPC 对话润色（作为后处理模块） | `scene_state` 需包含地图拓扑、角色属性、任务进度等完整快照，不可精简 |
| 为虚拟主播生成带口型同步、微表情和肢体动作的直播流 | **世界模型（Acting 邀测） + Qwen-Omni（语音生成）** | Acting 输出动作/表情/语音韵律帧；Qwen-Omni 将文本转为高质量语音波形，二者通过时间戳对齐 | Acting 需申请白名单；语音与动作需客户端做帧级融合渲染 |
| 快速搭建一个支持图片提问的客服机器人（如“这张发票金额是否正确？”） | **Qwen（`qwen3-vl-plus` + OpenAI Chat）** | 开箱即用的多模态理解，兼容主流前端 SDK，无需定义复杂 state schema | 避免使用 QVQ/QwQ 模型（system message 无效），优先选 `qwen3-vl-plus` |
| 实现电影分镜脚本自动生成：输入剧本，输出镜头列表（景别/运镜/时长/音效） | **世界模型（Directing）** | Directing 模型专为镜头语言建模，输出含 `shot_type`、`camera_movement`、`duration_sec` 等结构化字段 | 输入 `scene_state` 必须包含角色位置、道具状态、情绪曲线等导演级元信息 |

> **工程提示**：若项目需同时使用两类能力（如游戏内 NPC 既需世界状态决策，又需自然语言对话），推荐采用 **分层架构**：  
> **底层**：世界模型（Adventure/Directing）负责 `scene_state → next_scene_state + action_plan`；  
> **上层**：Qwen（Responses）接收 `action_plan` + `user_input`，生成符合角色设定的自然语言回复，并支持工具调用（如查询数据库获取角色背景）。  
> 此模式兼顾逻辑严谨性与表达丰富性，且便于独立扩缩容与监控。

---  
*最后更新：2025年4月*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)


