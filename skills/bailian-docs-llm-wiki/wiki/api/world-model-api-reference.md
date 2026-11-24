# world model api reference

世界模型 API 提供面向游戏与交互式叙事场景的多模态建模能力，支持剧情生成、角色行为决策、场景动态演化等核心功能。当前以 HappyOyster 系列为主要实现，包含 Adventure、Directing 和 Acting 三类子模型，分别对应不同层级的叙事控制粒度。所有接口均通过标准 HTTP POST 调用，遵循 OpenAPI 3.0 规范。

## 支持的模型/功能

- **Adventure 模型**：负责宏观剧情演进与世界状态迁移，适用于章节级叙事规划。  
- **Directing 模型**：聚焦镜头调度、节奏控制与多角色协同指令生成，常用于实时交互式演出编排。  
- **Acting 模型**（邀测中）：提供单角色微观行为建模（如表情、微动作、台词情绪适配），需申请白名单访问。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中标注的 `v1.2` 接口路径与 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的 `v1.1` 路径不一致（前者为 `/v1.2/acting/generate`，后者为 `/v1.1/adventure/step`），实际调用请以最新 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的版本对齐说明为准。

## 关键参数

所有请求需携带以下通用 Header：
- `Authorization: Bearer <api_key>`  
- `Content-Type: application/json`  

必填 Body 字段（以 Adventure 为例）：
- `world_state`: JSON 对象，描述当前世界快照（含时间、地点、角色状态等）  
- `narrative_context`: 字符串，上文剧情摘要（长度 ≤ 2048 字符）  
- `max_steps`: 整数，指定本次推演步数（1–5，默认 3）  

各模型特有参数详见对应 OpenAPI 文档，例如 Acting 模型要求额外传入 `character_id` 和 `emotion_intensity`。

## 使用方式

1. 获取 API Key（通过百炼控制台 →「世界模型」→「密钥管理」）  
2. 构造请求体，确保 `world_state` 符合 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 定义的 Schema  
3. 发送 POST 请求至对应模型 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/world-model/adventure/step`）  
4. 解析响应中的 `next_world_state` 与 `narrative_output` 字段用于后续迭代  

## 限制和注意事项

- 单次请求 `world_state` 总大小上限为 8 KB；超限将返回 `400 Bad Request`  
- Acting 模型暂不支持批量角色并发调用，每次请求仅处理一个 `character_id`  
- 所有模型均不保留会话状态，需由调用方维护完整世界状态并显式传入  
- 输入文本中禁止包含未脱敏的用户隐私数据（如手机号、身份证号），否则触发风控拦截  
> **注意**：[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中“响应延迟 SLA”条款（≤ 800ms @ p95）仅适用于华东1区部署实例；跨区域调用延迟可能增加 200–500ms。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


