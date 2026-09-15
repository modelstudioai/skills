# 暂停实例

暂停指定实例，保留文件系统与内存状态。再次连接实例时自动恢复。兼容 E2B 暂停实例协议，对应 SDK 的 pause()。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 接口

**POST** `/sandboxes/{sandboxID}/pause`

暂停指定实例，保留文件系统与内存状态。再次连接实例时自动恢复。兼容 E2B 暂停实例协议，对应 SDK 的 `pause()`。

## 路径参数

参数

必填

类型

说明

`sandboxID`

是

string

实例唯一 ID

## 请求示例

```
curl -X POST "$BASE_URL/sandboxes/sbx-xxx/pause" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

## 响应

暂停成功返回 204，无响应体。
