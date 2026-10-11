# Qwen API 与世界模型 API 对比

本文档面向百炼平台开发者，旨在清晰对比 **Qwen API**（千问大模型通用推理接口）与 **世界模型 API**（面向交互式叙事与动态环境建模的专用推理接口）在技术定位、能力边界、协议设计及工程实践层面的关键差异。随着多模态基础模型能力持续增强，以及垂直场景化推理需求日益凸显，准确理解二者适用范畴对技术选型、架构设计与成本优化具有决定性意义。本对比基于当前（2024年Q3）百炼平台正式发布的 API 规范与控制台能力，不涉及未公开或内测中的实验性功能。

## 关键维度对比

| 维度 | Qwen API | 世界模型 API |
|------|----------|--------------|
| **核心定位** | 通用大语言/多模态模型服务接口，覆盖文本生成、视觉理解、音频处理、工具调用、深度推理等广泛AI能力 | 专用领域推理接口，聚焦**动态世界建模**（World Modeling），支持冒险生成、导演调度、角色行为决策等强状态依赖、高一致性要求的交互式叙事场景 |
| **输入格式** | 多协议支持：<br>• OpenAI 兼容：`messages` 数组（含 `role`/`content`/`image_url` 等）<br>• Anthropic 兼容：`messages` + `tools` + `system`<br>• DashScope 原生：`input`（结构化文本/图像/音视频混合体）+ `parameters`；支持 `min_pixels`/`max_pixels`/`fps` 等媒体控制参数 | 统一 JSON 结构，`input` 字段为功能定制化对象：<br>• `adventure`：`prompt` + `world_seed` + 可选 `world_state`<br>• `directing`：`current_world_state` + `action_request` + `time_delta`<br>• `acting`：`character_id` + `context_state` + `goal`；**不支持原始图像/音视频二进制输入** |
| **输出格式** | 多协议响应结构：<br>• OpenAI：`choices[0].message.content`（文本）或 `choices[0].message.content[0].text/image_url`（多模态）<br>• Anthropic：`content[0].text` 或 `content[0].type === "tool_use"`<br>• DashScope：`output.text` / `output.choices[0].message.content` / `output.usage`；**支持流式响应（`stream: true`）** | 统一 JSON 响应：<br>• `output.text`（纯文本结果）<br>• `output.world_state`（更新后的完整世界状态快照，关键字段如 `scene_id`, `characters`, `timeline`, `inventory`）<br>• **明确不支持流式响应**（`stream` 参数被忽略，仅返回完整结果） |
| **支持模型** | 全系列千问模型：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`<br>• 多模态：`qwen3-vl-plus`, `qwen3.8-omni-flash`, `QVQ`, `Qwen2.5-VL`<br>• 音频：`Qwen-Audio`（仅 DashScope 协议）<br>• 代码/数学：`Qwen-Coder`, `Qwen-Math`<br>• 第三方模型：`deepseek-v4-pro`, `glm-5.3` 等（按协议白名单限制） | 专属模型族（HappyOyster 提供）：<br>• `happyoyster-adventure-v1`（冒险生成）<br>• `happyoyster-directing-v1`（导演调度）<br>• `happyoyster-acting-v1`（角色行为，邀测中）<br>**不接入任何通用大模型，无第三方模型支持** |
| **API 端点** | 多地域专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/v1/chat/completions`（OpenAI）<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/v1/messages`（Anthropic）<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（DashScope） | 统一全局端点：<br>`https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/{function}`<br>其中 `{function}` = `adventure` / `directing` / `acting`；**不支持地域路由，强制走 `dashscope.aliyuncs.com`** |
| **计费方式** | 按 **Token 消耗量** 计费：<br>• 输入 Token（含文本、图像像素折算、音频时长折算）<br>• 输出 Token<br>• 不同模型、不同模态输入类型（如高分辨率图像）有差异化单价<br>• 支持用量配额与预算告警 | 按 **请求次数（Call）** 计费：<br>• 每次成功调用（无论 `input` 大小或 `output` 长度）计为 1 Call<br>• `adventure` / `directing` / `acting` 分别独立计费<br>• 当前无基于 Token 的细粒度计费策略 |
| **典型场景** | • 智能客服对话系统<br>• 多模态内容审核与摘要<br>• Agent 工具调用（搜索/代码执行/网页抓取）<br>• 音视频理解与生成（字幕、描述、剪辑建议）<br>• 数学推理、编程辅助、文档分析 | • 游戏 NPC 动态行为引擎<br>• 互动小说/文字冒险游戏后端<br>• 影视分镜与剧情推演系统<br>• 教育类情境模拟（如历史事件沙盘、科学实验推演）<br>• 虚拟角色社交平台的世界状态同步服务 |
| **状态管理** | 无内置会话状态；需客户端通过 `messages` 数组维护上下文（如将历史消息作为 `user`/`assistant` 传入）；`cache_control` 可启用显式缓存 | **强状态依赖**：必须由客户端完整传递并接收 `world_state`；服务端不存储任何会话数据；`world_state` 是 JSON Schema 定义的结构化对象，包含时间线、角色状态、环境变量等，**一致性完全由客户端保障** |
| **工具调用能力** | 内置丰富工具：<br>• `web_search`, `code_interpreter`, `web_crawler`（Responses API）<br>• 自定义 Function Calling（OpenAI/Anthropic 协议）<br>• 工具调用可嵌套、可异步、可流式返回中间结果 | 无通用工具调用机制；所有“工具”能力已内化为模型功能：<br>• `adventure` 内置世界规则推演<br>• `directing` 内置多角色冲突消解与时间同步<br>• `acting` 内置角色人格一致性约束；**不可扩展自定义工具** |

## 各方案的适用场景建议

### ✅ 选择 Qwen API 当：
- 你的应用需要**通用语言理解与生成能力**（如问答、摘要、翻译、创作）；
- 输入包含**图像、视频、音频等多模态数据**，且需模型直接理解其语义；
- 业务逻辑依赖**外部工具协同**（例如实时搜索最新资讯、运行 Python 代码验证假设、解析网页表格）；
- 需要**低延迟流式响应**（如聊天界面逐字显示、代码补全实时反馈）；
- 团队已有 OpenAI/Anthropic SDK 生产经验，希望最小化迁移成本；
- 成本敏感且请求内容长度波动大——按 Token 计费在短文本/低复杂度任务中更具弹性。

### ✅ 选择 世界模型 API 当：
- 你的核心需求是构建一个**持久、连贯、可演化的虚拟世界**（如游戏世界、教育沙盒、叙事引擎）；
- 应用逻辑高度依赖**跨请求的状态一致性**（例如角色记忆、环境变化、时间流逝），且你有能力在客户端安全维护和序列化 `world_state`；
- 场景对**叙事逻辑合理性、角色行为一致性、世界规则自洽性**要求远高于通用文本流畅度；
- 无需处理原始音视频文件，输入以结构化提示（`prompt`）和状态快照（`world_state`）为主；
- 团队具备较强的**状态机设计与 JSON Schema 管理能力**，能应对 `world_state` 字段变更（如 `current_scene` → `scene_id`）；
- 业务模型更适配**固定调用频次预估**（如每用户每分钟 3 次冒险生成），而非按 Token 精细结算。

### ⚠️ 不推荐混用或强行替代的情况：
- **不要用 Qwen API 替代世界模型 API 实现长期世界演化**：Qwen 缺乏原生世界状态抽象，强行用 `messages` 拼接状态易导致上下文爆炸、逻辑断裂、一致性崩溃；
- **不要用世界模型 API 替代 Qwen API 处理通用 NLP 任务**：它不支持文本分类、情感分析、实体识别等标准任务，也无多模态理解能力；
- **避免在世界模型 API 中尝试注入非结构化长文本作为 `prompt`**：单次请求 `input` 严格限制 8192 字节，超限即失败；而 Qwen API 可轻松处理万字文档。

## 技术选型参考（给开发者的行动指南）

1. **先明确问题本质**：  
   > 你的需求是「让模型回答一个问题」，还是「让模型维持一个活的世界」？  
   若答案偏向后者，世界模型 API 是唯一正解；若前者，Qwen API 是首选。

2. **检查输入/输出契约**：  
   - 若输入含 `image_url`、`audio_url` 或需 `fps` 控制 → 必选 Qwen API（DashScope 或 OpenAI 协议）。  
   - 若输出必须包含 `world_state` 字段且需客户端持久化 → 必选世界模型 API。

3. **评估工程负载**：  
   - 选用世界模型 API 意味着你承担 `world_state` 的**序列化、版本兼容、冲突合并、存储与加载**全链路责任；Qwen API 则将此负担转移至上下文管理（更轻量但无状态保证）。

4. **验证权限与开通路径**：  
   - Qwen API 开通即用（控制台启用对应模型即可）；  
   - 世界模型 API 需**单独提交邀测申请**，`acting` 接口目前仅对白名单开放，务必提前规划接入周期。

5. **性能与调试建议**：  
   - Qwen API 推荐使用 DashScope SDK（原生支持多模态与高级参数），避免自行拼接 OpenAI 兼容请求；  
   - 世界模型 API 调试时务必校验 `/openapi.json` 获取实时 Schema，并用 `world_state` 的最小可行快照启动测试（避免初始状态过大导致 400 错误）。

6. **未来演进提示**：  
   - Qwen API 正持续扩展 `reasoning.effort`、`vl_high_resolution_images` 等深度控制能力，适合追求极致推理质量的场景；  
   - 世界模型 API 的 `acting` 接口正在扩大邀测范围，关注控制台「世界模型」服务页的更新公告。

---  
*本文档最后更新于 2024年10月*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)


