# 使用 License 模式接入 iOS SDK

本文档指导开发者通过License模式集成iOS SDK，实现设备管控和鉴权。多模态SDK需支持License计费模式，支持半托管和全托管两种接入模式。

## 1\. 模式说明

使用 License 计费模式访问多模态交互开发套件需要集成 License SDK，请参考本文第 4 节集成 SDK。

### 1.1. 半托管模式

适用场景：客户自有云服务，能对自己的设备进行管理和鉴权，客户云服务和设备端有双向通信通道；

-   服务端开发：
    
    -   参考[云端接口开发说明](https://help.aliyun.com/zh/model-studio/mmi-rtos-sdk#557a524795xam) 完成云端接口对接，设备计量管理服务提供设备注册和获取Token两个接口
-   设备端开发：
    
    -   接入方通过本SDK的genRegisterReq接口获取设备注册签名。
    -   拿到设备注册签名后调用接入方自有云端服务进行设备注册，接入方云端需集成POP SDK。
    -   设备注册返回后调用本SDK的writeDeviceInfo接口写入设备信息。
    -   调用本SDK的genGetTokenReq接口获取访问令牌信息的数据签名。
    -   调用本SDK的getToken获取解签后业务交互令牌信息，之后可使用令牌信息进行业务交互。

### 1.2. 全托管模式

适用场景：客户没有云服务，无法对设备进行管理，由阿里云进行设备管理和鉴权

-   服务端开发：
    
    -   无
-   设备端开发
    
    -   调用本SDK的deviceRegister接口执行设备注册。
    -   调用本SDK的getToken接口获取业务交互令牌，之后可使用令牌信息进行业务交互。

## 2\. 使用前注意需了解事项

-   使用License模式前在百炼控制台创建了应用，并购买了License。
-   SDK中封装了设备唯一标识生成逻辑并存储到keychain，避免同1设备重复注册，通过DeviceInfoUtils.shared.getDeviceId()调用，请务必使用SDK中获取deviceName接口逻辑或者接入方自行保证deviceName唯一性。

## 3\. 接口说明

### 3.1. SDK初始化 initialize

半托管和全托管模式均需先执行初始化接口

**入参：**

**字段**

**类型**

**必填**

**说明**

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

appSecret

String

是

应用密钥，在百炼控制台创建应用之后会生成该密钥

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

callBack

InitCallBack

是

SDK初始化回调，参考InitCallBack对象

**InitCallBack对象**

**返回值**

**方法名**

**说明**

void

success()

初始化成功

void

fail(ResultError error)

初始化失败

**ResultError对象**

**字段**

**类型**

**必填**

**说明**

code

int

否

返回错误码

message

String

否

返回错误码说明

**出参：**

无

**调用示例**
```
/// 初始化SDK，写入产品信息
func initializeExample() {
    let params = InitParams(
        appId: "your_app_id",
        appSecret: "your_app_secret",
        deviceName: "your_device_name_or_uuid"
    )

    // 定义回调类
    class InitCallback: InitCallBack {
        func success() {
            print("初始化成功")
        }

        func fail(error: ResultError) {
            print("初始化失败: \(error.message ?? "unknown error")")
        }
    }

    let callback = InitCallback()
    DeviceAuthClient.companion.instance.initialize(params: params, callBack: callback)
}
```

### 3.2. 半托管模式

#### 3.2.1. 设备注册相关接口

##### 3.2.1.1. 生成设备注册信息 genRegisterReq

**入参：**

**字段**

**类型**

**必填**

**说明**

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

payMode

String

是

计费方式：PAYG（后付费）、LICENSE（license计费）

reqNonce

String

是

请求随机串，长度26位

requestTime

String

是

请求时间

**出参：**

**字段**

**类型**

**必填**

**说明**

success

boolean

是

请求处理是否成功

code

int

否

请求失败code

message

String

否

请求失败描述

data

String

否

设备注册调用POP接口所需的签名参数

**调用示例：**
```
/// 半托管模式：生成设备注册请求签名
func genRegisterReqExample() {
        let registerInfo = DeviceRegisterInfo(
            reqNonce: "random_nonce_string",
            appId: "your_app_id",
            deviceName: "your_device_name",
            payMode: PayMode.license.payMode,
            requestTime: "\(Int64(Date().timeIntervalSince1970 * 1000))"
        )

        let result = DeviceAuthClient.companion.instance.genRegisterReq(registerInfo: registerInfo)

    if result.success {
            let signature = result.data
            print("生成注册签名成功: \(signature ?? "")")
            // 使用签名调用服务端注册接口
        } else {
            print("生成注册签名失败: \(result.message)")
        }
    }
```

##### 3.2.1.2. 写入设备注册信息 writeDeviceInfo

调用云端设备注册的pop接口得到的响应，需要再次传回设备端SDK，进行信息写入

**入参：**

**字段**

**类型**

**必填**

**说明**

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

reqNonce

String

是

请求发起随机串，长度26位

rspNonce

String

是

返回数据的随机串，长度26位

responseTime

String

是

返回数据的时间戳

signature

String

是

YOUR\_SIGNATURE

**出参：**

**字段**

**类型**

**必填**

**说明**

success

boolean

是

请求处理是否成功

code

int

否

请求失败code

message

String

否

请求失败描述

data

String

否

设备注册调用POP接口所需的签名参数

**调用示例：**
```
/// 半托管模式：写入设备注册成功的信息
func writeDeviceInfoExample() {
    let deviceInfo = DeviceRegisterRsp(
        appId: "your_app_id",
        reqNonce: "request_nonce",
        rspNonce: "response_nonce_from_server",
        responseTime: "response_time_from_server",
        deviceName: "your_device_name",
        signature: "signature_from_server"
    )

    let result = DeviceAuthClient.companion.instance.writeDeviceInfo(deviceInfo: deviceInfo)

    if result.success {
        print("写入设备信息成功")
    } else {
        print("写入设备信息失败: \(result.message)")
    }
}
```

#### 3.2.2. 获取业务交互令牌相关接口

##### 3.2.2.1. 生成获取访问令牌信息 genGetTokenReq

**入参：**

**字段**

**类型**

**必填**

**说明**

nonce

String

是

请求随机串，长度26位

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

payMode

String

是

计费方式：PAYG（后付费）、LICENSE（license计费）

tokenType

String

是

请求令牌的类型（当前仅支持MMI类型）

MMI：多模态交互令牌

requestTime

String

是

请求时间戳,单位ms

**出参：**

**字段**

**类型**

**必填**

**说明**

success

boolean

是

请求处理是否成功

code

int

否

请求失败code

message

String

否

请求失败描述

data

String

否

设备注册调用POP接口所需的签名参数

```
{
    "success": true,
    "data": "84uoRCyy6AG/SH7LrHjJW0D7lsBp/H4RReS7gJY5L0oC517xJWAmwtmghLjYkW/Qj4ZvK6vrM7QC5yxtMl3TQLHdAGSsqQLb0bP6zKOiDzoNFwqs61+GMQ7guTPjbE9Fqaf7"
}
```
**调用示例：**
```
/// 半托管模式：生成获取token请求的签名
func genGetTokenReqExample() {
     let getTokenParams = GenGetTokenParams(
         nonce: "random_nonce_string",
         appId: "your_app_id",
         deviceName: "your_device_name",
         payMode: PayMode.license.payMode,
         requestTime: "\(Int64(Date().timeIntervalSince1970 * 1000))",
         signature: nil, // 由SDK生成
         tokenType: "MMI"
     )

     let result = DeviceAuthClient.companion.instance.genGetTokenReq(getTokenParams: getTokenParams)

     if result.success {
         let signature = result.data
         print("生成token请求签名成功: \(signature ?? "")")
         // 使用签名调用服务端获取token接口
     } else {
         print("生成token请求签名失败: \(result.message)")
     }
 }
```

##### 3.2.2.2. 解签POP接口返回的token数据 getToken

**入参：**

**字段**

**类型**

**必填**

**说明**

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

reqNonce

String

是

请求随机串，长度26位

rspNonce

String

是

返回数据的随机串，长度26位

responseTime

String

是

返回数据的时间戳

signature

String

是

YOUR\_SIGNATURE

**出参：**

**字段**

**类型**

**必填**

**说明**

success

boolean

是

请求处理是否成功

code

int

否

请求失败code

message

String

否

请求失败描述

data

String

否

返回解签后的数据

**调用示例：**
```
/// 半托管模式：获取token后进行解签
func getTokenWithSignatureExample() {
    let tokenRsp = AnalyzeTokenSignRsp(
        reqNonce: "request_nonce",
        rspNonce: "response_nonce_from_server",
        responseTime: "response_time_from_server",
        appId: "your_app_id",
        deviceName: "your_device_name",
        signature: "signature_from_server"
    )

    let result = DeviceAuthClient.companion.instance.getToken(tokenRsp: tokenRsp)

    if result.success {
        let token = result.data
        print("获取token成功: \(token ?? "")")
        // 使用token进行后续业务调用
    } else {
        print("获取token失败: \(result.message)")
    }
}
```

### 3.3. 全托管模式

#### 3.3.1. 检查设备是否注册 deviceIsRegistered

**入参：** **无** **出参：**

设备是否注册

**调用示例：**
```
/// 检查设备是否完成注册
func checkDeviceRegisteredExample() {
    let isRegistered = DeviceAuthClient.companion.instance.deviceIsRegistered()

    if isRegistered {
        print("设备已注册")
    } else {
        print("设备未注册，需要先进行设备注册")
    }
}
```

#### 3.3.2. 设备注册 deviceRegister

**入参：**

**字段**

**类型**

**必填**

**说明**

params

Object

是

设备注册入参对象，参考DeviceRegisterParams对象

callBack

DeviceRegisterCallBack

是

设备注册回调

**DeviceRegisterParams对象**

**字段**

**类型**

**必填**

**说明**

nonce

String

是

请求随机串，长度26位

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

workspaceId

String

否

工作空间ID,使用工作空间额度注册才需要

deviceName

String

是

设备名称：（使用设备WIFI MAC或唯一序列号）

requestTime

String

是

请求时间

payMode

String

是

计费方式：PAYG（后付费）、LICENSE（license计费）

**出参：**

无

**调用示例：**
```
/// 全托管模式：设备注册
func deviceRegisterExample() {
    let params = DeviceRegisterParams(
        nonce: "random_nonce_string",
        appId: "your_app_id",
        workspaceId:"your_workspace_id"
        deviceName: "your_device_name",
        payMode: PayMode.license.payMode,
        requestTime: "\(Int64(Date().timeIntervalSince1970 * 1000))",
        signature: nil
    )

    // 定义回调类
    class DeviceRegisterCallback: DeviceRegisterCallBack {
        func success() {
            print("设备注册成功")
        }

        func fail(error: ResultError) {
            print("设备注册失败: \(error.message ?? "unknown error")")
        }
    }

    let callback = DeviceRegisterCallback()
    DeviceAuthClient.companion.instance.deviceRegister(
        params: params,
        callBack: callback,
        completionHandler: { _ in }
    )
}
```

#### 3.3.3. 获取业务交互令牌 getToken

**入参：**

**字段**

**类型**

**默认值**

**必填**

**说明**

params

Object

\-

是

设备认证所需参数对象，参考GenGetTokenParams对象

callBack

GetTokenCallBack

\-

是

获取token回调，参考GetTokenCallBack

对象

**GenGetTokenParams对象**

**字段**

**类型**

**默认值**

**必填**

**说明**

nonce

String

\-

是

16字节随机数（26字符)

