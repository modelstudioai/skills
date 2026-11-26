# world model api reference

世界模型 API 提供面向游戏化、叙事交互场景的多模态推理与行为生成能力，支持剧情推演、角色调度、动作决策等核心功能。当前以 HappyOyster 系列为主要实现载体，涵盖 Adventure（剧情推演）、Directing（场景调度）和 Acting（角色动作生成）三类子服务。所有接口均基于 RESTful 设计，需通过 API Key 鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于长周期剧情状态建模与分支推演，支持时间线锚定、因果链回溯及多结局概率预测。  
- **Directing 模型**：负责跨角色、跨场景的指令编排与资源协调，例如镜头切换、NPC 位置同步、环境状态广播等。  
- **Acting 模型**（邀测中）：生成细粒度角色行为序列（含肢体动作、语音节奏、微表情时序），当前仅对白名单用户开放。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中描述的 `action_duration_ms` 参数在 v2.3.1 版本后已弃用，实际应使用 `timing_profile` 字段替代；请以 [Adventure Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的参数规范为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `world_state_id` | string | 是 | 全局唯一世界快照 ID，由上一次响应返回或通过 `/state/init` 创建 |
| `context_window` | integer | 否 | 推理上下文长度（token），默认 4096，最大 8192（Adventure/Directing）或 2048（Acting） |
| `temperature` | number | 否 | 采样随机性，范围 [0.0, 2.0]，默认 0.7；Acting 模型建议 ≤1.0 以保障动作连贯性 |
| `response_format` | string | 否 | 可选 `"json"` 或 `"protobuf"`，默认 `"json"`；若选 `"protobuf"`，需在 `Accept` header 中声明 `application/x-protobuf` |

## 使用方式

1. 初始化世界状态：`POST /v1/world/state/init`，传入初始场景描述与角色配置；  
2. 调用具体模型：如 `POST /v1/world/adventure/step`（Adventure）、`POST /v1/world/directing/plan`（Directing）；  
3. 携带认证头：`Authorization: Bearer <your_api_key>`；  
4. 响应体包含 `next_world_state_id`，用于链式调用。完整请求示例见 [Directing Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 限制和注意事项

- 单次请求最大输入长度为 16KB（UTF-8 编码），超长文本需预截断或分块；  
- Acting 模型调用频率限制为 5 QPS/项目，且不支持流式响应；  
- 所有模型均不保留客户端侧会话状态，`world_state_id` 是维持世界一致性的唯一凭证；  
- 若连续 3 次请求返回 `429 Too Many Requests`，需退避至少 1 秒再重试；  
- 注意：[Adventure Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中提及的 `enable_debug_trace=true` 参数在生产环境将被忽略，仅测试环境生效。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


