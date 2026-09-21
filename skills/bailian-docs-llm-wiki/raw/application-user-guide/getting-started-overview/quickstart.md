# 快速开始

了解 ParseX 的控制台体验流程，快速体验平台功能。

1.  **选择文档并上传**
    
    已获得控制台访问权限并从正式授权入口进入后，在 Parse 或 Extract 控制台选择本地文件或者/样本文档并发起处理。体验页面支持单个文档最大 200MB、单张图片最大 20MB；API 调用的文件大小限制请查看 API 文档。配置要求分别参见[配置文档解析](raw/application-user-guide/getting-started-overview/overview/configuration.md)和[信息抽取控制台](raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)。
    
2.  **逐项核对结果**
    
    等待处理完成，将运行结果与原文和预期对照，检查内容完整性、结构准确度、抽取内容准确性等信息。结果区提供「抽取结果 JSON」与「抽取字段详情」两种查看方式，字段详情逐项列出字段值及其来源页码。
    
3.  **保存配置（可选）**
    
    可在体验页面将配置好的解析/抽取设置保存成配置，生成唯一的`config_id`进行接口调用。
    
4.  **按定好的配置或者参数调用**
    
    接口可复用同一 `config_id`进行调用，也可以自由传入解析/抽取的配置参数进行任务的调用。
    
5.  **查看任务**
    
    控制台操作可在“任务记录”中查看页面提供的状态、结果和用量。也可按照`biz_id`结果接口轮询处理状态。
