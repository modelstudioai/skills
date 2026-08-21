# 文件问答

在**智能体应用**中上传文件后，可以与文件内容进行智能问答。此功能通过三种不同的处理模式，支持对文档、图片、音视频等多种文件进行内容理解、信息提取和智能问答。根据您的具体需求，可以选择以下三种处理模式：

-   **全文引用**：通过内置解析器解析文件内容，将文件内容（在上下文长度限制内）作为整体提供给模型。
    
    -   **适合**：需要全局理解的任务，如文档总结、全文翻译、风格润色。
        
    -   **特点**：简单直接，但受限于模型的上下文长度。
        
-   **切片检索**（[RAG](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)）：通过内置解析器解析文件内容，将文件切分成小片段，提问时，系统会从文件切片中检索最相关的内容片段，并将其与用户问题一并提供给模型以生成回答。
    
    -   **适合**：长文档问答、知识库检索、需要精确定位信息来源的场景。
        
    -   **特点**：能处理超长文件，回答效果依赖切片和检索策略。
        
-   **自定义处理**：将文件信息（如 URL或内容本身）提供给模型，允许模型根据任务需求自主调用外部工具来处理文件。
    
    -   **适合**：需要对文件进行其他操作的任务，如图片风格转换、视频内容分析后生成报告等。
        
    -   **特点**：功能强大灵活，依赖于所配置的工具（[插件](https://help.aliyun.com/zh/model-studio/plug-in-overview)、[MCP](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#8319d03864jym)等）。
        

## **适用范围**

### **支持的地域**

本文档仅适用于中国大陆版（北京地域）。

### **支持的模型**

**说明**

数据更新可能存在延迟，模型的支持情况以智能体应用内显示为准。

**文本生成模型**

-   [千问Max](https://help.aliyun.com/zh/model-studio/models#qwen-max-cn-bj)、[千问Plus](https://help.aliyun.com/zh/model-studio/models#03a05ab98953u)、[千问Turbo](https://help.aliyun.com/zh/model-studio/models#218847c4b35vb)、[千问Long](https://help.aliyun.com/zh/model-studio/models#2a9527533ei3o)
    
-   [千问3-Coder-Plus](https://help.aliyun.com/zh/model-studio/models#d698550551bob)
    
-   [千问3开源模型](https://help.aliyun.com/zh/model-studio/models#2c9c4628c9yyd)、[千问2.5开源模型](https://help.aliyun.com/zh/model-studio/models#15f2bdc5dd3zd)、[千问2开源模型](https://help.aliyun.com/zh/model-studio/models#4969f9cd9170b)
    
-   [千问-QwQ](https://help.aliyun.com/zh/model-studio/models#5b345b2e75d35)、[千问-QwQ-Preview](https://help.aliyun.com/zh/model-studio/models#ff99b03558zo4)
    
-   [DeepSeek](https://help.aliyun.com/zh/model-studio/models#21ab4c25c7lml)
    

[视觉理解模型](https://help.aliyun.com/zh/model-studio/models#94b18818a6ywy)

-   千问VL-Max、千问VL-Plus、千问VL-OCR
    

### **支持的文件格式**

单个会话支持上传的文件上限10个，且单文件不超过10MB。

**重要**

上传的文件仅在**当前会话**中有效，刷新或关闭页面将导致文件丢失。请及时完成所需操作。

支持上传本地的文档、图片、视频或音频，格式要求为：

-   **文档：**`.doc`，`.docx`，`.wps`，`.ppt`，`.pptx`，`.xls`，`.xlsx`，`.md`，`.txt`，`.pdf`；
    
-   **图片：**`.png`，`.jpg`，`.jpeg`，`.bmp`，`.gif`；
    
-   **视频：**`.mp4`，`.mkv`，`.avi`，`.mov`，`.wmv`，`.webm`，`.flv`；
    
-   **音频：**`.aac`，`.amr`，`.flac`，`.m4a`，`.mp3`，`.mpeg`，`.ogg`，`.opus`，`.wav`，`.wma`。
    

对于需要处理超过10MB文件的场景，推荐使用文件上传API，详见本文的[API 参考](#25a34d7090ck8)章节。

## 如何使用

### **全文引用**

#### **使用步骤**

1.  在[智能体应用](https://bailian.console.aliyun.com/?tab=app#/app-center)中选择一个模型；
    
2.  在**规划** > **文件处理**模块中，选择**全文引用****；**
    
3.  在右侧调试窗口输入框左侧，点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009320.png)**图标上传本地文件后，可围绕文件内容进行对话。
    

#### **参数配置**

可点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009317.png)**进入配置页面：

-   **单文件最大解析长度（token）**：限制单个文件提取的 token 数量，超出部分将从**文件末尾**被截断。
    
-   **最大拼装长度（token）**：限制所有文件内容拼接后的总 token 数量，超出部分将从**最后拼接文件的末尾**开始被截断。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1010475.png)

**说明**

为避免信息丢失，应合理设置**单文件最大解析长度（token）**或考虑使用**切片检索**模式处理长文件。

#### **示例**

-   上传[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/faqsct/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，提问：“请帮我总结这个文件的内容。”。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009249.png)
    

### **切片检索**

#### **参数配置**

可点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009317.png)**进入配置页面：

-   **召回片段数**：模型回答时引用的相关文本片段的最大数量。
    
-   **最大拼装长度**：限制所有被召回片段拼接后的总 token 数量。若超出，系统将根据相关性得分从低到高依次丢弃召回的片段，直至满足长度限制。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009248.png)

#### **仅检索当前上传文件**

##### **使用步骤**

1.  在[智能体应用](https://bailian.console.aliyun.com/?tab=app#/app-center)中选择一个模型；
    
2.  在**规划** > **文件处理**模块中，选择**切片检索****；**
    
3.  在右侧调试窗口点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009320.png)**图标上传本地文件后，可围绕文件内容进行对话。
    

##### **示例**

上传[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/faqsct/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，提问：“请帮我推荐一款5000元左右的手机。”。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009479.png)

#### **混合检索文件与知识库**

##### **使用步骤**

1.  在[智能体应用](https://bailian.console.aliyun.com/?tab=app#/app-center)中选择一个模型；
    
2.  在**规划** > **文件处理**模块中，选择**切片检索****；**
    
3.  在**规划** > **知识** > **文档**模块中，点击 **+** 按钮，从已有[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)列表中选择并添加（若无，请先在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建）；
    
4.  在右侧调试窗口点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009320.png)**图标上传本地文件后，即可基于上传文件和已关联知识库的全部内容进行综合问答。
    

##### **示例**

先在知识库中存入一份视频文件，然后在输入框中点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009320.png)**图标上传[test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250922/ltuaji/test.mp4)，提问：“这个视频中的人物有没有出现在知识库中？”。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009418.png)

### **自定义处理**

#### **使用步骤**

1.  在[智能体应用](https://bailian.console.aliyun.com/?tab=app#/app-center)中选择一个模型；
    
2.  在**规划** > **文件处理**模块中，选择**自定义处理****；**
    
3.  在**技能**下，添加所需的工具（MCP、插件等）；
    
4.  在右侧调试窗口点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009320.png)**图标上传文件后，可通过对话下达指令，让模型调用已配置的工具对该文件进行处理。
    

#### **特定模型图片处理配置**

当您选择[千问VL系列模型](https://help.aliyun.com/zh/model-studio/vision)并上传文件后，可点击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009317.png)**图标，进行处理方式配置。

在**自定义处理**模式下，不同类型的文件处理逻辑如下：

-   **图片文件**：可选择以下两种处理方式：
    
    -   **模型处理**：模型仅使用自己的视觉能力来分析图片并直接回答，不会调用外部工具。适用于“看图问答”。
        
    -   **模型处理 + 规划**：模型在看懂图片后，会判断是否需要调用您配置的外部工具（如插件）来完成更复杂的任务。适用于需要编辑、转换或借助工具分析图片的场景。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009257.png)
    
-   **其他文件（文档、音视频等）**：模型将自主判断是否需要调用工具处理。
    

#### **示例**

**智能体配置：**

1.  选择**千问VL系列模型**，点击**自定义处理**选项旁的配置图标，将图片处理方式设为**模型处理+规划**。
    
2.  在**MCP服务**处添加**人物风格重绘**工具。
    

**使用：**上传示例文件[girl.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250922/lnfliw/girl.png)，提问：“帮我把这张图的画风转为炫彩卡通风格。”。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2154168571/p1009502.png)

## **API 参考**

### **前提条件**

1.  **应用发布**：调用 API 前，请确保应用已在控制台发布。
    
2.  **处理模式**：文件将按照您在智能体应用中保存的配置（如**全文引用**、**切片检索**）进行处理。API调用时**无法**动态切换处理模式。
    

### **调用限制**

文件问答功能的 API 调用遵循其所属**智能体应用**的统一限流策略。

-   **默认限制**：每个智能体应用的调用频率上限为 **100次/分钟**。
    
-   **共享配额**：此限制涵盖了对该应用的所有 API 请求，包括但不限于文件问答调用。例如，如果您在 1 分钟内调用了 50 次文件问答，那么该应用只剩下 50 次调用额度可用于其他 API 请求。
    

### **文件传递方式和参数说明**

**文件传递方式**

**API 参数**

**主要用途 / 特点**

通过`image_list`参数传递图片URL

`image_list`

进行**图片检索、视觉理解**，单文件大小限制10MB。

通过`file_list`参数传递通用文件URL

`file_list`

传递通用文件的URL。在**全文引用/切片检索**模式下，系统会提取并使用文件文本；在**自定义处理**模式下，模型将接收原始文件URL以调用工具。单文件大小限制10MB。

通过文件上传API接口

`session_file_id`

**生产环境推荐。**

**流程：**  
1\. 调用文件上传 API 上传文件，获取`session_file_id`。  
2\. 在对话API请求中传入此 ID。  
**优点**：支持更大文件，传输更稳定。  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

**更多调用信息请参考**：[上传文件（文档、图片、视频或音频）](https://help.aliyun.com/zh/model-studio/call-single-agent-application/#30619780ddy93)。

## 计费说明

-   **上传文件**：文件上传操作本身不收取费用。
    
-   **模型调用**：基于文件内容进行问答会消耗模型的输入和输出 Token，按所选模型的标准计费，详情请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)。不同模式下输入Token的计算方式不同：
    
    -   **全文引用模式**：会将整个文件内容（或截断后的内容）作为输入传递给模型，因此输入Token消耗较大。
        
    -   **切片检索模式**：仅将用户问题和检索到的最相关文本片段作为输入，输入Token消耗通常远小于全文引用模式，更适合处理长文档。
        
    -   **自定义处理模式**：Token消耗取决于模型与工具交互的复杂性，包括理解用户指令、调用工具、总结工具返回结果等环节。
        
-   **工具调用**：部分工具收费，具体费用在工具详情页展示。
    

## 常见问题

1.  **如何为API提供公网可访问的文件URL ？**
    
    推荐使用[阿里云对象存储OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，它提供了高可用、高可靠的存储服务，并且可以方便地生成公网访问URL。
    
    请确保您提供的URL可被阿里云百炼的服务正常访问：可在浏览器或通过 curl 命令访问该 URL，确保文件能够成功下载。
    
2.  **文件的有效期是多久？**
    
    -   **通过聊天窗口上传：**仅在**当前会话**中有效，关闭、刷新页面或会话超时都将导致文件失效。
        
    -   **通过文件上传 API（**`**session_file_id**`**）**：上传的文件有效期通常为 24 小时。
        
    -   **通过URL（**`**image_list**`**,** `**file_list**`**）**：文件的可访问性由您提供的 URL 自身决定。
        
3.  **为什么我的文件上传失败？**
    
    上传失败可能由多种原因导致：
    
    -   **文件本身：**检查文件大小、格式是否符合[支持的文件格式](#ec857a7815nnc)。
        
    -   **网络问题：**检查您的网络连接以及到服务终端节点的网络连通性。
        
    -   **URL方式：**确认URL公网可访问，且非临时签名URL。
        
    -   **API调用：**检查请求认证信息及参数格式是否正确。
        
    -   **错误信息：**仔细阅读API返回的错误响应体，它通常会指出具体问题。
        
4.  **为什么模型的回答不完整或不准确？**
    
    可能的原因：
    
    -   **内容截断**：文件内容被 token 限制截断，可在**全文引用**模式下，合理调高“单文件最大解析长度”和“最大拼装长度”参数。对于超长文件，建议切换至**切片检索**模式。
        
    -   **提问模糊**：提问不够具体，建议明确指出需要的信息类型，以便模型更好地理解您的意图。
        
    -   **检索效果不佳（切片检索模式）**：若使用**切片检索**模式，回答不准确可能是以下两点：1、检索到的相关片段不佳；2、切片策略不当。请尝试优化您的提问，使其更具指向性；在应用配置中调整切片大小，以优化检索的完整性。
        
    -   **文件内容质量不佳：**解析器可能难以处理低清晰度的扫描件、包含复杂表格/公式的文档、或编码不规范的文本文件。请尽量提供内容清晰、结构简单的源文件。
