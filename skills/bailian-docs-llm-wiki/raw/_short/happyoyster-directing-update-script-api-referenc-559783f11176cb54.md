# HappyOyster-Directing-剧本全量更新 API参考

在剧本模式 Travel 中提交完整的 45 个 turn，全量替换当前 Travel 的 acts。仅 creationModel=scriptlist 支持。

## 适用范围

在剧本模式（`creationModel=scriptlist`）Travel 中提交完整的 45 个 turn，全量替换当前 Travel 的 `acts`。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 的 `creationModel` 必须为 `scriptlist`，状态需为 `running` 或 `pending`。可通过[查询Travel状态](raw/_short/happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 剧本全量更新

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "scriptList": {
        "acts": [
            {
                "turn": 1,
                "content": "[character_1] wakes up and looks toward the door.",
                "cameraType": "Static",
                "shotSize": "Medium",
                "cut": "long-take"
            },
            {
                "turn": 2,
                "content": "[character_1] walks slowly across the dark room.",
                "cameraType": "Tracking",
                "shotSize": "Wide",
                "cut": "hard-cut"
            }
        ]
    },
    "userAgent": "your-client/1.2.0"
}'
```

> 示例中仅展示第 1、2 个 act 用于说明结构，**不可直接提交**。实际请求必须包含 turn 1–45 共 45 条，连续且不重复。

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### 请求体（Request Body）

**encryptedTravelId** `string` **（必选）**

要更新的 Directing 加密 Travel ID，`creationModel` 必须为 `scriptlist`。由[客户端进入房间](raw/_short/happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md)接口返回。

**scriptList** `object` **（必选）**

全量剧本容器。仅 `acts` 生效；即使包含 `subjects`、`synopsis`、`scene`、`style`、`speed`、`language`、`setting`、`soundtrack`、`prologue` 或 `videoTags`，这些字段也会被忽略，平台继续使用创建 World 时已保存的值。

**scriptList.acts** `array` **（必选）**

完整 act 列表。约束：

-   必须恰好 45 条
-   `turn` 必须覆盖 1–45，连续且不可重复
-   `content` 非空，单拍最长 2000 字；全部 `content` 合计最长 100000 字
-   `cameraType`（可选，默认 `Static`）、`shotSize`（可选 `Wide` / `Medium` / `Close-up`，默认 `Medium`）、`cut`（可选，默认 `long-take`）

本接口是全量替换，不支持只提交发生变化的 turn。

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`。

#### 响应参数

#### 更新已接受

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "accepted": true,
        "turnCount": 45
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

加密的 Travel ID。

**accepted** `boolean`

是否已接受完整剧本并进入处理流程。

**turnCount** `integer`

本次全量更新的 turn 数，固定为 `45`。

## 前置状态与调用注意事项

-   仅 `creationModel=scriptlist` 支持本接口；普通模式 Travel 误调用返回 `409000`。
-   Travel 状态必须为 `running` 或 `pending`。
-   `acts` 必须恰好 45 条；turn 必须为 1–45，连续且不可重复，否则返回 `400000`。
-   剧本内容未通过内容安全策略时返回 `403004`；触发版权或 IP 合规拒绝时返回 `403005`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

更新后：

-   [查询Travel状态](raw/_short/happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)：查看章节信息。
-   [暂停Travel](raw/_short/happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) / [回溯Travel](raw/_short/happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)。
-   [结束Travel](raw/_short/happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)：结束会话并处理产物。
