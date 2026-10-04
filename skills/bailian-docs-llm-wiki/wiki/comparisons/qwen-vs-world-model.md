# Qwen 系列模型与世界模型对比

本文旨在帮助开发者清晰区分 **Qwen 系列通用大模型** 与 **世界模型（World Model）专用引擎** 的技术定位、能力边界与适用场景，避免因概念混淆导致选型偏差。随着百炼平台能力持续演进，两类服务在目标用户、输入范式、输出语义及工程集成方式上已形成显著分野：Qwen 系列聚焦于**通用认知与多模态理解生成**，而世界模型专注于**结构化叙事空间中的动态状态推演与行为调度**。本对比基于当前（2024年Q3）百炼平台正式发布能力整理，适用于新项目技术架构设计与存量系统升级评估。

## 关键维度对比

| 维度 | Qwen 系列模型 | 世界模型 |
|------|----------------|------------|
| **核心定位** | 通用大语言模型（LLM）及多模态基础模型家族，面向文本理解、生成、推理、代码、音视频分析等广泛任务 | 面向交互式叙事系统的专用状态引擎，提供世界观演化、镜头调度、角色行为决策等三维协同建模能力 |
| **输入格式** | - OpenAI 兼容：`messages` 数组（含 `role`/`content`），支持 `system`（Responses）、工具调用（`tools`）<br>- Anthropic 兼容：`messages` + `system` 字符串/数组，支持 `output_config.effort`<br>- DashScope 原生：`input`（字符串/对象），支持细粒度图像/视频参数（`min_pixels`, `fps`, `max_frames`） | 强结构化 JSON：<br>- 必填 `input.world_state`（严格 Schema 校验，含 `time`, `entities`, `locations` 等字段）<br>- 可选 `input.context`（带 `role` 的历史交互序列）<br>- 所有字段需符合 [HappyOyster WorldState 定义](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) |
| **输出格式** | - OpenAI/Anthropic：标准 `choices[0].message.content` 或 `content` 数组（含 tool_use）<br>- DashScope：`output.text`（文本）或 `output.choices[0].message.content`（多模态）<br>- Responses API 支持结构化工具结果嵌入（如 `code_interpreter` 输出为 `execution_result`） | 统一返回 `output.result` 字段，内容为强类型 JSON：<br>- Adventure：`{ "next_state": {...}, "branch_options": [...] }`<br>- Directing：`{ "camera_actions": [...], "temporal_shift": "accelerate" }`<br>- Acting：`{ "actions": [{"type":"move","target":"door"}], "emotion": "tense" }` |
| **支持模型** | - 主流 Qwen 系列：`qwen3.8-max`, `qwen3.7-plus`, `qwen3-vl-plus`, `qwen-omni`, `qwen-coder`, `qwen-math`, `qwen-audio`<br>- 第三方直供模型（DeepSeek/Kimi/GLM/MiniMax，仅限华北2地域） | 固定三类专用模型 ID：<br>- `world-model-happyoyster-adventure`<br>- `world-model-happyoyster-directing`<br>- `world-model-happyoyster-acting`（邀测中，需白名单+`x-bailian-permission: acting-beta`） |
| **API 端点** | - OpenAI 兼容：`/v1/chat/completions`, `/v1/responses`（增强 Agent）<br>- Anthropic 兼容：`/v1/messages`<br>- DashScope 原生：`/text-generation/generation`, `/multimodal-generation/generation` | 统一基础路径 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/{module}`：<br>- `/adventure`<br>- `/directing`<br>- `/acting`（Beta） |
| **计费方式** | 按 token 计费（输入+输出 tokens），不同模型单价不同；多模态输入（图像/视频帧/音频）按等效文本 token 折算；配额计入 `qwen-*` 模块池 | 按次（per call）计费，与输入 token 长度无关；单次请求 `world_state` ≤8KB；配额独立为 `world-model` 池，不与通用模型共享 |
| **典型场景** | - 智能客服对话、文档摘要、报告生成<br>- 图像/视频内容理解（OCR、场景识别、图表分析）<br>- 代码补全与调试、数学解题、音频转写<br>- Agent 工具链编排（联网搜索、代码执行） | - 游戏引擎中 NPC 行为实时决策与剧情分支触发<br>- 互动影视中镜头语言自动生成与时空节奏控制<br>- 虚拟制片中多角色协同动作调度与情绪一致性维护<br>- 教育沙盒中动态世界状态演化与因果反馈模拟 |

## 各方案适用场景建议

### ✅ 选择 Qwen 系列模型，当您需要：
- **通用性优先**：处理开放域问答、跨领域知识推理、多轮自然对话；
- **多模态理解**：解析用户上传的图片、短视频、录音并生成语义描述或执行操作（如“分析这张财报截图”、“总结会议录音要点”）；
- **快速构建 AI Agent**：利用 Responses API 内置 `web_search`/`code_interpreter` 工具，无需自行开发插件即可实现联网检索、数据计算等能力；
- **技术栈兼容性**：已有 OpenAI 或 Anthropic SDK 生产环境，希望零改造迁移至百炼；
- **成本敏感型长文本处理**：对万字级文档摘要、法律合同审查等任务，Qwen 系列提供高性价比 token 计费模型（如 `qwen3.5-plus`）。

### ✅ 选择世界模型，当您需要：
- **强状态一致性**：构建需维持长期世界状态（时间线、实体关系、物理约束）的交互系统，例如 RPG 游戏服务器、虚拟仿真训练环境；
- **专业叙事控制**：要求输出严格遵循镜头语法（景别、运镜、焦距）、角色行为符合情感-动机-动作链（如“愤怒→握拳→逼近→低吼”）；
- **多模块协同调度**：同一请求需同时触发剧情演化（Adventure）、镜头切换（Directing）和角色微表情（Acting）三层响应；
- **确定性行为保障**：Acting 模块通过低 temperature（≤0.4）与状态校验机制，确保相同输入产生可复现的行为序列，满足游戏逻辑验证需求；
- **规避通用模型幻觉风险**：在关键叙事节点（如“主角是否死亡”），世界模型基于显式 `world_state` 推演，而非概率采样，大幅降低事实性错误。

> ⚠️ 注意：二者**不可互换替代**。试图用 Qwen 模型模拟世界状态演化将面临严重幻觉、状态漂移与性能瓶颈；反之，用世界模型处理日常客服对话则因缺乏通用知识与灵活格式支持而失败。

## 面向开发者的选型参考

| 选型问题 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| **我的应用是智能客服/知识库问答/办公助手** | Qwen 系列（推荐 `qwen3.7-plus` 或 `qwen3.8-max`） | 通用对话能力成熟，OpenAI 兼容 SDK 开箱即用，支持 `system` 提示定制人格，多模态扩展性强 |
| **我要开发一个文字冒险游戏，需根据玩家选择动态生成剧情分支与世界变化** | **组合使用**：<br>1. Qwen（`qwen3.8-max`）处理玩家自由输入理解与自然语言反馈生成<br>2. World Model（`adventure`）执行 `world_state` 推演与分支判定 | Qwen 解析模糊意图，World Model 保证状态演化的确定性与因果严谨性；二者通过 `world_state` JSON 传递结构化上下文 |
| **我需要让游戏角色在 Unity 中实时做出符合情绪的动作（如紧张时手抖、愤怒时砸桌）** | 世界模型（`acting` 模块，需申请白名单） | Acting 模块专为细粒度行为序列设计，输出含 `action_type`/`duration`/`emotion_intensity` 等游戏引擎可直接消费的字段；Qwen 无法提供此级结构化行为控制 |
| **我要分析一段 10 分钟的产品发布会视频，提取关键信息并生成PPT大纲** | Qwen 系列（`qwen3.8-omni-flash` + Responses API） | 支持视频 URL 输入 + `fps`/`max_frames` 控制，内置 `code_interpreter` 可自动整理结构化大纲，无需自研视频理解 pipeline |
| **我的系统需对接 Unreal Engine，要求每帧渲染前获取镜头运动指令（推/拉/摇/移）和焦点切换时机** | 世界模型（`directing` 模块） | Directing API 输出 `camera_actions` 数组，含 `operation`（"dolly_in"）、`target`（"character_A_head"）、`timing`（"frame_120"）等引擎原生可解析字段；Qwen 输出仅为自然语言描述，需额外 NLP 解析 |

**最终建议**：  
- **起步阶段**：优先验证 Qwen 系列能否满足核心需求（90% 的 AI 应用属于此范畴）；  
- **垂直深化**：当业务出现**强状态依赖、多实体协同、专业叙事语法**等特征时，引入世界模型作为专用子系统；  
- **混合架构**：推荐采用「Qwen 做前端理解与表达，世界模型做后端状态引擎」的分层设计，通过定义清晰的 `world_state` Schema 实现松耦合集成。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)


