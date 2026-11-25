# Codex

在 Codex 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="cdx-quickstart-h"></a>

## 快速开始

1.  1
    
    打开或新建配置文件
    
    <a id="cdx-config-h"></a>
    
    -   macOS / Linux：`~/.codex/config.toml`
    -   Windows：`C:\Users\<用户名>\.codex\config.toml`
    
2.  2
    
    配置模型
    
    > **说明**
    >
    > 如需在模型间切换，参见[配置模型元数据](#cdx-catalog-h)。
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="cdx-tpp-config-h"></a>
    
    <a id="cdx-tp-config-h"></a>
    
    将 `OPENAI_API_KEY` 替换为 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="code-block"></a>
    
    ```text
    model_provider = "Token_Plan"
    model = "auto"
    
    [model_providers.Token_Plan]
    name = "Token_Plan"
    base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "responses"
    ```
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="cdx-payg-config-h"></a>
    
    将 `OPENAI_API_KEY` 替换为[阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，并将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。以华北2（北京）地域为例。
    
    <a id="code-block-2"></a>
    
    ```text
    model_provider = "Model_Studio"
    model = "qwen3.7-max"
    
    [model_providers.Model_Studio]
    name = "Model_Studio"
    base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "responses"
    ```
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="cdx-cp-config-h"></a>
    
    将 `OPENAI_API_KEY` 替换为 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。Coding Plan 使用 Chat Completions API，需安装 Codex 0.93.0 或更早版本：
    
    <a id="code-block-3"></a>
    
    ```bash
    npm install -g @openai/codex@0.93.0
    ```
    
    <a id="code-block-4"></a>
    
    ```text
    model_provider = "Coding_Plan"
    model = "qwen3.7-plus"
    
    [model_providers.Coding_Plan]
    name = "Coding_Plan"
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "chat"
    ```
    
3.  3
    
    验证
    
    <a id="cdx-verify-h"></a>
    
    在项目目录中运行以下命令：
    
    <a id="code-block-5"></a>
    
    ```bash
    codex exec "你好"
    ```
    

<a id="配置模型元数据"></a>

<a id="cdx-catalog-h"></a>

<a id="cdx-switch-h"></a>

## 配置模型元数据

模型元数据用于在 Codex 中切换模型。不配置时，`config.toml` 中指定的模型仍可正常调用，但启动时会提示 `Model metadata ... not found`，Codex 按默认元数据处理模型。配置后，可通过 `codex -m` 或 TUI 的 `/model` 在模型间切换。

<a id="sec-tabs-2"></a>

<a id="token-plan-个人版"></a>

<a id="token-plan-个人版-h4"></a>

#### Token Plan 个人版

新建 `~/.codex/model-catalog.local.json`，写入以下内容：

<a id="code-block-6"></a>

```json
{
  "models": [
    {
      "slug": "auto",
      "display_name": "auto",
      "description": "DashScope model: auto",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 1,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen4-max",
      "display_name": "qwen4-max",
      "description": "DashScope model: qwen4-max",
      "default_reasoning_level": "high",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "high",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 2,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.8-max",
      "display_name": "qwen3.8-max",
      "description": "DashScope model: qwen3.8-max",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 3,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.8-flash",
      "display_name": "qwen3.8-flash",
      "description": "DashScope model: qwen3.8-flash",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 4,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.7-max",
      "display_name": "qwen3.7-max",
      "description": "DashScope model: qwen3.7-max",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 5,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.7-plus",
      "display_name": "qwen3.7-plus",
      "description": "DashScope model: qwen3.7-plus",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 6,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.6-flash",
      "display_name": "qwen3.6-flash",
      "description": "DashScope model: qwen3.6-flash",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 7,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.3",
      "display_name": "glm-5.3",
      "description": "DashScope model: glm-5.3",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 8,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.2",
      "display_name": "glm-5.2",
      "description": "DashScope model: glm-5.2",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 9,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4.1-flash",
      "display_name": "deepseek-v4.1-flash",
      "description": "DashScope model: deepseek-v4.1-flash",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 10,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4.1-flash-1017",
      "display_name": "deepseek-v4.1-flash-1017",
      "description": "DashScope model: deepseek-v4.1-flash-1017",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 11,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-pro",
      "display_name": "deepseek-v4-pro",
      "description": "DashScope model: deepseek-v4-pro",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 12,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-pro-0813",
      "display_name": "deepseek-v4-pro-0813",
      "description": "DashScope model: deepseek-v4-pro-0813",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 13,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-flash-0731",
      "display_name": "deepseek-v4-flash-0731",
      "description": "DashScope model: deepseek-v4-flash-0731",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 14,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    }
  ]
}
```

在 `~/.codex/config.toml` 中添加：

<a id="code-block-7"></a>

```text
model_catalog_json = "~/.codex/model-catalog.local.json"
```

配置完成后，可通过 `codex -m` 指定模型 ID（例如 `codex -m qwen3.8-flash`），或在 TUI 中输入 `/model` 在已配置的模型间切换。

<a id="token-plan-团队版"></a>

<a id="token-plan-团队版-h4"></a>

#### Token Plan 团队版

新建 `~/.codex/model-catalog.local.json`，写入以下内容：

<a id="code-block-8"></a>

```json
{
  "models": [
    {
      "slug": "auto",
      "display_name": "auto",
      "description": "DashScope model: auto",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 1,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen4-max",
      "display_name": "qwen4-max",
      "description": "DashScope model: qwen4-max",
      "default_reasoning_level": "high",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "high",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 2,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.8-max",
      "display_name": "qwen3.8-max",
      "description": "DashScope model: qwen3.8-max",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 3,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.8-flash",
      "display_name": "qwen3.8-flash",
      "description": "DashScope model: qwen3.8-flash",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 4,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.7-max",
      "display_name": "qwen3.7-max",
      "description": "DashScope model: qwen3.7-max",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 5,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.7-plus",
      "display_name": "qwen3.7-plus",
      "description": "DashScope model: qwen3.7-plus",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 6,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.6-flash",
      "display_name": "qwen3.6-flash",
      "description": "DashScope model: qwen3.6-flash",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 7,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.3",
      "display_name": "glm-5.3",
      "description": "DashScope model: glm-5.3",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 8,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.2",
      "display_name": "glm-5.2",
      "description": "DashScope model: glm-5.2",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 9,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4.1-flash",
      "display_name": "deepseek-v4.1-flash",
      "description": "DashScope model: deepseek-v4.1-flash",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 10,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4.1-flash-1017",
      "display_name": "deepseek-v4.1-flash-1017",
      "description": "DashScope model: deepseek-v4.1-flash-1017",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 11,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-pro",
      "display_name": "deepseek-v4-pro",
      "description": "DashScope model: deepseek-v4-pro",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 12,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-pro-0813",
      "display_name": "deepseek-v4-pro-0813",
      "description": "DashScope model: deepseek-v4-pro-0813",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 13,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-flash-0731",
      "display_name": "deepseek-v4-flash-0731",
      "description": "DashScope model: deepseek-v4-flash-0731",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 14,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.6-plus",
      "display_name": "qwen3.6-plus",
      "description": "DashScope model: qwen3.6-plus",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 15,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "kimi-k2.7-code",
      "display_name": "kimi-k2.7-code",
      "description": "DashScope model: kimi-k2.7-code",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 262144,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 16,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "kimi-k2.6",
      "display_name": "kimi-k2.6",
      "description": "DashScope model: kimi-k2.6",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 262144,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 17,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "kimi-k2.5",
      "display_name": "kimi-k2.5",
      "description": "DashScope model: kimi-k2.5",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 262144,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 18,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.1",
      "display_name": "glm-5.1",
      "description": "DashScope model: glm-5.1",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 202752,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 19,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5",
      "display_name": "glm-5",
      "description": "DashScope model: glm-5",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 202752,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 20,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "MiniMax-M2.5",
      "display_name": "MiniMax-M2.5",
      "description": "DashScope model: MiniMax-M2.5",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 204800,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 21,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    }
  ]
}
```

在 `~/.codex/config.toml` 中添加：

<a id="code-block-9"></a>

```text
model_catalog_json = "~/.codex/model-catalog.local.json"
```

配置完成后，可通过 `codex -m` 指定模型 ID（例如 `codex -m qwen3.6-plus`），或在 TUI 中输入 `/model` 在已配置的模型间切换。

<a id="按量计费-2"></a>

<a id="按量计费-2-h4"></a>

#### 按量计费

新建 `~/.codex/model-catalog.local.json`，写入以下内容：

<a id="code-block-10"></a>

```json
{
  "models": [
    {
      "slug": "qwen3.8-max",
      "display_name": "qwen3.8-max",
      "description": "DashScope model: qwen3.8-max",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": [
        "text",
        "image"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 1,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "qwen3.7-max",
      "display_name": "qwen3.7-max",
      "description": "DashScope model: qwen3.7-max",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 2,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "deepseek-v4-pro",
      "display_name": "deepseek-v4-pro",
      "description": "DashScope model: deepseek-v4-pro",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 3,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    },
    {
      "slug": "glm-5.2",
      "display_name": "glm-5.2",
      "description": "DashScope model: glm-5.2",
      "default_reasoning_level": "medium",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Balances speed and reasoning depth"
        },
        {
          "effort": "high",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 1000000,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": false,
      "input_modalities": [
        "text"
      ],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 4,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    }
  ]
}
```

在 `~/.codex/config.toml` 中添加：

<a id="code-block-11"></a>

```text
model_catalog_json = "~/.codex/model-catalog.local.json"
```

配置完成后，可通过 `codex -m` 指定模型 ID（例如 `codex -m qwen3.8-max`），或在 TUI 中输入 `/model` 在已配置的模型间切换。

> **说明**
>
> qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。可通过 `codex -m qwen4-max` 指定模型。

<a id="chat-completions-配置"></a>

<a id="cdx-api-h"></a>

## Chat Completions 配置

Codex 0.94.0 起只支持 Responses API。如果使用 Codex 0.93.0 或更早版本，或所用模型只支持 Chat Completions，请按以下方式配置。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux：`~/.codex/config.toml`
    -   Windows：`C:\Users\<用户名>\.codex\config.toml`
    
2.  2
    
    写入配置
    
    <a id="sec-tabs-3"></a>
    
    <a id="token-plan-2"></a>
    
    <a id="token-plan-2-h4"></a>
    
    #### Token Plan
    
    将 `OPENAI_API_KEY` 替换为 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="code-block-12"></a>
    
    ```text
    model_provider = "Token_Plan"
    model = "auto"
    
    [model_providers.Token_Plan]
    name = "Token_Plan"
    base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "chat"
    ```
    
    <a id="按量计费-3"></a>
    
    <a id="按量计费-3-h4"></a>
    
    #### 按量计费
    
    将 `OPENAI_API_KEY` 替换为[阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，并将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。以华北2（北京）地域为例：
    
    <a id="code-block-13"></a>
    
    ```text
    model_provider = "Model_Studio"
    model = "qwen3.8-max"
    
    [model_providers.Model_Studio]
    name = "Model_Studio"
    base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "chat"
    ```
    
    <a id="coding-plan-2"></a>
    
    <a id="coding-plan-2-h4"></a>
    
    #### Coding Plan
    
    将 `OPENAI_API_KEY` 替换为 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。
    
    <a id="code-block-14"></a>
    
    ```text
    model_provider = "Coding_Plan"
    model = "qwen3.7-plus"
    
    [model_providers.Coding_Plan]
    name = "Coding_Plan"
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    env_key = "OPENAI_API_KEY"
    wire_api = "chat"
    ```
    

<a id="使用-cc-switch"></a>

<a id="cdx-ccswitch-h"></a>

## 使用 CC Switch

[CC Switch](https://github.com/farion1231/cc-switch) 是社区开源的桌面 GUI，支持在多个 API Key 或计费套餐之间一键切换。

<a id="添加供应商"></a>

<a id="cdx-ccswitch-add-h"></a>

### 添加供应商

1.  1
    
    在 CC Switch 主界面顶部图标栏选中 Codex 图标，点击右上角 **+** 进入**添加新供应商**，按对应 Tab 填入配置后点击**添加**。
    
    <a id="sec-tabs-4"></a>
    
    <a id="token-plan-3"></a>
    
    <a id="token-plan-3-h4"></a>
    
    #### Token Plan
    
    -   供应商名称：百炼-Token Plan
    -   API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    <a id="按量计费-4"></a>
    
    <a id="按量计费-4-h4"></a>
    
    #### 按量计费
    
    -   供应商名称：百炼-按量计费
    -   API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    <a id="coding-plan-3"></a>
    
    <a id="coding-plan-3-h4"></a>
    
    #### Coding Plan
    
    -   供应商名称：百炼-Coding Plan
    -   API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    -   请求地址：`https://coding.dashscope.aliyuncs.com/v1`
    
2.  2
    
    展开**高级选项**填写模型名称，从对应套餐[支持的模型](../token-plan-guide/token-plan-overview.md)中选择，例如 `qwen3.8-max`。
    
3.  3
    
    回到主界面，点击该供应商右侧**启用**按钮，然后重新打开终端窗口执行 `codex` 使配置生效。
    

<a id="错误码"></a>

<a id="cdx-error-h"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="cdx-faq-h"></a>

## 常见问题

<a id="accordion-启动时提示-model-metadata-not-found-怎么办"></a>

启动时提示 Model metadata ... not found 怎么办？

这是未配置模型元数据时的提示。Codex 按默认元数据处理模型，不影响调用。如需在模型间切换，参见[配置模型元数据](#cdx-catalog-h)。

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-第三方工具提示-不支持国内模型-或-检查被拒-bad-request-400-怎么办"></a>

第三方工具提示“不支持国内模型”或“检查被拒 / Bad request (400)”怎么办？

**原因**：部分第三方管理工具（如 CC-Switch）在切换供应商时会发起“健康检查/连接测试”探测请求，该探测请求的格式与 Codex 实际调用的请求格式不同，百炼网关可能因此返回 400 Bad request 并提示“检查被拒”，工具据此显示“不支持国内模型”。此提示仅代表健康检查探测未通过，**并不代表百炼不支持中国内地模型，也不影响 Codex 的实际使用。**

**解决方案**：参照上文[快速开始](#cdx-quickstart-h)，直接在 `~/.codex/config.toml` 中完成配置，无需依赖第三方工具的健康检查结果。配置完成后按[验证](#cdx-verify-h)启动 Codex，能正常返回响应即表示可正常使用中国内地模型。

<a id="cdx-faq-healthcheck-h"></a>

<a id="accordion-报错-wire-api-配置问题怎么办"></a>

报错 wire\_api 配置问题怎么办？

**原因**：Codex 0.94.0 起不再支持 `wire_api = "chat"` 配置。根据版本不同，可能出现以下报错：

-   `wire_api = "chat" is no longer supported`
-   `unknown configuration field wire_api`

**解决方案**：

-   报错 `wire_api = "chat" is no longer supported`：将 `wire_api` 改为 `responses`，并确认 `base_url` 配置正确。
-   报错 `unknown configuration field wire_api`：从 `~/.codex/config.toml` 的对应 provider 节中删除 `wire_api` 字段。
-   需要继续使用 Chat Completions 时，安装 Codex 0.93.0 或更早版本（如 0.80.0）。
    
    <a id="cdx-faq-wire-api-h"></a>
    

<a id="accordion-报错-unexpected-status-401-unauthorized-怎么办"></a>

报错 unexpected status 401 Unauthorized 怎么办？

**原因**：

-   误用了其他方案的 API Key（Token Plan、Coding Plan 和按量计费的 API Key 互不相通）
-   订阅过期
-   API Key 复制不完整、有空格或拼写错误

**解决方案**：

-   确认使用的是所选方案对应的专属 API Key。
-   前往对应方案的管理页面确认订阅是否过期。
-   重新复制 API Key，确保完整且无空格。
-   如以上均正常仍报错，可在对应管理页面重置 API Key，重置后使用新 API Key 配置。
    
    <a id="cdx-faq-401-h"></a>
    

<a id="accordion-报错-unexpected-status-404-not-found-怎么办"></a>

报错 unexpected status 404 Not Found 怎么办？

**原因**：配置文件中的 `base_url` 或 `wire_api` 填写错误。

**解决方案**：确认 `base_url` 和 `wire_api` 与所选方案的配置一致，参见[快速开始](#cdx-quickstart-h)。

<a id="cdx-faq-404-h"></a>

<a id="accordion-报错-stream-disconnected-before-completion-stream-closed-before-response-completed-怎么办"></a>

报错 stream disconnected before completion: stream closed before response.completed 怎么办？

**原因**：Codex 与服务端的流式连接在响应完成前断开。常见于以下场景：

-   对话线程过长，Codex 触发上下文压缩时请求失败
-   网络不稳定，SSE 或 WebSocket 连接中途断开
-   服务端过载或触发限流，提前终止连接

**解决方案**：

-   开启新的对话线程，避免单个线程积累过多上下文。
-   检查网络连接是否稳定，关闭 VPN 或代理后重试。
-   等待一段时间后重试，Codex 内置了自动重试机制，多数情况下重试可恢复。
    
    <a id="cdx-faq-stream-h"></a>
    

<a id="accordion-报错-429-请求超频或额度用尽怎么办"></a>

报错 429 请求超频或额度用尽怎么办？

**原因**：429 错误有以下两种情形：

-   **请求超频**（`429 Requests rate limit exceeded`）：短时间内请求过于密集。
-   **限额用尽**（`429 Allocated quota exceeded` 或 `Your token-plan quota has been exhausted`）：Token Plan 套餐月额度用尽。

**解决方案**：

-   请求超频：等待一分钟后重试，降低请求频率。
-   限额用尽：等待下一个订阅月额度自动重置；或购买用量包（套餐月额度用尽后自动抵扣用量包额度）；或升级套餐。报错信息中的重置时间（如 `The quota will reset at HH:MM:SS UTC`）以协调世界时（UTC）为准，换算为北京时间（CST）需加 8 小时。
    
    <a id="cdx-faq-429-h"></a>
