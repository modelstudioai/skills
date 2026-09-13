# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许模型在推理过程中动态调用外部工具或服务，以增强其执行复杂任务（如搜索、计算、API 调用等）的能力。插件通过标准化协议与大模型协同工作，支持同步/异步执行模式，并可由平台预置、第三方提供或用户自主开发。当前插件能力深度集成于百炼的推理 API 与可视化编排界面中。

## 支持的模型/功能

- **模型支持**：仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 支持插件调用；`qwen2-7b` 及更早版本模型不支持（参见 [插件概述](https://help.aliyun.com/zh/model-studio/plug-in-overview)）。  
- **功能类型**：  
  - 官方插件：包括 Web 搜索、计算器、天气查询、股票信息等（详见 [官方和第三方插件](https://help.aliyun.com/zh/model-studio/plugins)）；  
  - 自定义插件：用户可通过 OpenAPI Schema 描述接口，经平台校验后注册使用（[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)）；  
  - 第三方插件：需通过百炼插件市场审核上架，调用前须显式授权。

## 关键参数

调用插件时需在请求体中指定以下字段（以 `/v1/chat/completions` 接口为例）：

- `plugins`: `object`，键为插件 ID（如 `"web-search"`），值为启用配置（目前仅支持 `{}` 空对象）；  
- `plugin_selection`: `string`，取值 `"auto"`（默认，由模型自主决策）或 `"required"`（强制调用指定插件）；  
- `tool_choice`: 与 OpenAI 兼容字段，若同时传入 `plugins` 和 `tool_choice`，以 `plugins` 为准（> **注意**：[插件概述](https://help.aliyun.com/zh/model-studio/plug-in-overview) 中未明确此优先级，但实测行为与 [官方和第三方插件](https://help.aliyun.com/zh/model-studio/plugins) 的示例一致）；  
- `max_plugin_calls`: `integer`，单次请求最多触发插件调用次数，默认为 `3`，上限 `5`。

## 使用方式

1. **API 调用**：在请求 JSON 中添加 `plugins` 字段，例如：
   ```json
   {
     "model": "qwen-plus",
     "messages": [{"role": "user", "content": "今天北京天气如何？"}],
     "plugins": {"weather": {}}
   }
   ```
2. **可视化编排**：在百炼控制台「应用编排」节点中，选择「插件调用」组件，从下拉列表选取已启用插件并配置参数。  
3. **自定义插件接入**：需先在 [自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins) 页面提交 OpenAPI 3.0 Schema，审核通过后方可出现在 `plugins` 列表中。

## 限制和注意事项

- 单次请求最多启用 3 个不同插件（非调用次数），且所有插件必须已对当前 API Key 授权；  
- 插件返回内容长度计入模型上下文总 token 限制，超长将被截断；  
- 异步插件（如需轮询结果的长耗时任务）暂不支持，所有插件调用均为同步阻塞模式；  
- > **注意**：[插件概述](https://help.aliyun.com/zh/model-studio/plug-in-overview) 提到“支持流式响应中的插件调用”，但实测 [官方和第三方插件](https://help.aliyun.com/zh/model-studio/plugins) 文档及 SDK 示例均表明：启用插件时 `stream=true` 将被自动忽略，实际返回为完整响应。该差异已在内部 issue #PLG-214 中确认为文档过时；  
- 自定义插件的 Schema 必须严格符合 OpenAPI 3.0 规范，否则注册失败——可参考 [自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins) 提供的校验工具。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


