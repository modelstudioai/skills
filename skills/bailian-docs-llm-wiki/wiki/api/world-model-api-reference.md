# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情推演、角色行为生成与环境状态演化。当前以 HappyOyster 系列为主要实现，涵盖 Adventure、Directing 和 Acting 三类核心功能模块。所有接口均通过标准 HTTP POST 调用，需携带有效 API Key 与 JSON 格式请求体。

## 支持的模型/功能

- **Adventure 模块**：用于动态生成故事世界的状态演化与分支路径，适用于游戏叙事、互动小说等场景。  
- **Directing 模块**：聚焦于多角色协同调度与镜头语言建模，支持时间轴对齐的指令编排。  
- **Acting 模块**（邀测中）：提供细粒度角色动作、情绪与台词联合生成能力，当前仅限白名单用户调用。  
该能力体系在 [世界模型](../../raw/model-api-reference/world-model-api-reference.md) 文档中被整体定义，各子模块的 OpenAPI 规范详见其对应参考页，例如 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 关键参数

所有请求共用以下基础参数：
- `model`: 必填，取值为 `"happyoyster-adventure"`、`"happyoyster-directing"` 或 `"happyoyster-acting"`（后者需邀测权限）  
- `input`: 必填，结构化输入对象，格式依模块而异（详见各子文档）  
- `stream`: 可选，布尔值，默认 `false`；仅 Adventure 和 Directing 支持流式响应  
- `max_steps`: 可选，整数，控制推演最大步数（默认 10，上限 50）  

> **注意**：原始文档中 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 将 `max_steps` 描述为“仅影响镜头切分粒度”，而 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 明确其作用于世界状态演化深度。实际行为以 Adventure 文档语义为准，Directing 模块中该参数暂不生效。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`  
2. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. 在 Body 中传入符合对应模块 schema 的 JSON 对象  
4. 解析响应中的 `output` 字段（非流式）或逐帧处理 `event` 流（流式）  

完整请求示例与错误码说明见 [世界模型](../../raw/model-api-reference/world-model-api-reference.md) 主文档及各子模块参考页。

## 限制和注意事项

- Acting 模块处于邀测阶段，未获授权时调用将返回 `403 Forbidden`  
- 单次请求 `input` 总长度（含文本与结构化字段）不得超过 8192 字符  
- Adventure 与 Directing 模块共享配额，QPS 限制为 5，突发流量可能触发 `429 Too Many Requests`  
- 所有输出内容均基于确定性采样（`temperature=0`），不可通过参数调整随机性  

> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中提及的 `"enable_emotion_calibration": true` 参数已在 v2.3.0 后移除，当前版本忽略该字段，文档尚未同步更新。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


