# 安全内容过滤

安全内容过滤是百炼平台内置的多模态、分层式内容安全防护机制，用于在模型输入（Prompt）和输出（Response）环节实时识别并拦截违法、违规、敏感或高风险内容，涵盖文本关键词匹配、实体识别（如身份证号、手机号）、图像鉴黄、涉政暴恐识别等策略，保障 AI 应用符合国家监管要求与企业合规标准。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用模型调用（文本生成类）**：所有百炼托管模型（包括 Qwen 系列及第三方接入模型）默认启用安全内容过滤。该能力由平台协议层与 AI 护栏层协同执行，无需额外配置即可生效；拦截结果通过响应字段 `safety_result` 返回，含 `action`（`allow`/`block`/`review`）与 `reason`，开发者应据此实现降级、重试或人工审核逻辑。

- **Agent 场景**：在 Agent 执行链路中，安全内容过滤不仅作用于最终响应，还延伸至工具调用返回内容（如搜索结果、API 响应体）。当启用 `governance_policy=strict` 且模型为 `qwen-max` 或 `qwen-plus` 时，系统会对工具返回文本进行二次过滤与脱敏（如自动掩码手机号），但**不扫描工具调用参数本身或中间思考过程**。

- **监控与可观测性**：内容安全拦截行为被统一记录为 `内容安全错误次数` 指标，在「模型监控」控制台详情页中展示（不可配置告警）。开发者可通过该指标趋势判断业务请求是否集中触发敏感策略，辅助优化 Prompt 设计或调整治理策略。

- **安全运营与审计**：拦截事件作为安全告警纳入 Agent 安全治理体系，可通过 Security API 的 `/agent_logs` 接口查询详细日志（含 `policy_code` 如 `vulnerability_scan`、`baseline_check`），支持按 `risk_level=high/medium/low` 筛选，并通过 `/export_agent_logs` 异步导出 Excel 进行合规留痕。

## 关键参数和配置

- `enable_content_safety`: 布尔型请求参数（默认 `true`），用于显式开启或关闭 AI 护栏层过滤。设为 `false` 仅禁用基于大模型的理解式过滤，**底层协议级关键词拦截（如涉政、暴恐词库）仍强制生效，不可绕过**。

- `safety_result`: 响应体中的只读字段，结构为：
  ```json
  "safety_result": {
    "action": "block",
    "reason": "contains_prohibited_words",
    "matched_rules": ["政治敏感词"]
  }
  ```
  开发者必须检查该字段，不可仅依赖 HTTP 状态码（拦截仍返回 `200 OK`）。

- Security API 中相关策略标识（`policy_code`）包括但不限于：  
  `baseline_check`（基础合规检查，免费）、  
  `vulnerability_scan`（漏洞提示拦截，免费）、  
  `text_moderation`（文本多维度审核）、  
  `image_moderation`（图像鉴黄/暴恐识别，需开通对应能力）。

> 注意：策略实际启用状态以 `/policies` 接口返回为准；`capabilities` 字段仅反映运行时能力开关，二者语义不同，不可混用。

## 面向开发者，简洁实用

- ✅ **必做**：始终解析 `safety_result.action`，对 `block` 做友好提示或 fallback；对 `review` 建议进入人工审核队列。  
- ✅ **推荐**：在生产环境开启推理日志投递，结合 `safety_result` 与完整 Prompt/Response 分析误拦/漏拦案例。  
- ⚠️ **避坑**：`enable_content_safety=false` 不等于“完全放开”，协议层硬过滤无法关闭；若需调试敏感词逻辑，请使用测试工作空间 + 白名单 IP + 低风险测试数据。  
- 📊 **监控建议**：将 `内容安全错误次数` 与 `失败次数` 对比分析——若前者占比突增，说明业务请求正高频触碰策略边界，需优化输入或申请策略白名单。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [model monitoring](../guides/model-monitoring.md)


