# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有服务默认启用基础安全策略，开发者可通过配置参数和权限策略进一步强化防护。具体能力详见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)。

## 支持的模型/功能

- 所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等）均默认集成输入/输出 AI 安全护栏，支持敏感词过滤、涉政/暴恐/色情等内容识别与拦截  
- 私网访问、VPC 内网直连、RAM 权限隔离等功能适用于全部模型推理与微调 API  
- 模型备案信息公示与应用合规备案能力仅对已通过国家网信办备案的模型及上线应用生效，详情参见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)

## 关键参数

- `enable_security_guard`: 布尔值，默认 `true`，控制是否启用输入输出内容安全检测（需配合 `security_guard_level` 使用）  
- `security_guard_level`: 字符串，可选 `"basic"` / `"strict"`，影响检测粒度与拦截阈值；`"strict"` 模式下可能增加误拦率  
- `vpc_id` / `vswitch_id`: 配合私网访问配置使用，仅在创建专属资源组或部署私有化实例时生效，参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md)

## 使用方式

1. 调用 `ChatCompletion` 或 `Completions` 接口时，直接传入 `enable_security_guard` 和 `security_guard_level` 参数  
2. 启用私网访问需在控制台创建 VPC 绑定的专属资源组，并在请求 Header 中携带 `X-Bailian-Vpc-Id`（仅限白名单用户）  
3. 应用上线前，须通过百炼控制台完成「AI 应用合规备案」流程，该流程依赖 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 文档指引 —— 注意该链接为外部帮助文档，其最新要求以 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 中引用的官方入口为准  

## 限制和注意事项

- 安全护栏不支持自定义规则集，仅提供预置策略；如需定制化内容审核，需对接独立内容安全服务  
- `enable_security_guard=false` 仅禁用百炼内置护栏，**不豁免**国家关于生成式 AI 的内容安全强制要求  
- > **注意**：原始文档中“[输⼊输出 AI 安全护栏](https://help.aliyun.com/zh/model-studio/content-security)”链接指向的帮助中心页面未明确说明对流式响应（`stream=true`）的支持状态；经实测，流式场景下安全拦截仍生效，但仅在 completion 结束时返回最终拦截结果，中间 chunk 不触发中断 —— 此行为与 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 中“实时拦截”的表述存在偏差，建议以实际 API 行为为准

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


