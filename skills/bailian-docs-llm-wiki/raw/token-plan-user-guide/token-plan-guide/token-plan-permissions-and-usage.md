# 权限与使用规范

Token Plan 的购买与订阅权限、RAM 子账号授权、使用范围、API Key 规范和数据使用政策。

<a id="购买与订阅"></a>

<a id="tppu-h-purchase"></a>

## 购买与订阅

-   主账号可直接购买 Token Plan。
-   RAM 子账号需主账号授权后才能购买、管理订阅或使用模型。
-   同一实名认证主体限购一份个人版和一份团队版，可同时购买；团队版可购买多个坐席，最多 1,000 个坐席。

<a id="ram-子账号授权"></a>

<a id="tppu-h-access"></a>

## RAM 子账号授权

RAM 子账号使用 Token Plan 前，需由主账号完成以下授权：

1.  **Token Plan 权限**：授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）。
2.  **费用中心权限**：授予 `AliyunBSSReadOnlyAccess`（只读）或 `AliyunBSSFullAccess`（管理）。
3.  **百炼控制台权限**：在账号管理页面为该 RAM 子账号分配管理员或订阅套餐权限。

> **说明**
>
> RAM 子账号无需单独实名认证。只要主账号已完成实名认证，并为 RAM 子账号分配了使用权限，该 RAM 子账号即可正常使用 Token Plan。

缺少费用中心权限时，RAM 子账号登录后**我的订阅**页面可能显示为空。

<a id="套餐使用范围"></a>

<a id="tppu-h-scope"></a>

## 套餐使用范围

Token Plan **仅限在编程工具和智能体工具**（如 Claude Code、Cursor、Qwen Code、Qoder、OpenClaw 等）中**交互式使用**，**不可用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景**。

模型通过工具的扩展机制（Skill、Slash Command 或 Agent）接入，工具内交互式发起的调用属于正常使用。**将 Token Plan 套餐 API Key 用于允许范围之外的调用可能被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。**

<a id="api-key-使用规范"></a>

<a id="tppu-h-key"></a>

## API Key 使用规范

-   **Token Plan 套餐 API Key**：以 `sk-sp-` 开头，仅用于 Token Plan 模型调用，只在生成时完整显示一次。
-   **个人版设备**：同一个 API Key 可配置到本人的多台设备（如家庭电脑和公司电脑），但仅限本人使用。
-   **不可共享**：API Key 仅限订阅人本人使用，不可共享或公开泄露。将 API Key 共享给他人使用可能被判定为违规并导致封禁。

<a id="数据使用政策"></a>

<a id="tppu-h-data"></a>

## 数据使用政策

| 版本 | 数据使用规则 |
| --- | --- |
| 个人版 | 使用期间，模型输入以及模型生成的内容将用于服务改进与模型优化。停止使用个人版服务可终止后续数据授权，但不涵盖已授权使用的数据。详细条款见[阿里云百炼服务协议第 5.2 条](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)。 |
| 团队版 | 不会使用对话数据训练模型。 |

<a id="常见问题"></a>

<a id="tppu-h-faq"></a>

## 常见问题

<a id="accordion-主账号和-ram-子账号都能购买吗"></a>

主账号和 RAM 子账号都能购买吗

可以。主账号可直接购买；RAM 子账号需先由主账号完成 Token Plan 权限、费用中心权限和账号管理权限授权。

<a id="accordion-ram-子账号需要哪些权限"></a>

RAM 子账号需要哪些权限

需要 Token Plan 系统策略、费用中心权限，以及百炼控制台的账号管理权限。具体策略见上文“RAM 子账号授权”。

<a id="accordion-我的订阅页面显示为空"></a>

我的订阅页面显示为空

通常是 RAM 子账号缺少费用中心权限。授予 `AliyunBSSReadOnlyAccess`（只读）或 `AliyunBSSFullAccess`（管理）。

<a id="accordion-ram-子账号能调用模型吗"></a>

RAM 子账号能调用模型吗

经主账号授权后可以。RAM 授权只决定管理权限，实际调用还需要对应的 Token Plan API Key。
