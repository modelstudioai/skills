# general text embedding

通用文本向量（general text embedding）将文本转换为数值向量，可用于语义搜索、推荐、聚类、分类等下游任务。百炼提供两类接口：面向实时场景的**同步接口**（OpenAI 兼容 / DashScope）和面向大批量文件处理的**异步批处理接口**，分别对应不同的模型系列与限额。

## 支持的模型

同步接口（参见 [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)）：

| 模型 | 向量维度 | 单次最大行数 | 单行最大 Token | 单价（千 Token） |
| --- | --- | --- | --- | --- |
| text-embedding-v4 | 2048 / 1536 / 1024（默认）/ 768 / 512 / 256 / 128 / 64 | 10 | 8,192 | 0.0005 元（Batch 0.00025 元） |
| text-embedding-v3 | 1024（默认）/ 768 / 512 / 256 / 128 / 64 | 10 | 8,192 | 同 v4 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 0.0007 元（Batch 0.00035 元） |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 同 v2 |

- v4 属于 Qwen3-Embedding 系列，语种覆盖最广（中、英、西、法、葡、印尼、日、韩、德、俄等 100+ 主流语种及多种编程语言）。
- v2/v1 仅覆盖约 10 个主流语种。

异步批处理接口（参见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)）：

| 模型 | 数据类型 | 向量维度 | 单次请求最大行数 | 单行最大 Token | 单价（千 Token） |
| --- | --- | --- | --- | --- | --- |
| text-embedding-async-v2 | float32 | 1,536 | 100,000 | 2,048 | 0.0007 元 |
| text-embedding-async-v1 | float32 | 1,536 | 100,000 | 2,048 | 0.0007 元 |

> **注意**：同步系列与批处理系列是两套独立模型（如 `text-embedding-v4` 与 `text-embedding-async-v2`），不能混用；批处理接口当前没有对应 v3/v4 的版本，向量维度固定为 1,536。

## 前提条件

- 已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
- 使用 SDK 调用需先[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（同步接口的 OpenAI 兼容模式则使用 OpenAI SDK）。
- DashScope SDK 当前仅支持 Python 与 Java。

## 同步接口（OpenAI 兼容）

详见 [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)。

- **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **HTTP Endpoint**：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`

### 关键请求参数

| 参数 | 必选 | 说明 |
| --- | --- | --- |
| `model` | 是 | 模型名，如 `text-embedding-v4` |
| `input` | 是 | 待向量化输入：字符串、字符串列表或文件对象 |
| `dimensions` | 否 | 向量维度，可选 `2048`、`1536`（仅 v4）、`1024`、`768`、`512`、`256`、`128`、`64`；默认 `1024`；**仅 v3/v4 支持该参数** |
| `encoding_format` | 否 | 当前仅支持 `float` |

输入长度规则：

- **v3 / v4**：字符串输入最长 8,192 Token；列表或文件最多 10 行，每行 ≤ 8,192 Token。
- **v1 / v2**：字符串输入最长 2,048 Token；列表或文件最多 25 行，每行 ≤ 2,048 Token。

### Python 调用示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

resp = client.embeddings.create(
    model="text-embedding-v4",
    input=["风急天高猿啸哀", "渚清沙白鸟飞回"],
    dimensions=1024,            # 仅 v3 / v4 支持
    encoding_format="float",
)
print(resp.model_dump_json())
```

### 响应结构

```json
{
  "data": [
    { "embedding": [-0.0695..., 0.0306...], "index": 0, "object": "embedding" }
  ],
  "model": "text-embedding-v4",
  "object": "list",
  "usage": { "prompt_tokens": 184, "total_tokens": 184 },
  "id": "73591b79-..."
}
```

`data[].embedding` 为 float 数组；`usage.prompt_tokens` 与 `total_tokens` 用于计费。

## 异步批处理接口

详见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)。适用于大文件、大批量、对延迟不敏感的离线向量化场景。

### HTTP 调用流程

HTTP 模式仅支持异步，分两步完成：

1. **创建任务**：

   ```
   POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding
   ```
   必须携带请求头 `X-DashScope-Async: enable`，否则会报 `current user api does not support synchronous calls`。

2. **查询任务结果**：

   ```
   GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
   ```

### 关键请求字段

- `model`：`text-embedding-async-v1` 或 `text-embedding-async-v2`。
- `input.url`：待向量化文本文件的公网可访问 URL，一行一条；**单文件 ≤ 200MB**、**最多 100,000 行**、**每行 ≤ 2,048 Token**。
- `parameters.text_type`：`document`（默认，对称任务）或 `query`（用于非对称检索的查询侧）。

### 任务状态枚举

`PENDING`（排队中）/ `RUNNING`（处理中）/ `SUCCEEDED`（成功）/ `FAILED`（失败）/ `CANCELED`（已取消）/ `UNKNOWN`（不存在或未知）。

成功响应中的 `output.url` 即为结果文件的下载地址。

> **注意**：任务数据（含结果 URL）**仅保留 24 小时**，超时后会被清除，请务必及时下载并落盘。

### DashScope SDK 调用

DashScope SDK 在底层异步服务上封装了同步与异步两种调用方式：

- **同步调用**：`BatchTextEmbedding.call(...)`，阻塞直至任务结束。
- **异步调用**：`async_call` 创建任务 → `fetch` 查询状态 → `wait` 阻塞等待 → `cancel` 取消（仅 `PENDING` 状态可取消）。

Python 示例：

```python
from dashscope import BatchTextEmbedding

result = BatchTextEmbedding.call(
    BatchTextEmbedding.Models.text_embedding_async_v1,
    url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241016/nigwvr/text_embedding_file.txt",
    text_type="document",
)
print(result)
```

## 限流与免费额度

- **同步接口**：限流策略参见[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)；v3/v4 各提供 100 万 Token 免费额度，v1/v2 各 50 万 Token，有效期为开通后 90 天。
- **异步批处理接口**：
  - 任务下发接口 RPS 限制为 **1**。
  - 排队中 + 运行中作业总数 ≤ **50**，同时并发运行作业 ≤ **3**。
  - v1 / v2 各赠送 2,000 万 Token 免费额度，有效期 90 天。

## 选型与使用建议

- **实时检索 / 在线服务**：优先使用同步接口 + `text-embedding-v4`，可通过 `dimensions` 压缩到更小维度以降低存储与检索成本。
- **离线索引、千万级文档批处理**：使用异步批处理接口（`text-embedding-async-v2`），单次最高 10 万行，但向量维度仅 1,536，且必须能提供公网可访问的输入 URL。
- **非对称检索（短 query → 长 document）**：批处理接口建议对查询侧使用 `text_type=query`，底库侧使用 `text_type=document`；聚类、分类等对称任务保持默认 `document` 即可（详见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)）。
- **迁移成本**：已有 OpenAI Embedding 调用代码可直接通过同步接口的 OpenAI 兼容模式迁移；需要异步、批量或 SDK 高级特性时再切换到 DashScope SDK。
- **错误处理**：异常响应中 `code` / `message` 字段对应错误码，对照[错误码](https://help.aliyun.com/zh/model-studio/error-code)排查；常见如 `invalid_api_key`（API Key 错误）、缺少 `X-DashScope-Async` 头等。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)













