# Qwen 大模型、World Model 与 Decision Model 对比

为帮助开发者在百炼平台中快速识别并选用最匹配业务需求的模型能力，本文对三类核心推理服务——**Qwen 大模型（通用大语言模型）**、**World Model（世界模型，面向交互式仿真）** 和 **Decision Model（决策模型，面向结构化判断）** 进行系统性对比。该对比基于当前（2024年Q3）百炼平台正式发布的 API 能力、协议规范与运行约束，聚焦技术选型关键维度，避免功能重叠导致的误用或性能浪费。

---

## 关键维度对比

| 维度 | Qwen 大模型 | World Model | Decision Model |
|------|-------------|-------------|----------------|
| **定位与本质** | 通用大语言模型（LLM），支持文本生成、多模态理解、工具调用与复杂推理 | 专用仿真建模模型，面向动态环境演化、角色行为推演与叙事控制 | 专用结构化决策模型，一次前向计算同步输出分类/是非/评分及其完整概率分布 |
| **输入格式** | 多协议灵活支持：<br>• OpenAI：`messages` 数组（含 `role`/`content`/`tool_calls`）<br>• Anthropic：`system` + `messages` + `input`<br>• DashScope 原生：`input`（string/object）、`parameters`；多模态需显式传入 base64 或 URL | 固定 JSON 对象：<br>`{ "model": "...", "input": { "world_state": {...}, "prompt": "...", "history": [...] } }`<br>`world_state` 为结构化环境快照，`prompt` 为动作指令 | 固定 TypeSafe System One 格式：<br>`{ "model": "decision-model-preview", "state": ..., "questions": { "q1": { "type": "choice", "criteria": [...] }, ... } }`<br>`state` 可为字符串、对象或数组；`questions` 定义待解问题类型与语义约束 |
| **输出格式** | 文本流或 JSON 对象：<br>• Chat：`choices[0].message.content`（文本）<br>• Responses：支持 `tool_use`、`response_id`、`thinking` 等结构化字段<br>• 多模态：返回 `output.text` + `output.media`（如 `image_urls`） | JSON 对象，含明确语义字段：<br>• Adventure：`output.action_sequence`（事件链数组）<br>• Directing：`output.scene_plan`（镜头/节奏/角色调度）<br>• Acting：`output.animation_clip_id`（动作片段 ID）<br>**无自由文本生成** | 纯结构化 JSON，**零文本生成**：<br>• `choice`: `{ "selected": "tier2", "probabilities": {"tier1":0.12,"tier2":0.78,...}, "confidence": 0.92 }`<br>• `noul`: `{ "noul": 0.87 }`（P(yes)）<br>• `score`: `{ "weighted_score": 3.2, "probabilities": [0.05,0.15,0.62,0.18], "legend": ["low","medium","high","critical"], "confidence": 0.89 }` |
| **支持模型** | 全系千问模型：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`, `qwen3.6-flash`, `qwen-coder-flash`<br>• 多模态：`qwen3.8-omni-flash`, `qwen3-vl-plus`, `qwen3.5-ocr`<br>• 第三方：DeepSeek v4、Kimi k3/k3.1-pro、GLM-5.x 等（部分能力受限） | HappyOyster 系列专属模型：<br>• `happyoyster-adventure`（开放世界演化）<br>• `happyoyster-directing`（全局叙事编排）<br>• `happyoyster-acting`（单角色实时动作，邀测中） | 仅 `decision-model-preview`（预览版），无变体或历史版本 |
| **API 端点（典型）** | • OpenAI 兼容：`/{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Anthropic 兼容：`/{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic/v1/messages`<br>• DashScope 原生：`/{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model`<br>（统一入口，通过 `model` 字段路由） | `/{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`<br>（TypeSafe System One 协议） |
| **计费方式** | 按 **输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)** 计费（含思考 [Token](../concepts/token.md)）；多模态按像素/帧数额外计费；不同模型单价差异显著（如 `qwen3.8-max` > `qwen3.6-flash`） | 按 **请求次数** 计费；无 Token 或像素计费项；`world_state` 大小影响序列化开销但不改变计费粒度 | 按 **请求次数** 计费；与输入长度、问题数量、输出复杂度无关；超长 `state`（>65536 token）直接拒绝，不计费 |
| **典型场景** | • 智能客服对话<br>• 多文档摘要与问答<br>• 代码生成与解释<br>• 图像/视频内容理解<br>• Agent 工具调用（搜索、计算、文件分析） | • 游戏 NPC 行为推演与状态更新<br>• 交互式叙事引擎（如文字冒险、虚拟导演）<br>• 沙盒仿真环境中的事件链生成（如“玩家进入洞穴→触发陷阱→蝙蝠群袭”）<br>• 影视分镜自动编排（镜头切换、角色走位） | • 工单智能分级与路由（“紧急/高/中/低”）<br>• 内容安全审核（“涉政/涉黄/正常”+置信度）<br>• Agent 执行完成度校验（“已完成/进行中/失败”）<br>• 任务优先级打分（0–5 分量表） |

