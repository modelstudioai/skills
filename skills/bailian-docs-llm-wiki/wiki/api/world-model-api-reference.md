# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情推演、角色行为生成与环境状态演化等核心任务。当前以 HappyOyster 系列为主要实现载体，涵盖 Adventure、Directing 和 Acting 三类子模型。所有接口均通过标准 HTTP POST 调用，返回结构化 JSON 响应。

## 支持的模型/功能

- **Adventure 模型**：用于动态世界状态建模与剧情分支推演，适用于游戏叙事、交互式小说等场景。  
- **Directing 模型**：聚焦于多角色协同调度与镜头语言生成，常用于虚拟制片与AI导演工作流。  
- **Acting 模型**（邀测中）：支持细粒度角色动作、情绪与台词联合生成，当前仅对白名单用户开放。详细能力请参阅 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中将 Acting 模型标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的最新修订版（2024-05-12）已提及 Acting 模型的 beta 接口已向部分企业客户全量开放，实际可用性请以控制台权限为准。

## 关键参数

所有请求需在 `POST` body 中提供以下必选字段：
- `scene_state`: JSON 对象，描述当前世界状态（如角色位置、物品持有、情绪值等），格式详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的 `SceneStateSchema` 定义。  
- `prompt`: 文本指令，明确指定期望的模型行为（例如 `"让主角向左移动并触发机关"`）。  
- `model`: 字符串，取值为 `"adventure"`, `"directing"` 或 `"acting"`（后者需授权）。

可选参数包括 `max_steps`（默认 3）、`temperature`（默认 0.7）和 `return_trace`（布尔值，启用后返回中间推理步骤）。

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke` 发起 POST 请求；  
2. Header 中设置 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；  
3. Body 示例：
```json
{
  "model": "adventure",
  "prompt": "主角发现密室入口，需要判断是否进入",
  "scene_state": {"characters": [{"id": "hero", "x": 5, "y": 3, "health": 82}], "objects": [{"id": "door", "locked": true}]}
}
```
完整请求示例与错误码说明见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `scene_state` 最大嵌套深度为 8 层，总 JSON 大小不超过 256 KB；  
- Acting 模型调用需额外申请 `world-model-acting` 权限，未授权时返回 `403 Forbidden`；  
- 所有模型均不支持跨会话状态持久化，如需长程一致性，请自行维护 `scene_state` 并在每次请求中显式传入；  
- 当前不支持流式响应（`stream: true` 参数无效），全部结果同步返回。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