appId

String

\-

是

应用标识，在百炼控制台创建应用之后会生成该ID

apiKey

String

\-

是

应用密钥，在百炼控制台密钥管理创建

deviceName

String

\-

是

设备唯一标识

requestTime

String

\-

是

请求时间戳（ms）

payMode

String

\-

是

计费方式：PAYG（后付费）、LICENSE（license计费）

tokenType

String

\-

是

请求令牌的类型（当前仅支持MMI类型）

MMI：多模态交互令牌

**出参：**

无

**调用示例：**
```
/// 全托管模式：获取token
func getTokenFullManagedExample() {
    let params = GenGetTokenParams(
        nonce: "random_nonce_string",
        appId: "your_app_id",
        deviceName: "your_device_name",
        payMode: PayMode.license.payMode,
        requestTime: "\(Int64(Date().timeIntervalSince1970 * 1000))",
        signature: nil,
        tokenType: "MMI"
    )

    // 定义回调类
    class GetTokenCallback: GetTokenCallBack {
        func success(tokenInfo: String?) {
            print("获取token成功: \(tokenInfo ?? "")")
        }

        func fail(error_ error: ResultError?) {
            print("获取token失败: \(error?.message ?? "unknown error")")
        }
    }

    let callback = GetTokenCallback()
    DeviceAuthClient.companion.instance.getToken(
        params: params,
        callBack: callback,
        completionHandler: { _ in }
    )
}
```

