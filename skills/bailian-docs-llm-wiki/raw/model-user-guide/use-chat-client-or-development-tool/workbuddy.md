# 接入 WorkBuddy

WorkBuddy 是一款桌面 AI Agent 工作台，可以通过按量计费、Coding Plan、Token Plan 个人版或 Token Plan 团队版接入阿里云百炼。

## 安装 WorkBuddy

前往 [WorkBuddy 官网](https://www.workbuddy.cn/)，点击**立即下载**，根据操作系统下载安装包并完成安装。启动后按照页面提示登录 WorkBuddy 账号。

## 配置接入凭证

1.  在对话界面底部点击模型选择器，在列表底部点击**配置自定义模型**；也可以从左下角头像进入**设置**，在左侧导航的功能分组中选择**模型**。
2.  点击**添加模型**，供应商选择**自定义**。
3.  填写接口地址、API Key 与模型名称；可点击**测试连接**确认接口连通。
4.  点击**保存**。

百炼提供四种计费方案，根据需要选择：

-   **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
-   **按量计费**：按实际调用量后付费。

**说明**

1.  接口地址**不会自动补全**，需填写完整的 Chat Completions 地址（结尾为 `/chat/completions`），见下方各方案配置。
2.  自定义模型仅支持 OpenAI 兼容的 Chat Completions 协议，不支持 Responses API 与 Anthropic 协议。

### Token Plan 个人版

配置项

说明

**接口地址**

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

**API Key**

填入 Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)。

**模型名称**

填写百炼模型名（如 `qwen3.7-plus`）。可用模型请参考 Token Plan 个人版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

### Token Plan 团队版

配置项

说明

**接口地址**

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

**API Key**

填入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/enterprise)。

**模型名称**

填写百炼模型名（如 `qwen3.7-plus`）。可用模型请参考 Token Plan 团队版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### Coding Plan

配置项

说明

**接口地址**

`https://coding.dashscope.aliyuncs.com/v1/chat/completions`

**API Key**

填入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。

**模型名称**

填写百炼模型名（如 `qwen3.7-plus`）。可用模型请参考 Coding Plan [支持的模型](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 按量计费

填入[阿里云百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)。可用模型请参考 [OpenAI 兼容接口支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

接口地址按地域选择，API Key 需与所选地域对应（URL 中的 `{WorkspaceId}` 需替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）：

-   华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
-   美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

## 验证配置

保存后，在对话界面底部的模型选择器中选择已添加的模型，输入任意问题，模型正常返回响应即配置成功。

更多 WorkBuddy 功能与模型配置说明，请参考 [WorkBuddy 官方文档](https://www.workbuddy.cn/docs/workbuddy/Overview)。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量计费：[错误码排查](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
-   Token Plan 个人版：[Token Plan 个人版常见问题](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
-   Token Plan 团队版：[Token Plan 团队版常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)

### 调用时报错模型不存在

模型名称会作为请求中的 `model` 参数发送，须与百炼模型名完全一致（区分大小写，不带额外前后缀）。在自定义模型设置中核对模型名称后重试。
