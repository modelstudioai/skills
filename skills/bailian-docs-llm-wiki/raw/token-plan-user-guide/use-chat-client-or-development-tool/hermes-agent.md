# Hermes Agent

在 Hermes Agent 中使用阿里云百炼模型。

<a id="快速接入"></a>

<a id="ha-quickstart-h"></a>

## 快速接入

选择你使用的客户端，完成配置。

<a id="sec-tabs"></a>

<a id="cli"></a>

<a id="cli-h4"></a>

#### CLI

1.  1
    
    获取 API Key
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    运行 `hermes model`，按计费方案选择 provider，输入 API Key 并选择模型。
    
    <a id="sec-tabs-2"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    1.  选择 `Qwen` > `Alibaba Cloud (Token Plan, China)`。
    2.  输入 Token Plan API Key，Base URL 保持默认。
    3.  选择模型。支持的模型见个人版[支持的模型](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)和团队版[支持的模型](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)。
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    1.  选择 `Qwen` > `Alibaba Cloud DashScope (China)`。
    2.  输入百炼 API Key。
    3.  以下以华北2（北京）为例，Base URL 填写 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。
    4.  选择模型。支持的模型见[支持的模型](../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#7f9c78ae99pwz)。
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    1.  选择 `Qwen` > `Alibaba Cloud (Coding Plan, China)`。
    2.  输入 Coding Plan 专属 API Key，Base URL 保持默认。
    3.  选择模型。支持的模型见 [Coding Plan 支持的模型](../coding-plan-guide/coding-plan.md)。
    
    > **说明**
    >
    > provider 列表中的模型可能多于当前套餐支持的模型，实际可用模型以套餐支持列表为准。
    
3.  3
    
    验证
    
    <a id="ha-verify-h"></a>
    
    运行以下命令验证：
    
    <a id="code-block"></a>
    
    ```bash
    hermes chat -q "你好"
    ```
    

<a id="桌面版"></a>

<a id="桌面版-h4"></a>

#### 桌面版

<a id="ha-desktop-h"></a>

1.  1
    
    配置模型
    
    按[通过配置文件接入](#ha-manual-h)写入对应方案的配置，或先在 CLI 中完成配置。
    
2.  2
    
    选择模型
    
    打开 Hermes Desktop，进入 **Settings → Model**，选择同名 provider 和模型。
    

<a id="通过配置文件接入"></a>

<a id="ha-plans-h"></a>

<a id="tp-ha-config-h"></a>

<a id="ha-manual-h"></a>

## 通过配置文件接入

`hermes model` 的 provider 列表从 v2026.8.31 起包含阿里云百炼。列表中没有时，按以下步骤接入。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux / WSL2：`~/.hermes/config.yaml`
    -   Windows：`%LOCALAPPDATA%\hermes\config.yaml`
    
2.  2
    
    写入配置
    
    将 `YOUR_API_KEY` 替换为对应方案的 API Key；按量计费还需将 `{WorkspaceId}` 替换为实际值。将配置写入 `model` 部分。
    
    <a id="sec-tabs-3"></a>
    
    <a id="token-plan-2"></a>
    
    <a id="token-plan-2-h4"></a>
    
    #### Token Plan
    
    <a id="ha-tpp-h"></a>
    
    <a id="ha-tp-h"></a>
    
    **OpenAI 兼容协议**
    
    <a id="code-block-2"></a>
    
    ```yaml
    model:
      default: auto
      provider: custom
      base_url: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      api_key: YOUR_API_KEY
    ```
    
    **Anthropic 兼容协议**
    
    <a id="code-block-3"></a>
    
    ```yaml
    model:
      default: auto
      provider: custom
      base_url: https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic
      api_mode: anthropic_messages
      api_key: YOUR_API_KEY
    ```
    
    <a id="按量计费-2"></a>
    
    <a id="按量计费-2-h4"></a>
    
    #### 按量计费
    
    <a id="ha-payg-h"></a>
    
    <a id="ha-payg-config-h"></a>
    
    以下示例使用华北2（北京）。
    
    **OpenAI 兼容协议**
    
    <a id="code-block-4"></a>
    
    ```yaml
    model:
      default: qwen3.8-max
      provider: custom
      base_url: https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      api_key: YOUR_API_KEY
    ```
    
    **Anthropic 兼容协议**
    
    <a id="code-block-5"></a>
    
    ```yaml
    model:
      default: qwen3.8-max
      provider: custom
      base_url: https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic
      api_mode: anthropic_messages
      api_key: YOUR_API_KEY
    ```
    
    <a id="coding-plan-2"></a>
    
    <a id="coding-plan-2-h4"></a>
    
    #### Coding Plan
    
    <a id="ha-cp-h"></a>
    
    <a id="ha-cp-config-h"></a>
    
    **OpenAI 兼容协议**
    
    <a id="code-block-6"></a>
    
    ```yaml
    model:
      default: qwen3.7-plus
      provider: custom
      base_url: https://coding.dashscope.aliyuncs.com/v1
      api_key: YOUR_API_KEY
    ```
    
    **Anthropic 兼容协议**
    
    <a id="code-block-7"></a>
    
    ```yaml
    model:
      default: qwen3.7-plus
      provider: custom
      base_url: https://coding.dashscope.aliyuncs.com/apps/anthropic
      api_mode: anthropic_messages
      api_key: YOUR_API_KEY
    ```
    
    > **说明**
    >
    > 使用 qwen4-max 时，`provider` 必须保持 `custom`，不要设为 `anthropic`，否则模型名会被改写并返回 400。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    
3.  3
    
    验证
    
    保存后运行 `hermes chat -q "你好"` 验证。
    

<a id="错误码"></a>

<a id="ha-faq-error-h"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="ha-faq-h"></a>

## 常见问题

<a id="accordion-hermes-model-中没有阿里云百炼"></a>

hermes model 中没有阿里云百炼

通过[配置文件接入](#ha-manual-h)。

<a id="ha-faq-provider-h"></a>

<a id="accordion-模型不可用"></a>

模型不可用

`hermes model` 的模型列表可能包含当前套餐不支持的模型。按对应套餐的支持列表选择，或选择 `Enter custom model name` 后输入模型 ID。

<a id="ha-faq-model-h"></a>

<a id="accordion-节省计划和资源包如何接入"></a>

节省计划和资源包如何接入

节省计划和资源包的接入方式同[按量计费](#ha-payg-h)，会自动抵扣符合条件的调用费用。抵扣规则见[节省计划与资源包](../../model-user-guide/test-1/savings-plan-and-resource-package.md)。

<a id="ha-savings-h"></a>
