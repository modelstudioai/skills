# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均默认启用或按需配置，开发者可通过 API 参数、控制台策略或 SDK 集成方式启用对应功能。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

以下安全与合规功能适用于全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）：
- 输入/输出内容安全过滤（基于关键词、敏感实体、多模态内容识别）
- 传输层 TLS 1.2+ 加密与双向证书校验
- 私网 VPC 内访问支持（需在 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 中完成 VPC 绑定与安全组设置）
- 模型备案状态实时查询（通过 `GET /v1/models/{model_id}/filing` 接口）
- 应用级合规备案引导（参见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)）

> **注意**：部分旧版 SDK（v3.2.0 之前）未默认启用输出内容安全过滤，需显式设置 `enable_output_safety_check=true`；新版本已统一为默认开启，详见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 关键参数

调用 `/v1/chat/completions` 或 `/v1/embeddings` 等接口时，以下参数控制安全行为：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_input_safety_check` | boolean | `true` | 启用输入内容安全检测（含 PII 识别、违法信息拦截） |
| `enable_output_safety_check` | boolean | `true` | 启用输出内容安全检测（防止生成违规、歧视性或越狱内容） |
| `safety_check_level` | string | `"standard"` | 可选 `"standard"` / `"strict"`；`"strict"` 拦截阈值更低，误拦率略升 |
| `request_context` | object | `{}` | 可传入 `user_ip`, `user_region`, `app_id` 等上下文字段，用于动态风控策略 |

上述参数行为以 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 定义为准。

## 使用方式

1. **API 调用**：在请求 body 中直接传入上述参数（如 `{"enable_output_safety_check": false}`），适用于临时关闭某次请求的安全检查（仅限测试环境，生产环境不建议禁用）  
2. **控制台策略**：在「安全中心 → 内容安全策略」中为模型或应用设置全局默认策略，优先级高于 API 参数  
3. **SDK 配置**：Python SDK v3.4.0+ 支持 `client.chat.completions.create(..., safety_check_level="strict")`；Java SDK 需通过 `SafetyConfig` 对象注入  

私网访问必须配合 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 完成网络侧设置，否则即使启用 `vpc_enabled=true` 参数仍会返回 403。

## 限制和注意事项

- 输入/输出安全检查对非 UTF-8 编码文本、Base64 图像块或长上下文（>32k tokens）可能降级为采样检测，完整覆盖需分段处理  
- `safety_check_level="strict"` 不支持流式响应（`stream=true`），启用时将自动转为非流式返回  
- 模型备案信息仅对已通过国家网信办审核的模型开放查询；未备案模型调用 `/filing` 接口返回 `404`，而非错误提示 —— 此行为与 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 描述一致  
- 权限管理粒度最小至「模型实例 + API Key」级别，不支持细粒度字段级权限（如禁止读取 `response.usage`），详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


