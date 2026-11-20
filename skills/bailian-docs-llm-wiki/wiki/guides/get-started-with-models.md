# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。本文档指导开发者完成模型选择、参数配置与首次调用，涵盖基础能力、关键约束及常见问题排查路径。所有模型均通过 Model Studio 统一管理与发布，实际可用模型以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 为准。

## 支持的模型与功能

- 当前支持 Qwen 系列（如 `qwen4-max`、`qwen2.5-72b`）、Qwen-VL 多模态模型，以及部分第三方兼容模型（需开通白名单）  
- 模型能力覆盖文本生成、[函数调用](../concepts/function-calling.md)（tool calling）、流式响应、JSON Schema 输出约束等；具体能力差异请参考各模型专属文档，例如 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 的上下文长度与系统提示支持细节  
- 所有模型均集成在 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 描述的统一架构中，不区分部署形态（SaaS 或私有化）

## 关键参数

- `model`: 必填，值必须来自 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中的 `model_id` 字段（区分大小写，不可拼写缩写）  
- `input.messages`: 至少包含一个 `role: "user"` 的消息对象；`system` 角色仅在部分模型（如 `qwen4-max`）中生效，详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)  
- `parameters.temperature`: 范围 0.0–2.0，设为 0 时启用确定性解码（非所有模型均支持，部分旧模型忽略该参数）  
- `stream`: 布尔值，设为 `true` 时返回 SSE 流式响应；注意流式响应中 `usage` 字段仅在末尾 chunk 中完整返回  

## 使用方式

1. 在控制台开通模型服务并获取 API Key（需绑定有效项目）  
2. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（通用 endpoint）  
3. 设置请求头：`Authorization: Bearer <api_key>`、`Content-Type: application/json`  
4. 发送 JSON body，最小合法示例：
   ```json
   {
     "model": "qwen4-max",
     "input": {"messages": [{"role": "user", "content": "你好"}]},
     "parameters": {"temperature": 0.8}
   }
   ```
> **注意**：部分旧版文档（如 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 中列举的 `InvalidParameter.ModelNotSupported`）未同步更新模型 ID 命名规范，实际报错应以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中的 `model_id` 为准，避免使用别名或旧代号（如 `qwen-max` 已弃用）。

## 限制和注意事项

- 单次请求最大输入 tokens 受模型自身限制（如 `qwen4-max` 为 32768），超出将触发 `400 Bad Request`；详细上限见各模型文档  
- 默认限流策略为每秒 5 QPS / 每分钟 300 次调用（按 project 维度统计），可申请提升，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)  
- 模型服务地域隔离：调用 endpoint 必须与所选 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 一致，跨 region 调用将返回 `403 Forbidden`  
- 不支持直接上传二进制文件（如图片）作为 `input.messages.content`；多模态输入需先调用文件上传接口获取 `file_id`，再在 message 中引用 —— 此流程在 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中有明确说明

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


