# asset center page

资产中心是百炼平台中统一管理、查看和调用各类模型资产（如大模型、插件、知识库、工作流等）的核心界面。开发者可通过该页面快速检索已部署的模型实例、配置运行参数并发起推理请求，所有操作均基于 RESTful API 或 SDK 封装。该页面不提供训练能力，仅面向推理与编排阶段的资产消费。

## 支持的模型/功能

- 支持调用已部署的 **大语言模型（LLM）**（如 Qwen 系列、Baichuan、GLM）、**多模态模型**（如 Qwen-VL）、**嵌入模型（Embedding）** 和 **重排序模型（Rerank）**  
- 支持通过「插件」方式接入外部 API（需在 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中完成插件注册与认证）  
- 支持绑定知识库与工作流，实现 RAG 与自动化任务编排（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）  
- 不支持直接上传或训练新模型；模型上线需经 Model Studio 审批后同步至资产中心  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，可在 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的模型卡片中获取 |
| `input` | object | 是 | 输入内容，结构依模型类型而异（LLM 为 `{"messages": [...]}`，Embedding 为 `{"text": "..."}`） |
| `parameters` | object | 否 | 推理参数，如 `temperature`、`max_tokens`；部分模型支持 `stream: true` 流式响应 |
| `enable_search` | boolean | 否 | 仅对启用了知识库绑定的模型生效，控制是否触发 RAG 检索 |

> **注意**：`parameters` 中的 `top_k` 在重排序模型中表示返回结果数，而在 Embedding 模型中无意义——该差异已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的参数说明表中明确区分，但旧版文档未同步更新，请以该链接为准。

## 使用方式

1. 登录百炼控制台 → 进入「模型服务」→ 「资产中心」  
2. 在模型列表中点击目标模型卡片，进入详情页  
3. 在「调试」Tab 中填写 `input` 与 `parameters`，点击「发送请求」  
4. 或使用 SDK（如 `dashscope` Python 包）调用：  
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen-max', input={'messages': [{'role': 'user', 'content': '你好'}]})
   ```

## 限制和注意事项

- 单次请求 `input.text` 最长支持 32768 字符（LLM），超长将被截断且**不报错**（参见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“输入限制”章节）  
- 免费试用额度仅适用于首次部署的模型实例，续用需绑定计费项；额度耗尽后请求将返回 `402 Payment Required`  
- 所有模型调用默认启用审计日志，敏感字段（如 `input.messages[*].content`）在日志中自动脱敏，不可关闭  
- 跨地域调用（如华东1模型从华北3发起请求）将产生额外网络延迟，建议就近部署与调用

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


