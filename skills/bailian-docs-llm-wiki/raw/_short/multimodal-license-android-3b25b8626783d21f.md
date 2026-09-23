# 使用 License 模式接入Android SDK

本文档指导开发者通过License模式集成Android SDK，实现设备管控和鉴权。License计费模式接入需参考该文档集成，支持半托管和全托管两种接入模式。

## 1\. 模式说明

使用 License 计费模式需要在多模态交互开发套件基础上集成 License SDK，请参考本文第 4 节集成 SDK。

**环境要求**：SDK 最低支持 Android 7.0（API 24），请在工程中配置 minSdkVersion 24 及以上。

### 1.1. 半托管模式

适用场景：客户自有云服务，能对自己的设备进行管理和鉴权，客户云服务和设备端有双向通信通道；

**接入方需参考以下步骤接入：**

-   服务端开发：
    
    -   参考云端接口开发说明 完成云端接口对接，设备计量管理服务提供设备注册 deviceRegister 和获取访问业务交互令牌 getToken 两个接口
-   设备端开发：
    
    -   接入方通过本SDK的genRegisterReq接口获取设备注册签名。
    -   拿到设备注册签名后调用接入方自有云端服务进行设备注册，接入方云端需集成POP SDK。
    -   设备注册返回后调用本SDK的writeDeviceInfo接口写入设备信息。
    -   调用本SDK的genGetTokenReq接口获取访问令牌信息的数据签名。
    -   拿到访问令牌信息的数据签名后调用接入方自有云端服务获取token，接入方云端需集成POP SDK。
    -   调用本SDK的getToken获取解签后业务交互令牌信息，之后可使用令牌信息进行业务交互。

### 1.2. 全托管模式

适用场景：客户没有云服务，无法对设备进行管理，由阿里云进行设备管理和鉴权

-   服务端开发：
    
    -   无
-   设备端开发
    
    -   调用本SDK的deviceRegister接口执行设备注册。
    -   调用本SDK的getToken接口获取业务交互令牌，之后可使用令牌信息进行业务交互。

## 2\. 使用前注意事项

-   使用 License 模式前在百炼控制台创建了应用，并购买了 License。
-   SDK 中封装了设备唯一标识生成逻辑并持久化数据到设备，避免同 1 设备重复注册，通过 `DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId()` 获取，请务必使用 SDK 中获取 deviceName 接口逻辑或者接入方自行保证 deviceName 唯一性。

**警告**⚠️ **deviceName 统一获取方式**：凡涉及设备注册、注册状态查询、获取 Token 的场景，deviceName 统一通过 `DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId()` 获取。该接口已内置历史兼容逻辑，存量设备会自动返回旧 ID 原值，无需额外处理。

### 2.1. 设备标识生成策略说明

新版 SDK 的设备标识由底层的 `DeviceIdentityManager` 统一生成，采用**多级降级策略**，确保所有 Android 设备都能获取到设备标识，优先级从高到低依次为：

1.  **CUSTOM（自定义标识）**：接入方通过 `setCustomIdentity(String)` 注入的标识（如自有服务端下发、OAID 等），按原值使用，不做派生。
2.  **MEDIA\_DRM**：MediaDrm ID（设备级唯一，大多数设备支持），派生为应用级标识。
3.  **ANDROID\_ID**：MediaDrm 不可用时使用 `Settings.Secure.ANDROID_ID` 派生为应用级标识。
4.  **FALLBACK\_UUID**：以上均不可用时，生成随机 UUID 并持久化到 SharedPreferences，再派生为应用级标识。

**警告****FALLBACK\_UUID 仅适用于测试环境，不可用于生产。** 该模式下设备标识在应用卸载重装后会发生变化，无法保证设备唯一性，卸载后将导致重复注册、Token 链路失效等问题。生产环境中如检测到 source 为 FALLBACK\_UUID，应通过 `setCustomIdentity()` 注入稳定标识或提示用户设备不兼容。

