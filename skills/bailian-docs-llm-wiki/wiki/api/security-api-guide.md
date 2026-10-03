# security api guide

百炼平台 Security API 提供模型输入/输出内容安全检测能力，支持文本、图像等多模态内容的风险识别（如涉黄、暴恐、违禁等）。该 API 以独立服务形式提供，需通过标准 HTTP 请求调用，并依赖平台统一认证机制。开发者应结合业务场景选择合适策略并关注配额与响应时效约束。

## 支持的模型/功能

Security API 当前不依赖大语言模型推理引擎，而是基于专用风控模型提供以下核心能力：
- 文本内容安全检测（支持 UTF-8 编码纯文本，最大长度 65536 字符）
- 图像内容安全检测（支持 JPG/PNG/WebP 格式，单图不超过 10 MB，分辨率建议 ≤ 4096×4096）
- 批量检测（最多 10 条样本/请求，需通过 `batch` 参数显式启用）

> **注意**：[原文标题](../../raw/application-api-reference/security-api-guide.md) 中列出的“音频检测”功能尚未上线，实际接口不支持 audio/mpeg 等类型；请以 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 的最新参数说明为准。

## 关键参数

必填参数：
- `input`：待检测内容，为对象类型，结构取决于 `type`（`text` 或 `image`）
- `type`：内容类型，取值 `"text"` 或 `"image"`
- `policy_id`：策略 ID（可选，若未指定则使用默认策略）

常用可选参数：
- `scene`：业务场景标识（如 `"chat"`、`"search"`），影响部分策略权重
- `return_full_result`：布尔值，设为 `true` 时返回各风险维度细项分值（默认 `false`）
- `timeout`：超时时间（毫秒），建议设为 5000–15000，避免因图像解码延迟导致失败

详细字段定义请参考 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <access_token>`，Token 通过百炼平台 OAuth2 流程获取（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）  
2. **请求示例（文本）**：
   ```http
   POST /v1/security/detect HTTP/1.1
   Content-Type: application/json
   Authorization: Bearer ak-xxx

   {
     "type": "text",
     "input": {"content": "这个商品很赞！"},
     "policy_id": "pol-abc123"
   }
   ```
3. **响应解析**：成功时返回 `code=200`，`result.action` 字段指示处置建议（`"allow"`/`"block"`/`"review"`），`result.risk_level` 为整数风险等级（0–5）

## 限制和注意事项

- QPS 限制：默认 10 次/秒（可申请提升），单次请求耗时超过 `timeout` 值将返回 `408 Request Timeout`
- 图像检测不支持 GIF 动画帧提取，仅分析首帧；若传入 GIF，需提前转为静态图
- 同一 `policy_id` 下策略更新后，新请求立即生效，但历史检测结果不可变更
- 调试阶段建议始终启用 `return_full_result=true` 并结合 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档理解各维度阈值逻辑

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


