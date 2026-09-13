# support

百炼平台的 `support` 接口用于获取模型服务相关的支持信息，包括模型能力范围、售后政策及常见问题指引。该接口不提供实时诊断或人工工单创建能力，而是作为开发者集成支持资源的统一入口。所有返回链接均指向阿里云官方帮助中心的最新文档。

## 支持的模型/功能

`support` 接口本身不绑定具体模型，但其返回的支持资源覆盖百炼平台当前全部商用模型，包括 Qwen 系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 及第三方托管模型。模型兼容性与能力边界以 [服务支持](../../raw/model-user-guide/support.md) 中引用的 [模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list) 为准。注意：部分新发布模型（如 Qwen3-32B）可能在 [服务支持](../../raw/model-user-guide/support.md) 页面更新前已上线，实际可用性请以控制台模型市场为准。

## 关键参数

该接口为静态资源聚合接口，**无请求参数**。调用时仅需携带标准鉴权头（`Authorization: Bearer <token>`）和 `Content-Type: application/json`。响应体为 JSON 格式，包含四个固定字段：`model_list_url`、`faq_url`、`agreements_url`、`after_sales_url`，其值均来自 [服务支持](../../raw/model-user-guide/support.md) 文档中列出的对应链接。

## 使用方式

通过 HTTP GET 请求访问 `https://dashscope.aliyuncs.com/api/v1/support`（生产环境）或沙箱环境对应 endpoint。示例 cURL：
```bash
curl -X GET \
  https://dashscope.aliyuncs.com/api/v1/support \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json"
```
响应示例：
```json
{
  "model_list_url": "https://help.aliyun.com/zh/model-studio/model-studio-model-list",
  "faq_url": "https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio",
  "agreements_url": "https://help.aliyun.com/zh/model-studio/related-agreements",
  "after_sales_url": "https://help.aliyun.com/zh/model-studio/after-sales-service-scope"
}
```

## 限制和注意事项

- 接口调用频率限制为 100 次/分钟，超出将返回 `429 Too Many Requests`；
- 所有返回 URL 均为外部跳转链接，平台不代理内容，也不缓存响应；
- > **注意**：[服务支持](../../raw/model-user-guide/support.md) 中的 `售后说明` 链接（`after_sales_url`）明确限定“仅限按量付费用户享受 7×24 小时技术响应”，包年包月实例故障响应 SLA 以合同附件为准，二者存在服务等级差异；
- > **注意**：原始文档未声明接口是否支持区域（Region）路由，但实测调用 `https://dashscope.aliyuncs.com/api/v1/support` 在 `cn-beijing` 和 `ap-southeast-1` 区域返回相同内容，建议默认使用全局 endpoint；
- 链接有效期由阿里云帮助中心统一维护，若发生 404，请同步检查 [服务支持](../../raw/model-user-guide/support.md) 是否已更新。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