兼容性说明：

-   `DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId()` 已内置历史兼容逻辑，存量设备自动返回旧 ID 原值，新设备走多级降级策略。`DeviceUUIDUtil.getAndroidId(context)` 仍可使用（内部委托给 DeviceIdentityManager），但已标记为弃用。
-   各来源标识的格式、长度与稳定性对比见第 7 节。

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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

callBack

InitCallBack

是

SDK初始化回调，参考InitCallBack对象

**重要**安全提示：`appSecret` 为敏感凭证，请勿硬编码在客户端代码中（避免随 APK 反编译泄露），建议由接入方服务端在运行时安全下发。

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
DeviceAuthClient.getInstance().initialize(new InitParams(YOUY_APP_ID, YOUR_APP_SECRET, YOUR_DEVICE_NAME), new InitCallBack() {
    @Override
    public void success() {
        Log.d(TAG, "initialize success");
    }

    @Override
    public void fail(ResultError resultError) {
        Log.e(TAG, "initialize fail: " + resultError.getMessage());
    }
});
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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

payMode

String

是

计费方式：PAYG（后付费）、LICENSE（license计费）

reqNonce

String

是

请求随机串，26位随机hex字符串

requestTime

String

是

请求时间戳

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
DeviceRegisterInfo deviceRegisterInfo = new DeviceRegisterInfo();
deviceRegisterInfo.setAppId(YOUR_APP_ID);
deviceRegisterInfo.setDeviceName(YOUR_DEVICE_NAME);
deviceRegisterInfo.setPayMode(PayMode.LICENSE.getPayMode());
deviceRegisterInfo.setReqNonce(RandomUtil.generateRandomHexString(26));
deviceRegisterInfo.setRequestTime(String.valueOf(System.currentTimeMillis()));
Result<String> result = DeviceAuthClient.getInstance().genRegisterReq(deviceRegisterInfo);
if (result.isSuccess()) {
    Log.d(TAG, "genRegisterReq: " + result.getData());
}
```

##### 3.2.1.2. 写入设备注册信息 writeDeviceInfo

调用云端设备注册的pop接口得到的响应，需要将注册信息写入到设备进行保存

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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

reqNonce

String

是

请求发起随机串，26位随机hex字符串

rspNonce

String

是

返回数据的随机串，26位随机hex字符串

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
DeviceRegisterRsp params = new DeviceRegisterRsp();
params.setAppId(YOUR_APP_ID);
params.setDeviceName(YOUR_DEVICE_NAME);
params.setReqNonce(YOUR_REQUEST_NONCE);
params.setRspNonce(YOUR_RESPONSE_NONCE);
params.setResponseTime(YOUR_RESPONSE_TIME);
params.setSignature(YOUR_RESPONSE_SIGNATURE);
Result<String> result = DeviceAuthClient.getInstance().writeDeviceInfo(params);
if (result.isSuccess()) {
    Log.d(TAG, "writeDeviceInfo success");
} else {
    Log.e(TAG, "writeDeviceInfo error: " + result.getMessage());
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

请求随机串，26位随机hex字符串

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

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
    "data": "84uoRCyy6AG/sss/xxxxx/Qj4ZvK6vrM7QC5yxtMl3TQLHdAGSsqQLb0bP6zKOiDzoNFwqs61+GMQ7guTPjbE9Fqaf7"
}
```
**调用示例：**
```
GenGetTokenParams params = new GenGetTokenParams();
params.setNonce(RandomUtil.generateRandomHexString(26));
params.setAppId(YOUR_APP_ID);
params.setDeviceName(YOUR_DEVICE_NAME);
params.setPayMode(PayMode.LICENSE.getPayMode());
params.setTokenType("MMI");
params.setRequestTime(String.valueOf(System.currentTimeMillis()));
Result<String> result = DeviceAuthClient.getInstance().genGetTokenReq(params);
if (result.isSuccess()) {
    Log.d(TAG, "getTokenSign: " + result.getData());
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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

reqNonce

String

是

请求随机串，26位随机hex字符串

rspNonce

String

是

返回数据的随机串，26位随机hex字符串

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
AnalyzeTokenSignRsp tokenSignRsp = new AnalyzeTokenSignRsp();
tokenSignRsp.setAppId(YOUR_APP_ID);
tokenSignRsp.setDeviceName(YOUR_DEVICE_NAME);
tokenSignRsp.setReqNonce(YOUR_REQUEST_NONCE);
tokenSignRsp.setRspNonce(YOUR_RESPONSE_NONCE);
tokenSignRsp.setResponseTime(YOUR_RESPONSE_TIME);
tokenSignRsp.setSignature(YOUR_RESPONSE_SIGNATURE);
Result<String> result = DeviceAuthClient.getInstance().getToken(tokenSignRsp);
if (result.isSuccess()) {
    Log.d(TAG, "analyzeTokenSign: " + result.getData());
}
```

