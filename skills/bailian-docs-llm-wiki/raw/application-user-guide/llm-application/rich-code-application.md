# 高代码应用

阿里云百炼平台的高代码应用功能，允许开发者基于完整的 Python 项目结构部署 AI 后端服务。

-   与"低代码/无代码"拖拽式开发不同，高代码应用允许您**使用代码编程的方式构建复杂 AI 服务**。
    
-   使用单条命令即可快速将 Python 项目部署为**公网可访问云上后端 API 服务**。
    
-   支持 **Serverless Function** 和 **K8s** 两种部署方式，满足不同场景需求：无状态快速拉起或高性能有状态长程任务。
    
-   支持**一站式 MCP 工具接入**，可在控制台直接关联知识库、工作流、插件等 MCP 服务。
    
-   支持**自定义前端体验**，提供直接体验、自定义交互卡片和自定义前端 WebUI 三种方式，基于 [Spark Design](https://github.com/agentscope-ai/agentscope-spark-design) 框架构建丰富的交互界面。
    
-   支持**自动化运维、可观测、日志服务、API网关等**企业级能力。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070633.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070634.png)
    

## **快速开始**

1.  前往[阿里云百炼-应用中心](https://bailian.console.aliyun.com/?tab=app#/app-center)，单击**创建应用**。在弹出的创建应用对话框左侧，选择**高代码应用**。
    
    选择创建类型：
    
    -   **控制台创建**：在控制台直接选择模板、配置资源并一键部署，推荐初次使用。
        
    -   **命令行创建**：在控制台创建空白应用后，通过 AgentScope-AI 命令行工具上传本地代码包部署。适合已有项目代码的开发者，详细流程请参考[API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)。
        
    
    填写**应用名称**后，单击**确认**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070627.png)
    
2.  确认创建后进入应用部署配置页面，按以下区域完成配置：
    
    > 创建时需按照页面引导授权函数计算 FC、API 网关两个服务的相关角色和权限。如遇权限不足，请联系您的账号管理员或 IT 管理员[获取相关授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070628.png)
    
    **选择部署方式**
    
    -   **Serverless Function**（默认）：适用于低负载、无状态、快速拉起的场景，部署花销低。
        
    -   **K8s**：适用于高性能、有状态、执行长程任务的 Agent，性能强。使用前需开通 ACK 容器服务并完成授权。
        
    
    **提交代码**
    
    -   **使用模板代码**（默认）：选择一个预置的应用模板快速开始。
        
    -   **上传代码包**：上传本地开发的 .whl 格式代码包。代码包制作方式请参考[API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)。
        
    
    平台提供以下应用模板：
    
    **模板**
    
    **说明**
    
    基础对话 Agent
    
    以 LLM 对话为主的基础示例 Agent，适合快速体验和二次开发。
    
    工具调用 Agent
    
    内置多种 MCP 工具（联网搜索、计算器等），展示工具调用能力。
    
    深度研究 Agent
    
    基于 AgentScope 组件搭建的深度研究 Agent，可进行互联网调研并生成研究报告。
    
    **选择部署资源**
    
    根据需要配置**规格方案**（vCPU、内存、磁盘大小）、**最小实例数**、**单实例并发度**和**部署地域**。初次体验保持默认即可。
    
    > 时延敏感业务建议最小实例数 ≥ 1，可实现毫秒级热启动、保障服务不中断。详见[实例类型和规格](https://help.aliyun.com/zh/functioncompute/fc/product-overview/instance-types-and-specifications#section-mfv-5fb-ehw)。
    
    配置完成后，单击**立即部署**开始部署。
    
    > 部署后将开始计费。应用测试会产生实际调用，函数、网关、存储、模型调用均会产生费用，具体费用以阿里云账单为准。
    
    **开启应用观测**
    
    开启后将可自定义地分析应用代码的调用路径，并监测调用参数。
    
3.  等待几分钟完成应用的构建和部署。页面会显示构建和部署的实时进度和耗时，可单击进度条旁的**日志**链接查看详细的构建日志和部署日志。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070629.png)
    
