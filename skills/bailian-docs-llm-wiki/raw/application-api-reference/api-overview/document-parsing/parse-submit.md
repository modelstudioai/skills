# 提交解析任务

提交文档或音视频解析任务，支持在线单文件与离线批量清单，返回任务 ID 用于异步查询。

在线任务提交单个文件，返回 `biz_id`；离线任务提交批量任务清单，返回 `biz_id_list`。解析为异步任务：提交后使用任务 ID 调用[查询解析结果](parse-result.md)获取处理状态和结果。

> **说明**
>
> 调用前请确保已获取 API Key，详见[鉴权](../authentication.md)。

<a id="请求参数"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `file_url` | string | 否 | 待解析在线文件的 URL。与 `batch_job_url` 二选一。单个文档支持 1.5 万页及以内且 1 GB 以内的 PDF、Word 等文档，支持 20 MB 以内的单张图片。 |
| `batch_job_url` | string | 否 | 待离线批量任务清单 URL。与 `file_url` 二选一。JSON 数组，每条为子任务：`file_url`/`file_name`/`file_id` 等。离线子任务数量支持 200 个及以内，超过 200 个时不处理。单个文档支持 1.5 万页及以内且 1 GB 以内的 PDF、Word 等文档，支持 20 MB 以内的单张图片。 |
| `file_name` | string | 否 | 在线业务文件名称。协议同时提供 `file_name_extension`，二者按文件信息填写方式二选一。 |
| `file_name_extension` | string | 否 | 在线业务文件类型。与 `file_name` 二选一。 |
| `config_id` | string | 否 | 配置 ID。例如 `config_xxx`，与内联参数同时传递时内联参数优先生效。 |
| `processing` | object | 否 | 处理配置。 |
| `processing.user_prompt` | string | 否 | 用户自定义 Prompt。 |
| `processing.doc_processing_config` | object | 否 | 文档解析处理配置。 |
| `processing.doc_processing_config.page_index` | string | 否 | 解析页数范围。例如 `1-10`。 |
| `processing.doc_processing_config.head_foot` | boolean | 否 | 是否解析页眉和页脚。 |
| `processing.doc_processing_config.layout_position` | boolean | 否 | 是否返回坐标。 |
| `processing.doc_processing_config.image_caption` | boolean | 否 | 是否生成图片描述。 |
| `processing.media_processing_config` | object | 否 | 音视频解析处理配置。 |
| `processing.media_processing_config.enable_diarization` | boolean | 否 | 是否进行人声分离。 |
| `processing.media_processing_config.enable_synopsis_parse` | boolean | 否 | 是否进行剧情解析。 |
| `processing.media_processing_config.enable_synopsis_segments` | boolean | 否 | 是否生成剧情解析段落。 |
| `processing.media_processing_config.enable_synopsis_summary` | boolean | 否 | 是否生成剧情解析摘要。 |
| `processing.media_processing_config.frame_extraction` | object | 否 | 抽帧配置。 |
| `processing.media_processing_config.frame_extraction.mode` | string | 否 | 抽帧模式。可选值：`auto`、`frame_rate` |
| `processing.media_processing_config.frame_extraction.frame_rate` | number | 否 | 抽帧帧率，范围为 `0.2`～`5` |
| `processing.media_processing_config.frame_extraction.output_image_width` | integer | 否 | 输出帧图像宽度。不指定时使用原始分辨率，取值范围 \[32, 4096\] |
| `processing.media_processing_config.frame_extraction.output_image_height` | integer | 否 | 输出帧图像高度。不指定时使用原始分辨率，取值范围 \[32, 4096\] |
| `output` | object | 否 | 输出配置。 |
| `output.output_file_format` | string\[\] | 否 | 输出格式字符串数组。可选值：`markdown` |
| `output.layout_table_format` | string | 否 | Markdown 中表格的输出格式。可选值：`markdown`、`html` |
| `output.oss_config` | object | 否 | OSS 输出配置。 |
| `output.oss_config.bucket` | string | 否 | 托管 OSS Bucket 名称。 |
| `output.oss_config.endpoint` | string | 否 | 托管 OSS Endpoint。 |
| `output.oss_config.access_key_id` | string | 否 | 托管 OSS AccessKey ID。 |
| `output.oss_config.access_key_secret` | string | 否 | 托管 OSS AccessKey Secret。 |
| `output.oss_config.security_token` | string | 否 | 托管 OSS Security Token。 |

> **说明**
>
> -   在线业务与离线业务：
>     -   在线业务：线上实时解析和返回任务，适合快速响应场景。
>     -   离线业务：一次提交多条子任务，适合可接受较长等待时间的场景。离线任务承诺提交后 7×24 小时内完成。
>     -   离线业务单次请求最多支持 200 条子任务，每个子任务独立计费。
>     -   在线业务和离线业务计费逻辑不同，详情参考[计费文档](../../../application-user-guide/agent-billing/pricing.md)。
> -   文件来源使用 `file_url` 或 `batch_job_url` 二选一：
>     -   `file_url` 非空时，`batch_job_url` 被忽略，走在线业务。
>     -   `file_url` 为空且 `batch_job_url` 非空时，`batch_job_url` 生效，走离线批量业务。
> -   `batch_job_url` 指向 JSON 数组格式的任务清单，每条为一个子任务，包含：
>     -   `file_url`：子任务文件 URL。
>     -   `file_name`：子任务文件名称。
>     -   `file_id`：自定义子任务 ID。
> -   处理定义使用 `config_id` 或内联 `processing`。离线业务的所有子任务共用一个配置，不支持单次请求内各子任务单独配置。