### 3.3. 全托管模式

#### 3.3.1. 检查设备是否注册 deviceIsRegistered

**入参：** **无** **出参：**

设备是否注册

**调用示例：**
```
boolean deviceIsRegistered = DeviceAuthClient.getInstance().deviceIsRegistered();
```

#### 3.3.2. 设备注册 deviceRegister

**入参：**

**字段**

**类型**

**必填**

**说明**

params

DeviceRegisterParams

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

请求随机串，26位随机hex字符串

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

workspaceId

String

否

工作空间ID,使用工作空间额度注册方式才需要

deviceName

String

是

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

requestTime

String

是

请求时间戳

payMode

String

是

计费方式：PAYG（后付费）、LICENSE（license计费）

**出参：**

无

**调用示例：**
```
DeviceRegisterParams params = new DeviceRegisterParams();
params.setNonce(RandomUtil.generateRandomHexString(26));
params.setAppId(YOUR_APP_ID);
params.setWorkspaceId(YOUR_WORKSPACE_ID);
params.setDeviceName(YOUR_DEVICE_NAME);
params.setRequestTime(String.valueOf(System.currentTimeMillis()));
params.setPayMode(PayMode.LICENSE.getPayMode());
DeviceAuthClient.getInstance().deviceRegister(params, new DeviceRegisterCallBack() {
    @Override
    public void success() {
        Log.d(TAG, "deviceRegister success");
    }

    @Override
    public void fail(ResultError error) {
        Log.e(TAG, error.getMessage());
    }
});
```

#### 3.3.3. 获取业务交互令牌 getToken

**入参：**

**字段**

**类型**

**默认值**

**必填**

**说明**

params

GenGetTokenParams

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

请求随机串，26位随机hex字符串

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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

requestTime

String

\-

是

请求时间戳

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
GenGetTokenParams params = new GenGetTokenParams();
params.setNonce(RandomUtil.generateRandomHexString(26));
params.setAppId(YOUR_APP_ID);
params.setApiKey(YOUR_API_KEY);
params.setDeviceName(YOUR_DEVICE_NAME);
params.setRequestTime(String.valueOf(System.currentTimeMillis()));
params.setPayMode(PayMode.LICENSE.getPayMode());
params.setTokenType("MMI");
DeviceAuthClient.getInstance().getToken(params, new GetTokenCallBack() {
    @Override
    public void success(String tokenInfo) {
        Log.d(TAG, "getToken success: " + tokenInfo);
    }

    @Override
    public void fail(ResultError error) {
        Log.e(TAG, error.getMessage());
    }
});
```

### 3.4. 获取License标识签名

**入参：**

**字段**

**类型**

**默认值**

**必填**

**说明**

params

LicenseSignatureParams

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

设备唯一标识，通过 DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId() 获取

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
/// 获取license标识签名
String taskId = UUID.randomUUID().toString().replace("-", "");
LicenseSignatureParams params = new LicenseSignatureParams(authParams.getAppid(), YOUR_DEVICE_NAME, taskId);
JSONObject licenseInfoSignature = DeviceAuthClient.getInstance().getLicenseSignature(params);
// 返回包含timestamp和license_info、device_info的JSON字符串
```

