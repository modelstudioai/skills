# 选择地域和服务部署范围

调用百炼前先选择**地域**和**服务部署范围：**

-   地域：决定**接入点和数据存储位置**，就近选择可降低延迟；
    
-   服务部署范围：决定**推理执行位置**，有数据合规需求选择特定地理边界的部署范围，无合规需求选择全球部署范围（推理资源池更大）。
    

一次完整的模型调用流程如下：

1.  应用经 Base URL 将请求发送到所选**地域**（如华北2-北京），请求数据存于该地域；
    
2.  接入地域将请求转发至**服务部署范围**内的推理节点完成计算（过程数据不持久化，传输全程加密）；
    
3.  推理结果回到接入地域存储，再响应给应用（用户静态数据始终存于所选地域）。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0856771871/CAEQbxiBgICHvaa58hkiIDlkZWFlMzZlYTEyOTQ3MmM5YzQ5ZTkyYTRkNGVkNzU47466796_20260515102254.505.svg)

## 选择地域和服务部署范围

按场景查表选地域和服务部署范围：

**使用场景**

**地域**

**服务部署范围**

无数据驻留限制，追求更大推理资源池（跨多地域调度推理，自行确保跨境合法）

美国（弗吉尼亚）

全球（任意可用节点，含中国境内及海外）

无数据驻留限制，追求更大推理资源池（跨多地域调度推理，自行确保跨境合法）

德国（法兰克福）

全球（任意可用节点，含中国境内及海外）

无数据驻留限制，追求更大推理资源池（跨多地域调度推理，自行确保跨境合法）

日本（东京）

全球（任意可用节点，含中国境内及海外）

要求数据不出中国内地

华北2（北京）

中国内地（限境内推理）

要求数据不经过中国内地（会跨多地域调度推理，自行确保跨境合法）

新加坡

国际（除中国内地以外的全球节点）

要求数据不出美国

美国（弗吉尼亚）

美国（限境内推理）

要求数据不出欧盟

德国（法兰克福）

欧盟（限境内推理）

要求数据不出日本

日本（东京）

日本（限境内推理）

## 各地域接入信息

每个地域有独立的 Base URL、API Key 和模型列表，**不能跨地域混用**。

**重要**

百炼为华北2（北京）、新加坡地域推出了新版域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`，`{WorkspaceId}` 为业务空间 ID（可前往各地域的[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取），`{region}` 取值为 `cn-beijing`、`ap-southeast-1`。**新版专属域名能够为推理请求提供更加卓越的性能和更高的稳定性，建议迁移至新域名**。现有域名仍可正常使用：

-   华北2（北京）：建议从 `dashscope.aliyuncs.com` 替换为 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
    
-   新加坡：建议从 `dashscope-intl.aliyuncs.com` 替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
    

### 华北2（北京）

-   Base URL（OpenAI 兼容）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，调用时请从`WorkspaceId`替换为真实的[业务空间 ID](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)。
    
-   Base URL（Anthropic 兼容）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
-   Base URL（DashScope）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`
    
-   API Key：[密钥管理（北京）](https://bailian.console.aliyun.com/?apiKey=1#/api-key)
    
-   模型列表：[可用模型（北京）](https://bailian.console.aliyun.com/cn-beijing?apiKey=1&tab=model#/model-market)
    

### 新加坡

-   Base URL（OpenAI 兼容）：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`，调用时请从`WorkspaceId`替换为真实的[业务空间 ID](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=globalset#/efm/business_management)。
    
-   Base URL（Anthropic 兼容）：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`
    
-   Base URL（DashScope）：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`
    
-   API Key：[密钥管理（新加坡）](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914)
    
-   模型列表：[可用模型（新加坡）](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914)
    

### 美国（弗吉尼亚）

-   Base URL（OpenAI 兼容）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    
-   Base URL（Anthropic 兼容）：`https://dashscope-us.aliyuncs.com/apps/anthropic`
    
-   Base URL（DashScope）：`https://dashscope-us.aliyuncs.com/api/v1`
    
-   API Key：[密钥管理（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)
    
-   模型列表：[可用模型（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914)
    

**限定美国境内推理**：使用带 `-us` 后缀的模型名称，如 `qwen-plus-us`；不带后缀时默认使用**全球**推理。

### 德国（法兰克福）

法兰克福通过**业务空间（Workspace）**区分部署范围，不同空间的 API Key 相互隔离。开始调用前先创建业务空间：

1.  前往[业务空间管理（法兰克福）](https://modelstudio.console.aliyun.com/eu-central-1?tab=globalset#/efm/business_management)，创建业务空间并选择部署模式（全球或欧盟）。
    
2.  [获取业务空间 ID（法兰克福）](https://modelstudio.console.aliyun.com/eu-central-1?tab=globalset#/efm/business_management)，替换下方 Base URL 中的 `{WorkspaceId}`。
    

-   Base URL（OpenAI 兼容）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
    
-   Base URL（Anthropic 兼容）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/apps/anthropic`
    
-   Base URL（DashScope）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1`
    
-   API Key：[密钥管理（法兰克福）](https://bailian.console.alibabacloud.com/?apiKey=1#/api-key)
    
-   模型列表：[可用模型（法兰克福）](https://help.aliyun.com/zh/model-studio/getting-started/models)
    

### 日本（东京）

东京通过**业务空间（Workspace）**区分部署范围，不同空间的 API Key 相互隔离。开始调用前先创建业务空间：

1.  前往[业务空间管理（东京）](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=globalset#/efm/business_management)，创建业务空间并选择部署模式（全球或日本）。
    
2.  [获取业务空间 ID（东京）](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=globalset#/efm/business_management)，替换下方 Base URL 中的 `{WorkspaceId}`。
    

-   Base URL（OpenAI 兼容）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`
    
-   Base URL（Anthropic 兼容）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/apps/anthropic`
    
-   Base URL（DashScope）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1`
    
-   API Key：[密钥管理（东京）](https://modelstudio.console.aliyun.com/ap-northeast-1?tab=dashboard#/api-key)
    
-   模型列表：[可用模型（东京）](https://modelstudio.console.alibabacloud.com/ap-northeast-1?tab=doc#/doc/?type=model&url=2840914)
    

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

## 相关文档

-   [通义千问 API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)
    
-   [选择模型](https://help.aliyun.com/zh/model-studio/models) — 各地域模型及上下文长度
    
-   [模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing) — 各地域价格
    
-   [限流](https://help.aliyun.com/zh/model-studio/rate-limit)— RPM、TPM 限制
    
-   [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key) — 创建和管理 Key
