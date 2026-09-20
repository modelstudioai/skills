# 使用文档解析控制台

在 ParseX 控制台中配置文档输入、解析选项。

通过文档解析控制台，您可以选择文件、调整解析设置，并对照原文件检查图文或音视频结果。

1.  **进入解析工作区**
    
    打开 [ParseX](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，登录后选择左侧「文档解析」。工作区包含输入、配置和结果等区域，您可以在同一页面完成一次体验。
    
    ![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dc8.png)
    
    **工作区部分**
    
    **用途**
    
    输入文件
    
    选择材料，确认文件名并查看原始内容
    
    解析配置
    
    调整本次处理要求
    
    结果区域
    
    解析完成后阅读和检查结果
    
2.  **选择材料**
    
    在输入区域上传文件，或选择内置样例。核对文件名，确认原文件能够正常查看或播放。
    
3.  **设置解析要求**
    
    1.  在**字段结构**中填写需要字段抽取的信息。
    2.  按[配置信息抽取](raw/application-user-guide/overview/overview/configuration.md)检查字段名称、类型和说明。
    3.  检查抽取设置与补充要求。
    
    已有合适配置时，按[保存与复用配置](raw/application-user-guide/overview/configurations.md)中的方法进入测试并复用。
    
4.  **提交解析**
    
    1.  确认选定文件与本次设置。
    2.  点击「运行文档解析」。
    3.  等待任务完成；需要查看处理进度时，进入[任务记录](raw/application-user-guide/overview/configurations/tasks.md)。
    
    已提交的任务使用提交时的设置。后续修改页面设置，需要再次运行才会得到新的结果。
    
5.  **查看结果并完成验证**
    
    **图文文档**完成后，可以切换 Markdown 和 JSON 视图：
    
    -   **Markdown**：适合阅读正文、查看表格和复制整理后的内容。
    -   **JSON**：适合检查结构化内容及结果中实际返回的信息。
    
    先选一页原文对照，依次核对标题、段落顺序、表格数字和图片描述。需要使用结果文本时，可使用结果区域的复制按钮。
    
    ![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dc4.png)
    
    **媒体材料**可结合段落内容和时间位置检查结果。视频结果包含「剧情概述」「解析段落结果」「剧情分段」「剧情摘要」四个视图。
    
    建议先看概述或摘要了解整体内容，再打开「解析段落结果」，选择感兴趣的音频或视频片段。点击带时间位置的片段后，播放器定位到相应位置，便于回听或回看。
    
    ![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dcc.png)
    
6.  **返回历史结果**
    
    进入[任务记录](raw/application-user-guide/overview/configurations/tasks.md)，找到对应解析任务，查看详情并从结果入口返回查看。
