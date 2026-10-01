# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，当前聚焦于冒险（Adventure）、导演（Directing）两类核心场景，支持结构化剧情推演、角色行为决策与多模态指令编排。该 API 为百炼平台内测能力，需申请权限后使用。详细接口定义与参数说明请参考 [原文标题](../../raw/model-api-reference/world-model-api-reference.md)。

## 支持的模型/功能

- **Adventure 模型**：用于生成动态剧情分支、环境响应与玩家交互反馈，适用于文字冒险、教育模拟等场景。  
- **Directing 模型**：用于解析导演意图、生成分镜脚本、协调角色动作与镜头调度，适用于虚拟制片与AIGC视频预演。  
- **Acting 模型（邀测中）**：面向角色实时表演建模，支持情绪驱动的动作与语音协同生成；当前仅对白名单用户开放，具体能力以 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 为准。

> **注意**：原始文档中将 Acting 模型标注为“邀测中”，但部分内部 SDK 文档已默认启用该模型入口。实际调用前请务必确认账户权限状态，避免 403 错误。

## 关键参数

所有世界模型 API 均遵循统一基础参数规范：
- `model`: 必填，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`（后者需权限）  
- `input`: 必填，结构化 JSON 对象，格式依模型类型而异（详见各 OpenAPI 参考）  
- `stream`: 可选，布尔值，仅 Adventure 和 Directing 支持流式响应；Acting 模型暂不支持流式（参见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)）  
- `max_tokens`: 建议显式指定，避免超长输出导致截断或超时  

## 使用方式

1. 确认已开通世界模型服务权限（控制台 → API 权限管理 → “世界模型”）  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`  
3. 在请求头中携带 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`  
4. 请求体示例（Adventure）：
   ```json
   {
     "model": "happyoyster/adventure",
     "input": {
       "scene": "forest_clearing",
       "player_action": "examine the old chest",
       "world_state": {"items": ["key", "map"], "enemies": []}
     }
   }
   ```

## 限制和注意事项

- 单次请求 `input` 字段总 token 数上限为 8192（含结构开销），超出将返回 `400 Bad Request`  
- Adventure 与 Directing 模型最大输出长度为 2048 tokens；Acting 模型当前限制为 512 tokens（以实际响应为准）  
- 所有模型均不支持系统提示词（`system` 字段被忽略），世界状态与指令必须通过 `input` 显式传递  
- 调用频率限制：默认 5 QPS / 账户，如需提升请提交工单申请  
- 注意模型间输入 schema 差异显著，切勿复用 Adventure 的 input 结构调用 Directing 接口——此类错误在日志中表现为 `invalid_input_schema`，调试时请严格对照各 OpenAPI 文档

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


