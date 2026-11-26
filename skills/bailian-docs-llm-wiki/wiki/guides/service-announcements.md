# service announcements

服务公告（Service Announcements）是百炼平台面向开发者发布的、影响 API 行为、计费模型、功能可用性或基础设施的正式变更通知。所有公告均按发布时间倒序排列，涵盖产品调整、调价、升级、下线、网络变更等类型。开发者应定期查阅以确保应用兼容性与成本可控性。最新公告可直接在 [产品公告](../../raw/product-updates/service-announcements/product-announcements.md) 中获取。

## 支持的模型/功能

服务公告覆盖以下核心能力范围：
- **模型生命周期管理**：包括主线/快照模型下线（如 `qwen-turbo` 资源包退市、`Qwen3.5` 旧版本下线）、模型升级（如 `Qwen-Image-2.0-Pro`、`Qwen3-VL-Flash`）、以及商业化启动（如 `千问联网检索 Agent`、`全妙-视频混剪`）；
- **MCP 相关服务**：MCP 广场整体演进，含 `WebParser` 下线、`天气通MCP` 下线、`4个MCP服务下线` 及 `部分MCP服务下线` 等多轮调整；
- **配套能力变更**：知识库 Metadata 抽取计费方式调整、记忆库商业化、Managed Agents 商业化、智能路由入口及权限调整、网关变更（多次通告）、DashScope 域名维护等；
- **基础设施升级**：北京地域公网出口 IP 扩容、美国（弗吉尼亚）业务空间部署模式变更、PTU（预置吞吐）能力升级等。

> **注意**：文档中存在多处模型下线时间冲突。例如 `[部分老旧模型下线通知](../../raw/product-updates/service-announcements/product-announcements.md)`（2026-07-14）与 `[部分老旧模型延期下线通知](../../raw/product-updates/service-announcements/product-announcements.md)`（2026-07-06）明确表明原计划下线被推迟，开发者需以延期通知为准。

## 关键参数

公告本身不定义运行时参数，但直接影响以下关键配置项的行为或有效性：
- `model` 名称：下线模型（如 `kimi-k2.5`、`GTE-RERANK`）将返回 `404 Model Not Found`；升级模型（如 `Qwen3.8-Max`）可能引入新字段或弃用旧字段；
- `endpoint` / `domain`：网关变更（如 `[网关变更通告](../../raw/product-updates/service-announcements/product-announcements.md)` 多次出现）和域名维护（`[百炼DashScope 域名进入维护状态通知](../../raw/product-updates/service-announcements/product-announcements.md)`）要求客户端及时切换至新域名；
- `pricing tier` / `plan`：`Token Plan` 个人版降价、`Coding Plan Lite` 停止新购与续费、`GLM-5.2 Fast mode` 降价等均需同步更新计费策略；
- `region`：北京/弗吉尼亚地域变更可能影响延迟与 SLA，需检查 `RegionEndpoint` 配置。

## 使用方式

- **主动订阅**：通过阿里云官网「产品公告」页或控制台消息中心接收推送；
- **程序化集成**：建议在 CI/CD 流程中定期拉取 [产品公告](../../raw/product-updates/service-announcements/product-announcements.md) 的 Markdown 源文件，解析 `<a id="announcement-XXXXXX">` 锚点及日期标签，构建本地变更日志；
- **关键路径验证**：对涉及下线/升级的模型或服务，应在公告生效前完成兼容性测试（如替换 `qwen-vl-ocr` 为新版 OCR 模型）；
- **告警联动**：将高频变更类型（如下线、网关变更）纳入监控系统，当 API 返回 `404` 或 `503` 且时间窗口匹配公告日期时触发告警。

## 限制和注意事项

- 所有下线类公告（如 `[Agent1.0长期记忆功能下线](../../raw/product-updates/service-announcements/product-announcements.md)`、`[DMS-数据库安全访问下线通知](../../raw/product-updates/service-announcements/product-announcements.md)`）均无回滚机制，调用将永久失败；
- 网关变更类通告（如 `[网关变更通告](../../raw/product-updates/service-announcements/product-announcements.md)` 共出现 3 次）通常伴随短暂不可用（<5 分钟），不承诺零中断；
- 调价类公告（如 `[DeepSeek-V4.1-Flash系列模型缓存命中价格调整通知](../../raw/product-updates/service-announcements/product-announcements.md)`）自生效日起按新单价计费，历史用量不追溯；
- 模型字段变更（如 `[部分模型字段变更通知](../../raw/product-updates/service-announcements/product-announcements.md)`）可能导致 JSON Schema 校验失败，需更新客户端解析逻辑；
- “其他”类通告（如 SLA 协议变更、服务协议更新）虽不直接影响 API，但具法律效力，建议法务团队同步审阅。

## 来源文档

- [产品公告](../../raw/product-updates/service-announcements/product-announcements.md)


