# 内容安全与合规

内容安全与合规是百炼平台面向生成式AI应用的核心横切能力，指通过多模态输入检测、可控输出拦截、策略化风险治理及全链路审计追溯等机制，确保模型交互内容符合国家监管要求（如《生成式人工智能服务管理暂行办法》）、企业安全策略与数据隐私规范。该能力默认启用、深度集成于调用链路，无需修改业务逻辑即可提供端到端防护。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：对文本、图像、音频等多模态输入自动执行涉黄、涉政、暴恐、广告、隐私信息（如身份证号、手机号）识别；对输出内容实时拦截越狱指令、有害生成、事实性错误及敏感信息泄露。防护强度可按需配置（基础/严格/自定义），并支持按请求粒度开关。
- **Agent 应用运行时**：在工具调用环节实施资产级防护，例如限制仅允许调用白名单内的插件、禁用高危函数（如 `os.system`）、校验工具参数合法性，防止 Agent 被诱导执行恶意操作。
- **私有化与高敏场景**：结合传输加密（AES+RSA 混合加密）、私网访问（PrivateLink）、安全存储空间等能力，实现“内容不出域、风险不外溢”的闭环管控，满足金融、政务等强合规场景要求。
- **安全运营与审计**：通过统一审计日志（含原始输入/输出、拦截原因、策略ID、时间戳）和 Security API，支持构建合规看板、自动化告警响应、定期导出报告，满足等保、GDPR 或行业审计要求。

## 关键参数和配置

| 参数名 | 位置 | 类型 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `safety_check` | API 请求体（同级于 `input` / `messages`） | boolean | `true` | 启用/禁用实时安全检测；生产环境强制为 `true`，设为 `false` 将被忽略 |
| `safety_level` | API 请求体 | string | `"basic"` | 防护强度：`"basic"`（默认规则）、`"strict"`（增强规则）、`"custom"`（需配合 `safety_policy_id`） |
| `safety_policy_id` | API 请求体 | string | — | 引用预置或自定义策略 ID；一个请求仅支持指定一个策略，复合策略需提前在控制台创建 |
| `audit_enabled` | API 请求体 | boolean | `false` | 开启后记录完整请求/响应及拦截详情，用于审计追溯；日志保留 90 天 |
| `X-DashScope-DataInspection` | HTTP Header | JSON string | — | 启用 AI 安全护栏（独立于 `safety_check`），格式如 `'{"input":"cip","output":"cip"}'`，支持细粒度开关 |

> ✅ **提示**：  
> - 控制台中可在「应用设置 → 安全策略」为整个应用或单个 Agent 绑定策略，策略将自动注入所有 API 调用；  
> - CLI 可通过 `bailian security enable --level strict --policy <id>` 快速启用；  
> - 安全策略本身（含规则组合、风险域分类如 `model_interaction`、`runtime_tool`）需在 [安全策略管理](../../raw/application-user-guide/security-guide/section-adv/policy.md) 中配置。

## 面向开发者，简洁实用

- **快速启用**：只需在 API 请求中添加 `"safety_level": "strict"`，即刻获得增强防护，无需改模型代码或重写逻辑。  
- **调试建议**：开发阶段开启 `audit_enabled: true`，结合 `RequestId` 查看拦截详情；若需临时绕过（仅限测试环境），显式传 `"safety_check": false`。  
- **多模态注意**：图像/音频检测延迟略高（+150–300ms），高并发场景请预留缓冲；确保上传文件格式合法（如 `.pdf` 必须小写后缀）。  
- **合规落地**：导出审计日志（调用 `/v1/audit/export`）或接入 Security API（如 `/agent_logs` 查询告警），可一键生成监管所需报告。  
- **避坑提醒**：`safety_policy_id` 不支持多个 ID 并列；`/export_agent_logs` 的 `params` 字段必须是 JSON **字符串**（如 `"{\"risk_level\":\"high\"}"`），不是对象。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application support](../guides/application-support.md)
- [model monitoring](../guides/model-monitoring.md)


