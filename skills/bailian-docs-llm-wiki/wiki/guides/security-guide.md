# security guide

百炼平台提供多层次安全防护能力，覆盖模型调用、Agent 资产管理、策略配置与风险审计等关键环节。开发者可通过控制台、CLI 或 API 集成安全策略，所有防护机制默认启用且可按需精细化配置。安全能力与模型服务深度耦合，不依赖额外部署。

## 支持的模型/功能

- 所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio）均默认启用输入内容安全检测（含敏感词、违规图像/音频识别）  
- Agent 框架支持资产级隔离：每个 Agent 实例拥有独立的安全策略上下文，策略生效范围严格限定于其绑定的模型和数据源  
- 安全能力与 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 中定义的四层防护体系（接入层、模型层、数据层、审计层）对齐  

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `security_level` | string | 安全检测强度，取值 `basic` / `standard` / `strict` | `standard` |
| `block_on_violation` | boolean | 检测到违规内容时是否阻断请求（`false` 时仅记录日志并返回 `warning` 字段） | `true` |
| `custom_policy_id` | string | 引用自定义安全策略 ID，需通过 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 创建 | `null` |

> **注意**：`security_level=strict` 会启用 OCR+语义双模检测，但可能增加 200–400ms 延迟；该行为与 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) 中“延迟说明”章节一致，但与旧版文档中“strict 模式无性能影响”的描述矛盾，以当前 API 文档为准。

## 使用方式

- **API 调用**：在请求 Header 中添加 `X-Security-Level: strict`，或在 JSON body 的 `parameters` 对象中传入上述关键参数  
- **CLI 配置**：使用 `bailian security set --level strict --block true` 命令全局设置，或通过 `--policy-id` 指定策略（详见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)）  
- **控制台配置**：在 Agent 编辑页 → “安全设置”标签页中调整，修改实时生效，无需重启服务  

## 限制和注意事项

- 单次请求最大文本长度受安全检测模块限制：`basic` 级别为 10k tokens，`strict` 级别为 5k tokens（超长内容将被截断并告警）  
- 图像/视频安全检测仅支持 JPEG/PNG/MP4 格式，AVIF、WebP 等格式暂不支持内容扫描  
- 自定义策略（`custom_policy_id`）最多关联 50 个 Agent 实例；超出后需解绑旧实例或联系技术支持扩容  
- 所有安全事件日志保留 90 天，审计详情需通过 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面导出，不开放原始日志 API 下载

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