### 3.4. 获取License标识签名

**入参：**

**字段**

**类型**

**默认值**

**必填**

**说明**

params

Object

\-

是

设备认证所需参数对象，参考LicenseSignatureParams对象

**LicenseSignatureParams对象**

**字段**

**类型**

**默认值**

**必填**

**说明**

appId

String

\-

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

\-

是

设备唯一标识

taskId

String

\-

是

本次连接唯一标识，用于在工程链路上跟踪任务执行。由客户端生成，格式建议为36位uuid字符串，格式示例："f894c16f-f20e-4c1d-837e-89e0fbc63a43"

**出参：**

**字段**

**类型**

**默认值**

**说明**

timestamp

String

\-

当前时间戳ms

license\_info

String

\-

license\_info签名信息

device\_info

String

\-

device\_info签名信息

**调用示例：**
```
/// 获取license签名
func getLicenseSignatureExample() {
    let params = LicenseSignatureParams(
        appId: "your_app_id",
        deviceName: "your_device_name",
        taskId: "your_task_id"
    )

    let licenseSignature = DeviceAuthClient.companion.instance.getLicenseSignature(params: params)
    print("License签名结果: \(licenseSignature)")
    // 返回包含timestamp和license_info的JSON字符串
}
```

### 3.5. 设备重置 deviceReset