<a id="返回结果"></a>

## 返回结果

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `request_id` | string | 请求 ID |
| `data.biz_id` | string | 在线业务任务 ID，用于调用 `/parse/result` |
| `data.biz_id_list` | array | 离线业务任务 ID 清单 |
| `data.biz_id_list[].biz_id` | string | 离线业务子任务 ID，用于调用 `/parse/result`。如果识别失败，不会返回此字段。 |
| `data.biz_id_list[].file_id` | string | 离线业务自定义单个子任务 ID。 |
| `data.biz_id_list[].code` | string | 离线业务子任务错误码。如果识别成功，不会返回此字段。 |
| `data.biz_id_list[].message` | string | 离线业务子任务错误信息。如果识别成功，不会返回此字段。 |
| `data.biz_id_list[].status` | string | 离线业务子任务状态。`success` / `fail`，表示子任务提交是否成功。 |

<a id="文档解析代码示例"></a>

## 文档解析代码示例

以下示例分别展示两种处理定义， `config_id` 与 `processing` 同时存在时，`processing` 会优先生效。示例中的 URL、任务 ID 和配置 ID 均为脱敏占位值。

在线任务：

<a id="sec-tabs"></a>

<a id="使用已保存的配置"></a>

<a id="使用已保存的配置-h4"></a>

#### 使用已保存的配置

<a id="code-block"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "file_url": "https://example.com/document.pdf",
    "file_name": "document.pdf",
    "config_id": "config_xxx"
}'
```

<a id="code-block-2"></a>

```json
{
    "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": {
        "biz_id": "parseX-2026xxxx-xxxxxxx"
    }
}
```

<a id="使用内联配置"></a>

<a id="使用内联配置-h4"></a>

#### 使用内联配置

<a id="code-block-3"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "file_url": "https://example.com/document.pdf",
    "file_name": "document.pdf",
    "processing": {
        "doc_processing_config": {
            "page_index": "1-10",
            "head_foot": false,
            "layout_position": true
        }
    },
    "output": {
        "output_file_format": [
            "markdown"
        ],
        "layout_table_format": "markdown"
    }
}'
```

<a id="code-block-4"></a>

```json
{
    "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": {
        "biz_id": "parseX-2026xxxx-xxxxxxx"
    }
}
```

离线任务：

<a id="sec-tabs-2"></a>

<a id="使用已保存的配置-2"></a>

<a id="使用已保存的配置-2-h4"></a>

#### 使用已保存的配置

<a id="code-block-5"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "batch_job_url": "https://example.com/manifest.json",
    "config_id": "config_xxx"
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

<a id="使用内联配置-2"></a>

<a id="使用内联配置-2-h4"></a>

#### 使用内联配置

<a id="code-block-7"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "batch_job_url": "https://example.com/manifest.json",
    "processing": {
        "doc_processing_config": {
            "page_index": "1-10",
            "head_foot": false,
            "layout_position": true
        }
    },
    "output": {
        "output_file_format": [
            "markdown"
        ],
        "layout_table_format": "markdown"
    }
}'
```

<a id="code-block-8"></a>

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

<a id="音视频解析代码示例"></a>

## 音视频解析代码示例

<a id="sec-tabs-3"></a>

<a id="使用已保存的配置-3"></a>

<a id="使用已保存的配置-3-h4"></a>

#### 使用已保存的配置

<a id="code-block-9"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "file_url": "https://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/static/Wan3.0模型创意视频.mp4",
    "file_name": "test.mp4",
    "config_id": "config_xxx"
}'
```

<a id="code-block-10"></a>

```json
{
    "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": {
        "biz_id": "parseX-Video-2026xxxx-xxxxxxx"
    }
}
```

<a id="使用内联配置-3"></a>

<a id="使用内联配置-3-h4"></a>

#### 使用内联配置

<a id="code-block-11"></a>

```text
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/parse/submit' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "file_url": "https://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/static/Wan3.0模型创意视频.mp4",
    "file_name": "test.mp4",
    "processing": {
        "media_processing_config": {
            "enable_diarization": true,
            "enable_synopsis_parse": true,
            "enable_synopsis_segments": true,
            "enable_synopsis_summary": true,
            "frame_extraction": {
                "mode": "auto",
                "output_image_width": 1024,
                "output_image_height": 1024
            }
        }
    }
}'
```

<a id="code-block-12"></a>

```json
{
    "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": {
        "biz_id": "parseX-Video-2026xxxx-xxxxxxx"
    }
}
```

> **警告**
>
> 解析接口支持的格式和限制见[支持的文件与限制](../../../application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)。

> **重要**
>
> 提交后，使用[查询解析结果](parse-result.md)轮询任务状态并获取解析结果。
