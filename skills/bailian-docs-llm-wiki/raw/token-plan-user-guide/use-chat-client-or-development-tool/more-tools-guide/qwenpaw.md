# QwenPaw

在 QwenPaw 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="qwp-config-h"></a>

<a id="qwp-quickstart-h"></a>

<a id="qwp-cli-config-h"></a>

## 快速开始

1.  1
    
    获取 API Key
    
    根据计费方案获取对应的 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    <a id="code-block"></a>
    
    ```bash
    qwenpaw models config
    ```
    
    按提示依次选择提供商、粘贴 API Key、选择模型。提供商对应关系：
    
    -   Token Plan：**Aliyun Token Plan**（`aliyun-tokenplan`）
    -   按量计费：**DashScope**（`dashscope`）
    -   Coding Plan：**Aliyun Coding Plan (China)**（`aliyun-codingplan`）
    
3.  3
    
    验证
    
    <a id="qwp-verify-h"></a>
    
    <a id="code-block-2"></a>
    
    ```bash
    qwenpaw task -i "你好"
    ```
    
    返回 `status: success` 即配置成功。
    

<a id="通过控制台接入"></a>

<a id="qwp-install-h"></a>

## 通过控制台接入

也可以使用 Console 可视化配置：启动 QwenPaw，访问 `http://127.0.0.1:8088/` 打开 Console。

1.  1
    
    配置提供商
    
    进入 **设置** > **模型**，按计费方案配置提供商：
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="tpp-h"></a>
    
    提供商选择 **Aliyun Token Plan**，填入 Token Plan 个人版或团队版专属 API Key。
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="qwp-payg-h"></a>
    
    提供商选择 **DashScope**，基础 URL 使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，将 `{WorkspaceId}` 替换为 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，填入百炼 API Key。
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="qwp-cp-h"></a>
    
    提供商选择 **Aliyun Coding Plan (China)**，填入 Coding Plan API Key。
    
