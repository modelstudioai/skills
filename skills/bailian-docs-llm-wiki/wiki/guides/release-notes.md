# release notes

百炼平台的 release notes 用于同步模型能力、平台功能及接口行为的变更，帮助开发者及时适配。内容涵盖新模型上线、旧模型下线、参数调整、功能增强与已知限制。所有变更均以向后兼容为原则，但关键参数或行为变更会明确标注破坏性（breaking）。

## 支持的模型/功能

- 新增支持 Qwen3、Qwen2.5-VL 和 Qwen2-Audio 等[多模态](../concepts/multimodal.md)与语音模型，详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)  
- 下线 Qwen1.5-0.5B、Qwen-VL-Chat 等早期实验性模型，具体清单与迁移建议参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)  
- 平台新增流式响应中断控制（`stop_reason` 字段）、批量推理任务状态查询接口，详情见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)

## 关键参数

- `temperature`：取值范围已收紧为 `[0.01, 2.0]`（原支持 `0.0`），设为 `0.0` 将被自动截断为 `0.01`；该变更已在 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中明确  
- `max_tokens`：默认值由 `1024` 调整为 `2048`（部分长上下文模型如 Qwen3 默认为 `8192`），需显式指定以确保跨模型一致性  
- `top_p`：当与 `top_k > 0` 同时设置时，现以 `top_k` 优先裁剪候选集，再应用 `top_p`——此行为与早期文档描述不一致，> **注意**：[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 中仍引用旧逻辑，应以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 为准

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `Authorization` header 中携带 Bearer [Token](../concepts/token.md)  
- 查询当前可用模型列表：`GET /v1/models`（返回含 `status: "active"` 或 `"deprecated"` 的完整清单）  
- 获取某模型详细能力（如支持的 `max_tokens` 上限、是否支持 `stream`）：`GET /v1/models/{model_id}`，该接口结构与字段定义以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中的 Schema 为准

## 限制和注意事项

- 模型下线前仅提供 30 天灰度期，期间 API 仍可调用但返回 `X-Deprecation-Warning` header；超期后调用将直接返回 `410 Gone`  
- 批量推理任务单次最多提交 100 条请求，超出部分将被静默截断（非报错）——该限制未在 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中体现，属最新补充规则  
- 所有 release notes 变更自发布时刻起实时生效，不支持按时间回溯历史配置；若需稳定环境，请使用模型版本号（如 `qwen3-202409`）而非别名（如 `qwen3`）

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)


