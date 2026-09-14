# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置及售后保障等环节。开发者可通过该支持体系快速集成和调试应用，确保生产环境稳定运行。具体能力与约束详见下文。

## 支持的模型/功能

当前 `application support` 仅面向百炼平台已上线的**托管型应用（Managed Application）** 提供支持，不覆盖自定义推理服务或本地部署模型。支持的功能包括：应用生命周期管理（创建/更新/下线）、API 调用配额控制、请求日志回溯（7 天内）、基础错误码映射（如 `429`, `503` 的语义解释）。详细功能列表请参阅 [服务支持](../../raw/application-user-guide/application-support.md)。

## 关键参数

调用 `application support` 相关接口（如 `/v1/applications/{app_id}/support`）需传入以下必选参数：
- `app_id`: 应用唯一标识，须与百炼控制台中显示的 ID 完全一致（区分大小写）；
- `support_type`: 取值为 `debug`, `quota`, `log` 之一，决定支持类型；
- `timestamp`: UNIX 时间戳（秒级），用于签名验证，误差不可超过 ±300 秒。  
参数规范与示例见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 使用方式

1. 登录百炼控制台 → 进入「应用管理」→ 选择目标应用 → 点击右上角「技术支持」；
2. 或通过 OpenAPI 调用 `POST /v1/applications/{app_id}/support`，需携带有效 AccessKey 及签名；
3. 提交后，系统将在 2 小时内生成诊断报告（含请求链路、模型响应延迟分布、失败原因分类）。  
完整操作流程与权限说明请参考 [服务支持](../../raw/application-user-guide/application-support.md)。

## 限制和注意事项

- 单个应用每月最多提交 5 次支持请求，超出后需联系商务升级；
- 日志回溯仅保留最近 7 天原始请求体（含 `input` 和 `parameters`），超过时限不可恢复；
- > **注意**：原始文档中提及的「[售后说明](https://help.aliyun.com/zh/model-studio/application-after-sales-service-scope)」链接已失效（HTTP 404），当前实际服务范围以控制台「技术支持」页内弹窗说明为准；  
- 不支持对已下线应用发起支持请求，若需恢复，请先重新上线应用。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