tips: 在百炼控制台重置设备后，需要调用SDK deviceReset接口重置设备，方可进行重新注册。

**入参：**

无

**出参：**

Boolean 是否重置成功

**调用示例：**
```
let result = DeviceAuthClient.companion.instance.deviceReset()
 if(result){
     print("设备重置成功")
 }else{
     print("设备重置失败")
 }
```

## 4\. 集成依赖库

使用最新版本 iOS SDK，引用其中的MultimodalDialogTongyiMetathings.framework

## 5\. 涉及多模态SDK接入修改

1.  在启动会话前完成tongyimetathings SDK的初始化和检测设备是否注册，未注册执行设备注册，具体参考接入示例工程。
2.  初始化该SDK，设备注册完成后获取多模态会话token，参考上述2.1，2.3接口，将getToken接口返回的dashToken数据设置为apiKey，具体参考示例工程。

```
chatView.updateParam(url: host, apiKey: dashToken, workSpaceId: workSpaceId, appId: appId, chain: chainMode, image_url: img, payType: self.mPayMode, voice: voice)
```

1.  创建会话时传入license计费标识,参考接入示例：

```
func connect(){
    self.conversation?.stop()
    isInDialog = false

    var mode = DialogMode.duplex
    if(!duplexMode){
        mode = DialogMode.tap2talk
    }
    let taskId = UUID().uuidString.replacingOccurrences(of: "-", with: "").lowercased()
    let promptParam = ["user_name" : "大米"]
    TYLogger.shared.debug("current voice:" + voice)
    var params:MultiModalRequestParam
            //构建License计费标识
            let deviceName = DeviceInfoUtils.shared.getDeviceId()
            let licenseParams = LicenseSignatureParams(appId: self.APP_ID, deviceName: deviceName, taskId: taskId)
            let signData = DeviceAuthClient.companion.instance.getLicenseSignature(params: licenseParams)
            print("signData: \(signData)")
             // 将 JSON 字符串转为字典
            guard let data = signData.data(using: .utf8),
                  let signatureJson = try? JSONSerialization.jsonObject(with: data) else {
                print("Failed to parse signData as JSON")
                return
            }
            let map: [String: Any] = ["signature": signatureJson]

            params = MultiModalRequestParam{ multiBuilder in
               multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                   upstreamBuilder.mode = mode.rawValue
                   upstreamBuilder.type = "AudioAndVideo"
               })

               multiBuilder.clientInfo = MultiModalRequestParam.ClientInfo(builder: {
                   clientInfoBuilder in
                   clientInfoBuilder.userId = "test-ios-user"
                   clientInfoBuilder.device = MultiModalRequestParam.ClientInfo.Device(uuid: deviceName)
                   clientInfoBuilder.passThroughParams = map
               })
               multiBuilder.downStream = MultiModalRequestParam.DownStream(builder: {
                   downStreamBuilder in
                   downStreamBuilder.sampleRate = 16000
                   downStreamBuilder.voice = voice
                   downStreamBuilder.intermediateText = textStreamFeedback ? "dialog" : "transcript"
               })
               multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                   bizBuilder in
                   bizBuilder.userPromptParams = promptParam
               })
           }
}
```
