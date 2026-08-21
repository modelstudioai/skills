# API概览

千问联网检索 Agent对外服务接口目录。所有接口使用 DashScope HTTP 协议对外提供服务。

## **API鉴权**

调用接口需要先[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，邀测期间，仅百炼**默认业务空间**所属的API Key有调用权限。

### **API目录**

**API名称**

**API概述**

[生成对话](https://help.aliyun.com/zh/model-studio/web-search-agent-api-chat)

千问联网检索Agent提供的 agent\_id 与 agent\_version 信息，提供联网知识检索、场景化对话等能力，支持多模态图像理解问答

[多模态文件操作](https://help.aliyun.com/zh/model-studio/web-search-agent-api-chat-multimodal-file)

使用联网搜索多模态能力时，可以通过如下文件接口，将需要与联网搜索 agent 交互的图片提前上传到 OSS 处，在进行联网问答时，使用已经提前上传到 OSS 图片 url， 可以提供更流畅的问答体验。
