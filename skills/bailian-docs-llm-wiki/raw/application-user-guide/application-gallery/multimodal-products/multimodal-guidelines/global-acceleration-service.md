# 全球加速服务使用说明

通过全球加速域名接入多模态交互开发套件，可降低网络延迟和模型 API 调用失败率，提升用户体验。

计费详情请参见[产品计费](raw/application-user-guide/application-gallery/multimodal-products/product-billing.md)。

## 通过 API 接入

将百炼默认域名 `dashscope.aliyuncs.com` 替换为 `multimodal-dialog-esa.aliyuncs.com`。对应的调用地址如下：

-   WebSocket：`wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference`
-   HTTP：`https://multimodal-dialog-esa.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

## 通过 SDK 接入

### Java SDK

```
Constants.baseWebsocketApiUrl = "wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference";
```

### Python SDK

如需全局修改调用地址，请在初始化 SDK 前设置：

```
dashscope.base_websocket_api_url = "wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference"
```

如需仅对本次调用修改调用地址，请在创建 `MultiModalDialog` 对象时传入 `url`：

```
conversation = MultiModalDialog(
    app_id=your_app_id,
    workspace_id=your_workspace_id,
    url="wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference",
    request_params=request_params,
    multimodal_callback=self.callback,
    model=self.model,
)
```

### Android SDK

创建 `MultiModalDialog` 对象时，将全球加速地址传入 `url` 参数：

```
multiModalDialog = new MultiModalDialog(
    this,
    "wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference",
    authParams.getChainMode(),
    authParams.getWorkspaceId(),
    authParams.getAppid(),
    authParams.getDialogMode()
);
```

### iOS SDK

创建 `MultiModalDialog` 对象时，将全球加速地址传入 `url` 参数：

```
self.conversation = MultiModalDialog(
    url: "wss://multimodal-dialog-esa.aliyuncs.com/api-ws/v1/inference",
    chainMode: self.chain,
    workSpaceId: self.WORKSPACE_ID,
    appId: self.APP_ID,
    mode: mode
)
```

### RTOS SDK

请将 RTOS SDK 升级到 1.1.0 或更高版本，然后调用以下接口获取建立连接所需的参数：

```
#include "c_mmi.h"

char *wss_host = c_mmi_get_wss_host_global();
char *wss_port = c_mmi_get_wss_port();
char *wss_api = c_mmi_get_wss_api();
char *wss_header = c_mmi_get_wss_header();

// 建立 WebSocket 连接。dummy_wss_connect 接口需由用户自行实现。
WSS_HANDLE *wss = dummy_wss_connect(wss_host, wss_port, wss_api, wss_header);
```
