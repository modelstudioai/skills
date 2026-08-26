# DeepSeek Harness

DeepSeek Harness 是 DeepSeek 开源的 AI Agent 框架，支持 Web UI 和命令行两种模式。通过阿里云百炼，可以使用按量计费、Coding Plan、Token Plan 个人版或 Token Plan 团队版接入 DeepSeek Harness。

## 安装 DeepSeek Harness

1.  安装 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。
2.  在终端中执行以下命令启动 DeepSeek Harness Web UI：

```
npx @deepseek-ai/dsh web
```

命令执行后，Web UI 默认运行在 `http://127.0.0.1:3080`。

## 配置接入凭证

编辑配置文件 `~/.dsh/settings.yaml`，添加百炼供应商和默认模型。也可启动 Web UI 后在 **Settings → Models → Add a custom provider** 中通过界面配置。

### Token Plan 个人版

将 YOUR\_API\_KEY 替换为 Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)。可用模型参见 Token Plan 个人版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

**Provider ID**

`bailian-tpp`

**Base URL**

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

**API Protocol**

`openai-completions`

**API Key**

Token Plan 个人版专属 API Key

**模型**

填入模型 ID，如 `qwen3.8-max`

也可直接编辑 `~/.dsh/settings.yaml`：

```
agent-default-model:
  provider: bailian-tpp
  model: qwen3.8-max

llm-pi-ai:
  providers:
    bailian-tpp:
      api: openai-completions
      baseURL: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      apiKeyEnv: BAILIAN_API_KEY
      models:
        - id: qwen3.8-max
        - id: qwen3.7-max
        - id: qwen3.7-plus
        - id: qwen3.6-flash
```

设置环境变量 `BAILIAN_API_KEY` 为你的 Token Plan 个人版 API Key：

```
export BAILIAN_API_KEY="YOUR_API_KEY"
```

也可在 Web UI 的 **Settings → Models** 页面直接填入 API Key。

### Token Plan 团队版

将 YOUR\_API\_KEY 替换为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。可用模型参见 Token Plan 团队版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

**Provider ID**

`bailian-tp`

**Base URL**

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

**API Protocol**

`openai-completions`

**API Key**

Token Plan 团队版专属 API Key

**模型**

填入模型 ID，如 `qwen3.8-max`

对应 `~/.dsh/settings.yaml` 配置：

```
agent-default-model:
  provider: bailian-tp
  model: qwen3.8-max

llm-pi-ai:
  providers:
    bailian-tp:
      api: openai-completions
      baseURL: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      apiKeyEnv: BAILIAN_API_KEY
      models:
        - id: qwen3.8-max
        - id: qwen3.7-max
        - id: qwen3.7-plus
        - id: qwen3.6-flash
```

### Coding Plan

将 YOUR\_API\_KEY 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。可用模型参见 Coding Plan [支持的模型](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

**Provider ID**

`bailian-coding`

**Base URL**

`[https://coding.dashscope.aliyuncs.com/v1](https://coding.dashscope.aliyuncs.com/v1)`

**API Protocol**

`openai-completions`

**API Key**

Coding Plan 专属 API Key

**模型**

填入模型 ID，如 `qwen3.7-plus`

对应 `~/.dsh/settings.yaml` 配置：

```
agent-default-model:
  provider: bailian-coding
  model: qwen3.7-plus

llm-pi-ai:
  providers:
    bailian-coding:
      api: openai-completions
      baseURL: https://coding.dashscope.aliyuncs.com/v1
      apiKeyEnv: BAILIAN_API_KEY
      models:
        - id: qwen3.7-plus
        - id: qwen3.6-plus
```

### 按量计费

将 YOUR\_API\_KEY 替换为[阿里云百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)。可用模型参见[OpenAI 兼容 - 支持的模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages)。

`Base URL` 按地域设置，请将 URL 中的 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)：

-   华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

**Provider ID**

`bailian`

**Base URL**

参见上方地域列表

**API Protocol**

`openai-completions`

**API Key**

百炼 API Key（`sk-` 开头）

**模型**

填入模型 ID，如 `qwen3.7-max`

对应 `~/.dsh/settings.yaml` 配置：

```
agent-default-model:
  provider: bailian
  model: qwen3.7-max

llm-pi-ai:
  providers:
    bailian:
      api: openai-completions
      baseURL: https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      apiKeyEnv: BAILIAN_API_KEY
      models:
        - id: qwen3.7-max
        - id: qwen3.7-plus
        - id: qwen3.6-flash
```

## 验证配置

配置保存后，在 Web UI 的模型选择器中选择已配置的模型，发送一条消息。若模型正常返回响应，配置成功。

## 常见问题

### 错误码

配置过程中遇到报错，参考对应套餐的常见问题文档：

-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
-   Token Plan 个人版：[Token Plan 常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
-   Token Plan 团队版：[Token Plan 团队版常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)

### Fetch available models 返回 401

百炼 OpenAI 兼容端点不提供 `GET /models` 接口，点击 **Fetch available models** 会返回 401 或 404。该按钮可忽略，在 Model catalog 中手动输入模型 ID 即可。

### 报错 MISSING\_CREDENTIAL

在 Web UI 的 **Settings → Models** 中重新输入 API Key 并保存；或确认环境变量 `BAILIAN_API_KEY` 已设置并重启 DeepSeek Harness。
