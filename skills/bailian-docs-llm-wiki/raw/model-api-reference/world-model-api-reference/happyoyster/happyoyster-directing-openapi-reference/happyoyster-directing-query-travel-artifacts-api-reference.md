# HappyOyster-Directing-查询Travel产物 API参考

查询已完成 Directing Travel 的录制原片和三个合成变体。原片可用是返回产物响应的前提；对外交付推荐使用 withInstructionAndWatermark。

## 适用范围

查询已完成 Directing Travel 的录制原片及三个合成版本。原片可用是返回产物响应的前提；合成版本可以仍在处理中。对外交付推荐使用 `withInstructionAndWatermark`。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：Travel 状态为 `completed`。原片可用是返回产物响应的前提。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)接口确认。
    
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

查询Travel产物

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts?encryptedTravelId={encryptedTravelId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### Query 参数

**encryptedTravelId** `string` **（必选）**

状态为 `completed` 的 Directing 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

#### 响应参数

四路产物全部就绪

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "composeStatus": "ready",
        "video": {
            "original": {
                "url": "https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_raw.mp4?v=2",
                "status": "ready",
                "resolution": "720p",
                "durationSec": 180
            },
            "withWatermark": {
                "url": "https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_wm.mp4?v=2",
                "status": "ready",
                "resolution": null,
                "durationSec": 180
            },
            "withInstruction": {
                "url": "https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_overlay.mp4?v=2",
                "status": "ready",
                "resolution": null,
                "durationSec": 180
            },
            "withInstructionAndWatermark": {
                "url": "https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_all.mp4?v=2",
                "status": "ready",
                "resolution": null,
                "durationSec": 180
            }
        }
    }
}
```

合成仍在处理

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "composeStatus": "processing",
        "video": {
            "original": {
                "url": "https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_raw.mp4?v=2",
                "status": "ready",
                "resolution": "720p",
                "durationSec": 180
            },
            "withWatermark": {
                "url": null,
                "status": "processing",
                "resolution": null,
                "durationSec": null
            },
            "withInstruction": {
                "url": null,
                "status": "processing",
                "resolution": null,
                "durationSec": null
            },
            "withInstructionAndWatermark": {
                "url": null,
                "status": "processing",
                "resolution": null,
                "durationSec": null
            }
        }
    }
}
```

**code** `integer`

返回码。`0` 表示成功，非 0 为错误码。

**message** `string`

错误信息。成功时为 `null`。

**data** `object`

响应数据。失败时为 `null`。

属性

**encryptedTravelId** `string`

加密 Travel ID。

**composeStatus** `string`

三个合成变体的聚合状态：

-   `ready`：`withWatermark`、`withInstruction`、`withInstructionAndWatermark` 均为 `ready`
-   `partial`：至少一个合成变体为 `ready`，但尚未全部就绪
-   `processing`：三个合成变体均非 `ready`

只聚合三个合成变体，不包含 `original`。

**video** `object`

四类主线视频产物，字段结构固定。每项含 `url`、`status`、`resolution`、`durationSec`。

-   `original`：录制原片，优先选择 720p
-   `withWatermark`：仅添加水印的合成版
-   `withInstruction`：仅添加用户指令字幕的合成版
-   `withInstructionAndWatermark`：用户指令字幕与水印合成版，推荐用于对外交付

**video.\*.url** `string`

视频 URL；`status=processing` 时为 `null`。

**video.\*.status** `string`

单项状态：

-   `ready`：该视频已就绪，URL 可访问
-   `processing`：正在处理；URL 为 `null`
-   `unavailable`：合成失败或 URL 暂不可用

**video.\*.resolution** `string`

原片命中 720p 时 `video.original.resolution` 为 `"720p"`；其它情况为 `null`。

**video.\*.durationSec** `integer`

统一解析得到的视频时长秒数；可解析时所有 `ready` 变体均填写该值，`processing` / `unavailable` 或时长暂不可解析时可为 `null`。

## 前置状态与调用注意事项

-   Travel 不是 `completed`、不存在、不归属或不是 Directing、原片不可用时，均返回 `404000`；原片可用是返回产物响应的前提。
-   需要全部合成版本时，可在 `composeStatus != ready` 时继续轮询。
-   `video.withInstructionAndWatermark` 是推荐的对外交付版本。
-   四个视频变体共用同一时长解析结果，因此同一次响应中已就绪且时长可解析的变体会返回一致的 `durationSec`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询Travel列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-list-api-reference.md)：查看其它历史 Travel。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-end-travel-api-reference.md)：结束新的 Travel 后再来查询产物。
