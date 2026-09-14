# support

百炼平台的 `support` 接口用于查询服务级支持信息，包括模型覆盖范围、售后政策及合规协议等。该能力不涉及模型推理调用，而是面向开发者提供自助式服务元数据查询。所有支持信息均以结构化链接形式返回，便于集成至内部运维或客户支持系统。

## 支持的模型/功能

`support` 接口本身不直接关联具体模型，但其返回的模型列表链接指向当前平台已上线并提供完整服务支持的全部大模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等）。模型覆盖状态与 [服务支持](../../raw/model-user-guide/support.md) 中公布的 [模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list) 严格一致。注意：部分实验性模型可能出现在控制台但未纳入此列表，实际支持范围请以该文档为准。

## 关键参数

该接口为只读静态资源访问，**无请求参数**。调用时无需传入 `model`、`prompt` 或认证 token；所有信息通过预置的公开链接聚合返回。响应体为 JSON，包含 `model_list_url`、`faq_url`、`agreements_url` 和 `after_sales_url` 四个字段，其值均来自 [服务支持](../../raw/model-user-guide/support.md) 文档中明确列出的 URL。

## 使用方式

直接向 `https://dashscope.aliyuncs.com/api/v1/support` 发起 GET 请求（无需鉴权），即可获得最新支持链接集合。示例响应：
```json
{
  "model_list_url": "https://help.aliyun.com/zh/model-studio/model-studio-model-list",
  "faq_url": "https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio",
  "agreements_url": "https://help.aliyun.com/zh/model-studio/related-agreements",
  "after_sales_url": "https://help.aliyun.com/zh/model-studio/after-sales-service-scope"
}
```
> **注意**：该接口不支持 POST 或带 body 的请求；若收到 405 错误，请确认请求方法为 GET。另需注意，[服务支持](../../raw/model-user-guide/support.md) 中的链接均为帮助中心页面，不提供 API 形式的模型元数据（如输入/输出 schema），如需结构化模型能力描述，请参考 [模型能力说明](../../raw/model-user-guide/capabilities.md)。

## 限制和注意事项

- 接口响应内容每日自动同步一次，非实时更新；紧急变更（如协议下线）可能存在最长 24 小时延迟。
- 所有返回链接均跳转至阿里云帮助中心，不支持内网代理或私有化部署环境直连。
- 售后服务范围（如 SLA、工单响应时效）以 [售后说明](../../raw/model-user-guide/support.md) 中的 [售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 为准，`support` 接口不校验用户账号权限或服务开通状态。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