4.  待部署完成后，配置阿里云百炼的 API Key 后，即可使用页面右侧的测试面板进行体验和调试。API Key 获取方式请参考：[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
    -   **文本对话体验**：直接与应用进行对话交互，快速验证应用功能。
        
    -   **API测试**：手动调用应用的 API 接口（如 `GET /health`、`/process`），适合开发调试。接口协议详情请参考[API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070630.png)
    

## **应用管理**

部署完成后，应用详情页左侧提供**部署**、**工具**、**网关**、**前端**四个功能 Tab，覆盖已部署应用的完整管理和体验流程。页面右侧面板提供**API测试**和**文本对话体验**两种测试模式，可随时验证应用功能。

### **部署**

部署 Tab 用于管理应用的部署状态、资源配置和运行日志。

-   **重新部署**：单击页面顶部的**重新部署**按钮，可以更新应用部署相关的所有设置，包含**上传新的代码包**（仅支持 .whl 格式）、**调整应用性能**（修改资源规格、实例数和并发度）、**修改部署地域**。
    
    > 更新配置或重启服务后，应用都将重新构建和部署。
    
-   **配置**：包含基础配置、环境变量、**触发器**三个可折叠配置区域。可查看和修改应用的基本信息、自定义环境变量（如 API Key）和 HTTP 触发器设置。
    
-   **日志**：可查看应用的运行日志，支持按时间范围筛选、按日志内容和实例 ID 过滤。构建过程日志可在部署状态栏中的**构建日志**和**部署日志**链接查看。
    
-   **停止服务**：当应用不再需要运行时，单击页面顶部的**停止服务**按钮停止应用以节省费用。
    

### **工具**

高代码应用支持一站式 **MCP** 工具接入，可在工具 Tab 中为应用关联知识库、工作流、插件等 MCP 服务。详细配置方式请参考[工具接入](https://help.aliyun.com/zh/model-studio/rich-code-application-mcp)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070631.png)

### **网关**

当**应用测试稳定、性能满足预期**后，建议开启**网关**功能，通过自定义域名和网关路由在生产环境访问云上服务。

1.  在高代码应用详情页的**网关** Tab 中，按照控制台引导，根据需求创建阿里云的[云原生API网关](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/what-is-cloud-native-api-gateway)。（将会产生少量的使用费用，具体价格表请参考[计费概述](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/billing-overview)）
    
    > 应用**部署**地域应与应用**网关**所在地域**相同**。
    
2.  创建路由并配置 Token 鉴权，使新的 API 路由生效后即可通过网关访问高代码应用。
    
3.  在**生产环境**中使用应用：推荐**打开**测试域名的"**禁止公网访问**"开关，测试用**触发器**将不再能够通过公网访问。
    
4.  调用示例：
    
    ```
    curl -i -X POST "http://{your-domain}/{your-agentCode}/process" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer 替换为应用网关鉴权token" \
      -d '{
        "input": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "你好" }
            ]
          }
        ],
        "session_id": "xxxxxx",
        "user_id": "xxxxx"
      }'
    ```
    

### **前端**

前端 Tab 提供三种前端体验方式，方便开发者为高代码应用构建丰富的交互界面：

-   **直接体验**：在右侧面板切换到**文本对话体验**模式，配置对话接口后即可直接与应用交互测试。
    
-   **自定义交互卡片**：在应用代码中自定义交互卡片样式，实现富文本、按钮、表单等交互元素。
    
-   **自定义前端 WebUI**：基于 [AgentScope Spark Design](https://github.com/agentscope-ai/agentscope-spark-design) 框架，构建完整的前端交互界面。Spark Design 提供 `@agentscope-ai/design`（UI 组件库）和 `@agentscope-ai/chat`（对话组件库）两个核心包，支持 Markdown 渲染、流式响应、语音输入等能力。详情请参考[Spark Design 在线文档](https://sparkdesign.agentscope.io/)。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2506686771/p1070632.png)

## **后续阅读**

-   [工具接入](https://help.aliyun.com/zh/model-studio/rich-code-application-mcp)：了解如何通过 MCP 协议接入知识库和外部工具服务。
    
-   [API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)：了解如何使用 AgentScope-AI 开发、上传和部署高代码应用。