### 3.5. 设备重置 deviceReset

tips: 在百炼控制台重置设备后，需要调用SDK deviceReset接口重置设备，可以进行重新注册。

**入参：**

无

**出参：**

Boolean 是否重置成功

**调用示例：**
```
boolean result = DeviceAuthClient.getInstance().deviceReset();
 if (!result) {
     showToast("设备重置失败");
 } else {
     showToast("设备重置成功，可以重新注册");
 }
```

### 3.6. 设备标识管理 DeviceIdentityManager

`DeviceIdentityManager` 是 SDK 设备标识的唯一推荐 API（单例），提供多级降级策略、历史兼容读取、自定义 namespace、自定义标识注入等能力。已内置旧版 SDK 的全部兼容逻辑，存量设备调用时自动返回旧 ID 原值。

**重要**`DeviceUUIDUtil.getAndroidId(context)` 已标记为弃用（since 1.0.7），内部完全委托给 `DeviceIdentityManager`，现有代码无需立即修改但建议逐步迁移至 `DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId()`。

#### 3.6.1. API 列表

方法

说明

`DeviceIdentityManager.getInstance()`

获取单例实例

`DeviceIdentity getDeviceIdentity(Context context)`

获取设备标识，namespace 默认为应用包名

`DeviceIdentity getDeviceIdentity(Context context, String namespace)`

获取设备标识，使用自定义 namespace 覆盖默认包名盐（传 null 使用默认包名）

`void setCustomIdentity(String identity)`

注入自定义设备标识，作为最高优先级标识按原值使用（不做派生）；传 null 清除；超过 40 字符将抛出 `IllegalArgumentException`

`void setOnIdentityResolvedListener(OnIdentityResolvedListener listener)`

设置标识解析完成回调，每次解析出设备标识后（包括缓存命中）触发；传 null 移除回调

`void clearCache(Context context)`

清除内存缓存及 MediaDrm ID 的磁盘缓存，下次获取时重新从设备获取并派生。注意：Fallback UUID 不会被此方法清除

#### 3.6.2. DeviceIdentity 返回值说明

方法

返回值

说明

`getId()`

String

最终选定的设备标识（派生后的应用级标识，CUSTOM 来源时为注入的原值），最大长度 40 字符

`getSource()`

IdentitySource

标识来源枚举，见下表

#### 3.6.3. IdentitySource 枚举说明

枚举值

说明

CUSTOM

自定义标识（外部注入），按原值使用

MEDIA\_DRM

MediaDrm ID（设备唯一，重装不变，出厂重置后变化）

ANDROID\_ID

Android ID（设备唯一，重装不变，出厂重置后变化）

FALLBACK\_UUID

随机UUID（卸载后变化）——⚠️ **仅限测试环境使用**

#### 3.6.4. 调用示例

```
// 1. 默认 namespace（应用包名）获取设备标识（推荐用于 deviceName）
DeviceIdentity identity = DeviceIdentityManager.getInstance().getDeviceIdentity(context);
String deviceId = identity.getId();                 // 40 字符固定长度哈希（CUSTOM 时为原值）
IdentitySource source = identity.getSource();       // 标识来源

// 2. 自定义 namespace（多个应用使用相同 namespace + 相同签名时可共享标识，参见第 8 节）
DeviceIdentity shared = DeviceIdentityManager.getInstance().getDeviceIdentity(context, "com.example.shared");

// 3. 注入服务端下发的自定义标识（最高优先级，按原值使用）
DeviceIdentityManager.getInstance().setCustomIdentity(identityFromServer);

// 4. 监听标识解析结果
DeviceIdentityManager.getInstance().setOnIdentityResolvedListener(new OnIdentityResolvedListener() {
    @Override
    public void onIdentityResolved(DeviceIdentity identity) {
        Log.d(TAG, "identity resolved: " + identity.getId() + ", source=" + identity.getSource());
    }
});

// 5. 清除缓存，下次获取时重新解析
DeviceIdentityManager.getInstance().clearCache(context);
```

