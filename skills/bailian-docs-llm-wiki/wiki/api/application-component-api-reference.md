# application component api reference

应用组件 API 提供了将百炼平台能力集成到自定义应用中的标准化接口，支持模型调用、工作流编排、知识库检索等核心场景。该 API 面向企业级开发者设计，强调稳定性、可扩展性与权限隔离。所有接口均需通过 RAM 授权并使用指定服务接入点调用。

## 支持的模型/功能

- **基础大模型调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型，以及部分第三方模型（需开通白名单）  
- **结构化能力组件**：包括 `text2sql`、`table-extract`、`document-parse` 等专用组件，详见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)  
- **工作流引擎集成**：支持通过 `workflow_id` 调用预置或自定义工作流，底层基于百炼可视化编排能力构建  

> **注意**：文档中提及的 `qwen-vl-plus` 模型在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中已标注为“已下线”，当前仅保留 `qwen-vl` 基础多模态能力，调用时请勿使用已废弃模型标识。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，必须从 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中选取有效值 |
| `input` | object | 是 | 输入数据结构，格式依组件类型而异（如文本类为 `{ "text": "..." }`，多模态类需含 `image_url` 字段） |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；范围 `[0.0, 1.0]`，`0` 表示确定性输出 |
| `parameters.max_tokens` | integer | 否 | 最大生成 token 数，默认 `1024`，上限 `4096` |

## 使用方式

1. **鉴权**：使用阿里云 RAM 子账号 AccessKey 或 STS [Token](../concepts/token.md)，并确保已授予 `bailian:InvokeApplicationComponent` 权限 —— 具体策略配置见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)  
2. **请求地址**：调用 `POST https://bailian.aliyuncs.com/api/v1/component/invoke`（生产环境），接入点详情参见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)  
3. **请求示例**（curl）：
   ```bash
   curl -X POST https://bailian.aliyuncs.com/api/v1/component/invoke \
     -H "Authorization: Bearer ${ACCESS_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen-turbo",
           "input": { "text": "你好，请总结以下内容：" }
         }'
   ```

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符；若含图像，单张 `image_url` 必须可公开访问且响应头含 `Content-Type: image/*`  
- QPS 限制默认为 5（按 AccessKey 维度），可通过工单申请提升  
- 所有组件调用均计入百炼平台资源配额，计费以实际 token 消耗为准，详细规则见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)  
- 返回字段 `output` 为字符串或结构化对象，具体形态由所选 `model_id` 决定，不可跨组件假设统一格式

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


