# 提交抽取任务

提交结构化信息抽取任务，支持在线单文件、复用解析结果与离线批量清单，返回任务 ID 用于异步查询。

提交结构化信息抽取任务。输入可以是文件 URL、此前解析任务返回的 `parsed_file_biz_id`，或离线批量任务清单 URL。在线任务返回 `biz_id`；离线任务返回 `biz_id_list`。提交后使用任务 ID 调用[查询抽取结果](extract-result.md)获取处理状态和结构化结果。

> **说明**
>
> 调用前请确保已获取 API Key，详见[鉴权](../authentication.md)。

<a id="请求参数"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `file_url` | string | 否 | 待抽取文档的可访问 URL。与 `parsed_file_biz_id`、`batch_job_url` 三选一。单个文档支持 1.5 万页及以内且 1 GB 以内的 PDF、Word 等文档，支持 20 MB 以内的单张图片。 |
| `parsed_file_biz_id` | string | 否 | 已完成解析的业务任务 ID。与 `file_url`、`batch_job_url` 三选一。 |
| `batch_job_url` | string | 否 | 待离线批量任务清单 URL。与 `file_url`、`parsed_file_biz_id` 三选一。JSON 数组，每条为子任务：`file_url`/`file_name`/`file_id`/`parsed_file_biz_id` 等。离线子任务数量支持 200 个及以内，超过 200 个时不处理。单个文档支持 1.5 万页及以内且 1 GB 以内的 PDF、Word 等文档，支持 20 MB 以内的单张图片。 |
| `file_name` | string | 否 | 在线业务文件名。协议同时提供 `file_name_extension`，二者按文件信息填写方式二选一。 |
| `file_name_extension` | string | 否 | 在线业务文件类型。与 `file_name` 二选一。 |
| `config_id` | string | 否 | 已保存的 Extract 配置 ID，例如 `config_xxx`。 |
| `processing` | object | 否 | 内联处理配置，优先级高于 `config_id`。 |
| `processing.user_prompt` | string | 否 | 用户 Prompt |
| `processing.extract_processing_config` | object | 否 | 内联抽取处理配置。使用 `processing` 时必须提供 |
| `processing.extract_processing_config.citation_required` | boolean | 否 | 是否返回引用信息，默认 `true` |
| `processing.extract_processing_config.allow_inference` | boolean | 否 | 是否允许推断，默认 `false` |
| `processing.extract_processing_config.extract_schema` | object | 否 | 抽取 Schema，值为 JSON 对象。使用内联处理配置时必须提供 |
| `output` | object | 否 | 输出配置 |
| `output.oss_config` | object | 否 | OSS 输出配置 |
| `output.oss_config.bucket` | string | 否 | OSS Bucket 名称 |
| `output.oss_config.endpoint` | string | 否 | OSS Endpoint |
| `output.oss_config.access_key_id` | string | 否 | OSS AccessKey ID |
| `output.oss_config.access_key_secret` | string | 否 | OSS AccessKey Secret |
| `output.oss_config.security_token` | string | 否 | OSS Security Token |

> **说明**
>
> -   在线业务与离线业务：
>     -   在线业务：线上实时解析和返回任务，适合快速响应场景。
>     -   离线业务：一次提交多条子任务，适合可接受较长等待时间的场景。离线任务承诺提交后 7×24 小时内完成。
>     -   离线业务单次请求最多支持 200 条子任务，每个子任务独立计费。
>     -   在线业务和离线业务计费逻辑不同，详情参考[计费文档](../../../application-user-guide/agent-billing/pricing.md)。
> -   文件来源使用 `file_url`、`parsed_file_biz_id` 或 `batch_job_url` 三选一：
>     -   `file_url` 或 `parsed_file_biz_id` 非空时，`batch_job_url` 被忽略，走在线业务。
>     -   `file_url` 和 `parsed_file_biz_id` 均为空且 `batch_job_url` 非空时，`batch_job_url` 生效，走离线批量业务。
> -   `batch_job_url` 指向 JSON 数组格式的任务清单，每条为一个子任务，包含：
>     -   `file_url`：子任务文件 URL。与 `parsed_file_biz_id` 二选一。
>     -   `parsed_file_biz_id`：已完成解析的在线或离线任务 ID。与 `file_url` 二选一。
>     -   `file_name`：子任务文件名称。
>     -   `file_id`：自定义子任务 ID。
> -   处理定义使用 `config_id` 或内联 `processing`。离线业务的所有子任务共用一个配置，不支持单次请求内各子任务单独配置。
> -   复用解析结果时，该结果需要仍在 7 天保留期内，并且输入类型必须支持复用。

