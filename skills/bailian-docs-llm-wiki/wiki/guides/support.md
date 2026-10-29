# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、服务范围及售后政策，不提供实时推理功能，仅作为元信息查询入口。开发者可通过该接口确认模型可用性、调用限制和合规要求。所有返回内容均以平台最新控制台配置和[服务支持](../../raw/model-user-guide/support.md)文档为准。

## 支持的模型/功能

- 支持查询百炼 Model Studio 中已上线的全部大模型（含开源微调模型与专属模型），具体清单见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)  
- 支持按模型 ID、场景标签（如 `text-generation`, `embedding`, `multimodal`）筛选可用模型  
- 不支持动态注册未接入百炼调度系统的第三方模型；所有模型必须通过百炼控制台完成部署与授权后方可被 `support` 接口识别  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 否 | 指定模型 ID，留空则返回全部支持模型摘要 |
| `with_details` | boolean | 否 | `true` 时返回模型详细能力描述（如输入长度上限、token 计费粒度），默认 `false` |
| `region` | string | 否 | 指定地域（如 `cn-shanghai`），影响返回的可用模型集（部分模型仅限特定 region） |

> **注意**：`region` 参数行为与 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“跨地域模型是否通用”一节存在表述差异——后者称“模型全局可见”，但实际 API 响应受 region 隔离策略约束，以接口实际返回为准。

## 使用方式

通过 HTTP GET 请求调用：
```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model_id=qwen-max&with_details=true" \
  -H "Authorization: Bearer $API_KEY"
```
响应为 JSON 格式，包含 `models` 数组及 `service_scope` 字段（含售后覆盖范围、SLA 承诺等）。完整字段定义参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- 单日调用频次上限为 1000 次（按 API Key 统计），超出后返回 `429 Too Many Requests`  
- `with_details=true` 时响应延迟可能达 300–500ms，建议缓存结果或仅在初始化阶段调用  
- 返回的模型状态（如 `status: "active"`）不保证实时性，模型下线可能存在最多 5 分钟同步延迟  
- 所有服务条款、数据隐私责任及免责范围，以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 最终版本为准，本接口不构成法律承诺

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