## 4\. 集成SDK及依赖库

使用最新版本 Android SDK，引用其中的 `multimodal_dialog_tongyimetathings-<版本号>.aar`

本文档中出现的 `<版本号>`为占位符，请替换为您实际拿到的文件名。

各版本的变更内容与升级影响请查阅 10 节「版本发布记录」。

### 4.1. Gradle 集成步骤

1.  将 `multimodal_dialog_tongyimetathings-<版本号>.aar` 放入 app 模块的 `libs/` 目录。
2.  在 app 模块的 `build.gradle` 中添加依赖：

```
dependencies {
    implementation fileTree(dir: 'libs', include: ['*.aar'])
    // 或显式引用：
    // implementation files('libs/multimodal_dialog_tongyimetathings-<版本号>.aar')

    // 必需：AAR 不内联第三方依赖，以下依赖必须由接入方显式声明
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
}
```

1.  确认 `minSdkVersion` 不低于 24（Android 7.0）：

```
android {
    defaultConfig {
        minSdkVersion 24
    }
}
```

1.  Sync 工程后即可使用 SDK 接口。

**关于第三方依赖（必读）**：AAR 格式不内联依赖，SDK 产物 `classes.jar` 中**只包含 SDK 自身类**，不含 okhttp 的任何类。因此上述依赖必须在 app 模块中显式声明，否则 SDK 在发起设备注册、获取 Token 等网络请求时会抛出 `NoClassDefFoundError`。

依赖

依赖版本

版本要求

`com.squareup.okhttp3:okhttp`

4.12.0

**必须为 4.x**，okhttp 3.x 与 4.x API 不兼容，使用 3.x 会导致运行期异常

若您的工程已引入上述依赖，无需重复声明，但请确认 okhttp 大版本为 4.x。

### 4.2. 混淆规则

若工程开启了代码混淆（ProGuard/R8），请在混淆配置文件中添加以下 keep 规则，避免设备标识相关类被混淆或裁剪：

```
-keep class com.aliyun.bailian.billingsignature.identity.DeviceIdentityManager { *; }
-keep class com.aliyun.bailian.billingsignature.identity.DeviceIdentity { *; }
-keep class com.aliyun.bailian.billingsignature.identity.IdentitySource { *; }
-keep class com.aliyun.bailian.billingsignature.identity.OnIdentityResolvedListener { *; }
-keep class com.aliyun.bailian.billingsignature.utils.DeviceUUIDUtil { *; }
```

## 5\. 涉及多模态SDK接入修改

1.  在启动会话前完成tongyimetathings SDK的初始化和检测设备是否注册，未注册执行设备注册，具体参考接入示例工程。
2.  初始化该 SDK，设备注册完成后获取多模态会话 token：全托管模式参考上述 3.3.3 节（getToken）接口，半托管模式参考上述 3.2.2 节接口，将 getToken 接口返回的 dashToken 数据设置为 apiKey，具体参考示例工程。

```
multimodalParams.setApiKey(jsonObject.getString("dashToken"));
```

1.  创建会话时传入license计费标识,参考接入示例：

