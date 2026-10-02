# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均默认启用，开发者可通过配置参数或控制台策略进行精细化管控。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

以下安全与合规能力适用于全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型：
- 输入/输出内容安全过滤（基于关键词、语义与多模态风险识别）
- TLS 1.2+ 传输加密（强制启用，不可禁用）
- RAM 权限细粒度控制（支持 `qwen:InvokeModel`、`qwen:ListModels` 等最小权限策略）
- 私网 VPC 访问支持（需在模型部署时显式开启 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)）
- 模型备案信息自动同步至国家网信办公示系统（仅限已通过备案的商用模型）

> **注意**：[输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 中提及的“可关闭风控”选项已于 v2.3.0 版本移除；当前所有 API 调用均强制执行内容安全检测，该变更已在 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 的最新修订中明确说明。

## 关键参数

调用 `/v1/chat/completions` 或 `/v1/models/{model}/invoke` 时，以下参数影响安全行为：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `safety_check` | boolean | 控制是否启用内容安全过滤（默认 `true`；设为 `false` 将被忽略，见上文注意项） |
| `response_format` | string | 当设为 `"json_object"` 时，输出将额外校验 JSON 结构安全性，防止注入攻击 |
| `x-bailian-tenant-id` | string | 必须携带有效租户 ID，用于审计日志归属与权限上下文绑定 |

## 使用方式

1. **权限配置**：在 RAM 控制台为服务角色附加 `AliyunBaiLianFullAccess` 或按需组合最小权限策略，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)  
2. **私网调用**：创建模型服务时勾选「私网访问」，并确保客户端 VPC 与服务 VPC 已建立对等连接或云企业网（CEN）路由 —— 配置方法见 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)  
3. **合规备案**：AI 应用上线前，须完成《生成式人工智能服务备案》及百炼平台内 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，否则无法通过生产环境审核  

## 限制和注意事项

- 所有请求必须使用 HTTPS，HTTP 请求将被网关直接拒绝  
- 内容安全过滤不支持自定义规则集（如白名单/黑名单），仅支持平台预置策略；如需定制化风控，需接入独立安全网关  
- 模型备案信息仅对已发布至「百炼市场」的商用模型自动公示；私有部署模型需自行向监管部门提交 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 材料  
- 传输层加密证书由平台统一管理，不支持客户上传自签名证书

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


