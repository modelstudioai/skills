# Dify

Dify 是一个开源的大模型应用开发平台，您可以基于阿里云百炼提供的模型 API 来构建大模型应用。

## **前提条件**

您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并确保已开通阿里云百炼的模型服务。

## **1\. 配置模型**

### **1.1. 安装模型供应商**

前往[Dify 市场](https://cloud.dify.ai/plugins?category=discover)，在**模型**下找到**通义千问**并安装最新版插件。

**说明**

-   千问插件非阿里云提供，由 Dify 官方维护。若安装最新版插件报错，可尝试安装较早版本。
    
-   使用阿里云百炼提供的 DeepSeek 模型也请使用**通义千问**插件。
    

### **1.2. 配置 API Key**

单击页面右上角的头像-**设置**，在**模型供应商**处找到**通义千问**卡片，点击**设置**。

-   若使用**北京地域**模型，在卡片的 **API-KEY 设置**界面填入**中国内地版** API Key，并设置**使用国际端点**为**否**。
    
-   若使用**新加坡地域**模型，在卡片的 **API-KEY 设置**界面填入****国际版**** API Key，并设置**使用国际端点**为**是**。
    

> 若 API Key 配置过程报错：**Invalid API-key provided**，可尝试安装较早版本的千问插件。

### **1.3. 选择模型**

单击**通义千问**卡片中的显示模型，打开您需要使用的模型开关。

> 若插件内暂未包含最新版千问模型，可尝试安装 **OpenAI-API-compatible** 插件，在插件设置中的 **API endpoint URL** 填入`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京地域）或`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（新加坡地域）。

## **2\. 开始使用**

Dify 具有多种大模型应用类型，请选择您使用的类型进行参考。

## 聊天助手/Agent

1.  **创建一个聊天助手或Agent**
    
    在[工作室](https://cloud.dify.ai/apps)单击**创建空白应用**，在**新手适用**中创建一个聊天助手或Agent并进入。
    
2.  **选择模型**
    
    在应用页面右上角可以选择模型，以**通义千问**下的**qwen-plus-latest(Qwen3)**为例，打开思考模式并设置为True。
    
3.  **对话测试**
    
    输入“你是谁”，模型会在思考后进行回答。
    
    您也可以使用 [Qwen-VL](https://help.aliyun.com/zh/model-studio/vision) 或 [QVQ](https://help.aliyun.com/zh/model-studio/visual-reasoning) 模型针对图片进行提问。在选择视觉模型后界面左侧会出现**视觉**开关，打开即可在右侧的对话框输入图片。
    

## Chatflow/工作流

1.  **创建一个Chatflow或者工作流**
    
    在[工作室](https://cloud.dify.ai/apps)创建一个Chatflow或者工作流并进入。
    
2.  **添加LLM节点**
    
    在画布中添加一个LLM节点，选中节点进入编辑界面，选择您需要使用的模型。此处选择qwen-plus-2025-07-28(Qwen3)，打开思考模式并设置为True。
    
    如果您使用 [Qwen-VL](https://help.aliyun.com/zh/model-studio/vision) 或 [QVQ](https://help.aliyun.com/zh/model-studio/visual-reasoning) 模型，请打开LLM节点的视觉开关：
    
    在LLM节点编辑面板底部找到**视觉**开关并打开，下方可设置**分辨率**为**高**或**低**。
    
3.  **运行LLM节点**
    
    单击**添加消息**，在**USER**对应的消息下输入问题：“你是谁”，单击节点右上角的运行按钮![20251127203142](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4671034671/p1030341.jpg)。
    
    运行完成后，输出结果的`text`字段中，思考内容被`...`标签包裹，标签之后为模型的回复正文。
    
    LLM节点返回的`text`字段包含思考与回复内容，您可以使用Dify的代码执行节点，通过正则表达式分别提取。
    

## 知识库

1.  **创建知识库**
    
    创建一个[知识库](https://cloud.dify.ai/datasets)并进入。
    
2.  **选择数据源**
    
    在此步骤上传您的知识库文件。
    
3.  **文本分段与清洗**
    
    您可以在此步骤配置阿里云百炼提供的 Embedding 模型与 Rerank 模型，此处以 text-embedding-v4 与 gte-rerank-v2 为例。其余参数请您按需配置。
    
    > gte-rerank-v2仅支持**北京地域**。
    
    > Embedding 模型暂时无法选择multimodal-embedding-v1模型，敬请关注后续动态。
    

## **常见问题**

### **Q1：在千问插件内配置 API Key 报错？**

A：有以下常见原因：

-   最新版插件性能可能不稳定，请尝试安装较低版本插件。
    
-   使用了子业务空间的 API Key。`0.0.41`版本的千问插件会校验`qwen-turbo`模型调用权限，请为`qwen-turbo`[添加模型调用权限](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)。
    
    > 千问插件非阿里云官方维护，后续版本校验策略以实际情况为准。建议使用默认业务空间的 API Key。
    
-   端点设置错误，请根据 API Key 所在地域设置是否 **使用国际端点**。
    

### **Q2：如何使用** [Qwen-Omni](https://help.aliyun.com/zh/model-studio/qwen-omni)/[Qwen-Audio](https://help.aliyun.com/zh/model-studio/audio-language-model)/[Qwen-OCR](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)模型？

A：以上模型均不支持直接在 Dify 上配置，您可通过 Chatflow 或工作流的 HTTP 节点接入，接入细节请参见文档中的 Curl 命令。

> 为了降低HTTP节点的超时风险，建议您通过流式输出方式调用。

### **Q3：如何使用万相模型？**

A：Dify 没有提供万相模型相关的插件，通过Dify的Chatflow/工作流的节点可达到文生图/视频的功能。请参考以下步骤：

1.  **下载并导入工作流模板**
    
    下载我们写好的模板：[万相-文生图Demo.yml](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250520/uuxncy/%E9%80%9A%E4%B9%89%E4%B8%87%E7%9B%B8-%E6%96%87%E7%94%9F%E5%9B%BEDemo.yml)或 [万相-文生视频Demo.yml](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250522/ksblgi/%E9%80%9A%E4%B9%89%E4%B8%87%E7%9B%B8-%E6%96%87%E7%94%9F%E8%A7%86%E9%A2%91Demo.yml)，在[工作室](https://cloud.dify.ai/apps)单击**导入DSL文件**并选择下载的模板文件。
    
2.  **配置环境变量**
    
    进入工作流界面，找到![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5589338471/p958072.png)，并将`DASHSCOPE_API_KEY`的值修改为您的API Key。
    
3.  **测试生图效果**
    
    单击界面的**运行**按钮即可生成作品。以文生图工作流输入“小猫”为例，可以得到图片。
    
    > 视频生成工作流会返回视频的URL。
    
    > 文生视频的时间一般在5分钟以上，请耐心等待。
    
4.  **发布为工具（可选**
    
    为了在其它大模型应用中使用万相的文生图/视频功能，您可以在界面右上方单击**发布**并选择**发布为工具**。
    

> 模板使用的模型为北京地域的`wanx2.1-t2i-turbo`（文生图）/`wanx2.1-t2v-turbo`（文生视频）。您可以在STEP1节点修改模型，在STEP1和STEP3节点修改地域API。

### **Q4：如何私有化部署 Dify？**

A：[Dify 云服务](https://cloud.dify.ai/apps)存在多项限制，例如最多创建 5 个应用。私有化部署请参见[阿里云 Dify 部署解决方案](https://www.aliyun.com/solution/tech-solution/rapidly-deploy-dify-to-accelerate-ai-application-development/)。
