# Qwen大模型、World Model与决策模型对比

为帮助开发者在百炼平台上高效选型，本文对三类核心AI能力——通用大语言模型（Qwen）、叙事与交互式内容生成的世界模型（World Model）、以及面向结构化判断的专用决策模型（Decision Model）——进行系统性对比。随着AI应用从“生成”向“理解—推理—行动”纵深演进，不同任务范式对模型能力、接口语义与工程约束提出差异化要求。本对比聚焦实际开发视角，涵盖协议设计、输入输出契约、能力边界与落地适配性，旨在为架构设计、API集成与成本优化提供可操作的技术参考。

## 关键维度对比

| 维度 | Qwen大模型 | World Model | 决策模型 |
|------|-------------|--------------|------------|
| **输入格式** | 多样化：<br>• 文本：`messages[]`（含 `system`/`user`/`assistant` 角色）<br>• 多模态：`image_url`、`video_url`、`input_audio` 等（依模型支持）<br>• 结构化提示：`output_config.format.type = "json_schema"`（Anthropic接口） | 严格结构化 JSON：<br>• 顶层 `model` + `input` 对象<br>• `input` 字段依模块而异（如 `Adventure` 含 `world_seed`、`narrative_goal`；`Directing` 含 `scene_context`）<br>• 不支持自由文本对话历史，需显式传入 `history`（若模型支持） | 高度契约化：<br>• `state`：任意类型（string/object/array），作为决策上下文（自动序列化）<br>• `questions`：对象字典，每个 question 含 `type`（`choice`/`noul`/`score`）、`instructions`、`criteria`<br>• **无 messages、无 role、无 prompt 工程空间** |
| **输出格式** | 自由文本为主，支持部分结构化：<br>• OpenAI/Anthropic 接口：`content` 字符串或 `tool_calls` 数组<br>• Anthropic Messages：可强制 `json_schema` 输出（强类型校验）<br>• DashScope 原生：支持多模态输出（如 `output.images`） | 纯 JSON 结构化响应：<br>• `Adventure`：返回 `world_graph`、`character_relations`、`branch_points` 等叙事图谱字段<br>• `Directing`：返回 `dialogue_schedule`、`camera_actions`、`timing_map` 等导演指令<br>• **不生成自然语言描述，所有字段语义明确、可解析** | 100% 结构化、零文本输出：<br>• 每个问题返回确定性结果：<br> - `choice`：`selected_option` + `probabilities` + `confidence`<br> - `noul`：`yes_probability`（0.0–1.0）<br> - `score`：`expected_score` + `level_probabilities` + `confidence`<br>• **无 `content`、无 `text`、无流式 chunk，响应即最终决策** |
| **支持模型** | 多模型统一接口：<br>• Qwen 系列：`qwen3.8-max`、`qwen3-vl-plus`、`qwen3-coder-flash`、`qwen3.5-ocr` 等<br>• 第三方模型：DeepSeek、Kimi、GLM、MiniMax（部分接口受限）<br>• 多模态专属：Qwen-VL、Qwen-Omni、QVQ、QwQ、Qwen-Audio（仅 DashScope） | 模块化命名模型：<br>• `happyoyster/adventure-v1`<br>• `happyoyster/directing-v1`<br>• `happyoyster/acting-v1`（邀测中）<br>• **无通用基座模型，每个功能对应独立训练模型** | 单一预览模型：<br>• 固定 `model = "decision-model-preview"`<br>• **无版本别名、无替代型号、无多模态扩展计划** |
| **API 端点** | 多协议并行：<br>• OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（带工具链）<br>• Anthropic 兼容：`/apps/anthropic/v1/messages`<br>• DashScope 原生：`/api/v1/services/aigc/{text-generation\|multimodal-generation}/generation` | 统一端点：<br>• `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`<br>• **不区分地域，不支持 WorkspaceId 域名** | 专用端点：<br>• `POST /compatible-mode/v1/systemone`（地域专属域名，如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`）<br>• **路径固定，不可替换为其他 `/v1/xxx`** |
| **计费方式** | 按 token 计费：<br>• 输入 token（`input_tokens`）+ 输出 token（`output_tokens` 或 `max_completion_tokens`）<br>• 多模态模型按像素/帧数加权计费（如 `total_pixels`）<br>• 流式响应按实际返回 token 计费 | 按请求计费（Request-based）：<br>• 单次 API 调用计为 1 次调用，无论 `input` 大小或响应长度<br>• **无 token 拆分计费，无流式增量计费** | 按请求 + 问题数复合计费：<br>• 基础单位为「1 次请求」，但单请求内每增加 1 个 `question` 均产生额外计费单元<br>• **问题数 ≤16 为推荐区间，超量将显著提升单价与延迟** |
| **典型场景** | • 智能客服对话（多轮、工具调用）<br>• 多模态内容理解（图文问答、视频摘要）<br>• 代码生成与解释<br>• Agent 编排与自主任务执行 | • 游戏剧情动态生成与分支管理<br>• 虚拟制片中的镜头调度与角色互动编排<br>• 互动小说/AR 故事引擎的实时叙事演化<br>• AI 导演辅助系统 | • 工单智能分派（选择处理团队）<br>• 内容安全审核（是/否/不确定/可能违规）<br>• 智能体任务路由（根据状态选择下一步动作）<br>• 服务结果置信度校验（如 OCR 识别结果可信度打分） |

## 各方案适用场景建议

### ✅ 选择 Qwen 大模型，当：
- 任务本质是**开放生成、复杂推理或跨模态理解**（如：“根据这份财报PDF和会议录音，总结三大风险并生成PPT大纲”）；
- 需要**灵活的对话状态管理**（多轮上下文、记忆、工具调用闭环）；
- 已有 OpenAI/Anthropic 技术栈，追求**最小迁移成本**；
- 应用对输出形式包容性强（接受文本、JSON、[函数调用](../concepts/function-calling.md)等混合结果）。

> ⚠️ 注意：避免用于高确定性、低延迟决策（如实时风控），因文本生成存在非确定性与 token 开销。

### ✅ 选择 World Model，当：
- 核心目标是**构建动态、可交互的叙事世界**，而非回答问题或执行任务；
- 需要**领域强语义的结构化输出**（如“生成包含3个NPC、2条冲突线、5个关键抉择点的世界观”）；
- 场景具备明确创作阶段划分（世界观设计 → 镜头编排 → 角色演绎）；
- 团队具备内容策划与导演思维，而非纯软件工程背景。

> ⚠️ 注意：不适用于通用 NLP 任务（如情感分析、摘要）；当前 Acting 模块邀测中，生产环境需评估权限稳定性。

### ✅ 选择 决策模型，当：
- 业务逻辑本质是**离散分类、二元判断或有序评分**，且要求**结果可验证、可审计、可置信度量化**；
- 系统对**延迟敏感（毫秒级响应）与确定性要求极高**（如金融交易路由、医疗初筛）；
- 需要**一次请求并发处理多个正交决策问题**（如：同时判断“是否涉政”、“是否涉黄”、“严重度等级”）；
- 工程团队希望**彻底规避 prompt 工程、温度调参、输出解析等不确定性环节**。

> ⚠️ 注意：无法生成解释性文本（如“为什么判定为涉黄？”需额外调用 Qwen）；当前仅预览版，不承诺 SLA 与长期接口兼容性。

## 面向开发者的技术选型参考

| 选型考量 | Qwen | World Model | 决策模型 |
|----------|------|--------------|------------|
| **上手门槛** | ★★★★☆（协议丰富，文档成熟，SDK 支持全） | ★★☆☆☆（需理解叙事建模范式，子模块文档分散，无官方 SDK） | ★★★★☆（接口极简，`typesafe-sdk` 封装完善，Playground 可视化调试） |
| **调试效率** | 高（Playground 支持多协议实时测试、流式预览、token 统计） | 中（需按模块分别测试，无统一 Playground，错误信息偏抽象） | 极高（Playground 提供概率分布可视化、置信度热力图、问题级失败定位） |
| **可观测性** | 完整（`usage` 字段含 `input_tokens`/`output_tokens`/`cache_creation_input_tokens` 等） | 低（仅返回 `request_id` 和基础耗时，无 token/计算量指标） | 中（返回 `confidence`、各选项 `probabilities`，但无底层计算开销暴露） |
| **扩展性** | 高（支持自定义 Function Calling、MCP 工具、知识库检索） | 低（模块功能固化，暂无插件或工具链扩展机制） | 无（纯决策内核，不支持任何外部调用或状态外溢） |
| **生产就绪度** | ★★★★★（全链路监控、熔断、重试、缓存控制 `cache_control.type="ephemeral"`） | ★★☆☆☆（邀测阶段，QPS 限流严格，无会话状态保持，错误恢复需业务侧实现） | ★★★☆☆（预览版，但协议稳定、错误码完备；需自行实现 `state` 截断保护与 `questions` 规模治理） |

**最终建议**：  
- **构建 AI Agent** → 以 Qwen 为核心，World Model 作为“叙事执行器”，决策模型作为“路由中枢”；  
- **重构传统规则引擎** → 优先评估决策模型，其结构化输出天然适配数据库写入与告警触发；  
- **开发创意生产力工具** → World Model 是不可替代的原生能力，Qwen 可作为辅助解释层（如用 Qwen 解释 World Model 生成的 `branch_points`）；  
- **快速验证 MVP** → 从 Qwen Chat 接口起步（兼容 OpenAI），再按需引入 World Model 或决策模型专业化升级。  

> 所有服务均使用统一认证（`Authorization: Bearer <API Key>`），开发者可在同一项目中混合调用，通过百炼控制台统一查看用量、设置配额与配置告警。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


