# 释放实例

释放指定实例，回收计算与网络资源。释放后实例不可恢复。兼容 E2B 释放实例协议，对应 SDK 的 kill()。

<a id="前提"></a>

<a id="h-sbxapi-delete-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../sandbox-api-overview.md)。

<a id="接口"></a>

<a id="h-sbxapi-delete-endpoint"></a>

## 接口

**DELETE** `/sandboxes/{sandboxID}`

释放指定实例，回收计算与网络资源。释放后实例不可恢复。兼容 E2B 释放实例协议，对应 SDK 的 `kill()`。

<a id="路径参数"></a>

<a id="h-sbxapi-delete-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `sandboxID` | 是 | string | 实例唯一 ID |

<a id="请求示例"></a>

<a id="h-sbxapi-delete-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X DELETE "$BASE_URL/sandboxes/sbx-xxx" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应"></a>

<a id="h-sbxapi-delete-resp"></a>

## 响应

释放成功返回 204，无响应体。
