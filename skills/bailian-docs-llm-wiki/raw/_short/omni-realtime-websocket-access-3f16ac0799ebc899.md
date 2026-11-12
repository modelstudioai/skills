# Qwen-Omni-Realtime WebSocket 接入

Qwen-Omni-Realtime WebSocket 接入

## 适用范围

本文面向 Qwen-Omni-Realtime。示例模型为 `qwen3.8-omni-flash-realtime`，`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 的配置参见事件参考。历史型号 `qwen3-omni-flash-realtime-2025-09-15` 的参数参见 [Python SDK](raw/_short/omni-realtime-python-sdk-0d3c931c58118ee5.md)。

-   使用所选地域和业务空间对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡域名：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
-   长期 API Key 保存在服务端，不放入浏览器或移动端应用。

## 地址与鉴权

通过查询参数 `model` 指定要调用的模型。

WebSocket`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime`

WebSocket`wss://WorkspaceId.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime`

`qwen3.8-omni-flash-realtime` 必须使用业务空间专属域名。旧型号可继续使用原域名：北京为 `wss://dashscope.aliyuncs.com`，新加坡为 `wss://dashscope-intl.aliyuncs.com`。详情参见 [Python SDK](raw/_short/omni-realtime-python-sdk-0d3c931c58118ee5.md)。

在 WebSocket 握手请求头中设置 `Authorization: Bearer <API_KEY>`。不要把长期 API Key 放入浏览器或移动端。

可选的 `user-agent` 请求头用于标识客户端。通用 WebSocket 接入资料还列有 `X-DashScope-WorkSpace`（业务空间 ID）和 `X-DashScope-DataInspection`（数据合规检查配置），这两个请求头按模型要求使用。

临时 API Key 的生成方式和权限说明参见[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 会话配置

建立连接并收到 `session.created` 后发送 `session.update`。收到 `session.updated` 确认后再发送输入；错误通过 `error` 事件处理。

以下示例对应 `qwen3.8-omni-flash-realtime`，其他版本使用各自事件参考中的配置，不混用字段层级。

```
{
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Tina",
    "turn_detection": {
      "type": "server_vad"
    }
  }
}
```

## 输入、结果与结束

音频通过 `input_audio_buffer.append` 发送；输入格式、提交条件和图像输入限制见[客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)。处理[服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)中的结果、状态和错误，不将连接建立视为业务请求已完成。

自动轮次与 Manual 模式、Function Calling 和 MCP 的时序见[交互流程](raw/_short/omni-realtime-interaction-process-144f8455755c1f0a.md)。接收完所需结果后关闭 WebSocket 连接。

## 错误处理

握手失败时，核对域名、地域、业务空间、API Key、模型名称及模型开通状态与权限。连接建立后，根据 `error` 事件定位问题，并参见[错误码](raw/model-api-reference/preparations/error-code.md)。保留事件 ID 便于排查，不以无响应判定协议不支持。

## SDK 与参考

-   [交互流程](raw/_short/omni-realtime-interaction-process-144f8455755c1f0a.md)
-   [Python SDK](raw/_short/omni-realtime-python-sdk-0d3c931c58118ee5.md)
-   [Java SDK](raw/_short/omni-realtime-java-sdk-5b43428f0b0df256.md)
