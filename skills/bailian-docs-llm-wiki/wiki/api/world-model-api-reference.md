# world model api reference

世界模型 API 提供面向游戏与交互式叙事场景的多模态建模能力，支持剧情生成、角色行为决策、场景动态演化等核心功能。当前以 HappyOyster 系列为主要实现，包含 Adventure、Directing 和 Acting 三类子模型，分别对应不同层级的叙事控制粒度。所有接口均通过标准 HTTP POST 调用，遵循 OpenAPI 3.0 规范。

## 支持的模型/功能

- **Adventure 模型**：负责宏观剧情演进与世界状态迁移，适用于章节级叙事规划。  
- **Directing 模型**：聚焦镜头调度、节奏控制与多角色协同指令生成，常用于实时交互式演出编排。  
- **Acting 模型**（邀测中）：提供单角色微观行为建模（如表情、微动作、台词情绪适配），需申请白名单访问。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中标注的 `v1.2` 接口路径与 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的 `v1.1` 路径不一致（前者为 `/v1.2/acting/generate`，后者为 `/v1.1/adventure/step`），实际调用请以最新 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的版本对齐说明为准。

## 关键参数

所有请求需携带以下通用 Header：
- `Authorization: Bearer <api_key>`（必填）
- `Content-Type: application/json`（必填）

共性 Body 参数包括：
- `world_state`: JSON 对象，描述当前世界快照（必填，结构详见各子模型文档）  
- `context_window`: 整数，指定上下文窗口长度（单位：token），默认 `2048`，最大 `8192`  
- `temperature`: 浮点数，控制输出随机性（`0.0`–`1.5`），默认 `0.7`  

模型特有参数见对应 OpenAPI 文档，例如 Acting 模型额外要求 `character_id` 和 `emotion_intensity` 字段。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建，权限需勾选 `world-model:read`  
2. 构造请求：根据目标模型选择对应 endpoint（如 Adventure 使用 `POST https://dashscope.aliyuncs.com/api/v1.1/adventure/step`）  
3. 发送并解析响应：成功返回 `200 OK`，`response.choices[0].message.content` 为结构化 JSON 输出，含 `next_world_state` 与 `narrative_actions` 字段  

示例 cURL（Adventure）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1.1/adventure/step" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "world_state": {"scene": "forest", "characters": ["hero", "villain"]},
        "temperature": 0.5
      }'
```

## 限制和注意事项

- 单次请求 `world_state` 大小上限为 512 KB；嵌套深度不得超过 12 层  
- Acting 模型目前仅支持中文输入与输出，且不兼容 `stream=true` 流式响应（该限制未在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中明确说明，但实测会返回 `400 Bad Request`）  
- 所有模型均不支持跨会话状态持久化，`world_state` 必须由客户端完整维护并每次显式传入  
- 超时时间为 30 秒，超时后服务可能已执行部分计算但不保证返回结果一致性

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


