# world model api reference

世界模型 API 提供面向交互式叙事与动态环境建模的推理能力，支持冒险生成、导演调度、角色行为决策等场景。当前以邀测形式开放部分功能，所有接口均基于标准 OpenAPI 规范实现。开发者需通过百炼平台申请对应模型权限后方可调用。

## 支持的模型/功能

目前世界模型 API 由 HappyOyster 团队提供，包含三类核心能力：
- **Adventure（冒险生成）**：根据用户输入构建连贯、可扩展的叙事世界与事件流；
- **Directing（导演调度）**：协调多角色状态、时间线与环境响应，维持世界一致性；
- **Acting（角色行为）**：驱动单个角色在给定情境下的细粒度动作与对话决策（当前处于邀测中，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)）。

> **注意**：[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中对 `world_state` 参数的 schema 描述存在字段命名不一致（如 `current_scene` vs `scene_id`），建议以最新 OpenAPI YAML 文件定义为准，实际请求前请校验 `/openapi.json` 响应。

## 关键参数

所有接口共用以下基础参数（除特别说明外均为必填）：
- `model`: 模型标识符，如 `happyoyster-adventure-v1`、`happyoyster-directing-v1`；
- `input`: JSON 对象，结构依功能而异，详见各子文档；
- `temperature`: 控制输出随机性，范围 `[0.0, 1.0]`，默认 `0.7`；
- `max_tokens`: 最大生成 token 数，上限为 `2048`（Acting 接口限 `1024`）。

## 使用方式

1. 在百炼控制台开通「世界模型」服务并申请对应模型权限；
2. 获取 API Key（见 [API 密钥管理](../../raw/auth/api-key-management.md)）；
3. 构造 HTTP POST 请求，`Content-Type: application/json`，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/<function>`，其中 `<function>` 取值为 `adventure`、`directing` 或 `acting`；
4. 示例请求体（Adventure）：
   ```json
   {
     "model": "happyoyster-adventure-v1",
     "input": {
       "prompt": "主角进入被遗忘的钟楼，发现三扇刻有星图的门",
       "world_seed": "20240521"
     },
     "parameters": {
       "temperature": 0.5,
       "max_tokens": 1024
     }
   }
   ```

## 限制和注意事项

- 单次请求最大 `input` 字节数为 8192；超过将返回 `400 Bad Request`；
- Acting 接口仅对白名单用户开放，未授权调用将返回 `403 Forbidden`；
- 所有世界模型接口暂不支持流式响应（`stream: true` 无效），完整结果将在 `output.text` 中返回；
- 状态一致性依赖客户端维护 `world_state` 上下文，服务端不持久化会话——此设计已在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确说明，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 未强调，开发者须主动传递完整状态快照。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


