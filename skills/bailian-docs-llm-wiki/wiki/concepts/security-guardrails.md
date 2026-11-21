# AI 安全护栏

AI 安全护栏是百炼平台在请求链路关键节点（输入/输出侧）部署的轻量级、可配置的内容安全检测与干预机制，用于实时识别并拦截涉黄、涉政、广告、暴力、违禁等高风险内容，保障模型调用符合国家法规与企业合规要求。它不依赖模型自身能力，而是由平台统一注入检测逻辑，具备低延迟、高覆盖、策略可管可控的特点。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用模型调用（文本/图片类）**：适用于所有支持的文本生成、多模态理解与生成模型（如 Qwen-VL、Qwen2.5、Qwen3 等）。需通过请求头 `X-DashScope-DataInspection` 显式启用，或在业务空间维度全局开关（控制台 → 安全设置 → 内容安全）。
- **Agent 场景**：与 Agent 治理机制协同工作——AI 安全护栏负责输入指令与最终输出的内容层过滤（如用户提问含违法信息、Agent 回复含敏感词），而 Agent 治理侧重工具调用、权限控制与运行时行为约束（如禁止调用未授权 API）。二者分层防护，互不替代。
- **Security API 集成**：安全护栏的拦截事件会自动归入 `content_safety` 类型告警，可通过 Security API 的 `/alerts` 接口查询、筛选（如 `risk_level=high&status=intercepted`）和导出，实现可观测性闭环。
- **合规交付支撑**：所有拦截日志（不含原始内容）默认接入审计系统，配合模型备案号、加密传输与私网访问能力，共同满足《生成式人工智能服务管理暂行办法》对内容审核、日志留存与数据不出域的要求。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `X-DashScope-DataInspection` | HTTP Header | string | 是（按需启用） | JSON 字符串，指定检测范围。示例：<br>`{"input":"cip","output":"cip"}`（同时检测输入与输出）<br>`{"input":"off","output":"cip"}`（仅检测输出）<br>取值为 `"cip"`（启用）、`"off"`（关闭） |
| `workspace_id`（业务空间） | 请求上下文 | string | 是（隐式） | 决定是否继承该空间全局开关状态；若未传 `X-DashScope-DataInspection`，则以控制台中该空间的「内容安全总开关」为准 |
| `region` | Endpoint 域名 | string | 是 | **仅限 `cn-beijing`（华北2）**，其他地域调用将静默跳过检测 |

> ⚠️ 注意：  
> - 安全护栏检测不改变模型推理逻辑，拦截后返回标准错误响应（HTTP 400 + `{"code":"ContentSafetyViolation", "message":"..."}`），不触发重试或 fallback；  
> - 检测基于规则+轻量模型，**不支持自定义敏感词库或语义级深度识别**（如需更细粒度控制，请结合 Agent 治理中的正则脱敏或自定义规则扩展）；  
> - 输入检测作用于 `messages` 中全部 `content` 字段（含 system/user/assistant 角色），输出检测作用于模型最终返回的 `content`。

## 面向开发者，简洁实用

- ✅ **快速启用**：在 SDK 调用中添加一行 header 即可（Python 示例）：
  ```python
  headers = {"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'}
  response = dashscope.Generation.call(..., headers=headers)
  ```
- ✅ **调试建议**：开发阶段可先设为 `{"input":"off","output":"cip"}`，仅校验输出安全性，避免误拦截测试输入；上线前务必开启双向检测。
- ✅ **可观测性**：拦截事件 5 秒内同步至 Security API 告警系统，推荐每日定时调用 `/alerts?status=intercepted&current_page=1&page_size=100` 拉取当日拦截摘要，用于策略优化与合规报告。
- ❌ **不适用场景**：语音、视频流式输入、非文本/图片类模型（如语音合成 TTS）、以及非北京地域部署的应用——请改用应用层前置校验或私有化部署方案。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [application support](../guides/application-support.md)


