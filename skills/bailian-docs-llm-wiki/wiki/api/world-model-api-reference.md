# world model api reference

世界模型 API 提供对多模态世界模拟能力的程序化调用，支持场景生成、角色行为编排与动态交互推演。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索推演）、Directing（叙事调度）和 Acting（角色动作生成）三类核心能力。所有接口均通过 RESTful 方式提供，需使用平台颁发的 API Key 进行鉴权。

## 支持的模型/功能

- **Adventure 模型**：用于生成符合物理规律与逻辑约束的开放世界状态演化序列，适用于沙盒环境建模与因果链推理。  
- **Directing 模型**：负责多角色叙事节奏控制、事件触发条件判定与剧情分支调度，常用于交互式故事引擎。  
- **Acting 模型**（邀测中）：面向单角色的细粒度动作生成与微表情/姿态合成，依赖前置的场景与角色状态输入。  
> **注意**：Acting 模型当前仅对白名单用户开放，其输入 schema 与 Adventure/Directing 存在显著差异，详见 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 中的子路径说明。

## 关键参数

所有请求需包含以下通用参数：
- `model`: 必填，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`  
- `input`: 必填，结构化 JSON 对象，具体字段依模型而异（如 Adventure 要求 `world_state` 和 `action_plan`；Directing 要求 `narrative_context` 和 `trigger_rules`）  
- `temperature`: 可选，控制输出随机性（0.0–1.0），默认 `0.7`；Acting 模型建议设为 ≤0.3 以保障动作连贯性  

详细参数定义请参考各子模块的 OpenAPI 文档，例如 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `RequestBody` 描述。

## 使用方式

1. 向 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke` 发起请求  
2. 请求头需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. 响应体为标准 JSON，含 `output`（模型输出）、`usage`（token 消耗）和 `request_id` 字段  
4. 错误响应遵循 RFC 7807 标准，常见错误码包括 `400 Bad Request`（参数校验失败）、`403 Forbidden`（模型未授权）及 `429 Too Many Requests`（QPS 超限）  

示例调用可直接复用 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的 `curl` 片段，但需注意 `model` 字段值须与实际调用一致。

## 限制和注意事项

- 单次请求 `input` 总长度（字符数）上限为 8192；超过将返回 `400` 错误  
- Adventure 模型不支持跨时间步长的长期状态回溯，历史状态需由客户端显式维护并传入  
- Acting 模型输出为动作 token 序列，**不包含音频或视频编码**，需配合渲染服务使用  
> **注意**：原始文档中提及的 `"Acting 模型支持实时语音驱动"` 与当前 API 实际能力不符，该描述已过时，请以 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 的最新子路径为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


