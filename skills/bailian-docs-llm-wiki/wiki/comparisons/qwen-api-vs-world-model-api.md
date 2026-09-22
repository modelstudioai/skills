# Qwen API 与世界模型 API 对比

本对比旨在帮助开发者在百炼平台技术选型中，清晰区分 **Qwen API**（通用大模型能力接口）与 **世界模型 API**（面向交互式叙事与智能体行为编排的专用建模接口）的核心定位、能力边界与适用场景。随着多智能体系统、游戏化应用、教育模拟及复杂工作流自动化等需求兴起，两类 API 常被同时引入架构设计，但其设计理念、输入范式、状态管理机制与工程集成方式存在本质差异。本文基于当前（2024年Q3）正式可用能力，提供客观、可落地的技术对比参考。

## 关键维度对比

| 维度 | Qwen API | 世界模型 API |
|------|----------|----------------|
| **核心定位** | 通用大语言/多模态模型服务接口，聚焦内容生成、理解、工具调用与结构化输出 | 面向“世界建模”的专用推理接口，聚焦冒险生成（Adventure）、导演调度（Directing）、角色执行（Acting）三阶段行为编排 |
| **输入格式** | 灵活多样：<br>• OpenAI/Anthropic 协议：`messages` 数组（含 `system`/`user`/`assistant`/`tool` 角色消息）<br>• DashScope 原生：`input` 支持 `string` 或结构化对象（含 `input_text`/`input_image`/`input_audio` 等）<br>• Responses API：支持 `previous_response_id` 实现隐式上下文复用 | 严格结构化 JSON：<br>• `input` 必须为符合模型语义的 JSON 对象（如 Adventure 要求 `world_state` + `goal`；Directing 要求 `agents` + `resources` + `constraints`）<br>• 无自由文本对话流，不接受自然语言指令作为主输入 |
| **输出格式** | 多样化响应：<br>• 标准文本流（`content` 字段）或结构化 JSON（通过 `output_config.format.type = "json_schema"` 强约束）<br>• 工具调用返回 `tool_calls` 数组<br>• 多模态输出含 `image_url`/`audio_url` 等元数据 | 纯结构化 JSON 输出：<br>• `output` 字段为预定义 Schema 的 JSON 对象（如 Adventure 输出 `next_scene` + `state_updates`；Directing 输出 `scheduling_plan` + `conflict_resolution`）<br>• 不返回自由文本摘要，所有语义均编码于字段值中 |
| **支持模型** | • 千问全系：`qwen3.8-*`、`qwen3-vl-plus`、`qwen-omni-*`、`qwen-audio` 等<br>• 第三方模型：DeepSeek-v4、Kimi-k3、GLM-5、MiniMax-M2/M3（限华北2地域） | • `happyoyster-adventure-v1`（稳定可用）<br>• `happyoyster-directing-v1`（稳定可用）<br>• `happyoyster-acting-v1`（邀测中，需权限申请）<br>• **不支持任何千问或第三方通用模型** |
| **API 端点** | • OpenAI 兼容：`/{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Anthropic 兼容：`/{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic/v1/messages`<br>• DashScope 原生：`/{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/...` | • Adventure：`/{WorkspaceId}.{region}.maas.aliyuncs.com/v1/models/happyoyster-adventure-v1:generate`<br>• Directing：`/{WorkspaceId}.{region}.maas.aliyuncs.com/v1/models/happyoyster-directing-v1:generate`<br>• Acting：`/{WorkspaceId}.{region}.maas.aliyuncs.com/v1/models/happyoyster-acting-v1:act`（邀测端点） |
| **计费方式** | 按 **[Token](../concepts/token.md) 消耗量** 计费（输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)），不同模型单价不同（如 `qwen3.8-max` 高于 `qwen-turbo`）；多模态输入按像素/时长折算 Token；工具调用、缓存命中等不额外计费 | 按 **请求次数（Call）** 计费，与输入长度、输出复杂度无关；当前定价统一（以控制台最新公示为准）；邀测功能（如 Acting）暂不计费 |
| **状态与会话管理** | • 支持显式 Session 缓存（`x-dashscope-session-cache: enable`）<br>• Responses API 支持 `previous_response_id` 构建多轮链路<br>• `cache_control.type = "ephemeral"` 可标记缓存断点 | • **无内置会话状态管理**<br>• 所有状态（如 `world_state`、`session_id`）必须由调用方在客户端维护并显式传入每次请求<br>• Adventure/Directing 输出中不包含可复用的 session token 或 context ID |
| **典型场景** | • 智能客服问答、文档摘要、代码生成<br>• 多模态理解（图像问答、视频摘要、语音转写）<br>• 工作流自动化（调用搜索/代码解释器/知识库）<br>• 结构化数据提取（JSON Schema 输出） | • 游戏动态关卡生成与剧情分支演化<br>• 教育模拟中的虚拟实验环境状态推演<br>• 多机器人协同任务调度（如仓储AGV路径规划+冲突仲裁）<br>• 虚拟角色驱动（NPC行为决策+动作执行） |

## 各方案适用场景建议

### ✅ 选择 Qwen API 当：
- 你的任务本质是 **“理解与生成”**：如将用户提问转化为答案、将图片描述为文字、将需求文档转为代码、从PDF中抽取结构化表格。
- 你需要 **灵活的输入表达**：支持自然语言指令、多轮对话、混合模态（图文音视频）输入。
- 你依赖 **外部工具协同**：需自动触发网络搜索、运行Python代码、查询向量数据库或调用自定义函数。
- 你追求 **模型生态广度**：需在千问系列与 DeepSeek/Kimi/GLM 等模型间快速切换验证效果。
- 你已有 OpenAI/Anthropic 技术栈：可零改造迁移，复用 SDK 与提示工程经验。

### ✅ 选择 世界模型 API 当：
- 你的任务本质是 **“建模与编排”**：需对一个动态变化的“世界”（如游戏地图、实验室环境、工厂产线）进行状态演化预测、多实体行为协调或单实体动作执行。
- 你拥有 **明确定义的世界状态 Schema**：能将业务域抽象为 `world_state`（实体属性+关系）、`goal`（目标条件）、`agents`（智能体集合）等结构化输入。
- 你要求 **强确定性与可追溯性**：调度结果必须满足资源约束、时序逻辑与冲突消解规则，且每步输出可被下游系统直接解析执行。
- 你构建的是 **多阶段智能体系统**：例如先用 Adventure 生成剧情分支 → 再用 Directing 分配角色任务 → 最后用 Acting 驱动具体角色说话/移动/交互。
- 你愿意承担 **额外的状态管理成本**：自行持久化 `world_state`、处理超时重试、实现会话一致性校验。

### ⚠️ 不建议混用或替代的场景：
- **不要用 Qwen API 替代 World Model 的 Directing**：Qwen 可“描述”调度方案，但无法保证资源占用率≤100%、时间窗不重叠、优先级冲突已仲裁——这些是 Directing 的硬性约束求解能力。
- **不要用 World Model API 替代 Qwen 的多模态理解**：World Model 输入必须是结构化 JSON，无法直接接收原始图片 URL 或音频 Base64，需前置用 Qwen-VL/Qwen-Audio 提取特征后再构造 `input`。
- **避免在无状态服务中直接调用 Acting**：因其不维护会话，若两次请求 `action_context` 语义断裂（如前次说“开门”，后次说“进入房间”但未传门状态），将返回 `422` 错误。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| 构建一个支持上传截图并解释问题的客服助手 | ✅ Qwen API（`qwen3-vl-plus` + OpenAI 兼容） | 直接支持 `image_url` 输入，返回自然语言解答，无需手动解析图像特征 |
| 开发一款 Roguelike 游戏，每次进入新区域需生成独特地形+怪物+事件 | ✅ World Model API（`happyoyster-adventure-v1`） | Adventure 模块专为“世界状态→场景演化”设计，输出含 `terrain_type`、`encounter_pool`、`event_trigger` 等结构化字段，便于游戏引擎直接加载 |
| 实现跨部门会议纪要自动归档：识别发言人、提取待办、关联项目管理系统 | ✅ Qwen API（`qwen3.8-max` + `function` 工具调用） | 可用 `web_search` 查项目编号，`code_interpreter` 解析时间格式，`file_search` 匹配历史纪要，最终用 JSON Schema 输出标准字段 |
| 设计智能仓储系统：100台AGV需在3分钟内完成200个订单分拣，避开拥堵区 | ✅ World Model API（`happyoyster-directing-v1`） | Directing 内置资源约束求解器，输入 `agents`（AGV列表）、`tasks`（订单）、`map_constraints`（禁行区），输出带时间戳的 `execution_sequence`，精度与实时性远超 LLM 自由生成 |
| 创建虚拟教师，能根据学生答题情况动态调整讲解策略与演示动画 | ⚠️ **组合使用**：<br>• 用 Qwen API（`qwen3.8-omni-flash`）理解学生文本/语音作答<br>• 提取关键概念后，调用 World Model API（`adventure-v1`）生成教学路径分支<br>• 最终用 `acting-v1` 驱动虚拟人执行“板书”、“播放动画”、“提问”等原子动作 | 单一 API 无法覆盖“感知→决策→执行”全链路；Qwen 负责认知层，World Model 负责行为层，二者通过结构化中间表示（如 `concept_graph`、`teaching_step`）衔接 |

> **最后建议**：在 POC 阶段，优先用 Qwen API 快速验证业务逻辑可行性；当系统演进至需要**确定性行为编排**、**多智能体协同**或**世界状态一致性保障**时，再引入 World Model API 作为能力升级。两者非竞争关系，而是百炼平台面向不同抽象层级提供的互补能力组件。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)


