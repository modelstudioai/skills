# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均基于阿里云整体安全体系构建，并符合中国法律法规及行业监管要求。开发者需结合自身业务场景，合理配置参数并履行应用级合规义务。

## 支持的模型/功能

- **AI 安全护栏**：对输入输出内容进行实时检测与拦截，支持敏感词过滤、价值观对齐、违法不良信息识别等策略，适用于 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公有云部署模型；  
- **私网访问与 VPC 隔离**：支持通过阿里云专有网络（VPC）调用模型服务，避免公网暴露，详见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)；  
- **模型与应用双备案支持**：平台提供模型备案信息公示入口，并支持 AI 应用完成《生成式人工智能服务管理暂行办法》要求的备案流程，相关指引见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)。

## 关键参数

- `enable_security_guard`: 布尔值，默认 `true`，启用输入输出 AI 安全护栏（仅对 `/v1/chat/completions` 和 `/v1/text/embedding` 等接口生效）；  
- `security_level`: 字符串，可选 `"standard"`（默认）或 `"strict"`，影响敏感内容拦截阈值；  
- `vpc_endpoint`: 字符串，当使用私网访问时必填，格式为 `https://<service-id>.<region>.aliyuncs.com`，配置方式参见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)。

## 使用方式

1. 调用 API 时在请求头中携带 `X-DashScope-Security-Token`（如启用 [Token](../concepts/token.md) 验证）；  
2. 在请求体中显式设置 `enable_security_guard: true` 及所需 `security_level`；  
3. 私网调用需将 endpoint 替换为 VPC 内网地址，并确保 ECS 实例所属安全组放行对应端口；  
4. 模型备案信息可通过控制台「模型市场 → 已购模型 → 备案详情」查看；应用备案需在「AI 应用中心 → 应用管理 → 合规备案」中发起。

## 限制和注意事项

- AI 安全护栏不支持自定义规则集，策略由平台统一维护更新；  
- `enable_security_guard` 对流式响应（`stream: true`）仍生效，但拦截结果以首个 chunk 的 `finish_reason: "content_filter"` 形式返回；  
- 私网访问仅支持同地域 VPC，跨地域需通过云企业网（CEN）打通；  
> **注意**：原始文档中「[输⼊输出 AI 安全护栏](https://help.aliyun.com/zh/model-studio/content-security)」链接已重定向至新版内容安全控制台，其策略配置粒度与 API 参数行为存在差异，当前 API 层仅支持全局开关与等级控制，不开放细粒度 action 配置。  
> **注意**：文档中「[私网访问配置](https://help.aliyun.com/zh/model-studio/secure-storage)」标题存在误导——该链接实际指向密钥安全存储说明，而非 VPC 访问配置；正确指引应参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 中的「私网访问配置」条目。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


