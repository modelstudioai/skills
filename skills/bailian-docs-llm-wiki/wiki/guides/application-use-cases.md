# application [use cases](use-cases.md)

`application use cases` 是百炼平台面向实际业务场景提供的端到端集成方案集合，覆盖主流办公协同平台（如企业微信、钉钉、微信公众号）及私有化部署需求（如本地知识库RAG）。所有用例均基于标准 API 调用与 SDK 封装，无需修改核心模型逻辑，开发者可快速复用已有工作流。详细实现步骤和代码片段请参考对应子文档。

## 支持的模型/功能

- 所有用例默认支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类推理模型，部分 RAG 场景推荐使用 `qwen-plus` 以平衡效果与延迟 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases.md)  
- 企业微信、钉钉、微信公众号等渠道集成均依赖平台提供的 **消息路由中间件** 和 **OAuth2.0 回调认证模块**，不直接暴露模型 endpoint  
- 基于本地知识库构建 RAG 应用需配合 `retrieval` 组件启用向量检索能力，并支持自定义分块策略与嵌入模型（默认 `text-embedding-v1`）[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases.md)

## 关键参数

- `app_id`：每个集成场景必须配置的百炼应用唯一标识，用于鉴权与用量统计  
- `callback_url`：仅限企业微信、钉钉等需要服务端回调的场景，须为 HTTPS 协议且通过平台白名单校验  
- `retrieval_config`：RAG 场景专用参数，含 `top_k`（默认 3）、`score_threshold`（默认 0.3）等字段，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases.md)  

## 使用方式

1. 在控制台创建对应场景的应用（如“钉钉机器人”），获取 `app_id` 与初始化密钥  
2. 按照子文档指引完成渠道侧配置（如钉钉开发者后台添加 Bot、微信公众号启用客服接口）  
3. 调用 `POST /v1/applications/{app_id}/messages` 提交用户消息，平台自动完成上下文管理、工具调用与渠道适配渲染  
> **注意**：微信公众号智能客服文档中提及的“模板消息主动推送”功能已于 v2.3.0 版本下线，当前仅支持用户触发后的 48 小时内被动回复，详见 [10分钟实现微信公众号智能客服](../../raw/application-user-guide/application-use-cases.md)

## 限制和注意事项

- 单个应用每秒请求上限为 5 QPS（企业版可提升至 50 QPS），超限返回 `429 Too Many Requests`  
- 企业微信与钉钉集成不支持富文本卡片中的按钮跳转外链（受渠道方安全策略限制）  
- RAG 场景中，若上传文档含非 UTF-8 编码（如 GBK），解析可能失败，建议预处理为 UTF-8 格式  
- 所有渠道集成均要求 `callback_url` 响应时间 ≤ 3s，否则渠道将中断连接并重试，影响用户体验

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