2.  2
    
    选择或添加模型
    
    模型已预设。需要新增时，点击 **添加模型**，填写模型 ID：
    
    -   Token Plan：填写[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型
    -   按量计费：例如 `qwen3.8-max`、`qwen3.8-flash`
    -   Coding Plan：例如 `qwen3.7-plus`
    
3.  3
    
    设置默认模型
    
    <a id="qwp-default-h"></a>
    
    进入 **设置** > **模型** > **默认LLM**，选择模型并保存。
    

<a id="通过配置文件接入"></a>

<a id="qwp-config-file-h"></a>

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    `~/.qwenpaw.secret/providers/custom/<provider-id>.json`
    
2.  2
    
    写入配置
    
    <a id="sec-tabs-2"></a>
    
    <a id="token-plan-个人版"></a>
    
    <a id="token-plan-个人版-h4"></a>
    
    #### Token Plan 个人版
    
    <a id="code-block-3"></a>
    
    ```json
    {
      "id": "bailian-token-plan",
      "name": "Alibaba Cloud Model Studio",
      "base_url": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      "api_key": "YOUR_API_KEY",
      "chat_model": "OpenAIChatModel",
      "models": [
        {
          "id": "auto",
          "name": "Auto",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen4-max",
          "name": "Qwen4 Max",
          "supports_image": true,
          "max_tokens": 262144,
          "max_input_length": 983616,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.8-max",
          "name": "Qwen3.8 Max",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.8-flash",
          "name": "Qwen3.8 Flash",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.7-max",
          "name": "Qwen3.7 Max",
          "supports_image": false,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.7-plus",
          "name": "Qwen3.7 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.6-flash",
          "name": "Qwen3.6 Flash",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4.1-flash",
          "name": "DeepSeek V4.1 Flash",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4.1-flash-1017",
          "name": "DeepSeek V4.1 Flash 1017",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-pro",
          "name": "DeepSeek V4 Pro",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-pro-0813",
          "name": "DeepSeek V4 Pro 0813",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-flash-0731",
          "name": "DeepSeek V4 Flash 0731",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5.3",
          "name": "GLM-5.3",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5.2",
          "name": "GLM-5.2",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        }
      ],
      "is_custom": true
    }
    ```
    
    <a id="token-plan-团队版"></a>
    
    <a id="token-plan-团队版-h4"></a>
    
    #### Token Plan 团队版
    
    <a id="code-block-4"></a>
    
    ```json
    {
      "id": "bailian-token-plan",
      "name": "Alibaba Cloud Model Studio",
      "base_url": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      "api_key": "YOUR_API_KEY",
      "chat_model": "OpenAIChatModel",
      "models": [
        {
          "id": "auto",
          "name": "Auto",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen4-max",
          "name": "Qwen4 Max",
          "supports_image": true,
          "max_tokens": 262144,
          "max_input_length": 983616,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.8-max",
          "name": "Qwen3.8 Max",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.8-flash",
          "name": "Qwen3.8 Flash",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.7-max",
          "name": "Qwen3.7 Max",
          "supports_image": false,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.7-plus",
          "name": "Qwen3.7 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.6-plus",
          "name": "Qwen3.6 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.6-flash",
          "name": "Qwen3.6 Flash",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4.1-flash",
          "name": "DeepSeek V4.1 Flash",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4.1-flash-1017",
          "name": "DeepSeek V4.1 Flash 1017",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-pro",
          "name": "DeepSeek V4 Pro",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-pro-0813",
          "name": "DeepSeek V4 Pro 0813",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-flash-0731",
          "name": "DeepSeek V4 Flash 0731",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "kimi-k2.7-code",
          "name": "Kimi K2.7 Code",
          "supports_image": true,
          "max_tokens": 98304,
          "max_input_length": 262144,
          "generate_kwargs": {}
        },
        {
          "id": "kimi-k2.6",
          "name": "Kimi K2.6",
          "supports_image": true,
          "max_tokens": 98304,
          "max_input_length": 262144,
          "generate_kwargs": {}
        },
        {
          "id": "kimi-k2.5",
          "name": "Kimi K2.5",
          "supports_image": true,
          "max_tokens": 98304,
          "max_input_length": 262144,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5.3",
          "name": "GLM-5.3",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5.2",
          "name": "GLM-5.2",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5.1",
          "name": "GLM-5.1",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5",
          "name": "GLM-5",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "MiniMax-M2.5",
          "name": "MiniMax M2.5",
          "supports_image": false,
          "max_tokens": 32768,
          "max_input_length": 196608,
          "generate_kwargs": {}
        }
      ],
      "is_custom": true
    }
    ```
    
    <a id="按量计费-2"></a>
    
    <a id="按量计费-2-h4"></a>
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。
    
    <a id="code-block-5"></a>
    
    ```json
    {
      "id": "bailian-payg",
      "name": "Alibaba Cloud Model Studio",
      "base_url": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
      "api_key": "YOUR_API_KEY",
      "chat_model": "OpenAIChatModel",
      "models": [
        {
          "id": "qwen3.8-max",
          "name": "Qwen3.8 Max",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.7-plus",
          "name": "Qwen3.7 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.8-flash",
          "name": "Qwen3.8 Flash",
          "supports_image": true,
          "max_tokens": 131072,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4-pro-0813",
          "name": "DeepSeek V4 Pro 0813",
          "supports_image": false,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "deepseek-v4.1-flash",
          "name": "DeepSeek V4.1 Flash",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        }
      ],
      "is_custom": true
    }
    ```
    
    <a id="coding-plan-2"></a>
    
    <a id="coding-plan-2-h4"></a>
    
    #### Coding Plan
    
    <a id="code-block-6"></a>
    
    ```json
    {
      "id": "bailian-coding-plan",
      "name": "Alibaba Cloud Model Studio",
      "base_url": "https://coding.dashscope.aliyuncs.com/v1",
      "api_key": "YOUR_API_KEY",
      "chat_model": "OpenAIChatModel",
      "models": [
        {
          "id": "qwen3.7-plus",
          "name": "Qwen3.7 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.6-plus",
          "name": "Qwen3.6 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        },
        {
          "id": "kimi-k2.5",
          "name": "Kimi K2.5",
          "supports_image": true,
          "max_tokens": 98304,
          "max_input_length": 262144,
          "generate_kwargs": {}
        },
        {
          "id": "glm-5",
          "name": "GLM-5",
          "supports_image": false,
          "max_tokens": 16384,
          "max_input_length": 202752,
          "generate_kwargs": {}
        },
        {
          "id": "MiniMax-M2.5",
          "name": "MiniMax M2.5",
          "supports_image": false,
          "max_tokens": 32768,
          "max_input_length": 196608,
          "generate_kwargs": {}
        },
        {
          "id": "qwen3.5-plus",
          "name": "Qwen3.5 Plus",
          "supports_image": true,
          "max_tokens": 65536,
          "max_input_length": 1000000,
          "generate_kwargs": {}
        }
      ],
      "is_custom": true
    }
    ```
    
    > **说明**
    >
    > 使用 qwen4-max 时，1.1.x 默认 `max_tokens=8192`，需在 `generate_kwargs.max_tokens` 中调大；2.2.x 也建议显式设置。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    

<a id="错误码"></a>

<a id="qwp-error-h"></a>

## 错误码

<a id="qwp-faq-errorcode-h"></a>

按计费方案排查：

-   Token Plan：[Token Plan 常见问题](../../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="qwp-faq-h"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-报错-401-incorrect-api-key-provided"></a>

报错 401 Incorrect API key provided

<a id="qwp-faq-401-h"></a>

可能原因：

-   各计费方案的 API Key 不通用，确认 API Key 与基础 URL 来自同一方案。
-   按量计费的 API Key 与基础 URL 不在同一地域。

<a id="accordion-长对话或工具调用时报错上下文超限"></a>

长对话或工具调用时报错上下文超限

<a id="qwp-faq-context-h"></a>

在该模型的提供商**设置**页面展开**进阶配置**，按 JSON 格式调整 `max_tokens` 等生成参数后保存：

<a id="code-block-7"></a>

```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 4096
}
```