<a id="返回结果"></a>

## 返回结果

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `request_id` | string | 请求 ID |
| `data.biz_id` | string | 在线业务任务 ID，用于调用 `/extract/result` |
| `data.biz_id_list` | array | 离线业务任务 ID 清单 |
| `data.biz_id_list[].biz_id` | string | 离线业务子任务 ID，用于调用 `/extract/result`。如果识别失败，不会返回此字段。 |
| `data.biz_id_list[].file_id` | string | 离线业务自定义单个子任务 ID。 |
| `data.biz_id_list[].code` | string | 离线业务子任务错误码。如果识别成功，不会返回此字段。 |
| `data.biz_id_list[].message` | string | 离线业务子任务错误信息。如果识别成功，不会返回此字段。 |
| `data.biz_id_list[].status` | string | 离线业务子任务状态。`success` / `fail`，表示子任务提交是否成功。 |

<a id="代码示例"></a>

## 代码示例

以下示例分别展示两种处理定义， `config_id` 与 `processing` 同时存在时，`processing` 会优先生效。示例中的 URL、任务 ID 和配置 ID 均为脱敏占位值。

在线任务：

<a id="sec-tabs"></a>

<a id="使用已保存配置"></a>

<a id="使用已保存配置-h4"></a>

#### 使用已保存配置

<a id="code-block"></a>

```bash
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/extract/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "file_url": "https://example.com/contracts/sample.pdf",
    "file_name": "sample.pdf",
    "config_id": "config_xxx"
  }'
```

<a id="使用内联配置"></a>

<a id="使用内联配置-h4"></a>

#### 使用内联配置

`extract_schema` 为 JSON 对象。

<a id="code-block-2"></a>

```bash
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/extract/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "parsed_file_biz_id": "biz_xxx",
    "processing": {
        "user_prompt": "按 Schema 抽取合同信息",
        "extract_processing_config": {
            "citation_required": true,
            "allow_inference": false,
            "extract_schema": {
                "type": "object",
                "properties": {
                    "contract_number": {
                        "type": "string"
                    },
                    "total_amount": {
                        "type": "number"
                    }
                }
            }
        }
    }
}'
```

<a id="code-block-3"></a>

```json
{
  "request_id": "request_xxx",
  "data": {
    "biz_id": "biz_xxx"
  }
}
```

离线任务：

<a id="sec-tabs-2"></a>

<a id="使用已保存配置-2"></a>

<a id="使用已保存配置-2-h4"></a>

#### 使用已保存配置

<a id="code-block-4"></a>

```bash
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/extract/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "batch_job_url": "https://example.com/manifest.json",
    "config_id": "config_xxx"
  }'
```

<a id="使用内联配置-2"></a>

<a id="使用内联配置-2-h4"></a>

#### 使用内联配置

`extract_schema` 为 JSON 对象。

<a id="code-block-5"></a>

```bash
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/extract/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "batch_job_url": "https://example.com/manifest.json",
    "processing": {
        "user_prompt": "按 Schema 抽取合同信息",
        "extract_processing_config": {
            "citation_required": true,
            "allow_inference": false,
            "extract_schema": {
                "type": "object",
                "properties": {
                    "contract_number": {
                        "type": "string"
                    },
                    "total_amount": {
                        "type": "number"
                    }
                }
            }
        }
    }
}'
```

<a id="code-block-6"></a>

```json
{
    "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": {
        "biz_id_list": [
            {
                "biz_id": "parseX-pre-2026xxxx-xxxxxxx",
                "file_id": "file_001",
                "status": "success"
            },
            {
                "file_id": "file_002",
                "code": "MissingFileUrl",
                "message": "FileUrl is mandatory.",
                "status": "fail"
            }
        ]
    }
}
```

> **警告**
>
> 重要提示
>
> -   复用的解析结果若已超过 7 天保留期或类型不匹配，接口会返回对应错误；详见[错误码](../errors.md)。
> -   Schema 规模和长文档页数仅按工程设计边界规划，公开配额以正式页面为准，见[支持的文件与限制](../../../application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)。
> -   抽取接口不支持音视频输入。

> **重要**
>
> 提交后，使用[查询抽取结果](extract-result.md)轮询任务状态并获取结构化结果。
