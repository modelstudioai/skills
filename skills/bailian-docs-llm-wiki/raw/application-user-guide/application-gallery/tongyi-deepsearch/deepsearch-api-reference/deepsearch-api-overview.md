# API概览

本产品（通义深度搜索）对外服务接口目录。所有接口使用 DashScope HTTP 协议对外提供服务。

## API鉴权

调用接口需要先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，邀测期间，仅百炼**默认业务空间**所属的API Key有调用权限。

## API目录

**API名称**

**API概述**

[生成对话](raw/application-user-guide/application-gallery/tongyi-deepsearch/deepsearch-api-reference/deepsearch-api-list/deepsearch-chat-generate.md)

基于智能体应用管理提供的 agent\_id 与 agent\_version 信息，提供场景化对话、研究、写作相关能力。

[上传文件](raw/application-user-guide/application-gallery/tongyi-deepsearch/deepsearch-api-reference/deepsearch-api-list/deepsearch-file-upload.md)

基于动态文件操作接口能力获取处理好的文件信息，支持智能体应用的 API 调用通过 parameters.agent\_options.sessions\_files 参数完成“动态文档解析”工具的文件数据注入。

[对话文件管理](raw/application-user-guide/application-gallery/tongyi-deepsearch/deepsearch-api-reference/deepsearch-api-list/deepsearch-session-file-management.md)

深度搜索应用支持按 session\_id 维护对话文件目录树：可基于临时文件ID和文件/目录元信息更新目录树，也可删除文件并获取目录树信息，该能力仅适用于法律阅卷场景。

[生成报告导出](raw/application-user-guide/application-gallery/tongyi-deepsearch/deepsearch-api-reference/deepsearch-api-list/deepsearch-report-export.md)

深度搜索应用生成的结果报告文件（md、html、pdf）获取。

[对接自有知识库](raw/application-user-guide/application-gallery/tongyi-deepsearch/deepsearch-api-reference/deepsearch-api-list/docking-self-built-database.md)

支持接入自有知识库，用户可以参考该接口规范进行知识库对接，该能力仅适用于通用场景。
