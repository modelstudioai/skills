# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖认证凭证获取、SDK 集成、服务端点配置等关键环节。开发者需按顺序完成这些准备，否则将无法发起有效请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中定义的规范流程。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），并统一支持同步推理、流式响应、批量调用及[异步任务](../concepts/asynchronous-task.md)提交等核心能力。模型能力边界由实际调用的 endpoint 决定，与准备工作本身无关。具体模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 Base URL 总览章节。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 中传递  
- `base_url`：可选，默认为 `https://dashscope.aliyuncs.com/api/v1`；如需访问专属实例或测试环境，须显式指定，详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)  
- `model`：非 preparation 阶段参数，但 SDK 初始化时若预设 model（如 `DashScopeClient(model="qwen-max")`），会影响后续调用的默认行为，该用法在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：[SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的 `dashscope.api_key = "xxx"` 全局赋值方式已被弃用，2.x+ SDK 要求每个 Client 实例独立传入 `api_key`，混用将导致认证失败。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥，严禁硬编码或提交至代码仓库  
2. **安装 SDK**：执行 `pip install dashscope>=2.0.0`（Python）或对应语言最新稳定版，旧版本存在已知安全缺陷，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)  
3. **初始化 Client**：传入 `api_key` 和（可选）`base_url`，例如：  
   ```python
   from dashscope import Generation
   client = Generation(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/api/v1")
   ```
4. **调用前验证**：建议首次集成时用空请求测试连通性（如 `client.models.list()`），避免因网络或配置问题阻塞后续开发  

## 限制和注意事项

- 单个 API Key 默认限速 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- API Key 仅对创建者所在工作空间生效，跨工作空间调用需单独申请密钥  
- 所有 preparation 操作必须在调用模型前完成；运行时动态修改 `api_key` 或 `base_url` 不被 SDK 支持，需重建 Client 实例  
- 企业版用户若启用 VPC 内网访问，必须使用专属 `base_url`，且该地址不兼容公网 DNS 解析 —— 此限制未在 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 中明确标注，实际部署时需额外确认网络策略

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


