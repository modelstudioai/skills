# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，包括剧情推演、角色行为调度和场景动态控制等。该接口当前以邀测形式开放，支持多阶段协同建模，适用于游戏引擎集成、互动影视开发及智能 NPC 构建等场景。所有功能均基于百炼平台统一鉴权与配额体系。

## 支持的模型/功能

目前世界模型 API 覆盖三类核心能力模块，均由 HappyOyster 团队提供：

- **Adventure（剧情推演）**：支持长周期世界观演化、多线索分支预测与因果链推理，详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing（场景调度）**：提供镜头语言编排、时空节奏控制与多实体协同指令生成，详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting（角色行为）**：处于邀测阶段，支持细粒度动作序列生成与情感状态驱动的行为决策，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：文档 1 中将 Acting 模块标注为“邀测中”，但最新控制台权限策略已允许白名单用户直接调用 `/v1/acting/generate` 端点——请以 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中的 `x-bailian-permission: acting-beta` 请求头要求为准，而非界面提示。

## 关键参数

所有世界模型 API 共享以下必需参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`world-model-happyoyster-adventure`、`world-model-happyoyster-directing` 或 `world-model-happyoyster-acting` |
| `input.world_state` | object | 是 | 当前世界快照（JSON Schema 见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的 `WorldState` 定义） |
| `input.context` | array[object] | 否 | 最近 N 轮交互历史，每项含 `role`（"user"/"assistant"/"director"）与 `content` |
| `parameters.temperature` | number | 否 | 默认 0.7；Acting 模块建议 ≤0.4 以保障行为一致性 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>`，API Key 需具备 `world-model` 权限范围  
2. **请求示例（Adventure）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/adventure \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "world-model-happyoyster-adventure",
           "input": {
             "world_state": { "time": "2024-06-01T14:30:00Z", "entities": [...] },
             "context": [{"role":"user","content":"主角进入废墟"}]
           },
           "parameters": {"temperature": 0.6}
         }'
   ```
3. 响应结构统一遵循 `output.result` 字段返回结构化动作指令或状态更新，具体格式参见各子模块文档。

## 限制和注意事项

- 单次请求 `input.world_state` 不得超过 8KB，嵌套深度 ≤7 层  
- Adventure 与 Directing 模块支持最大上下文长度 4096 tokens；Acting 模块限 2048 tokens（因行为序列需高确定性）  
- 所有世界模型调用计入 `world-model` 独立配额池，不与 `qwen-max` 等通用模型共享——配额详情见控制台「用量管理」页  
- 若遇到 `429 Too Many Requests`，需检查是否误复用同一 `world_state.id` 进行高频重放推演；建议为每次推演生成唯一 `trace_id` 并记录至日志  

> **注意**：原始文档未明确说明 `world_state` 的校验规则，但实际接口会拒绝含非法时间格式（如 `"2024/06/01"`）或缺失 `entities` 字段的请求。该行为已在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的「输入验证」章节补充说明。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


