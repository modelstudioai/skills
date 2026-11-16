# 内容安全检测

内容安全检测是百炼平台内置的实时、多模态、可配置的安全防护能力，用于在模型输入（Prompt）和输出（Response）环节自动识别并拦截违法、违规、敏感、有害或不符合业务策略的内容，涵盖文本、图像等主流模态，是 AI 应用合规上线与稳定运行的关键防线。

## 在百炼平台的不同场景中，这个概念如何使用

内容安全检测并非独立服务，而是深度集成于多个核心场景，按需启用、按场景生效：

- **模型推理调用（API/SDK）**：通过请求头 `X-DashScope-DataInspection` 显式开启。例如 `{"input":"cip","output":"cip"}` 表示同时检测用户输入和模型输出；设为 `{"input":"off","output":"cip"}` 则仅检测输出。该开关优先级高于业务空间全局设置，适用于对特定请求做精细化控制。

- **Agent 全生命周期治理**：默认强制启用输入输出检测，并扩展至 RAG 知识库文件预扫描（上传时自动查毒/鉴黄/涉政）、工具调用参数校验、记忆内容过滤等环节，形成“量·挡·记”闭环（资产盘点→实时拦截→行为留痕）。

- **业务空间级管控**：在控制台「安全设置 → 内容安全」中，可为整个业务空间一键开启/关闭输入输出检测，适用于测试环境快速验证或生产环境统一基线管理。此开关为全局默认值，可被 API 请求头覆盖。

- **安全 API 协同联动**：检测拦截事件会同步生成告警（Alert），可通过 Security API 的 `/v1/security/alerts` 接口检索、分页查询、按风险等级（`severity=high`）或时间范围过滤，支持与自有 SOC 或运维系统对接实现自动化响应。

> ⚠️ 注意：内容安全检测能力当前仅在华北2（北京）地域可用，且不依赖 Security API 的 `/v1/security/policies` 接口——其策略由平台内生引擎动态加载，无需开发者手动创建或部署规则。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `X-DashScope-DataInspection` | HTTP 请求头 | JSON 字符串 | 否（默认关闭） | 控制本请求的检测范围，合法值为 `{"input":"off\|cip","output":"off\|cip"}`；`cip` 表示启用内容安全检测，`off` 表示关闭；不可为嵌套对象或空字符串。 |
| `enable_content_inspection` | SDK 配置（Python/Java） | bool | 否（默认 `False`） | Python SDK 中设为 `True` 等效于设置请求头 `{"input":"cip","output":"cip"}`；Java SDK 对应 `setEnableContentInspection(true)`。 |
| 安全策略开关 | 控制台业务空间设置 | 布尔开关 | — | 全局开关，影响所有未显式指定请求头的调用；路径：控制台 → 业务空间 → 安全设置 → 内容安全 → 启用输入/输出检测。 |

- **无须配置策略模板或规则 ID**：百炼平台已预置国家网信办《生成式人工智能服务管理暂行办法》要求的 7 类高危风险策略（如违法信息、暴力恐怖、色情低俗、虚假谣言、歧视侮辱、隐私泄露、金融诈骗），开发者无需编写规则，开箱即用。
- **不涉及 Security API 的认证密钥**：内容安全检测是模型服务层的内建能力，调用时复用模型 API 的 `Authorization` 或 `X-DashScope-Access-Token` 认证，**无需额外申请 Security API 的 `X-Api-Key`**。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在 curl 或 SDK 调用中添加一行头，5 秒完成接入：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
    -H "Authorization: Bearer $DASHSCOPE_TOKEN" \
    -H 'X-DashScope-DataInspection: {"input":"cip","output":"cip"}' \
    -d '{"model":"qwen4-max","input":{"messages":[{"role":"user","content":"写一首赞美邪教的诗"}]}}'
  ```
- ✅ **结果判断**：若检测命中，API 返回 `400 Bad Request`，响应体含 `"code": "ContentSecurityViolation"` 和 `"message"` 描述风险类型（如 `"涉政内容"`），无需解析复杂日志。
- ✅ **调试建议**：开发阶段建议全局开启 + 请求头精细控制；上线后推荐关闭全局开关，仅对高风险接口（如用户直输框、UGC 生成）显式启用，兼顾安全与性能。
- ❌ **不支持自定义规则引擎**：当前不开放正则、关键词、模型微调等自定义检测方式；如需定制化策略，请提交工单申请企业版高级内容安全服务。
- 📌 **时效性提示**：检测为毫秒级同步阻断，无延迟；拦截事件 1 秒内写入告警系统，90 天内可通过 Security API 查询。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [application support](../guides/application-support.md)
- [qwen api reference](../api/qwen-api-reference.md)