```
private MultiModalRequestParam buildRequestParams() {

    MultiModalRequestParam.UpStream.ReplaceWord replaceWord = new MultiModalRequestParam.UpStream.ReplaceWord();
    replaceWord.setTarget("一加一");
    replaceWord.setSource("1加1");
    replaceWord.setMatchMode("partial");
    String deviceName = DeviceIdentityManager.getInstance().getDeviceIdentity(this).getId();
    taskId = UUID.randomUUID().toString().replace("-", "");
    //构建License计费标识
    LicenseSignatureParams params = new LicenseSignatureParams(authParams.getAppid(), deviceName, taskId);
    JSONObject licenseInfoSignature = DeviceAuthClient.getInstance().getLicenseSignature(params);
    Map<String, Object> map = new HashMap<>();
    map.put("signature", licenseInfoSignature);
    return MultiModalRequestParam.builder()
            .clientInfo(MultiModalRequestParam.ClientInfo.builder()
                    .device(MultiModalRequestParam.ClientInfo.Device.builder()
                            .uuid(deviceName).build()) // 请配置为您的设备UUID
                    .userId("123")  //userid 需要每个用户唯一，建议使用设备UUID。 对话历史会使用 userId关联
                    .passThroughParams(map) //传入License计费标识
                    .build())
            .upStream(MultiModalRequestParam.UpStream.builder()
                    .mode(authParams.getDialogMode().getValue())
                    .type("AudioAndVideo")
                    .asrPostProcessing(Collections.singletonList(replaceWord))
                    .build())
            .downStream(MultiModalRequestParam.DownStream.builder()
                    .voice(mVoiceType) //tts 音色对应的模型需要和管控台配置的模型一致。longxiaochun_v2对应了cosyvoice_v2
                    .sampleRate(48000)
                    .intermediateText(textStreamFeedback ? "dialog" : "transcript")
                    .build())
            .build();
}
```

## 6\. 权限说明

SDK 运行所需权限：

权限

用途

必需性

`android.permission.INTERNET`

设备注册、获取 Token 等网络请求

必需

`android.permission.WRITE_EXTERNAL_STORAGE`

writeDeviceInfo 持久化设备注册信息到外部公共目录

Android 10 以下必需

`android.permission.READ_EXTERNAL_STORAGE`

读取已持久化的设备注册信息（deviceIsRegistered 判断）

Android 10 以下必需

`android.permission.MANAGE_EXTERNAL_STORAGE`

存量设备卸载重装后读取外部存储中的旧设备标识和注册信息

Android 11+ 必需

**AndroidManifest.xml 声明示例：**
```
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
    android:maxSdkVersion="28" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
    android:maxSdkVersion="28" />
<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
```

## 7\. 设备 ID 格式与稳定性说明

来源

格式

长度

卸载重装

恢复出厂

CUSTOM

原值

≤40

取决于接入方

取决于接入方

MEDIA\_DRM

SHA-256派生

40

不变

可能变化

ANDROID\_ID

SHA-256派生

40

不变

变化

FALLBACK\_UUID

SHA-256派生

40

⚠️ 变化（仅限测试）

变化

说明：

-   旧版 SDK 已注册设备的历史 ID 按原值保留（不做派生），不会因升级 SDK 而变化。

## 8\. 多应用共享设备标识

默认情况下，派生使用的 namespace 为**应用包名**，因此同一台设备上不同应用获取到的设备 ID **互不相同**（应用级隔离）。

如果多个应用需要共享同一个设备标识（例如同一厂商的多个应用共用设备注册记录），可采用以下方案：

1.  **相同 namespace + 相同签名**：多个应用调用 `getDeviceIdentity(context, "相同的namespace")` 传入相同的自定义 namespace，且各应用使用**相同的签名**（Android 8.0+ 的 `ANDROID_ID` 按「设备 + 应用签名」隔离，签名不同的应用取到的 ANDROID\_ID 不同，会导致派生结果不一致）。
2.  **服务端统一下发**：由接入方服务端生成统一设备 ID，各应用启动后通过 `DeviceIdentityManager.getInstance().setCustomIdentity(id)` 注入，作为最高优先级标识按原值使用。

**Android 8.0+ ANDROID\_ID 签名隔离机制说明**：自 Android 8.0（API 26）起，`Settings.Secure.ANDROID_ID` 的取值与「设备 + 应用签名密钥 + 用户」绑定，同一设备上不同签名的应用获取到的 ANDROID\_ID 不同。因此跨应用共享标识时，要么保证签名一致，要么采用服务端下发（`setCustomIdentity`）方案。

