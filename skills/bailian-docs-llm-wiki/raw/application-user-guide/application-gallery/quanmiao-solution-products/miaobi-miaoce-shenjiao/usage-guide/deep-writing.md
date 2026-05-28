# 深度写作

本文档是关于全妙深度写作的操作指导。

## **功能概述**

深度写作是一个基于开源的multi-agent框架构建的deep research类型的实例，该功能深度融合客户业务数据，围绕数据分析、工具链建设与输出形态设计，实现研究报告生成的端到端智能化流程，能够自动生成新媒体账号监控日报、行业市场分析报告、专题片脚本等多种内容产品

## **功能入口**

进入[妙笔](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_media&from=bailian#/home)，功能入口在**内容创作Agent>深度写作**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054594.png)

## **功能介绍**

### **配置页**

按照要求进行配置并输入写作主题后，点击即可一键启动写作，下面是配置项介绍：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054663.png)

-   **上传本地素材**
    
    -   上传参考文档，最多10个，支持txt、doc、pdf格式，单文件最大10MB；
        
    -   上传数据表，最多3个，支持csv、xlsx格式，单文件最大10MB；
        
-   **写作信源**
    
    -   默认提供「互联网搜索」，联网搜索时可以添加指定网址；
        
        **说明**
        
        在「互联网搜索」中，您可添加指定网站并开启「限定权威数据源」开关。启用后，深度写作将仅从您信任的站点中检索信息，确保内容素材来源权威、可靠、可控。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054627.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054628.png)
        
    -   添加指定数据源，目前支持两种方式：本地上传文档作为数据源，通过API引入数据源；
        
    -   授权OSS对接数据源。
        
        **说明**
        
        添加指定数据源和授权OSS对接数据源的操作方式可参考《[新建数据源](https://help.aliyun.com/zh/model-studio/ai-miaosou#885a03b827reb)》文档进行配置。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054617.png)
    
-   **子Agent**
    
    -   项目经理：负责规划任务，与用户一起分析任务目标，并将目标拆解成任务分发给其他Agent，并检查每个阶段性成果。
        
    -   数据收集员：负责从互联网搜索，阅读资料，并将有效信息整理成文档，作为后续的分析素材。
        
    -   报告撰写师：负责撰写文档，总结现有材料，形成行文清晰的文档，输出给用户。
        
    -   数据分析员：负责分析数据，包括离线分析数据和在线搜索的数据，并根据分析结果绘制图表。
        
        **说明**
        
        当启用「数据分析员」子Agent 时，系统提供两种图表呈现方式：可选择仅生成图表，或同时输出图表与原始数据表格，满足不同场景下的查看与验证需求。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054614.png)
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054613.png)
    
-   **方法论**：官方提供案头调研报告、市场分析报告、消费者洞察报告、纪录片脚本的方法论，用户也可以自定义方法论，创作不同类型的报告；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054650.png)
    
-   **目录**：开启目录开关后，生成的报告开头将自动生成目录，点击目录中的章节标题即可快速跳转至对应内容。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054651.png)
    

### **结果页**

**说明**

深度写作任务需进行深度检索与内容规划，单次生成预计耗时 20 分钟以上。我们已为您开启站内提醒，任务完成后将第一时间通知您，请耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054660.png)

1.  写作完成后界面如下图所示，以下逐一介绍各模块的功能。
    

-   左侧是项目管理Agent设计的执行计划，各Agent会协同完成任务；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054681.png)
    
-   右侧是结果：
    
    -   报告：展示生成的报告，包含验真视图和发布视图。验真视图允许您在线查验报告的数据与生成依据，完整保留中间文件以支持溯源；而发布视图则是下载后正式报告，删除了中间文件；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054677.png)
        
    -   活动：任务的思考和执行过程；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054678.png)
        
    -   文件：任务执行过程中生成的中间文件，基于检索到的数据源进行整理与摘要后形成，支持在线预览与下载，并可追溯原始搜索数据源。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054680.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054676.png)
        
    -   数据源：生成当前报告所检索的数据源。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054679.png)
        

2.  **溯源验真**：在验真视图下，所有生成内容均关联可追溯的中间文件。您可通过中间文件查看其原始来源，实现完整溯源与真实性验证。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054670.png)
    
3.  **AI导读**：系统为每篇报告自动生成内容概述、关键要点、关键词、速读摘要和思维导图，并支持基于报告内容的问答功能，让您读得更快、理解得更深、问得更准。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054671.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054673.png)
    
4.  **报告下载**：支持导出为 Markdown、PDF 或 ZIP 压缩包（含完整资源）三种格式。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6522283771/p1054682.png)
