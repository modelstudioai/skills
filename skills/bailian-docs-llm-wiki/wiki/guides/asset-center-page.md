# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理模型、向量模型等）的核心页面，提供模型的上传、版本管理、部署配置与生命周期操作。开发者可通过该页面完成模型的注册、元信息维护及与应用的绑定。所有操作均通过 REST API 或控制台界面触发，后端服务基于 Model Registry 架构实现。

## 支持的模型/功能

资产中心支持以下模型类型及其核心功能：
- **微调模型（Fine-tuned Models）**：支持 LoRA、Full-parameter 等微调产出的 `.bin`/`.safetensors` 模型文件注册与多版本管理；
- **推理模型（Inference Models）**：支持 Hugging Face 格式（含 `config.json` + `pytorch_model.bin`）或 ONNX 模型导入，自动解析 tokenizer 和 model type；
- **向量模型（Embedding Models）**：支持 SentenceTransformer、OpenAI-compatible embedding 模型注册，需显式声明 `input_type="text"` 与 `output_dim`；
- **自定义模型（Custom Models）**：允许上传 Docker 镜像 URI 及启动脚本，适用于非标准框架（如 DeepSpeed、vLLM 自托管实例）。

> **注意**：文档 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中未明确列出 ONNX 支持，但实际接口 `POST /v1/assets` 已兼容 ONNX 模型上传（参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的 `model_format` 字段枚举值）。

## 关键参数

注册或更新模型时需在请求体中指定以下必填/可选参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `name` | string | 是 | 全局唯一模型标识符（仅限小写字母、数字、连字符），长度 3–64 字符 |
| `version` | string | 否 | 语义化版本号（如 `1.2.0`），未提供时由系统自动生成 `vYYYYMMDDHHMMSS` 格式时间戳 |
| `model_format` | string | 是 | 取值：`huggingface`, `onnx`, `safetensors`, `custom`（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)） |
| `framework` | string | 否 | 如 `pytorch`, `tensorflow`, `triton`；`custom` 类型下为必填 |
| `metadata` | object | 否 | 键值对形式的扩展元数据（如 `{"task": "text-embedding", "license": "apache-2.0"}`） |

## 使用方式

### 控制台操作
1. 进入「模型管理」→「资产中心」页面；
2. 点击「新建模型」，选择模型类型并填写表单；
3. 上传模型文件（ZIP 包或单文件），确认元信息后提交。

### API 调用（推荐）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/assets \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "my-llm-v2",
        "model_format": "huggingface",
        "framework": "pytorch",
        "metadata": {"task": "text-generation"}
      }'
```
上传文件需后续调用 `PUT /v1/assets/{asset_id}/upload` 接口（参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的分步流程说明）。

## 限制和注意事项

- 单个模型文件大小上限为 **10 GB**；ZIP 包解压后总大小不可超过 **20 GB**；
- `name` 字段不支持修改，如需重命名须新建资产并迁移关联部署；
- 版本删除后不可恢复，且已绑定的在线服务将立即失效（无自动降级机制）；
- 自定义模型（`model_format=custom`）要求镜像必须监听 `0.0.0.0:8080` 并响应 `/health` 健康检查，否则部署失败。

> **注意**：[资产中心](../../raw/model-user-guide/asset-center-page.md) 中标注的“支持 TensorFlow SavedModel”已被弃用，当前仅保留 `huggingface`/`onnx`/`safetensors`/`custom` 四种格式（以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 为准）。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


