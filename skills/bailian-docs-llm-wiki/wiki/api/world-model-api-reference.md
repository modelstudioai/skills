# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的鉴权与错误码规范。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing**：用于多角色协同调度、镜头语言编排与节奏控制，适用于影视化叙事或虚拟演出编导；参考 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting**（邀测中）：用于单角色实时情绪建模、台词生成与微表情驱动，依赖前置的 Adventure 与 Directing 输出作为上下文约束；参考 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：`Acting` 模块文档中声明“支持[流式输出](../concepts/streaming.md)”，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确指出其响应为全量同步返回，且未定义 `stream` 参数——实际调用时启用 `stream=true` 将被忽略并返回 400 错误。

## 关键参数

所有接口共用以下必需参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`world-model-happyoyster-v1`（暂不支持其他别名） |
| `input` | object | 是 | 结构化输入，具体 schema 因功能类型而异（详见各子文档） |
| `parameters.temperature` | number | 否 | 默认 `0.7`，范围 `[0.0, 1.5]`；`Acting` 模块建议 ≤0.5 以保障角色一致性 |

此外，`Acting` 接口要求 `input.context_id` 必须为上游 `Adventure` 或 `Directing` 调用返回的 `task_id`，否则返回 `INVALID_CONTEXT` 错误。

## 使用方式

1. 通过百炼控制台申请世界模型 API 权限（路径：**模型服务 > 世界模型 > 申请邀测**）  
2. 获取 API Key（位于**账号设置 > API 密钥管理**）  
3. 发送 POST 请求至对应 endpoint（如 `/v1/adventure`），示例：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/adventure \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "world-model-happyoyster-v1",
           "input": { "world_seed": "cyberpunk_2077", "n_branches": 3 },
           "parameters": { "temperature": 0.6 }
         }'
   ```

## 限制和注意事项

- 单次请求 `input` 总 token 数上限为 8192；超出将触发 `INPUT_LENGTH_EXCEEDED` 错误  
- `Adventure` 与 `Directing` 接口最大响应时长为 30 秒，超时返回 `TIMEOUT`；`Acting` 为 15 秒（因其强实时性要求）  
- 所有接口均不支持跨区域调用：若在 `cn-shanghai` 区域申请权限，则必须使用 `https://dashscope.aliyuncs.com/api/v1/...`（而非国际站域名）  
- 请勿缓存 `Acting` 接口响应结果用于长期角色扮演——[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 明确说明其输出含时效性状态签名，过期后不可复用

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


