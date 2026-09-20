# HappyOyster-Acting-查询Travel产物 API参考

查询已完成 Acting Travel 的录制原片和三个合成变体。对外交付推荐使用 withInstructionAndWatermark。

## 适用范围

查询已完成 Acting Travel 的录制原片和三个合成变体。`withInstruction` 是用户过程指令的叠加版本；对外交付推荐使用 `withInstructionAndWatermark`。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：Travel 状态为 `completed`。原片 URL 可用是返回产物响应的前提。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-travel-status-api-reference.md)接口确认。
    
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

#### 查询Travel产物

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts?encryptedTravelId={encryptedTravelId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### Query 参数

**encryptedTravelId** `string` **（必选）**

状态为 `completed` 的 Acting 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-enter-travel-api-reference.md)接口返回。

#### 响应参数

#### 四路产物全部就绪

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

#### 合成仍在处理

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
-   `partial`：至少一个合成变体为 `ready`，但未全部就绪
-   `processing`：三个合成变体均不是 `ready`

只聚合三个合成变体，不包含 `original`。

**video** `object`

主线视频的四种固定变体。每项含 `url`、`status`、`resolution`、`durationSec`。

-   `original`：录制原片，优先返回可用的 720p 表示
-   `withWatermark`：仅水印合成版
-   `withInstruction`：用户过程指令叠加的合成版
-   `withInstructionAndWatermark`：用户过程指令叠加 + 水印合成版，推荐用于对外交付

**video.\*.url** `string`

下载 URL；`processing` 或 `unavailable` 时为 `null`。

**video.\*.status** `string`

单项状态：

-   `ready`：已就绪，`url` 可访问
-   `processing`：仍在合成，`url=null`
-   `unavailable`：合成失败或 URL 暂不可用，`url=null`

**video.\*.resolution** `string`

`original` 命中 720p 时为 `"720p"`；其它情况可能为 `null`。

**video.\*.durationSec** `integer`

统一解析得到的视频时长秒数；可解析时所有 `ready` 变体均填写该值，`processing` / `unavailable` 或时长暂不可解析时可为 `null`。

## 前置状态与调用注意事项

-   客户端可在 `composeStatus != ready` 时按受控间隔轮询。
-   `video.withInstruction` 是过程指令叠加版，不是无指令原片。
-   对外交付推荐读取 `video.withInstructionAndWatermark`；如业务只需要原片，可继续读取 `video.original.url`。
-   四个视频变体共用同一时长解析结果，因此同一次响应中已就绪且时长可解析的变体会返回一致的 `durationSec`。
-   使用 `TRAVEL_NO_STREAM_AUTO_END` 结束的 Travel 为 `failed`，不会生成可查询产物。
-   收到 `404000` 时不要一律展示为「尚未完成」：请先通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-travel-status-api-reference.md)或[查询Travel列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-travel-list-api-reference.md)读取 `status` 与 `errorCode`，`failed` 的 Travel 应展示失败原因。

##### 404000 场景

场景

接口行为

Travel 仍在进行中（`init` / `pending` / `running` / `paused`）

返回业务码 `404000`，`message` 为 `Video is still being generated, please try again once the process is complete`

Travel 已 `failed`

返回业务码 `404000`，`message` 为 `Experience failed and no video was produced (errorCode=<errorCode>): <errorMessage>`；失败为终态，不会再有成片

Travel 不存在、不归属或不是 Acting

返回业务码 `404000`

原片 URL 不可用

返回业务码 `404000`；原片是整个接口的硬门槛

原片已就绪、合成仍在处理

HTTP 200；对应合成项 `status=processing`、`url=null`

合成失败或 URL 暂不可用

HTTP 200；对应合成项 `status=unavailable`、`url=null`

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询Travel列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-travel-list-api-reference.md)：查看其它历史 Travel。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-end-travel-api-reference.md)：结束新的 Travel 后再来查询产物。
