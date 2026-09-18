# world model api reference

世界模型 API 提供面向交互式内容生成的多模态建模能力，支持剧情推演、角色行为决策与场景动态演化等核心任务。当前以邀测形式开放部分功能，所有接口均需通过百炼平台鉴权调用。详细协议规范与字段定义请参阅 [世界模型](../../raw/model-api-reference/world-model-api-reference.md)。

## 支持的模型/功能

- **Adventure 模型**：用于长周期剧情规划与环境状态演化，适用于游戏叙事、教育模拟等场景；文档见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing 模型**：聚焦多角色协同调度与镜头语言生成，输出结构化导演指令；文档见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting 模型（邀测中）**：驱动单角色实时响应与微表情/动作生成，当前仅限白名单用户调用；详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：`Acting` 模型在 [世界模型](../../raw/model-api-reference/world-model-api-reference.md) 中标注为“内测阶段”，但其子文档明确写明“邀测中”，二者语义一致，无实质矛盾；实际接入请以子文档的准入条件为准。

## 关键参数

所有请求需携带 `X-Model-Name`（值为 `adventure` / `directing` / `acting`）和 `X-Session-ID`（长度 32 位 hex 字符串）。  
必填请求体字段包括：  
- `scene_context`: JSON 对象，描述当前世界状态（最大嵌套深度 5，总字符数 ≤ 8192）  
- `history`: 最近 10 轮交互的数组（每项含 `role`, `content`, `timestamp`），超出部分将被截断  
- `output_format`: 可选 `"json"` 或 `"text"`，默认 `"json"`  

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/world-model` 发送 POST 请求  
2. 设置 `Content-Type: application/json` 和鉴权 Header（`Authorization: Bearer <api_key>`）  
3. 请求体示例（Adventure 场景）：  
```json
{
  "scene_context": {"location": "古堡大厅", "time": "午夜", "characters": ["侦探", "管家"]},
  "history": [{"role": "user", "content": "打开烛台", "timestamp": 1717023456}],
  "output_format": "json"
}
```

## 限制和注意事项

- 单次请求 `scene_context` + `history` 总 token 数上限为 4096（按 dashscope tokenizer 计算）  
- `Acting` 模型不支持流式响应，且每次调用必须指定 `character_id`（需提前在控制台注册角色）  
- 所有模型均不支持跨 session 状态持久化，世界状态需由客户端显式维护并随每次请求传入  
- 若发现 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `max_steps` 参数说明与实际返回 `422` 错误提示不一致，请以错误响应中的 `detail` 字段为准——该差异已在最新版 [世界模型](../../raw/model-api-reference/world-model-api-reference.md) 的“已知问题”章节中同步说明。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