## 9\. 常见问题 FAQ

### Q: DeviceUUIDUtil 和 DeviceIdentityManager 什么区别？

**A:** `DeviceIdentityManager` 是唯一推荐的设备标识 API，已内置历史兼容逻辑。`DeviceUUIDUtil` 已标记为弃用，内部完全委托给 `DeviceIdentityManager`，现有代码无需立即修改但建议逐步迁移。迁移方式：将 `DeviceUUIDUtil.getAndroidId(context)` 替换为 `DeviceIdentityManager.getInstance().getDeviceIdentity(context).getId()` 即可，存量设备 ID 不会变化。

### Q: FALLBACK\_UUID 可以用于生产环境吗？

**A:** ⚠️ **不可以。** FALLBACK\_UUID 仅适用于测试环境。该模式基于随机 UUID 持久化到 SharedPreferences，应用卸载重装后标识会发生变化，无法保证设备唯一性，生产环境中将导致以下问题：

-   设备重复注册，消耗 License 配额
-   Token 链路与旧设备标识绑定失效，业务交互中断
-   设备计量数据不连续，影响运营统计

**建议做法**：在生产环境中，如果检测到 `identity.getSource() == IdentitySource.FALLBACK_UUID`，应：

1.  通过 `DeviceIdentityManager.getInstance().setCustomIdentity(stableId)` 注入稳定标识（如服务端下发的设备 ID 或 OAID）；
2.  或向用户提示设备不兼容，引导联系支持。

## 10\. 版本发布记录

本栏目记录各版本对接入方可见的变更。

版本号

versionCode

主要变更

升级影响

1.0.7

202608012

1\. 新增设备标识管理接口 `DeviceIdentityManager`，支持自定义标识注入、命名空间派生（详见 3.6 节）  
2\. 设备标识持久化改为应用私有存储（SharedPreferences），设备标识获取不再需要外部存储权限；设备注册信息持久化仍使用外部公共目录（详见 6 节）  
3\. 设备 ID 采用多级降级策略（MEDIA\_DRM → ANDROID\_ID → FALLBACK\_UUID）并统一为 40 字符派生值（详见 7 节）  
4\. `DeviceUUIDUtil` 标记为弃用，推荐直接使用 `DeviceIdentityManager`

**兼容升级**。存量已注册设备的历史 ID 按原值自动兼容读取，`deviceName` 保持不变，无需重新注册；

1.0.6

20260724

优化 IPv6 优先连接逻辑，提升双栈网络环境下的连接建立效率

无接口变更，直接替换 AAR

1.0.5

20260610

优化 OkHttpClient 连接配置，支持 IPv6 优先连接

无接口变更，直接替换 AAR

1.0.4

20260602

`DeviceRegisterParams` 新增 `workspaceId` 字段，支持按工作空间额度注册设备（详见 3.3 节）

新增可选字段，不影响存量调用

1.0.3

20260413

1\. 支持自定义存储路径存储设备相关信息  
2\. SDK 版本号动态关联至 `BuildConfig.SDK_VERSION`

无接口变更，直接替换 AAR

1.0.2

20260326

so 库同时支持 `armeabi-v7a` 与 `arm64-v8a` 两种 CPU 架构

无接口变更，直接替换 AAR

1.0.1

20250808

初始版本发布：  
1\. 半托管模式：设备注册签名（`genRegisterReq`）、设备信息写入（`writeDeviceInfo`）、Token 请求签名（`genGetTokenReq`）、Token 响应解签（`getToken`）  
2\. 全托管模式：设备注册（`deviceRegister`）、获取 Token（`getToken`）  
3\. License 标识签名（`getLicenseSignature`）、设备重置（`deviceReset`）、注册状态查询（`deviceIsRegistered`）  
4\. 基于 Native so 库的通信安全保障

—
