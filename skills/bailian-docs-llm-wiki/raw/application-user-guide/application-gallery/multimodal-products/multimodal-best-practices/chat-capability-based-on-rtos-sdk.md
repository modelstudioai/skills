# 基于RTOS SDK (License模式) 实现聊天能力

本文介绍如何基于RTOS SDK (License模式) 实现聊天能力。

## 1\. 开发准备

根据[应用创建](https://help.aliyun.com/zh/model-studio/multimodal-app-creation)的文档，创建应用，购买 license，获取 [APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和 AppSecret。

参考[RTOS C SDK（License模式）](https://help.aliyun.com/zh/model-studio/mmi-rtos-sdk)，根据芯片型号，下载相应的 SDK 包。

如采用半托管模式，需要根据[RTOS C SDK（License模式）](https://help.aliyun.com/zh/model-studio/mmi-rtos-sdk)，完成服务端相关接口对接。

## 2\. SDK 适配

**说明**

**本文档示例和日志中所有形如**`**<ID>**`**中的**`**ID**` **均为数据，文档中展示的为脱敏数据。**

不同芯片平台需要使用对应平台的toolchain进行编译，目前百炼已经支持的芯片清单，可直接下载SDK。

如果是新的芯片平台，请联系阿里云销售寻求技术支持。通过联系阿里云相关工作人员获得SDK，SDK包名称如下:

`aliyun_sdk_<PLATFORM>_<SDK_VERSION>.tar.xz`

### **2.1. SDK 目录结构说明**

获取的 SDK 目录结构如下

```
├── ReleaseNote.md
├── include
│   ├── c_utils
│   │   ├── c_utils.h
│   │   └── ...
│   ├── c_mmi.h
│   ├── lib_c_license.h
│   ├── lib_c_sdk.h
│   ├── libqwen_sdk.h
│   ├── qwen_test.h
│   └── ...
├── libs
│   ├── libc_license.a
│   ├── libc_mmi_cmd.a
│   ├── libhal_dummy.a
│   ├── libqwen_sdk.a
│   ├── libqwen_test.a
│   └── ...
└── third_party
    ├── cJSON
    │   ├── cJSON.h
    │   └── libcjson.a
    └── tinycrypt
        ├── include
        │   └── ...
        └── libtinycrypt.a
```

**说明：**

-   include目录下包含使用SDK所需要的头文件，需要将该目录添加至工程头文件目录下。
    
-   libqwen\_sdk.a包含SDK核心代码，必须加载。
    
-   libc\_license.a包含license模式相关代码，如使用license模式接入必须加载，如使用后付费模式接入不能加载该库。
    
-   libhal\_dummy.a包含dummy hal代码，用于SDK未适配前检查编译环境用，在完成hal移植后建议删除该库。
    
-   libqwen\_test.a包含测试代码，自动化测试过程需要加载该库，正式生产需要去除。
    
-   libtinycrypt.a包含加解密依赖接口，如果平台未集成该三方库则必须加载。
    
-   libcjson.a包含SDK相关依赖接口，如果平台未集成该三方库则必须加载。
    

### **2.2. SDK HAL 层适配**

SDK 包中如下列出的五个头文件中的函数声明，开发者必须根据自己的开发平台实现相关函数。

```
aliyun_sdk/include/c_utils/
    ├──hal_util_mem.h
    ├──hal_util_mutex.h
    ├──hal_util_random.h
    ├──hal_util_storage.h
    ├──hal_util_time.h
    └──...
```

以下函数需要开发者自行适配，不适配会导致 SDK无法正常工作。

需要实现的函数列表如下，具体函数说明请参考 SDK 包中对应头文件：

-   **内存模块（**`**aliyun_sdk/include/c_utils/hal_util_mem.h**`**）**
    

```
void * util_malloc(int32_t size);
void util_free(void *ptr);
```

-   **随机数模块（**`**aliyun_sdk/include/c_utils/hal_util_random.h**`**）**
    

```
int32_t util_random_init(uint32_t seed);
uint32_t util_random(void);
```

-   **存储模块（**`**aliyun_sdk/include/c_utils/hal_util_storage.h**`**）**
    

```
int32_t util_storage_erase(void);
int32_t util_storage_storage(uint8_t *data, uint32_t size);
int32_t util_storage_load(uint8_t *data, uint32_t size);
```

-   **时间模块（**`**aliyun_sdk/include/c_utils/hal_util_time.h**`**）**
    

```
void util_msleep(uint32_t ms);
int64_t util_get_timestamp_ms(void);
uint8_t util_timestamp_inited(void);
```

-   **互斥锁模块（**`**aliyun_sdk/include/c_utils/hal_util_mutex.h**`**）**
    

```
/* 互斥锁结构体定义 */
typedef struct _util_mutex_t {
    void *mutex_handle; /* 互斥锁句柄，具体实现依赖于平台 */
} util_mutex_t;

util_mutex_t * util_mutex_create(void);
void util_mutex_delete(util_mutex_t *mutex);
int32_t util_mutex_lock(util_mutex_t *mutex, int32_t timeout);
int32_t util_mutex_unlock(util_mutex_t *mutex);
```

### **2.3. HAL 层移植验收标准**

在实现以上各模块之后，加载`libsdk_test.a`，在主程序中直接调用函数`aliyun_sdk_test()`，就会对以上工作模块进行测试，输出日志可查看测试结果。

将输出日志反馈给阿里云进行确认。

测试成功的输出日志示例：

```
[UT][I][aliyun_sdk_test]********************* Hal Test Start *********************
[UT][I][aliyun_sdk_test]********************* memory test done *******************
[UT][I][aliyun_sdk_test]time is 1753344478377
[UT][I][aliyun_sdk_test]********************* time test done *********************
[UT][I][aliyun_sdk_test]********************* storage test done ******************
[UT][I][aliyun_sdk_test]********************* random test done *******************
[UT][I][aliyun_sdk_test]********************* mutex test done ********************
[UT][I][aliyun_sdk_test]********************* Hal Test End ***********************
```

## 3\. 设备初始化

在使用 SDK 前，需要通过阿里云百炼平台——[多模态控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app)，创建应用并获取 AppId 、API Key

-   license模式，还需要通过购买 license 获得对应的 AppSecret
    

初始化示例代码如下：（以 license全托管模式为例）

```
#include "c_mmi.h"
#include "lib_c_license.h"

int dummy_aliyun_sdk_init(void)
{
    // 初始化SDK
    c_mmi_sdk_init();

    if (c_license_device_is_registered() == 0) {
        c_mmi_storage_reset();
        // 预置AppId
        c_mmi_storage_set_app_id_str("Your AppId");
        // 预置AppSecret
        c_license_set_app_secret_str("Your AppSecret");
        // 预置DeviceName
        c_mmi_set_device_name("Your DeviceName");
        // 保存配置信息
        c_mmi_storage_save();
    }
    // 预置ApiKey，全托管模式必须配置ApiKey，半托管模式不需要
    // 设备每次开机后均需要重新配置api key
    c_mmi_storage_set_api_key("Your ApiKey");

    mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

    // 必须要配置evt_cb，否则会导致sdk运行异常
    mmi_config.evt_cb = _mmi_event_callback;		// 注册事件回调函数，详细说明见下文
    // 配置工作模式
    mmi_config.work_mode = C_MMI_MODE_PUSH2TALK;
    mmi_config.text_mode = C_MMI_TEXT_MODE_BOTH;
    // 配置上下行音频数据格式
    mmi_config.upstream_mode = C_MMI_STREAM_MODE_PCM;
    mmi_config.downstream_mode = C_MMI_STREAM_MODE_MP3;
    // 配置缓冲区大小
    mmi_config.recorder_rb_size = 8 * 1024;
    mmi_config.player_rb_size = 8 * 1024;

    c_mmi_config(&mmi_config);
    
    //... 其他代码
}
```

注：DeviceName 为每个设备唯一标识符，由开发者自定义，要求不超过 32 字符即可；建议采用 MAC 地址、IMEI 等设备唯一信息。

参考日志

```
[c_license_reset]ver[0x00010100][1.1.0] done
[UT][I][c_mmi_storage_save]stroage [176]
[UT][I][c_mmi_storage_save]ver[0x00010100][1.1.0] done
[UT][E][c_mmi_storage_init]reset done
[UT][W][c_mmi_sdk_init]license enable
[LICENSE][W][c_license_device_is_registered]load flag 0x00000000/0x0000001d
[LICENSE][I][c_license_reset]ver[0x00010100][1.1.0] done
[LICENSE][I][c_license_set_app_id_str]app_id    [Your AppId]
[LICENSE][I][c_license_set_app_secret_str]app_secret    [00000000000000000000000000000000]
[LICENSE][I][c_license_set_device_name]device_name      [Your DeviceName]
[UT][I][c_mmi_set_device_name]device_name [Your DeviceName]
[UT][D][_get_storage_path]path [/Users/lancelot/Desktop/code/esp32_v3/qwen_sdk/build_mac/device_data.bin]
[UT][I][c_mmi_storage_save]stroage [176]
[UT][I][c_mmi_storage_save]ver[0x00010100][1.1.0] done
[UT][I][c_mmi_storage_set_api_key]app_id    [Your ApiKey]
[UT][I][c_mmi_config]device_name [Your DeviceName]
[UT][I][c_mmi_config]load dialog_id []
[UT][I][c_mmi_config]done
[UT][I][c_mmi_config_print]>>>>>>>>>>> mmi config start <<<<<<<<<<<
[UT][I][c_mmi_config_print]device_name [Your DeviceName]
[UT][I][c_mmi_config_print]dialog_id []
[UT][I][c_mmi_config_print]event_callback [0x10264ee18]
[UT][I][c_mmi_config_print]work_mode [push2talk]
[UT][I][c_mmi_config_print]text_mode [transcript,dialog]
[UT][I][c_mmi_config_print]voice_id [longxiaochun_v2]
[UT][I][c_mmi_config_print]story_voice_id [longxiaochun_v2]
[UT][I][c_mmi_config_print]upstream_mode [pcm]
[UT][I][c_mmi_config_print]downstream_mode [mp3]
[UT][I][c_mmi_config_print]recorder_rb_size [8192]
[UT][I][c_mmi_config_print]player_rb_size [8192]
[UT][I][c_mmi_config_print]transmit_rate_limit [0]
[UT][I][c_mmi_config_print]enable_cbr [0]
[UT][I][c_mmi_config_print]frame_size [60]
[UT][I][c_mmi_config_print]bit_rate [32]
[UT][I][c_mmi_config_print]us_sample_rate [24000]
[UT][I][c_mmi_config_print]ds_sample_rate [24000]
[UT][I][c_mmi_config_print]vocabulary_id [NULL]
[UT][I][c_mmi_config_print]volume [50]
[UT][I][c_mmi_config_print]speech_rate [100]
[UT][I][c_mmi_config_print]pitch_rate [100]
[UT][I][c_mmi_config_print]>>>>>>>>>>> mmi config end <<<<<<<<<<<
```

## 4\. 设备侧网络通信构建

SDK使用中需要使用`HTTP`和`WEBSOCKET`协议，需要开发者实现相应收发流程，SDK 仅负责发送数据的封装和接收数据的解析。

### **4.1. HTTP 通信**

文档中将 http 通信相关功能简化为接收和发送两个函数，具体不同平台实现需要开发者自行适配，以下示例代码仅用于说明交互流程。

```
// http发送函数
int dummy_http_request(char* method, char* host, char* api, char *port, char* header, \
                         char* body, int(*rsp_async_cb)(char* rsp_data, int rsp_len));

// http接收函数,实现设备注册
int dummy_http_response_for_register(char* rsp_data, int rsp_len);

// http接收函数,实现获取Token
int dummy_http_response_for_token(char* rsp_data, int rsp_len);
```

#### **4.1.1. 设备注册**

设备注册示例代码如下：

```
int dummy_http_response_for_register(int status, char* rsp_data, int rsp_len)
{
    int err;

    // ... 客户其他业务逻辑

    // 解析并完成注册
    // SDK中的解析函数只需要报文中的data字段，如下http接收报文所示
    err = c_license_analyze_register_rsp(rsp_body_data);
    c_mmi_storage_save();
    
    // ... 客户其他业务逻辑

    return err;
}

int dummy_aliyun_sdk_init(void)
{
    // 初始化SDK
    c_mmi_sdk_init();

    if (c_license_device_is_registered() == 0) {
        c_mmi_storage_reset();
        // 预置AppId
        c_mmi_storage_set_app_id_str("Your AppId");
        // 预置AppSecret
        c_license_set_app_secret_str("Your AppSecret");
        // 预置DeviceName
        c_mmi_set_device_name("Your DeviceName");
        // 保存配置信息
        c_mmi_storage_save();
    }
    // 预置ApiKey，全托管模式必须配置ApiKey，半托管模式不需要
    // 设备每次开机后均需要重新配置api key
    c_mmi_storage_set_api_key("Your ApiKey");

    mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

    // 必须要配置evt_cb，否则会导致sdk运行异常
    mmi_config.evt_cb = _mmi_event_callback;		// 注册事件回调函数，详细说明见下文
    // 配置工作模式
    mmi_config.work_mode = C_MMI_MODE_PUSH2TALK;
    mmi_config.text_mode = C_MMI_TEXT_MODE_BOTH;
    // 配置上下行音频数据格式
    mmi_config.upstream_mode = C_MMI_STREAM_MODE_PCM;
    mmi_config.downstream_mode = C_MMI_STREAM_MODE_MP3;
    // 配置缓冲区大小
    mmi_config.recorder_rb_size = 8 * 1024;
    mmi_config.player_rb_size = 8 * 1024;

    c_mmi_config(&mmi_config);
    
    // 设备注册
    if (c_license_device_is_registered() == 0) {
        char time_ms_str[C_UTIL_TIMESTAMP_MS_LEN + 1];
        snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
        // 根据当前时间戳timestamp_str（毫秒），生成注册信息字串req
        c_device_gen_register_req(req, timestamp_str);
        // 获取服务端返回设备信息
        dummy_http_request(METHOD, HOST, API, PORT, HEADER, req, dummy_http_response_for_register);
    }

    //... 其他代码，完整示例见下文
}
```

上述代码中：

-   如采用半托管模式，http 通信的参数根据开发者`**自行开发的服务端**`注册接口进行配置
    
-   如采用全托管模式，http 通信参数由阿里云提供，接入信息如下：
    
    Host: bailian.multimodalagent.aliyuncs.com
    
    Register API: /api/device/v1/register
    

* * *

**示例数据**

设备端SDK生成的请求数据包示例，如下是http请求报文中body字段

```
{
    "appId": "Your AppId",
    "deviceName": "Your DeviceName",
    "nonce": "Nonce",
    "requestTime": "Time",
    "sdkVersion": "1.1.0",
    "signature": "Signature"
}
```

设备端解析的注册信息数据包示例，如下是http回应报文中data字段

```
{
    "appId": "Your AppId",
    "deviceName": "Your DeviceName",
    "nonce": "Nonce",
    "requestTime": "Time",
    "sdkVersion": "1.1.0",
    "signature": "Signature"
}
```

**注意：调用c\_license\_analyze\_register\_rsp时，入参数据必须与示例数据格式保持一致**

调试日志如下：

```
[LICENSE][I][c_license_gen_register_str]req_str [356][{"appId":"mm_Your AppId","deviceName":"Your DeviceName","nonce":"Nonce","requestTime":"Time","sdkVersion":"1.1.0","signature":"Signature"}]
[LICENSE][I][c_license_analyze_register_rsp]rsp_str [376][{"nonce":"Nonce","responseTime":"Time","appId":"mm_Your AppId","deviceName":"Your DeviceName","signature":"Signature"}]
[LICENSE][I][c_license_analyze_register_rsp]nonce       [Nonce]
```

完整的 http 发送报文如下所示：

```
POST /api/device/v1/register HTTP/1.1
Host: bailian.multimodalagent.aliyuncs.com
Accept: */*
Content-Type: application/json
Content-Length: 356

{"appId":"Your AppId","deviceName":"Your DeviceName","nonce":"Nonce","requestTime":"Time","sdkVersion":"1.1.0","signature":"Signature"}
```

完整的 http 接收报文如下所示：

```
HTTP/1.1 200 OK
content-type: application/json
date: Wed, 07 Jan 2026 11:38:25 GMT
req-cost-time: 28
req-arrive-time: 1767785905379
resp-start-time: 1767785905407
x-envoy-upstream-service-time: 27
server: istio-envoy
x-request-id: efa2b37a-4acc-473d-8d86-bfc87ad52821
transfer-encoding: chunked

1ea
{"code":200,"success":true,"message":"success","localizedMsg":null,"data":{"nonce":"Nonce","responseTime":"Time","appId":"Your AppId","deviceName":"Your DeviceName","signature":"Signature"}
0
```

#### **4.1.2. 设备登录**

设备**每次**在连接阿里云多模态交互 AI 应用前，需要先获取 token 才能进行连接，获取 token示例代码如下：

```
int dummy_http_response_for_token(int status, char* rsp_data, int rsp_len)
{
    int err;

    // ... 客户其他业务逻辑

    // 解析并获取token，数据要求同上
    err = c_license_analyze_get_token_rsp(rsp_data);
    
    // ... 客户其他业务逻辑

    return err;
}

int dummy_aliyun_sdk_init(void)
{
    // 初始化SDK
    c_mmi_sdk_init();

    if (c_license_device_is_registered() == 0) {
        c_mmi_storage_reset();
        // 预置AppId
        c_mmi_storage_set_app_id_str("Your AppId");
        // 预置AppSecret
        c_license_set_app_secret_str("Your AppSecret");
        // 预置DeviceName
        c_mmi_set_device_name("Your DeviceName");
        // 保存配置信息
        c_mmi_storage_save();
    }
    // 预置ApiKey，全托管模式必须配置ApiKey，半托管模式不需要
    // 设备每次开机后均需要重新配置api key
    c_mmi_storage_set_api_key("Your ApiKey");

    mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

    // 必须要配置evt_cb，否则会导致sdk运行异常
    mmi_config.evt_cb = _mmi_event_callback;		// 注册事件回调函数，详细说明见下文
    // 配置工作模式
    mmi_config.work_mode = C_MMI_MODE_PUSH2TALK;
    mmi_config.text_mode = C_MMI_TEXT_MODE_BOTH;
    // 配置上下行音频数据格式
    mmi_config.upstream_mode = C_MMI_STREAM_MODE_PCM;
    mmi_config.downstream_mode = C_MMI_STREAM_MODE_MP3;
    // 配置缓冲区大小
    mmi_config.recorder_rb_size = 8 * 1024;
    mmi_config.player_rb_size = 8 * 1024;

    c_mmi_config(&mmi_config);
    
    // 设备注册
    if (c_license_device_is_registered() == 0) {
        char time_ms_str[C_UTIL_TIMESTAMP_MS_LEN + 1];
        snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
        // 根据当前时间戳timestamp_str（毫秒），生成注册信息字串req
        c_device_gen_register_req(req, timestamp_str);
        // 获取服务端返回设备信息
        dummy_http_request(METHOD, HOST, API, PORT, HEADER, req, dummy_http_response_for_register);
    }

    // 设备登录
    if (c_license_is_token_expire() == 0) {
        char time_ms_str[C_UTIL_TIMESTAMP_MS_LEN + 1];
        char api_key[C_MMI_API_KEY_LEN + 1] = { 0 };
        int32_t ret;

        snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
        // 根据当前时间戳timestamp_str（毫秒），生成登录信息字串req
        ret = c_mmi_storage_get_api_key(api_key);
        if (ret == UTIL_SUCCESS) {
            c_license_gen_get_token_str(req_str, sizeof(req_str), time_ms_str, api_key);
        } else {
            c_license_gen_get_token_str(req_str, sizeof(req_str), time_ms_str, NULL);
        }
        // 获取服务端返回登录信息
        dummy_http_request(METHOD, HOST, API, PORT, HEADER, req_str, dummy_http_response_for_token);
    }

    //... 其他代码，完整示例见下文
}
```

上述代码中：

-   如采用半托管模式，http 通信的参数根据开发者`**自行开发的服务端**`设备登录（getToken）进行配置
    
-   如采用全托管模式，http 通信参数由阿里云提供，，接入信息如下：
    
    Host: bailian.multimodalagent.aliyuncs.com
    
    Register API: /api/token/v1/getToken
    

* * *

#### **4.1.3. 示例数据**

设备端SDK生成的请求数据包示例，如下是http请求报文中body字段

```
{
    "appId": "Your AppId",
    "deviceName": "Your DeviceName",
    "nonce": "Nonce",
    "requestTime": "Time",
    "sdkVersion": "1.1.0",
    "tokenType": "MMI",
    "signature": "Signature"
}
```

设备端解析的注册信息数据包示例,，如下是http回应报文中data字段

```
{
    "nonce": "Nonce",
    "responseTime": "Time",
    "appId": "Your AppId",
    "deviceName": "Your DeviceName",
    "requestIp": "Your IP",
    "signature": "Signature"
}
```

**注意：调用c\_license\_analyze\_get\_token\_rsp时，入参数据必须与示例数据格式保持一致。**

调试日志如下：

```
[LICENSE][I][_gen_get_token_str]plaintext [201][{"apiKey":"Your ApiKey","appId":"Your AppId","deviceName":"Your DeviceName","payMode":"LICENSE","requestTime":"Time","sdkVersion":"1.1.0","tokenType":"MMI"}]
[LICENSE][I][_gen_get_token_str]req_str [462][{"appId":"Your AppId","deviceName":"Your DeviceName","nonce":"Nonce","requestTime":"Time","sdkVersion":"1.1.0","tokenType":"MMI","signature":"Signature"}]
[LICENSE][I][c_license_analyze_get_token_rsp]rsp_str [603][{"nonce":"Nonce","responseTime":"Time","appId":"Your AppId","deviceName":"Your DeviceName","requestIp":"Your IP","signature":"Signature"}]
[LICENSE][I][c_license_analyze_get_token_rsp]nonce      [Nonce]
```

完整的 http 发送报文如下所示：

```
POST /api/token/v1/getToken HTTP/1.1
Host: bailian.multimodalagent.aliyuncs.com
Accept: */*
Content-Type: application/json
Content-Length: 462

{"appId":"Your AppId","deviceName":"Your DeviceName","nonce":"Nonce","requestTime":"Time","sdkVersion":"1.1.0","tokenType":"MMI","signature":"Signature"}
```

完整的 http 接收报文如下所示：

```
HTTP/1.1 200 OK
content-type: application/json
date: Wed, 07 Jan 2026 11:38:24 GMT
req-cost-time: 54
req-arrive-time: 1767785905624
resp-start-time: 1767785905678
x-envoy-upstream-service-time: 39
server: istio-envoy
x-request-id: da621d59-5911-44ac-a7be-0e5977de40a3
transfer-encoding: chunked

2cd
{"code":200,"success":true,"message":"success","localizedMsg":null,"data":{"nonce":"Nonce","responseTime":"Time","appId":"Your AppId","deviceName":"Your DeviceName","requestIp":"Your IP","signature":"Signature"},"requestId":"RequestId"}
0
```

### **4.2. WEBSOCKET 通信**

在完成设备登录功能对接后，开始进行 websocket 通信调试。

阿里云百炼多模态交互 SDK 仅进行 websocket 数据的处理，不负责数据的收发动作；建议开发者创建相应的 websocket 数据收发线程以实现 websocket 数据的接收与发送；本文档示例代码按该交互方式进行说明。

websocket 示例代码

```
// 进行websocket连接
int dummy_wss_connect(char* host, char* port, char* api, char* header);

// 开启websocket收发线程
int dummy_wss_thread_start(void* params);

// 实际执行的websocket发送函数
int dummy_wss_send(int data_type, char* payload_data, int size);

// 实际执行的websocket接收函数
int dummy_wss_recv(int* opcode, char* payload_data, int* recv_size);

// 此函数基于websocket协议异步发送数据
int dummy_wss_task_send(void);

// 此函数基于websocket协议异步接收数据
int dummy_wss_task_recv(void);
```

#### **4.2.1. 建立 websocket 连接**

以下示例代码描述了如何建立 websocket连接，SDK会提供host、port、api以及header字段，其余字段需要开发者自己填充打包并完成发送流程。

```
int dummy_wss_init(void)
{ 
    // 建立websocket连接，获取连接字段
    char *wss_host = c_mmi_get_wss_host();
    char *wss_port = c_mmi_get_wss_port();
    char *wss_api = c_mmi_get_wss_api();
    char *wss_header = c_mmi_get_wss_header();

    UTIL_LOG_I("work");
    // 建立wss连接
    int ret = dummy_wss_connect(wss_host, wss_port, wss_api, wss_header);
    
    return ret;

}
```

注意，本 SDK 与云端的 websocket 通信需要建立 TLS 隧道，需要做如下配置：

-   TLS 版本要求 TLS1.2 或以上
    
-   开启 SNI（SERVER NAME INDICATION）
    
-   配置 CA 证书（[GlobalSign Root CA - R3](https://secure.globalsign.net/cacert/Root-R3.crt)）（也可至GlobalSign官网下载）
    

* * *

websocket建立连接时upgrade请求报文示例

```
GET <WSS API> HTTP/1.1
Host: <WSS HOST>
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: FhVlQeR4S1N06+1/SU79XA== 
Sec-WebSocket-Version: 13
<WSS HEADER>
```

websocket建立连接时回应报文示例

```
HTTP/1.1 101 Switching Protocols
upgrade: websocket
connection: upgrade
sec-websocket-accept: sqchBdVDX8kKBgi90/PFl5+/4VI=
date: Thu, 24 Jul 2025 08:25:24 GMT
server: istio-envoy
```

**日志示例**

```
[UT][I][dummy_wss_init]work
[UT][I][dummy_wss_connect]wss update
[UT][I][dummy_wss_connect]request[239][GET <wss_api> HTTP/1.1
Host: <WSS HOST>
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: FhVlQeR4S1N06+1/SU79XA==
Sec-WebSocket-Version: 13
<WSS HEADER>

]
[UT][I][dummy_wss_connect]Reading response...
[UT][I][dummy_wss_connect]response[MMI][187][HTTP/1.1 101 Switching Protocols
upgrade: websocket
connection: upgrade
sec-websocket-accept: sqchBdVDX8kKBgi90/PFl5+/4VI=
date: Thu, 24 Jul 2025 08:25:24 GMT
server: istio-envoy

]
[UT][I][dummy_wss_connect][MMI]done
```

**正确建立 websocket 后，可以观察平台相应的日志，正确场景下该连接会保持 1 分钟，后被服务端主动断开。**

#### **4.2.2. websocket 数据交互**

**使用阿里云百炼多模态交互 SDK 时 ，所有通过 websocket 进行交互的数据均需通过 SDK 进行处理，否则可能导致不可预知的问题。**

以下示例代码描述了如何通过创建线程实现 websocket 数据交互。

```
int dummy_wss_task_recv(void)
{
    int opcode;
    char data[8 * 1024];
    int recv_size;

    while(1) {
        // 通过websocket接收服务端下行数据
        dummy_wss_recv(&opcode, data, &recv_size);
        if(recv_size) {
            // 将接收服务端下行数据送入SDK进行解析
            c_mmi_analyze_recv_data(opcode, _data, recv_size);
        } else {
            util_msleep(10);
        }
    }
    return 0;
}

int dummy_wss_task_send(void)
{
    uint8_t opcode;
    uint8_t data[8 * 1024];
    uint32_t size;

    while(1) {
        // 从SDK获取打包好的payload数据
        size = c_mmi_get_send_data(&opcode, data, sizeof(payload_data));
        if (size == 0) {
            util_msleep(10);
        } else {
            // 将payload数据传入websocket发送函数，自行打包帧头进行发送
            dummy_wss_send(opcode, data, size);
        }
    }
    return 0;
}
```

注意事项：

-   websocket 接收的**data** 大小根据下行的数据格式不同，建议值如下：
    
    -   下行 PCM 格式数据时，建议**data** 大小设置为 8K 及以上。
        
    -   下行 MP3 格式数据时，建议**data** 大小设置为 8K 及以上。
        
    -   下行 opus 格式数据时，建议**data** 大小设置为 4K 及以上。
        
-   websocket 发送的**data** 大小不得低于 1.5K
    
-   调用`c_mmi_analyze_recv_data`或`c_mmi_get_send_data`函数时，`opcode` 为`WS_DATA_TYPE_TEXT` 或`WS_DATA_TYPE_BINARY` ，该值在 SDK 头文件中定义；开发者需要参考具体平台的定义实现及 websocket 协议，理解该值。
    

当完成数据对接后，可以看到如下日志

```
[UT][I][dummy_wss_thread_start][dummy_wss_task_send] send task [0x135e27180]
[UT][I][dummy_wss_thread_start][dummy_wss_task_recv] recv task [0x135e271a0]
[UT][I][_gen_cmd_start]task_id [<TASK ID>]
[UT][I][_send_cmd_start]send [run-task] [0-2] [0]
[UT][D][c_mmi_analyze_recv_data]recv[109][{"header":{"task_id":"<TASK ID>","event":"task-started","attributes":{}},"payload":{}}]
[UT][I][c_mmi_analyze_recv_data]recv [task-started] [0-2]
[UT][D][c_mmi_analyze_recv_data]recv[192][{"header":{"task_id":"<TASK ID>","event":"result-generated","attributes":{}},"payload":{"output":{"event":"Started","dialog_id":"<DIALOG_ID>"}}}]
[UT][I][_on_payload_event_start]recv [Started] [0-3]
[UT][D][c_mmi_analyze_recv_data]recv[223][{"header":{"task_id":"<TASK ID>","event":"result-generated","attributes":{}},"payload":{"output":{"event":"DialogStateChanged","state":"Listening","dialog_id":"<DIALOG_ID>"}}}]
[UT][I][_on_payload_event_state_change]recv [Listening] [0-4]
```

## 5\. 语音交互流程开发

### **5.1. 音频数据接口**

音频数据接口主要包含麦克风和播放器的实现函数，需要开发者自行实现。

以下代码仅作演示，实现和业务逻辑仅供参考。

```
//当recorder start后，麦克风开始异步获取数据
int dummy_recorder_async_callback(void);
// 启动麦克风录音
int dummy_recorder_start(void);
// 停止麦克风录音
int dummy_recorder_stop(void);
// 从硬件麦克风获取数据
int dummy_hw_recorder_get_data(uint8_t* data, uint32_t size);
// 获取麦克风工作状态
int dummy_recoder_is_work(void);

// 当player start后，播放器开始异步播放音频
int dummy_player_async_callback(void);
// 启动喇叭播放音频
int dummy_player_start(void);
// 停止喇叭播放音频
int dummy_player_stop(void);
// 将数据放入喇叭硬件进行播放
int dummy_hw_player_put_data(uint8_t* data, uint32_t size);
// 获取喇叭工作状态
int dummy_palyer_is_work(void);
```

本文档使用多线程实现喇叭播放与麦克风录音，因此构建以下示例

```
void dummy_recorder_task(void)
{
    uint32_t send_size =0;
    uint32_t size = 640;
    uint8_t* data = (uint8_t*) util_malloc(size);

    while(1) {
        if(dummy_recoder_is_work()) {
            send_size = dummy_hw_recorder_get_data(data, size);
            if(send_size){
                // 将音频采集硬件采集到的数据输出至SDK ringbuffer
                c_mmi_put_recorder_data(data, send_size);
            } else {
                util_msleep(10);
            }
        
        } else {
            util_msleep(10);
        }
    }
}

void dummy_player_task(void)
{
    uint8_t data[640];
    uint32_t size = 640;
    uint32_t recv_size = 0;

    while(1) {
        if (dummy_player_is_work()) {
            recv_size = c_mmi_get_player_data(data, size);
            if(recv_size){
                // 将SDK ringbuffer中的音频数据输出给到播放器进行播放
                dummy_hw_player_put_data(data, size)
            } else {
                util_msleep(10);
            }
        } else {
            util_msleep(10);
        }
    }
}
```

### **5.2. 按键接口**

本文档示例为 PUSH TO TALK，因此需要有按键按下和按键抬起两个事件的捕捉，本文档采用事件回调形式实现，此处只给出回调函数，具体逻辑与实现需要开发者自行实现。

以下代码仅做演示：

```
// 按键抬起时触发
int dummy_button_up(void);
// 按键按下时触发
int dummy_button_down(void);
```

示例实现与调用如下所示：

```
int dummy_button_up(void)
{
    // 关闭麦克风
    dummy_recorder_stop();
    // 通知云端服务开始处理音频数据
    c_mmi_stop_speech();

    return 0;
}

int dummy_button_down(void)
{
    // 关闭喇叭
    dummy_player_stop();
    // 通知云端即将开始发送音频数据，SDK会根据云端对该指令的响应触发C_MMI_EVENT_SPEECH_START
    c_mmi_start_speech();

    return 0;
}
```

### **5.3. 事件回调**

阿里云百炼多模态交互 SDK 语音交互相关的事件回调如下：

```
enum {
    C_MMI_EVENT_USER_CONFIG,        // 用户对于sdk的配置应该在该事件回调中实现，如音频缓冲区大小、工作模式、音色等
    C_MMI_EVENT_DATA_INIT,	        // 当SDK完成初始化后触发该事件，可在该事件回调中开始建立业务连接
    C_MMI_EVENT_SPEECH_READY,	    // 当正确建立WSS连接后触发该事件，在push和tap模式下仅在该事件后才可以调用speech start
    C_MMI_EVENT_SPEECH_PREPARE,     // 当SDK已准备好可以开始新一轮对话时触发此事件
    C_MMI_EVENT_SPEECH_START,       // 当SDK开始进行音频上行时触发此事件
    C_MMI_EVENT_SPEECH_RESTART,     // 当SDK重新开始进行音频上行时触发此事件
    C_MMI_EVENT_DATA_DEINIT,	    // 当SDK注销后触发此事件

    C_MMI_EVENT_ASR_START,	        // 当ASR开始返回数据时触发此事件
    C_MMI_EVENT_ASR_INCOMPLETE,	    // 此事件返回尚未完成ASR的文本数据（全量）
    C_MMI_EVENT_ASR_COMPLETE,	    // 此事件返回完成ASR的全部文本数据（全量）
    C_MMI_EVENT_ASR_END,		    // 当ASR结束时触发此事件

    C_MMI_EVENT_LLM_INCOMPLETE,	    // 此事件返回尚未处理完成的LLM文本数据（全量）
    C_MMI_EVENT_LLM_COMPLETE,	    // 此事件返回处理完成的LLM全部文本数据（全量）

    C_MMI_EVENT_TTS_START,	        // 当开始音频下行时触发此事件
    C_MMI_EVENT_TTS_END,	        // 当音频完成下行时触发此事件

    C_MMI_EVENT_HEARTBEAT,	        // 当SDK收到云端心跳回复时触发此事件
};
```

参考示例代码如下：

```
int _mmi_event_callback(uint32_t event, void *param)
{
    char *text;

    text = param;
    switch (event) {
        case C_MMI_EVENT_USER_CONFIG:
            // 开始新对话
            c_mmi_reset_dialog_id();
            break;
        case C_MMI_EVENT_DATA_INIT:
            // Mmi data ready, 开始网络连接
            dummy_wss_init();
            break;
        case C_MMI_EVENT_DATA_DEINIT:
            UTIL_LOG_W("will disconnect");
            break;
        case C_MMI_EVENT_SPEECH_START:
            UTIL_LOG_D("enable recorder when send speech");
            dummy_player_stop();
            dummy_recorder_start();
            break;
        case C_MMI_EVENT_ASR_START:
            UTIL_LOG_I("event [C_MMI_EVENT_ASR_START]");
            break;
        case C_MMI_EVENT_ASR_INCOMPLETE:
            UTIL_LOG_D("ASR [%s]", text);
            break;
        case C_MMI_EVENT_ASR_COMPLETE:
            if (text) {
                UTIL_LOG_D("ASR C [%s]", text);
            } else {
                UTIL_LOG_D("ASR C [NULL]");
            }
            break;
        case C_MMI_EVENT_ASR_END:
            UTIL_LOG_D("disable record when ASR complete");
            dummy_recorder_stop();
            break;
        case C_MMI_EVENT_LLM_INCOMPLETE:
            UTIL_LOG_D("LLM [%s]", text);
            break;
        case C_MMI_EVENT_LLM_COMPLETE:
            UTIL_LOG_D("LLM C [%s]", text);
            break;
        case C_MMI_EVENT_TTS_START:
            UTIL_LOG_I("enable player when dialog start");
            dummy_player_start();
            break;
        case C_MMI_EVENT_TTS_END:
            break;
        default:
            break;
    }

    return UTIL_SUCCESS;
}
```

示例日志如下

```
[UT][I][_on_payload_event_state_change]recv [Listening] [0-4]
[UT][D][dummy_button_down]
[UT][I][dummy_player_stop]
[UT][I][_send_cmd_req2spk]ready to send [1-4]
[UT][I][_send_cmd_speech]send [SendSpeech] [1-5] [0]
[UT][D][dummy_mmi_event_callback]enable recorder when send speech
[UT][I][dummy_recorder_start]
[UT][I][_on_payload_event_speech_start]recv [SpeechStarted][ASR Start] [1-5]
[UT][I][dummy_mmi_event_callback]event [C_MMI_EVENT_ASR_START]
[UT][D][dummy_button_up]
[UT][I][dummy_recorder_stop]
[UT][I][_send_cmd_stop_speech]send [StopSpeech] [1-5] [0]
[UT][I][_on_payload_event_speech_content]recv [SpeechContent][ASR Text] [1-5]
[UT][D][dummy_mmi_event_callback]ASR C [今天天气怎么样？]
[UT][I][_on_payload_event_speech_end]recv [SpeechEnded][ASR End] [1-6]
[UT][D][dummy_mmi_event_callback]disable record when ASR complete
[UT][I][dummy_recorder_stop]
[UT][I][_on_payload_event_state_change]recv [Thinking] [1-7]
[UT][D][_on_payload_event_state_change]prepare player rb
[UT][I][_on_payload_event_state_change]recv [Responding][Audio Start] [1-8]
[UT][I][dummy_mmi_event_callback]enable player when dialog start
[UT][I][dummy_player_start]
[UT][I][_on_payload_event_respond_start]recv [RespondingStarted][Audio Start] [1-8]
[UT][I][_on_payload_event_respond_content]recv [RespondingContent][LLM Text] [1-8]
[UT][D][dummy_mmi_event_callback]LLM C [今天上海市天气多云，白天最高气温33℃，夜间有小雨，气温27℃。东风吹，风力1-3级。]
[UT][I][_on_payload_event_respond_end]recv [RespondingEnded][Audio End] [1-9]
[UT][D][_on_payload_event_respond_end]recv audio data size [371200]
```

## 6\. SDK 完整构建流程

### **6.1. 完整示例代码**

示例代码如下

```
#include "lib_c_license.h"
#include "lib_c_mmi.h"

#define C_SDK_REQ_LEN_REGISTER	500
char req[C_SDK_REQ_LEN_REGISTER];

int dummy_http_response_for_register(int status, char* rsp_data, int rsp_len)
{
    int err;

    // ... 客户其他业务逻辑

    // 解析并完成注册
    // SDK中的解析函数只需要报文中的data字段，如下http接收报文所示
    err = c_license_analyze_register_rsp(rsp_body_data);
    c_mmi_storage_save();
    
    // ... 客户其他业务逻辑

    return err;
}

int dummy_http_response_for_token(int status, char* rsp_data, int rsp_len)
{
    int err;

    // ... 客户其他业务逻辑

    // 解析并获取token，数据要求同上
    err = c_license_analyze_get_token_rsp(rsp_data);
    
    // ... 客户其他业务逻辑

    return err;
}

int dummy_aliyun_sdk_init(void)
{
    // 初始化SDK
    c_mmi_sdk_init();

    if (c_license_device_is_registered() == 0) {
        c_mmi_storage_reset();
        // 预置AppId
        c_mmi_storage_set_app_id_str("Your AppId");
        // 预置AppSecret
        c_license_set_app_secret_str("Your AppSecret");
        // 预置DeviceName
        c_mmi_set_device_name("Your DeviceName");
        // 保存配置信息
        c_mmi_storage_save();
    }
    // 预置ApiKey，全托管模式必须配置ApiKey，半托管模式不需要
    // 设备每次开机后均需要重新配置api key
    c_mmi_storage_set_api_key("Your ApiKey");

    mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

    // 必须要配置evt_cb，否则会导致sdk运行异常
    mmi_config.evt_cb = _mmi_event_callback;    // 注册事件回调函数，详细说明见下文
    // 配置工作模式
    mmi_config.work_mode = C_MMI_MODE_PUSH2TALK;
    mmi_config.text_mode = C_MMI_TEXT_MODE_BOTH;
    // 配置上下行音频数据格式
    mmi_config.upstream_mode = C_MMI_STREAM_MODE_PCM;
    mmi_config.downstream_mode = C_MMI_STREAM_MODE_MP3;
    // 配置缓冲区大小
    mmi_config.recorder_rb_size = 8 * 1024;
    mmi_config.player_rb_size = 8 * 1024;

    c_mmi_config(&mmi_config);
    
    // 设备注册
    if (c_license_device_is_registered() == 0) {
        char time_ms_str[C_UTIL_TIMESTAMP_MS_LEN + 1];
        snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
        // 根据当前时间戳timestamp_str（毫秒），生成注册信息字串req
        c_device_gen_register_req(req, timestamp_str);
        // 获取服务端返回设备信息
        dummy_http_request(METHOD, HOST, API, PORT, HEADER, req, dummy_http_response_for_register);
    }

    // 设备登录
    if (c_license_is_token_expire() == 0) {
        char time_ms_str[C_UTIL_TIMESTAMP_MS_LEN + 1];
        char api_key[C_MMI_API_KEY_LEN + 1] = { 0 };
        int32_t ret;

        snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
        // 根据当前时间戳timestamp_str（毫秒），生成登录信息字串req
        ret = c_mmi_storage_get_api_key(api_key);
        if (ret == UTIL_SUCCESS) {
            c_license_gen_get_token_str(req_str, sizeof(req_str), time_ms_str, api_key);
        } else {
            c_license_gen_get_token_str(req_str, sizeof(req_str), time_ms_str, NULL);
        }
        // 获取服务端返回登录信息
        dummy_http_request(METHOD, HOST, API, PORT, HEADER, req_str, dummy_http_response_for_token);
    }

    //... 其他代码
}

int dummy_wss_init(void)
{ 
    // 建立websocket连接，获取连接字段
    char *wss_host = c_mmi_get_wss_host();
    char *wss_port = c_mmi_get_wss_port();
    char *wss_api = c_mmi_get_wss_api();
    char *wss_header = c_mmi_get_wss_header();
    
    // 建立wss连接
    int ret = dummy_wss_connect(wss_host, wss_port, wss_api, wss_header);
    
    return ret;
}

void dummy_recorder_task(void)
{
    uint32_t send_size =0;
    uint32_t size = 640;
    uint8_t* data = (uint8_t*) util_malloc(size);

    while(1){
        if(dummy_recoder_is_work()){
            send_size = dummy_hw_recorder_get_data(data, size);
            if(send_size){
                // 将音频采集硬件采集到的数据输出至SDK ringbuffer
                c_mmi_put_recorder_data(data, send_size);
            }
            else{
                util_msleep(10);
            }
        
        } else {
            util_msleep(10);
        }
    }
}

void dummy_player_task(void)
{
    uint8_t data[640];
    uint32_t size = 640;
    uint32_t recv_size = 0;

    while(1) {
        if(dummy_player_is_work()){
            recv_size = c_mmi_get_player_data(data, size);
            if(recv_size){
                // 将SDK ringbuffer中的音频数据输出给到播放器进行播放
                dummy_hw_player_put_data(data, size)
            } else {
                util_msleep(10);
            }
        
        } else {
            util_msleep(10);
        }
    }
}

int dummy_wss_task_recv(void)
{
    int opcode;
    char* payload_data;
    int recv_size;
    while(1){
        dummy_wss_recv(&opcode, &pauload_data, &recv_size);
        if(recv_size)
            // 将收到的websocket数据送入SDK进行解析，其中只需要送入opcode，payload数据.
            c_mmi_analyze_recv_data(opcode, payload_data, recv_size);
        else
            util_msleep(10);
    }
    return 0;
}

int dummy_wss_task_send(void)
{
    uint8_t data_type;
    uint8_t payload_data[1024];
    uint32_t size;

    while(1){
        // 从SDK获取打包好的payload数据
        size = c_mmi_get_send_data(&data_type, payload_data, size);
        if (size == 0) {
            util_msleep(10);
        } else {
            // 将payload数据传入websocket发送函数，自行打包帧头进行发送
            dummy_wss_send(data_type, data, size);
        }
    }
    return 0;
}

int dummy_button_up(void)
{
    // 关闭麦克风
    recorder_stop();
    // 通知云端服务开始处理音频数据
    c_mmi_stop_speech();

    return 0;
}

int dummy_button_down(void)
{
    // 关闭喇叭
    player_stop();
    // 通知云端即将开始发送音频数据，SDK会根据云端对该指令的响应触发C_MMI_EVENT_SPEECH_START
    c_mmi_start_speech();

    return 0;
}

int _mmi_event_callback(uint32_t event, void *param)
{
    char *text;

    text = param;
    switch (event) {
        case C_MMI_EVENT_USER_CONFIG:
            // 开始新对话
            c_mmi_reset_dialog_id();
            break;
        case C_MMI_EVENT_DATA_INIT:
            // Mmi data ready, 开始网络连接
            dummy_wss_init();
            break;
        case C_MMI_EVENT_DATA_DEINIT:
            UTIL_LOG_W("will disconnect");
            break;
        case C_MMI_EVENT_SPEECH_PREPARE:
            break;
        case C_MMI_EVENT_SPEECH_START:
            UTIL_LOG_D("enable recorder when send speech");
            dummy_player_stop();
            dummy_recorder_start();
            break;
        case C_MMI_EVENT_ASR_START:
            UTIL_LOG_I("event [C_MMI_EVENT_ASR_START]");
            break;
        case C_MMI_EVENT_ASR_INCOMPLETE:
            UTIL_LOG_D("ASR [%s]", text);
            break;
        case C_MMI_EVENT_ASR_COMPLETE:
            if (text) {
                UTIL_LOG_D("ASR C [%s]", text);
            } else {
                UTIL_LOG_D("ASR C [NULL]");
            }
            break;
        case C_MMI_EVENT_ASR_END:
            UTIL_LOG_D("disable record when ASR complete");
            dummy_recorder_stop();
            break;
        case C_MMI_EVENT_LLM_INCOMPLETE:
            UTIL_LOG_D("LLM [%s]", text);
            break;
        case C_MMI_EVENT_LLM_COMPLETE:
            UTIL_LOG_D("LLM C [%s]", text);
            break;
        case C_MMI_EVENT_TTS_START:
            UTIL_LOG_I("enable player when dialog start");
            du mmy_player_start();
            break;
        case C_MMI_EVENT_TTS_END:
            break;
        default:
            break;
    }

    return UTIL_SUCCESS;
}

int main(void)
{
    int ret = dummy_aliyun_sdk_init();
    
    // 开启websocket收发线程，由开发者自己实现
    dummy_wss_thread_start();
    return ret;
}
```

### **6.2. 完整示例日志**

完整示例日志如下：

```
[UT][I][c_storage_init]sdk ver       [0x00000300]
[UT][I][c_storage_init]flag          [0x0000003f]
[UT][I][c_storage_init]app_id        [<APP ID>]
[UT][I][c_storage_init]app_secret    [<APP SECRET>]
[UT][I][c_storage_init]device_name   [<DEVICE NAME>]
[UT][I][c_storage_init]nonce         [<NONCE>]
[UT][I][c_storage_init]dialog_id     [<DIALOG ID>]
[UT][I][c_storage_init]load          [<DATA>]
[UT][I][c_storage_init]device_secret [<DEVICE SECRET>]
[UT][I][c_mmi_register_event_callback]register event callback [<POINT ADDRESS>]
[UT][I][c_mmi_set_work_mode]work_mode[push2talk]
[UT][D][c_mmi_set_text_mode]text_mode[]
[UT][D][c_mmi_set_voice_id]voice_id[longxiaochun_v2]
[UT][D][c_mmi_set_upstream_mode]upstream_mode[pcm]
[UT][D][c_mmi_set_downstream_mode]downstream_mode[pcm]
[UT][I][c_mmi_config]device_name [<DEVICE NAME>]
[UT][I][c_mmi_config]load dialog_id [<DIALOG ID>]
[UT][I][c_mmi_config]done
[UT][I][c_device_gen_register_req]req_str [383][{"appId":"<YOUR APPID>","deviceName":"<YOUR DEVICE NAME>","nonce":"<YOUR NONCE>","requestTime":"1753326620619","sdkVersion":"0.3.2","signature":"<Signature>"}]
[UT][I][c_device_analyze_register_rsp]rsp_str [403][{"nonce":"<YOUR NONCE>","responseTime":"1753326621269","appId":"<YOUR APPID>","deviceName":"<YOUR DEVICE NAME>","signature":"<Signature>"}]
[UT][I][c_device_analyze_register_rsp]nonce  [<NONCE>]
[UT][I][c_dev_gen_get_token_req]plaintext [164][{"appId":"<YOUR APP ID>","deviceName":"<YOUR DEVICE NAME>","payMode":"LICENSE","requestTime":"1753327457730","sdkVersion":"0.3.2","tokenType":"MMI"}]
[UT][I][c_dev_gen_get_token_req]req_str [420][{"appId":"<YOUR APP ID>","deviceName":"<YOUR DEVICE NAME>","nonce":"<NONCE>","requestTime":"1753327457730","sdkVersion":"0.3.2","tokenType":"MMI","signature":"<SIGNTURE>"}]
[UT][I][c_mmi_analyze_get_token_rsp]rsp_str [589][{"nonce":"<NONCE>","responseTime":"1753327458081","appId":"<YOUR APP ID>","deviceName":"<YOUR DEVICE NAME>","requestIp":"YOUR IP","signature":"<SIGNATURE>"}]
[UT][I][c_mmi_analyze_get_token_rsp]nonce    [<NONCE>]
[UT][I][_mmi_event_callback]C_MMI_EVENT_DATA_INIT
[UT][I][dummy_wss_init]work
[UT][I][dummy_wss_connect]wss update
[UT][I][dummy_wss_connect]request[239][GET <wss_api> HTTP/1.1
Host: <WSS HOST>
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: FhVlQeR4S1N06+1/SU79XA==
Sec-WebSocket-Version: 13
<WSS HEADER>

]
[UT][I][dummy_wss_connect]Reading response...
[UT][I][dummy_wss_connect]response[MMI][187][HTTP/1.1 101 Switching Protocols
upgrade: websocket
connection: upgrade
sec-websocket-accept: sqchBdVDX8kKBgi90/PFl5+/4VI=
date: Thu, 24 Jul 2025 08:25:24 GMT
server: istio-envoy

]
[UT][I][dummy_wss_connect][MMI]done
[UT][I][dummy_wss_thread_start][dummy_wss_task_send] send task [0x135e27180]
[UT][I][dummy_wss_thread_start][dummy_wss_task_recv] recv task [0x135e271a0]
[UT][I][_gen_cmd_start]task_id [<TASK ID>]
[UT][I][_send_cmd_start]send [run-task] [0-2] [0]
[UT][D][c_mmi_analyze_recv_data]recv[109][{"header":{"task_id":"<TASK ID>","event":"task-started","attributes":{}},"payload":{}}]
[UT][I][c_mmi_analyze_recv_data]recv [task-started] [0-2]
[UT][D][c_mmi_analyze_recv_data]recv[192][{"header":{"task_id":"<TASK ID>","event":"result-generated","attributes":{}},"payload":{"output":{"event":"Started","dialog_id":"<DIALOG_ID>"}}}]
[UT][I][_on_payload_event_start]recv [Started] [0-3]
[UT][D][c_mmi_analyze_recv_data]recv[223][{"header":{"task_id":"<TASK ID>","event":"result-generated","attributes":{}},"payload":{"output":{"event":"DialogStateChanged","state":"Listening","dialog_id":"<DIALOG_ID>"}}}]
[UT][I][_on_payload_event_state_change]recv [Listening] [0-4]
[UT][D][dummy_button_down]
[UT][I][dummy_player_stop]
[UT][I][_send_cmd_req2spk]ready to send [1-4]
[UT][I][_send_cmd_speech]send [SendSpeech] [1-5] [0]
[UT][D][_mmi_event_callback]enable recorder when send speech
[UT][I][dummy_recorder_start]
[UT][I][_on_payload_event_speech_start]recv [SpeechStarted][ASR Start] [1-5]
[UT][I][_mmi_event_callback]event [C_MMI_EVENT_ASR_START]
[UT][D][dummy_button_up]
[UT][I][dummy_recorder_stop]
[UT][I][_send_cmd_stop_speech]send [StopSpeech] [1-5] [0]
[UT][I][_on_payload_event_speech_content]recv [SpeechContent][ASR Text] [1-5]
[UT][D][_mmi_event_callback]ASR C [今天天气怎么样？]
[UT][I][_on_payload_event_speech_end]recv [SpeechEnded][ASR End] [1-6]
[UT][D][_mmi_event_callback]disable record when ASR complete
[UT][I][dummy_recorder_stop]
[UT][I][_on_payload_event_state_change]recv [Thinking] [1-7]
[UT][D][_on_payload_event_state_change]prepare player rb
[UT][W][c_mmi_analyze_recv_data]recv [8000] in thinking
[UT][W][c_mmi_analyze_recv_data]recv [1788] in thinking
[UT][I][_on_payload_event_state_change]recv [Responding][Audio Start] [1-8]
[UT][I][_mmi_event_callback]enable player when dialog start
[UT][I][dummy_player_start]
[UT][I][_on_payload_event_respond_start]recv [RespondingStarted][Audio Start] [1-8]
[UT][I][_on_payload_event_respond_content]recv [RespondingContent][LLM Text] [1-8]
[UT][D][_mmi_event_callback]LLM C [今天上海市天气多云，白天最高气温33℃，夜间有小雨，气温27℃。东风吹，风力1-3级。]
[UT][I][_on_payload_event_respond_end]recv [RespondingEnded][Audio End] [1-9]
[UT][D][_on_payload_event_respond_end]recv audio data size [371200]
```
