# 选择地域、服务部署范围和接入域名

调用百炼前先选择 地域 、 服务部署范围、接入域名：

## 地域概述

地域决定**接入点和数据存储位置**，就近选择可降低延迟。

-   服务部署范围：决定**推理执行位置**，有数据合规需求选择特定地理边界的部署范围，无合规需求选择全球部署范围（推理资源池更大）；
-   接入域名：影响**并发上限、超时等服务保障**，各地域具有独立的接入域名。

一次完整的模型调用流程如下：

1.  应用经接入域名将请求发送到所选**地域**，请求数据存于该地域；
2.  接入地域将请求转发至**服务部署范围**内的推理节点完成计算（传输全程加密）；
3.  推理结果回到接入地域存储，再响应给应用（用户静态数据始终存于所选地域）。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9377607871/CAEQchiBgICkyp3I_hkiIGFjZmY5ZThjZWM2MzRkMmJhNTk5NWVmYTkwMWY3ZGI07466796_20260515102254.505.svg)

## 选择地域和服务部署范围

不同地域支持不同的服务部署范围，百炼将在所选范围内进行推理调度。例如美国（弗吉尼亚）支持全球和美国，德国（法兰克福）支持全球和欧盟等。完整的地域与服务部署范围对应关系，请前往[控制台](https://bailian.console.aliyun.com/)查看。

## 选择接入域名

百炼为模型推理 API 提供业务空间专属、DashScope 和试用三种接入域名，适用于从试用体验到企业级生产的不同场景。推荐使用**业务空间专属域名**，各域名的核心差异如下：

**对比项**

**业务空间专属域名（推荐）**

**DashScope 域名（现有域名）**

**试用域名**

**域名格式**

`{WorkspaceId}.{region}.maas.aliyuncs.com`

`dashscope.aliyuncs.com`

> 以华北2（北京）地域为例

`trial.{region}.maas.aliyuncs.com`

**适用场景**

推荐在生产环境中使用，具备更高并发承载能力与网络隔离性，保障大流量场景下的稳定、低延迟访问体验。

存量业务兼容，建议[迁移至业务空间专属域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

快速体验、功能验证，不建议用于生产环境。

**鉴权方式**

仅访问当前业务空间

可访问所有业务空间

可访问所有业务空间

**限流额度**

RPM、TPM 按模型区分，主账号维度合并计算

RPM、TPM 按模型区分，主账号维度合并计算

RPM 为1000（主账号维度），TPM 按模型区分

**请求超时**

3600 秒

600 秒

600 秒

**协议支持**

HTTP、SSE、WebSocket、WebRTC、AOQ（AI over QUIC）

HTTP、SSE、WebSocket

HTTP、SSE

**SLA**

99.9%

99.9%

不提供

## 各地域接入信息

每个地域有独立的接入域名、API Key 和模型列表，**不能跨地域混用**。

**地域**

**地域ID**

**业务空间专属域名**

**DashScope 域名**

**试用域名**

**API Key**

**模型列表**

华北2（北京）

`cn-beijing`

`{WorkspaceId} .cn-beijing.maas.aliyuncs.com`

`dashscope.aliyuncs.com`

`trial.cn-beijing.maas.aliyuncs.com`

[密钥管理](https://bailian.console.aliyun.com/?apiKey=1#/api-key)

[可用模型](https://bailian.console.aliyun.com/cn-beijing?apiKey=1&tab=model#/model-market)

新加坡

`ap-southeast-1`

`{WorkspaceId} .ap-southeast-1.maas.aliyuncs.com`

`dashscope-intl.aliyuncs.com`

`trial.ap-southeast-1.maas.aliyuncs.com`

[密钥管理](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/api-key)

[可用模型](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914)

德国（法兰克福）

`eu-central-1`

`{WorkspaceId} .eu-central-1.maas.aliyuncs.com`

不支持

暂不支持

[密钥管理](https://bailian.console.alibabacloud.com/?apiKey=1#/api-key)

[可用模型](https://modelstudio.console.aliyun.com/eu-central-1?tab=doc#/doc/?type=model&url=2840914)

日本（东京）

`ap-northeast-1`

`{WorkspaceId} .ap-northeast-1.maas.aliyuncs.com`

不支持

暂不支持

[密钥管理](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=dashboard#/api-key)

[可用模型](https://modelstudio.console.alibabacloud.com/ap-northeast-1?tab=doc#/doc/?type=model&url=2840914)

美国（弗吉尼亚）

`us-east-1`

`{WorkspaceId} .us-east-1.maas.aliyuncs.com`

不支持

暂不支持

[密钥管理](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)

[可用模型](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914)

-   **德国（法兰克福）、日本（东京）**地域通过**业务空间（Workspace）**区分服务部署范围，开始调用前需前往业务空间管理页面创建业务空间并选择服务部署范围：[德国（法兰克福）](https://modelstudio.console.aliyun.com/eu-central-1?tab=globalset#/efm/business_management)（全球/欧盟）、[日本（东京）](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=globalset#/efm/business_management)（全球/日本）。
-   **美国（弗吉尼亚）**地域使用带 `-us` 后缀的模型名称（如 `qwen-plus-us`）可限定美国境内推理，不带后缀的默认**全球**推理。
-   **华北2（北京）**和**新加坡地域**各仅支持一种服务部署范围，无需选择。
-   **新加坡**地域支持中国站企业实名认证账号直接开通，无主体类型、行业或资格限制；按量付费，账单在百炼侧结算，支持人民币支付。

## 迁移至业务空间专属域名

从 DashScope 域名或试用域名迁移到业务空间专属域名只需两步，无需修改业务逻辑代码：

1.  **获取业务空间专属域名**：
    
    -   方式一：在[API Key 创建](https://bailian.console.aliyun.com/cn-beijing#/api-key)后的弹窗中，复制 **API Host** 。
    -   方式二：在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面，复制 **API Host** 列的内容。
2.  **替换 Base URL 中的域名**：将原域名替换为业务空间专属域名。以华北2（北京）地域为例，`llm-xxx` 为业务空间 ID：
    
    -   OpenAI 兼容接口：从 `https://dashscope.aliyuncs.com/compatible-mode/v1` 替换为 `https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    -   DashScope 接口：从 `https://dashscope.aliyuncs.com/api/v1` 替换为 `https://llm-xxx.cn-beijing.maas.aliyuncs.com/api/v1`
    -   Anthropic 兼容接口：从 `https://dashscope.aliyuncs.com/apps/anthropic` 替换为 `https://llm-xxx.cn-beijing.maas.aliyuncs.com/apps/anthropic`

## 各地域功能支持

**功能**

**华北2（北京）**

**新加坡**

**美国（弗吉尼亚）**

**德国（法兰克福）**

**日本（东京）**

实时推理

支持

支持

支持

支持

支持

批量推理

支持

支持

不支持

不支持

不支持

模型体验

支持

支持

支持

支持

支持

模型监控

支持

支持

支持

支持

支持

模型告警

支持

支持

不支持

不支持

不支持

传输安全

支持

支持

支持

支持

支持

权限管理

支持

支持

支持

支持

支持

模型调优

支持

不支持

不支持

不支持

不支持

应用开发

支持

不支持

不支持

不支持

不支持

## 相关文档

-   [通义千问 API 参考](raw/model-api-reference/qwen-api-reference.md)
-   [选择模型](raw/model-user-guide/get-started-with-models/models.md) — 各地域模型及上下文长度
-   [模型调用计费](raw/model-user-guide/test-1/model-pricing.md) — 各地域价格
-   [限流](raw/model-user-guide/get-started-with-models/rate-limit.md)— RPM、TPM 限制
-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md) — 创建和管理 Key
-   [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md) — 模型服务调用地址
-   [概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
