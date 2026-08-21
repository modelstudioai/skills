# Base URL总览

Base URL 是模型 API 的调用地址。Base URL必须与同一计费方案的 API Key 配套使用，否则会报错 401。各地域的 API Key 相互独立、不能跨地域使用。

## 按量付费

根据使用场景选择合适的域名：

-   Dashscope 域名（`dashscope.aliyuncs.com` 等）：原有中心化共享域名，当前可继续使用，建议迁移至业务空间专属域名。
    
-   业务空间专属域名（`[workspace-id].[region].maas.aliyuncs.com`）：推荐用于生产环境，提供更高吞吐、更低时延与业务空间级流量隔离。
    
-   试用域名（`trial.[region].maas.aliyuncs.com`）：适用于临时测试与快速验证，限流值较小。
    

### Dashscope 域名

支持跨业务空间的 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/api_key) 调用。

**地域**

**OpenAI 兼容**

**Anthropic 兼容**

华北2（北京）

`https://dashscope.aliyuncs.com/compatible-mode/v1`

`https://dashscope.aliyuncs.com/apps/anthropic`

新加坡

`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

`https://dashscope-intl.aliyuncs.com/apps/anthropic`

美国（弗吉尼亚）

`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

`https://dashscope-us.aliyuncs.com/apps/anthropic`

如需使用 DashScope 原生 API，请将上表 URL 中域名后的路径替换为`/api/v1`，例如北京地域为`https://dashscope.aliyuncs.com/api/v1`。

### 业务空间专属域名

仅限业务空间所属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/api_key) 调用。

**地域**

**OpenAI 兼容**

**Anthropic 兼容**

华北2（北京）

`https://[{WorkspaceId}](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management).cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

`https://[{WorkspaceId}](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management).cn-beijing.maas.aliyuncs.com/apps/anthropic`

新加坡

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/ap-southeast-1).ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/ap-southeast-1).ap-southeast-1.maas.aliyuncs.com/apps/anthropic`

日本（东京）

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=globalset#/efm/business_management).ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=globalset#/efm/business_management).ap-northeast-1.maas.aliyuncs.com/apps/anthropic`

德国（法兰克福）

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/eu-central-1?tab=globalset#/efm/business_management).eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/eu-central-1?tab=globalset#/efm/business_management).eu-central-1.maas.aliyuncs.com/apps/anthropic`

美国（弗吉尼亚）

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management).us-east-1.maas.aliyuncs.com/compatible-mode/v1`

`https://[{WorkspaceId}](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management).us-east-1.maas.aliyuncs.com/apps/anthropic`

如需使用 DashScope 原生 API，请将上表 URL 中域名后的路径替换为`/api/v1`，例如北京地域为`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`。

### 试用域名

支持跨业务空间的 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/api_key) 调用。

**地域**

**OpenAI 兼容**

**Anthropic 兼容**

华北2（北京）

`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

`https://trial.cn-beijing.maas.aliyuncs.com/apps/anthropic`

新加坡

`https://trial.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

`https://trial.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`

## Token Plan

仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务。使用 Token Plan 的[专属 API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。

**地域**

**OpenAI 兼容**

**Anthropic 兼容**

华北2（北京）

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

## Coding Plan

仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务。使用 Coding Plan 的[专属 API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan) 。

**地域**

**OpenAI 兼容**

**Anthropic 兼容**

华北2（北京）

`https://coding.dashscope.aliyuncs.com/v1`

`https://coding.dashscope.aliyuncs.com/apps/anthropic`

## 相关文档

-   [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
-   [选择地域、服务部署范围和接入域名](https://help.aliyun.com/zh/model-studio/regions/)
