# DeepSeek Harness

在 DeepSeek Harness 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="dsh-quickstart-h"></a>

## 快速开始

<a id="dsh_install_h"></a>

1.  1
    
    启动 Web UI
    
    运行以下命令启动 DeepSeek Harness Web UI：
    
    <a id="code-block"></a>
    
    ```bash
    dsh web
    ```
    
    默认地址为 `http://127.0.0.1:3080`，本机启动时会自动打开浏览器。
    
2.  2
    
    获取 API Key
    
    根据计费方案获取对应的 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
3.  3
    
    配置模型
    
    <a id="dsh_config_h"></a>
    
    在 Web UI 中进入 **设置 → 模型**，点击 **添加模型提供商**，切换到 **自定义模型 API**。DeepSeek Harness 未内置百炼提供商，Provider ID 可自定义（小写），下表以 `bailian-tpp`、`bailian`、`bailian-coding` 为例：
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="dsh_tpp_h"></a>
    
    <a id="dsh_tp_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | Provider ID | `bailian-tpp` |
    | 显示名称 | Alibaba Cloud Model Studio |
    | 基础 URL | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API 协议 | OpenAI Chat Completions |
    | API 密钥 | 上一步获取的 Token Plan API Key |
    | 模型 | 填写[个人版](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型 |
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="dsh_payg_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | Provider ID | `bailian` |
    | 显示名称 | Alibaba Cloud Model Studio |
    | 基础 URL | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，`{WorkspaceId}` 替换为 [Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain) |
    | API 协议 | OpenAI Chat Completions |
    | API 密钥 | 上一步获取的百炼 API Key |
    | 模型 | 例如 `qwen3.8-max`、`qwen3.8-flash` |
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="dsh_cp_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | Provider ID | `bailian-coding` |
    | 显示名称 | Alibaba Cloud Model Studio |
    | 基础 URL | `https://coding.dashscope.aliyuncs.com/v1` |
    | API 协议 | OpenAI Chat Completions |
    | API 密钥 | 上一步获取的 Coding Plan API Key |
    | 模型 | 填写[支持的文本生成模型](../coding-plan-guide/coding-plan.md) |
    
    保存后，在 Web UI 的模型选择器中选择已添加的模型。
    
4.  4
    
    验证
    
    <a id="dsh_verify_h"></a>
    
    在 Web UI 中发送一条消息，模型正常返回响应即表示配置成功。
    

<a id="通过配置文件接入"></a>

<a id="dsh-config-file-h"></a>

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    `~/.dsh/profiles/web/cordis.patch.yml`
    
2.  2
    
    写入配置
    
    按计费方案添加以下配置。只添加对应条目，不要覆盖已有配置。启动前设置 `BAILIAN_API_KEY` 环境变量：
    
    <a id="code-block-2"></a>
    
    ```bash
    export BAILIAN_API_KEY="YOUR_API_KEY"
    ```
    
    <a id="sec-tabs-2"></a>
    
    <a id="token-plan-个人版"></a>
    
    <a id="token-plan-个人版-h4"></a>
    
    #### Token Plan 个人版
    
    <a id="code-block-3"></a>
    
    ```yaml
    - id: llm-pi-ai
      config:
        providers:
          bailian-tpp:
            apiKeyEnv: BAILIAN_API_KEY
            api: openai-completions
            baseURL: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
            models:
              - id: auto
              - id: qwen4-max
              - id: qwen3.8-max
              - id: qwen3.8-flash
              - id: qwen3.7-max
              - id: qwen3.7-plus
              - id: qwen3.6-flash
              - id: deepseek-v4.1-flash
              - id: deepseek-v4.1-flash-1017
              - id: deepseek-v4-pro
              - id: deepseek-v4-pro-0813
              - id: deepseek-v4-flash-0731
              - id: glm-5.3
              - id: glm-5.2
    ```
    
    <a id="token-plan-团队版"></a>
    
    <a id="token-plan-团队版-h4"></a>
    
    #### Token Plan 团队版
    
    <a id="code-block-4"></a>
    
    ```yaml
    - id: llm-pi-ai
      config:
        providers:
          bailian-tpp:
            apiKeyEnv: BAILIAN_API_KEY
            api: openai-completions
            baseURL: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
            models:
              - id: auto
              - id: qwen4-max
              - id: qwen3.8-max
              - id: qwen3.8-flash
              - id: qwen3.7-max
              - id: qwen3.7-plus
              - id: qwen3.6-plus
              - id: qwen3.6-flash
              - id: deepseek-v4.1-flash
              - id: deepseek-v4.1-flash-1017
              - id: deepseek-v4-pro
              - id: deepseek-v4-pro-0813
              - id: deepseek-v4-flash-0731
              - id: kimi-k2.7-code
              - id: kimi-k2.6
              - id: kimi-k2.5
              - id: glm-5.3
              - id: glm-5.2
              - id: glm-5.1
              - id: glm-5
              - id: MiniMax-M2.5
    ```
    
    <a id="按量计费-2"></a>
    
    <a id="按量计费-2-h4"></a>
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)：
    
    <a id="code-block-5"></a>
    
    ```yaml
    - id: llm-pi-ai
      config:
        providers:
          bailian:
            apiKeyEnv: BAILIAN_API_KEY
            api: openai-completions
            baseURL: https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
            models:
              - id: qwen3.8-max
              - id: qwen3.7-plus
              - id: qwen3.8-flash
              - id: deepseek-v4-pro-0813
              - id: deepseek-v4.1-flash
    ```
    
    <a id="coding-plan-2"></a>
    
    <a id="coding-plan-2-h4"></a>
    
    #### Coding Plan
    
    <a id="code-block-6"></a>
    
    ```yaml
    - id: llm-pi-ai
      config:
        providers:
          bailian-coding:
            apiKeyEnv: BAILIAN_API_KEY
            api: openai-completions
            baseURL: https://coding.dashscope.aliyuncs.com/v1
            models:
              - id: qwen3.7-plus
              - id: qwen3.6-plus
              - id: kimi-k2.5
              - id: glm-5
              - id: MiniMax-M2.5
              - id: qwen3.5-plus
    ```
    
    > **说明**
    >
    > 使用 qwen4-max 时，需要显式缓存可添加 `compat.cacheControlFormat: anthropic`；需要更高输出可设置 `maxTokens: 262144`。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    

保存后重启 DeepSeek Harness，在模型选择器中选择已添加的模型。

<a id="错误码"></a>

<a id="dsh_error_h"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="dsh_faq_h"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-fetch-available-models-返回-401"></a>

Fetch available models 返回 401

百炼 OpenAI 兼容端点不提供 `GET /models` 接口，点击 **Fetch available models** 会返回 401 或 404。该按钮可忽略，在模型目录中手动输入模型 ID 即可。

<a id="dsh_faq_fetch_h"></a>

<a id="accordion-报错-missing-credential"></a>

报错 MISSING\_CREDENTIAL

在 Web UI 的 **设置 → 模型** 中重新输入 API Key 并保存；或确认环境变量 `BAILIAN_API_KEY` 已设置并重启 DeepSeek Harness。

<a id="dsh_faq_missing_cred_h"></a>

<a id="accordion-配置后找不到已添加的模型"></a>

配置后找不到已添加的模型

重启 DeepSeek Harness，再在 Web UI 的模型选择器中选择。新增模型时，在 **设置 → 模型** 中编辑该提供商，在模型目录中添加模型 ID 并保存；也可以编辑 `cordis.patch.yml` 的 `models`。