---

## 各方案适用场景建议

### ✅ 推荐使用 Qwen 大模型，当：
- 业务需要**自然语言交互能力**（如对话、写作、翻译）；
- 需要**多模态理解**（图文/音视频解析、OCR、文档结构化）；
- 场景涉及**工具调用与自主规划**（如联网搜索、代码执行、文件分析）；
- 对输出形式无强结构化要求，接受文本流或自由格式响应；
- 开发者已有 OpenAI/Anthropic SDK 集成经验，追求快速迁移。

> ⚠️ 注意：若仅需简单分类或打分，使用 Qwen 会显著增加延迟、成本与后处理复杂度，不推荐。

### ✅ 推荐使用 World Model，当：
- 构建**动态仿真系统**（游戏、数字孪生、教育沙盒）；
- 需要**环境状态驱动的行为生成**（非静态规则，而是基于 `world_state` 的因果推演）；
- 场景强调**多实体协同与时间演进**（如“狼发现玩家→潜行接近→发动攻击”）；
- 需要**叙事层抽象控制**（如镜头语言、节奏张力、角色关系变化）；
- 已具备外部状态管理能力（`world_state` 需由业务侧维护并每次显式传入）。

> ⚠️ 注意：World Model 不适合纯文本问答、知识检索或通用生成任务；其 `input.history` 仅为上下文建模，**不持久化状态**。

### ✅ 推荐使用 Decision Model，当：
- 业务本质是**确定性结构化判断**（非生成、非探索）；
- 要求**毫秒级低延迟响应**（如实时风控、工单分派）；
- 需要**可解释的概率分布与置信度**，用于下游阈值控制、融合决策或人工复核；
- 输入上下文高度结构化或可标准化（如 JSON 工单、对话摘要、日志片段）；
- 希望规避 LLM 的幻觉、冗余输出与 token 成本波动。

> ⚠️ 注意：Decision Model **完全不生成文本**，无法用于回答开放式问题、创作或解释性输出；问题定义需提前设计好 `criteria` 映射。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐模型 | 关键理由 | 验证建议 |
|----------|-----------|-----------|-----------|
| “用户上传一张发票图片，我要提取金额、日期、供应商，并填入 ERP 表单” | ✅ Qwen（`qwen3.5-ocr` 或 `qwen3-vl-plus`） | 支持图像理解 + 结构化文本抽取 + 多轮修正；可结合 `file_search` 工具做历史比对 | 在 Playground 上传样例发票，测试 OCR 准确率与字段映射稳定性 |
| “开发一款文字冒险游戏，玩家每步操作后，世界状态（位置、物品、NPC情绪）需动态更新并生成下一步事件” | ✅ World Model（`happyoyster-adventure`） | 专为 `world_state` + `prompt` 推演设计；输出 `action_sequence` 直接驱动游戏逻辑；无需自行编写状态转移规则 | 构造最小 `world_state`（如 `{"location":"castle","items":["key"],"npcs":{"guard":{"mood":"angry"}}}`），测试“用钥匙开门”是否触发合理事件链 |
| “客服工单系统需自动判断：① 是否需升级至专家？② 属于哪个产品线？③ 用户情绪等级（1–5）？” | ✅ Decision Model | 三类问题（`noul`/`choice`/`score`）可一次请求并行求解；返回概率分布便于设置动态阈值（如 P(升级) > 0.85 才转交）；65536 token 上下文足够容纳完整工单文本 | 使用 Playground 的「工单分流」预设模板，调整 `instructions` 强化领域术语（如“专家=高级技术支持工程师”），观察置信度变化 |
| “我已有 OpenAI SDK，想快速替换为百炼服务，保持现有聊天接口不变” | ✅ Qwen（OpenAI 兼容协议） | 完全兼容 `/v1/chat/completions`，仅需更换 Base URL 与 API Key；支持 `stream`、`function_call` 等全部 OpenAI 字段 | 替换 endpoint 后运行回归测试，重点验证 `tool_calls` 解析与 `previous_response_id` 会话连续性 |
| “需要为短视频自动生成分镜脚本：包含镜头类型、时长、主体动作、BGM 建议” | ✅ World Model（`happyoyster-directing`） | `Directing` 模型专精于多模态叙事编排；输入视频描述 + 风格要求，输出结构化 `scene_plan`，可直接对接剪辑 API | 提供 3 种不同风格提示（如“科技感快剪”、“温情慢镜头”、“悬疑蒙太奇”），对比输出的专业性与一致性 |

> 💡 **终极选型口诀**：  
> **生成文本 → Qwen**  
> **演化世界 → World Model**  
> **做出决定 → Decision Model**  
> 三者能力正交，极少重叠；混合使用时（如 World Model 输出事件 → Qwen 生成旁白 → Decision Model 判断玩家意图），请通过业务逻辑层解耦调用，避免模型职责混淆。

---  
*最后更新：2024年10月*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


