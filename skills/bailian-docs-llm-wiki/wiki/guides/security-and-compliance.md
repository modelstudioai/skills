# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均基于阿里云整体安全体系构建，并符合中国《生成式人工智能服务管理暂行办法》等法规要求。开发者需结合自身业务场景，在调用模型前完成必要的合规配置与备案。

## 支持的模型/功能

以下安全与合规能力适用于所有在百炼平台托管或调用的模型（包括通义千问系列、Qwen-VL、Qwen-Audio 等），但部分功能依赖[模型部署](../concepts/model-deployment.md)方式：
- **输入输出 AI 安全护栏**：对请求 [prompt](prompt.md) 和响应 content 实时进行涉政、暴恐、色情、违禁等 12 类风险识别与拦截（详见 [原文标题](../../raw/model-user-guide/security-and-compliance.md)）；
- **私网访问配置**：仅支持通过 VPC 内网调用模型服务，避免公网暴露（参见 [原文标题](../../raw/model-user-guide/security-and-compliance.md)）；
- **模型备案信息公示**：所有上线模型均已完成国家网信办备案，备案号可在控制台「模型详情页 → 合规信息」查看（依据 [原文标题](../../raw/model-user-guide/security-and-compliance.md)）。

> **注意**：应用合规备案（即 AI 应用上线前的备案）要求独立于模型备案，且仅适用于面向公众提供服务的 Web/App 应用；内部工具类应用无需备案，但需确保不绕过输入输出安全护栏。

## 关键参数

调用模型 API 时，可通过以下参数启用/控制安全能力：
- `enable_security_check: true`（默认 `false`）：启用输入输出 AI 安全护栏（仅对 `/v1/chat/completions` 等支持护栏的接口生效）；
- `security_level: "strict" | "balanced" | "relaxed"`：指定护栏敏感度，默认为 `"balanced"`；
- `private_network_only: true`：强制仅允许 VPC 内网调用（需提前在模型服务配置中开启私网访问）。

## 使用方式

1. **开通权限**：主账号需在 RAM 控制台为子账号授予 `AliyunBailianFullAccess` 或最小化策略 `AliyunBailianSecurityReadOnlyAccess`（参考 [权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview)）；  
2. **配置私网访问**：在模型服务详情页 → 「网络配置」中开启 VPC 访问并绑定交换机（对应 [私网访问配置](https://help.aliyun.com/zh/model-studio/secure-storage)）；  
3. **启用护栏**：在 API 请求 body 中显式设置 `enable_security_check: true`，否则默认不触发内容安全检测。

## 限制和注意事项

- 输入输出安全护栏仅支持 UTF-8 编码文本，不支持二进制文件（如图片 base64）的内容级扫描；图像类风险需依赖前置鉴黄服务；
- `security_level: "strict"` 可能导致合法但表述模糊的请求被误拦截，建议灰度验证后上线；
- 模型备案信息由平台自动同步，但**应用合规备案需开发者自主完成**，未备案的公众应用可能被监管部门下架（依据 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)）；
- 所有安全能力均不替代开发者自身的数据脱敏与隐私保护义务，敏感字段（如身份证号、手机号）须在调用前自行处理。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


