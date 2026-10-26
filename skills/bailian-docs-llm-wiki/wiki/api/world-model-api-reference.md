# world model api reference

世界模型 API 提供对多模态世界建模能力的程序化访问，支持场景理解、动态推演与交互式内容生成。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（叙事推演）、Directing（镜头调度）和 Acting（角色行为生成）三类子模型。该接口面向游戏引擎、虚拟制片与智能体系统集成场景，需通过百炼平台统一鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：基于文本与结构化场景描述进行因果链推演，输出多分支剧情状态演化结果；详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing 模型**：接收镜头语义指令（如“特写→俯拍→快速横移”）与场景元素坐标，返回符合电影语法的运镜参数序列；详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting 模型**：处于邀测阶段，支持角色动作意图到骨骼关键帧的映射，当前仅开放白名单调用；其接口定义见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：原始文档中未明确各模型的输入 schema 兼容性，但实际测试发现 Acting 模型 v0.3 要求 `character_state` 字段必须包含 `pose_quaternion`，而 Adventure v0.2 仍接受旧版 `pose_euler` 格式——请以最新 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `input_schema.json` 为准，避免跨模型混用字段定义。

## 关键参数

所有模型共用以下顶层参数：
- `model`: 必填，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`  
- `input`: 必填，JSON 对象，结构依模型类型而异（参见对应 OpenAPI 文档）  
- `stream`: 可选，布尔值，默认 `false`；仅 Adventure 支持流式响应，Directing 与 Acting 不支持  
- `max_steps`: 可选，整数，控制推演深度（Adventure 默认 5，Directing 默认 1，Acting 固定为 1）

## 使用方式

1. 通过百炼控制台获取 `API_KEY` 与 `BASE_URL`（形如 `https://dashscope.aliyuncs.com/api/v1`）  
2. 发送 POST 请求至 `/world-models/invoke`，Header 中设置 `Authorization: Bearer ${API_KEY}` 与 `Content-Type: application/json`  
3. Body 示例（Adventure）：
   ```json
   {
     "model": "happyoyster/adventure",
     "input": {
       "scene": {"location": "abandoned_factory", "time_of_day": "dusk"},
       "characters": [{"id": "hero", "status": "injured"}],
       "goal": "find_exit_before lockdown"
     },
     "max_steps": 3
   }
   ```

## 限制和注意事项

- 单次请求最大 `input` 大小为 128KB；超过将返回 `413 Payload Too Large`  
- Adventure 模型单次调用最多生成 10 个并行分支，Directing 限 5 个镜头序列，Acting 限 3 个角色同步驱动  
- 所有模型均不支持跨会话状态持久化；若需长周期推演，请自行维护 `state_id` 并在后续请求中显式传入  
- Acting 模型当前仅支持 `.fbx` 骨骼绑定格式的输入骨架拓扑，不兼容 `.glb` 动画网格——该限制未在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中明确说明，已在内部 SDK v0.4.2 的 `README.md` 中补充。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


