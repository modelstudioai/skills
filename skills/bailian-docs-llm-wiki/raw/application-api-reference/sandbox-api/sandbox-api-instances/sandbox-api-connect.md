# 连接实例

连接到已有实例，返回数据面访问所需的 token 与 domain 信息。兼容 E2B 连接实例协议，对应 SDK 的 connect()。

<a id="前提"></a>

<a id="h-sbxapi-connect-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../sandbox-api-overview.md)。

<a id="接口"></a>

<a id="h-sbxapi-connect-endpoint"></a>

## 接口

**POST** `/sandboxes/{sandboxID}/connect`

连接到已有实例，返回数据面访问所需的 token 与 domain 信息。兼容 E2B 连接实例协议，对应 SDK 的 `connect()`。

<a id="路径参数"></a>

<a id="h-sbxapi-connect-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `sandboxID` | 是 | string | 实例唯一 ID |

<a id="请求体"></a>

<a id="h-sbxapi-connect-req"></a>

## 请求体

请求体可选。

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `timeout` | 否 | integer | 连接后实例的超时时间，单位秒，取值范围 \[300,604800\] |

<a id="请求示例"></a>

<a id="h-sbxapi-connect-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X POST "$BASE_URL/sandboxes/sbx-xxx/connect" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"timeout": 3600}'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-sbxapi-connect-resp"></a>

## 响应示例

<a id="code-block-2"></a>

```json
{
  "sandboxID": "sbx-xxx",
  "templateID": "your-template-id",
  "envdVersion": "your-envd-version",
  "domain": "your-sandbox-domain",
  "envdAccessToken": "your-envd-access-token",
  "trafficAccessToken": "your-traffic-access-token",
  "envdUrl": "your-envd-url",
  "state": "running"
}
```

<a id="响应字段"></a>

<a id="h-sbxapi-connect-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sandboxID` | string | 实例唯一 ID |
| `templateID` | string | 模版 ID |
| `envdVersion` | string | envd 版本 |
| `domain` | string | 数据面访问域名 |
| `envdAccessToken` | string | envd 访问 token |
| `trafficAccessToken` | string | 流量访问 token |
| `envdUrl` | string | envd 访问地址 |
| `state` | string | 实例状态，例如 `running` |
