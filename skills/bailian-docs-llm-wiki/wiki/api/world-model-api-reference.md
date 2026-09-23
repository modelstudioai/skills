# world model api reference

世界模型 API 提供面向仿真、游戏与交互式叙事场景的多模态建模能力，支持环境演化、角色行为决策与动态剧情生成。当前以 HappyOyster 系列模型为核心实现，涵盖 Adventure（探索建模）、Directing（叙事调度）和 Acting（角色实时动作生成）三类功能。所有接口均通过标准 HTTP POST 调用，需携带 `Authorization` 与 `Content-Type: application/json` 头。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态演化与玩家意图推理，适用于沙盒类仿真环境。  
- **Directing 模型**：负责多角色叙事节奏控制、冲突触发与分支剧情编排，输出结构化导演指令。  
- **Acting 模型**：处于邀测阶段，提供低延迟角色动作序列生成（如肢体姿态、微表情、语音同步信号），详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的最新修订版（2024-05-12）已包含 Acting 的预注册接入流程，实际可用性请以控制台权限为准。

## 关键参数

所有请求共用以下必需参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 输入上下文，结构依模型而异；Adventure 接受 world_state + player_action，Directing 接受 scene_graph + narrative_goals |
| `stream` | boolean | 否 | 默认 `false`；仅 Directing 模型支持流式响应（逐句输出导演指令） |
| `max_tokens` | integer | 否 | 最大输出 token 数，Adventure 建议 ≤ 512，Directing ≤ 1024，Acting 不支持该参数 |

详细参数定义请参阅 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的「Request Body」章节。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建，确保已开通 `world-model` 权限组。  
2. 构造请求：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "happyoyster-directing",
           "input": {"scene_graph": {...}, "narrative_goals": ["resolve_conflict"]},
           "stream": false
         }'
   ```
3. 解析响应：返回 `output.choices[0].message.content`（字符串）或 `output.choices[0].message.delta`（流式 chunk）。完整响应格式见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的「Response Format」节。

## 限制和注意事项

- 单次请求 `input` 总长度（含 JSON 序列化后）不得超过 8192 字符；超长 world_state 需先调用 `/v1/services/aigc/world-model/compress` 预处理。  
- Acting 模型暂不支持 `stream=true`，且输入中 `player_action` 字段必须为非空字符串（即使为占位符 `"idle"`）。  
- 所有模型均不支持跨会话状态持久化，需由客户端维护 `session_id` 并在每次请求 `input` 中显式传入。  
- 错误码 `429 Too Many Requests` 表示当前 [Token](../concepts/token.md) 速率超限（默认 5 QPS），非配额耗尽；配额详情请查阅控制台「用量统计」页。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


