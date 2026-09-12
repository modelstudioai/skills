# support

百炼平台的 `support` 接口用于获取模型服务相关的支持信息，包括模型兼容性、问题排查指引及售后政策等。该能力不提供实时诊断或人工工单创建，而是返回结构化支持元数据供开发者集成到控制台或调试工具中。实际使用需结合 [服务支持](../../raw/model-user-guide/support.md) 中定义的外部链接体系。

## 支持的模型/功能

当前 `support` 接口覆盖所有已上线的百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方精调模型），但**不支持**自定义部署模型或私有化集群中的模型。接口返回的支持资源类型包括：模型能力说明页、常见问题（FAQ）索引、服务协议文本链接及售后范围说明。具体模型清单以 [服务支持](../../raw/model-user-guide/support.md) 中引用的[模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list)为准。

## 关键参数

- `model_id`（必填，string）：模型唯一标识，如 `qwen-max` 或 `qwen-plus`；必须与 [服务支持](../../raw/model-user-guide/support.md) 所列模型 ID 严格一致  
- `language`（可选，string，默认 `"zh"`）：返回文案语言，仅支持 `"zh"` 和 `"en"`  
- `include_faq`（可选，boolean，默认 `false`）：是否内联 FAQ 条目（仅限基础问题，非全文）

> **注意**：原始文档未定义 `include_faq=true` 时的响应格式，实际返回结构与 [服务支持](../../raw/model-user-guide/support.md) 中的 FAQ 链接跳转逻辑不一致，建议始终设为 `false` 并自行解析外部 FAQ 页面。

## 使用方式

通过 HTTP GET 请求调用 `/v1/support` 端点，携带认证 Header（`Authorization: Bearer <api_key>`）及查询参数：

```bash
curl -X GET "https://dashscope.aliyuncs.com/v1/support?model_id=qwen-max&language=zh" \
  -H "Authorization: Bearer sk-xxx"
```

响应为 JSON，包含 `model_info`、`faq_url`、`agreement_url`、`after_sales_url` 四个字段，各 URL 均指向 [服务支持](../../raw/model-user-guide/support.md) 中列出的对应帮助中心页面。

## 限制和注意事项

- 单账号 QPS 限制为 5，超出后返回 `429 Too Many Requests`  
- `model_id` 若不在当前白名单中，返回 `404 Not Found`（而非重定向至通用支持页）  
- 所有返回的外部链接均可能随 help.aliyun.com 内容更新而变更，不应硬编码解析逻辑  
- 售后范围说明（`after_sales_url`）仅适用于按量付费用户，包年包月实例需参考独立售后条款 —— 此差异未在 [服务支持](../../raw/model-user-guide/support.md) 中明确提示，开发者需主动核对 [售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 最新版本

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)



