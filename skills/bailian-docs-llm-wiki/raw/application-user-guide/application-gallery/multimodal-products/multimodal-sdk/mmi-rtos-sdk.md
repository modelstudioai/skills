# RTOS C SDK（License模式）

本文介绍如何使用阿里云百炼大模型服务提供的嵌入式C SDK进行实时多模态交互。重点说明了在License模式下如何进行设备管理与实时多模态交互，包括SDK下载和安装，License模式下全托管和半托管方式，云端和设备端关键接口及代码示例。

## **前提条件**

**重要**

1.  开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
2.  根据[应用创建](https://help.aliyun.com/zh/model-studio/multimodal-app-creation)的文档完成应用创建。
    
3.  根据[应用配置](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration)的文档完成应用的配置。
    
4.  License模式[产品计费](https://help.aliyun.com/zh/model-studio/product-billing)
    

-   已适配的硬件列表
    

**序号**

**硬件平台信息**

**SDK包下载地址**

**厂商**

**芯片平台**

**架构**

**发布版本**

1

爱旗

AiW626X

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/putaja/qwen_sdk_core_aiw626x_v1.1.0_f83856a_663682.tar.gz)

2

翱捷

ASR1606

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/hzflir/qwen_sdk_core_asr1606_v1.1.0_f83856a_663876.tar.gz)

3

博通

BK7252

Armv8

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/kbgjhu/qwen_sdk_core_bk7252_v1.1.0_f83856a_663682.tar.gz)

博通

BK7258

Armv8

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/hsfhex/qwen_sdk_core_bk7258_v1.1.0_f83856a_663682.tar.gz)

4

创芯慧联

LM600

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/zulajo/qwen_sdk_core_lm600_v1.1.0_f83856a_663682.tar.gz)

创芯慧联

LM620

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/sgkkui/qwen_sdk_core_lm620_v1.1.0_f83856a_663682.tar.gz)

5

海思

AV100

Armv8

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/gpmroe/qwen_sdk_core_av100_v1.1.0_f83856a_663683.tar.gz)

海思

AV200

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/hbskay/qwen_sdk_core_av200_v1.1.0_f83856a_663683.tar.gz)

海思

Hi3516CV610

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/wrveqg/qwen_sdk_core_hi3516cv610_v1.1.0_f83856a_663683.tar.gz)

6

杰理

AC7911

PI32V2

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/iewmpy/qwen_sdk_core_ac7911_v1.1.0_f83856a_663683.tar.gz)

杰理

JL7014

PI32V2

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/beuivk/qwen_sdk_core_jl7014_v1.1.0_f83856a_663683.tar.gz)

7

君正

G32S10M

RISC-V 32

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/xupulu/qwen_sdk_core_g32s10m_v1.1.0_f83856a_663683.tar.gz)

君正

T23

MIPS32

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/gbameh/qwen_sdk_core_t23_v1.1.0_f83856a_663683.tar.gz)

8

乐鑫

ESP32

LX6

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/rmrpcj/qwen_sdk_core_esp32_v1.1.0_f83856a_663692.tar.gz)

乐鑫

ESP32S3

LX7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/ngnmtd/qwen_sdk_core_esp32s3_v1.1.0_f83856a_663692.tar.gz)

9

全志

F133

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/htlzps/qwen_sdk_core_f133_v1.1.0_f83856a_663683.tar.gz)

全志

R128

RISC-V 64

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/jcjfjn/qwen_sdk_core_r128_v1.1.0_f83856a_663683.tar.gz)

全志

V821

RISC-V 32

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/hizxie/qwen_sdk_core_v821_v1.1.0_f83856a_663683.tar.gz)

全志

V853

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/nqcbob/qwen_sdk_core_v853_v1.1.0_f83856a_663683.tar.gz)

全志

XR872

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/fqlccy/qwen_sdk_core_xr872_v1.1.0_f83856a_663683.tar.gz)

10

瑞芯微

RK3506

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/kzebca/qwen_sdk_core_rk3506_v1.1.0_f83856a_663683.tar.gz)

瑞芯微

RK3588

Armv8

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/dfcbyn/qwen_sdk_core_rk3588_v1.1.0_f83856a_663683.tar.gz)

11

瑞昱

RTL8711

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/wknhlt/qwen_sdk_core_rtl8711_v1.1.0_f83856a_663683.tar.gz)

瑞昱

RTL8721

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/mzsatw/qwen_sdk_core_rtl8721_v1.1.0_f83856a_663683.tar.gz)

12

芯迈微

XMW718

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/dmqvat/qwen_sdk_core_xmw718_v1.1.0_f83856a_663683.tar.gz)

13

星宸科技

SSC309QL

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/oazrqt/qwen_sdk_core_ssc309ql_v1.1.0_f83856a_663683.tar.gz)

14

星翼科技

XY4100LC

RISC-V 32

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/myfote/qwen_sdk_core_xy4100lc_v1.1.0_f83856a_663876.tar.gz)

15

移芯

EC718PM

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/tnoccs/qwen_sdk_core_ec718pm_v1.1.0_f83856a_663877.tar.gz)

16

紫光展锐

UMS9117

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/rqymtg/qwen_sdk_core_ums9117_v1.1.0_f83856a_663878.tar.gz)

紫光展锐

W217

Armv7

v1.1.0

[SDK下载链接](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251222/fgwopl/qwen_sdk_core_w217_v1.1.0_f83856a_663879.tar.gz)

## 1\. 接入模式说明

#### **半托管模式**

适用场景：客户未来有后运营/设备升级等需求的。客户自有云服务，能对自己的设备进行管理和鉴权，客户云服务和设备端有双向通信通道；

**警告**

同一个DeviceName注册过后，无法再次注册去获取设备证书

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1975660571/p966440.jpeg)

-   服务端开发：
    
    -   参考[云端接口说明](#557a524795xam)部分完成云端接口对接，设备计量管理服务提供设备注册和获取Token两个接口
        
-   设备端开发
    
    -   参考[芯片平台HAL层对接](#GiY73)部分进行芯片适配（若采用阿里云推荐芯片/模组，则可以省略此步骤）
        
    -   参考[设备端业务逻辑对接](#3ba890579dmb9)部分在集成SDK后完成业务逻辑开发，设备按**一型一密**进行注册，设备预置创建应用时生成的AppId和AppSecret
        

#### **全托管模式**

适用场景：客户一次性售卖硬件无后向运营需求，且客户没有云服务，无法对设备进行管理，由阿里云进行设备管理和鉴权。

**警告**

同一个DeviceName注册过后，无法再次注册去获取设备证书

![yuque\_diagram (3)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7496264571/p987882.jpg)

-   服务端开发：
    
    -   无
        
-   设备端开发
    
    -   参考[芯片平台HAL层对接](#GiY73)部分进行芯片适配（若采用阿里云推荐芯片/模组，则可以省略此步骤）
        
    -   参考[设备端业务逻辑对接](#3ba890579dmb9)部分在集成SDK后完成业务逻辑开发，设备按**一型一密**进行注册，设备预置创建应用时生成的AppId和AppSecret
        

**说明**

1.  **什么是一型一密？**
    
    就是同一产品型号下所有设备预烧录相同的产品信息（AppId、AppSecret）。当设备到计量管理服务进行注册时，会对其携带的设备信息（AppId、AppSecret、DeviceName）进行认证。认证通过后，会下发设备唯一的设备证书（即三元组AppId、DeviceName和DeviceSecret），后续设备通过该证书才能完成后续所有通信链路的鉴权。
    

1.  **如何查看AppId和AppSecret？**
    
    在我的应用界面能够直接复制应用ID（AppID）。在配置应用按钮边上有三个小点的按钮，点击后能够查看AppSecret**（购买License之后才会有）**
    
    ![截屏2025-08-04 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7496264571/p993335.png)
    

## 2\. 云端接口开发说明

#### **导入依赖包**

java版本

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>bailianmodelonchip20240816</artifactId>
  <version>1.4.0</version>
</dependency>
```

**说明**

maven仓库地址：[https://repo1.maven.org/maven2](https://repo1.maven.org/maven2)

endPoint：bailianmodelonchip.cn-beijing.aliyuncs.com

regionId：cn-beijing

python版本

```
pip install alibabacloud-bailianmodelonchip20240816==1.0.2
```

### **2.1 设备注册接口** deviceRegister

在设备首次联网后，设备需要通过客户云服务调用该接口，向百炼设备计量管理服务进行注册，以获取设备的三元组信息。鉴权采用阿里云POP网关鉴权，需集成POP SDK

**接口入参：DeviceRegisterRequest对象**

**参数**

**类型**

**必填**

**描述**

nonce

String

是

设备端上传的16字节随机数（32字符)，参考[设备注册接口](#Gejwz)

appId

String

是

产品标识，在百炼控制台创建应用之后会生成该ID

requestTime

String

是

设备端上传的请求时间戳（ms），参考[设备注册接口](#Gejwz)

signature

String

是

JSON加密信息，由设备端生成并上传，参考[设备注册接口](#Gejwz)

**接口出参：DeviceRegisterResponseBody对象**

**参数**

**类型**

**必填**

**描述**

code

String

是

错误码

httpStatusCode

Integer

是

http状态码

200 成功

其他 失败

message

String

是

错误信息

requestId

String

是

请求ID

success

Boolean

是

成功标志

data

DeviceRegisterResponseBodyData

是

注册结果，直接透传给设备端

**DeviceRegisterResponseBodyData**

**参数**

**类型**

**描述**

nonce

String

16字节随机数（32字符)

responseTime

String

响应时间戳（ms）

appId

String

产品标识

deviceName

String

设备唯一标识

signature

String

设备三元组信息，设备端SDK可解析，参考[设备注册接口](#Gejwz)

Java示例

```
package pop;

import com.alibaba.fastjson.JSON;
import com.aliyun.bailianmodelonchip20240816.Client;
import com.aliyun.bailianmodelonchip20240816.models.*;
import com.aliyun.teaopenapi.models.Config;

public class DeviceTest {

    public static void main(String[] args) {
        Config config = new Config();
        config.setAccessKeyId("your-ak");
        config.setAccessKeySecret("your-as");
        config.setEndpoint("bailianmodelonchip.cn-beijing.aliyuncs.com");

        try {
            Client client = new Client(config);
            deviceRegister(client);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void deviceRegister(Client client) throws Exception {
        DeviceRegisterRequest request = new DeviceRegisterRequest();
        request.setNonce("Your Nonce");
        request.setRequestTime("1748312026868");
        request.setAppId("Your AppId");
        request.setSignature("Your Signature");

        DeviceRegisterResponse response = client.deviceRegister(request);
        DeviceRegisterResponseBody.DeviceRegisterResponseBodyData data = response.getBody().getData();
        
        //以json格式，透传data给设备端，厂商自行实现
        System.out.println("透传结果：" + JSON.toJSONString(data));
    }
}
```

Python示例

```
import sys
from typing import List

from Tea.exceptions import UnretryableException, TeaException
from alibabacloud_bailianmodelonchip20240816 import models as bailian_model_on_chip_20240816_models
from alibabacloud_bailianmodelonchip20240816.client import Client as BailianModelOnChip20240816Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

class PopDeviceRegister:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> BailianModelOnChip20240816Client:
        config = open_api_models.Config(
            access_key_id='your-ak',
            access_key_secret='your-as'
        )

        config.endpoint = f'bailianmodelonchip.cn-beijing.aliyuncs.com'
        return BailianModelOnChip20240816Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = PopDeviceRegister.create_client()
        device_register_request = bailian_model_on_chip_20240816_models.DeviceRegisterRequest(
            nonce='Your Nonce',
            request_time='1750313647162',
            app_id='Your AppId',
            signature='Your Signature'
        )
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.device_register_with_options(device_register_request, headers, util_models.RuntimeOptions())
            print('body', res.body)
            if res.body.success:
                print('data', res.body.data)
        except UnretryableException as e:
            # 网络异常
            print(e)
        except TeaException as e:
            # 业务异常
            print(e)
        except Exception as e:
            # 其他异常
            print(e)

if __name__ == '__main__':
    PopDeviceRegister.main(sys.argv[1:])
```

**重要**

1.  **your-ak**和**your-as**可从阿里云官网控制台获取，具体请参见：[链接](https://ram.console.aliyun.com/profile/access-keys)
    
2.  **endPoint**：bailianmodelonchip.cn-beijing.aliyuncs.com
    
3.  DeviceRegisterResponseBodyData需要通过JSON.toJSONString转换成json格式，再下发给设备端，这部分逻辑需要厂商自行实现
    

### **2.2 获取访问业务交互令牌接口** getToken

设备完成注册之后，在使用多模态交互相关能力时需要动态获取访问令牌，可以通过该接口从百炼设备计量管理服务获取对应的令牌。采用阿里云POP网关鉴权，需集成POP SDK

**接口入参：**

**GetTokenRequest**

**参数**

**类型**

**必填**

**描述**

nonce

String

是

16字节随机数（32字符)

appId

String

是

应用标识，在百炼控制台创建应用之后会生成该ID

deviceName

String

是

从设备上传的设备唯一标识

requestTime

String

是

请求时间戳（ms）

signature

String

是

JSON加密信息，由设备端SDK生成，参考[获取交互令牌接口](#Yo6VT)

tokenType

String

是

请求令牌的类型（当前仅支持MMI类型）

MMI：多模态交互令牌

tokenKey

String

是

用来换取令牌的Key，需要根据不同的令牌类型传递不同的值（当前仅支持MMI类型）

MMI：传入百炼的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)

**接口出参**

**GetTokenResponseBody**

**参数**

**类型**

**必填**

**描述**

code

String

是

错误码

httpStatusCode

Integer

是

http状态码

200 成功

其他 失败

message

String

是

错误信息

requestId

String

是

请求ID

success

Boolean

是

成功标志

data

GetTokenResponseBodyData

是

结果，可直接透传给设备端解析，参考[获取交互令牌接口](#Yo6VT)

**GetTokenResponseBodyData**

**参数**

**类型**

**描述**

nonce

String

16字节随机数（32字符)

responseTime

String

响应时间戳（ms）

appId

String

应用标识

deviceName

String

设备唯一标识

signature

String

token加密信息，设备端SDK可解析

Java示例

```
package pop;

import com.alibaba.fastjson.JSON;
import com.aliyun.bailianmodelonchip20240816.Client;
import com.aliyun.bailianmodelonchip20240816.models.*;
import com.aliyun.teaopenapi.models.Config;

public class TokenTest {

    public static void main(String[] args) {
        Config config = new Config();
        config.setAccessKeyId("your-ak");
        config.setAccessKeySecret("your-as");
        config.setEndpoint("bailianmodelonchip.cn-beijing.aliyuncs.com");

        try {
            Client client = new Client(config);
            getToken(client);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void getToken(Client client) throws Exception {
        GetTokenRequest request = new GetTokenRequest();
        request.setNonce("Your Nonce");
        request.setRequestTime("1748570866553");
        request.setAppId("Your AppId");
        request.setDeviceName("Your DeviceName");
        request.setTokenType("MMI");
        request.setTokenKey("Your TokenKey");
        request.setSignature("Your Signature");

        GetTokenResponse response = client.getToken(request);
        GetTokenResponseBody.GetTokenResponseBodyData data = response.getBody().getData();
        
        //以json格式，透传data给设备端，厂商自行实现
        System.out.println("执行结果：" + JSON.toJSONString(data));
    }
}
```

Python示例

```
import sys
from typing import List

from Tea.exceptions import UnretryableException, TeaException
from alibabacloud_bailianmodelonchip20240816 import models as bailian_model_on_chip_20240816_models
from alibabacloud_bailianmodelonchip20240816.client import Client as BailianModelOnChip20240816Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

class PopGetToken:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> BailianModelOnChip20240816Client:
        config = open_api_models.Config(
            access_key_id='your-ak',
            access_key_secret='your-as'
        )

        config.endpoint = f'bailianmodelonchip.cn-beijing.aliyuncs.com'
        return BailianModelOnChip20240816Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = PopGetToken.create_client()
        get_token_request = bailian_model_on_chip_20240816_models.GetTokenRequest(
            nonce='Your Nonce',
            request_time='1750313823168',
            app_id='Your AppId',
            device_name='Your DeviceName',
            token_type='MMI',
            token_key='Your Token Key',
            signature='Your Signature'
        )
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.get_token_with_options(get_token_request, headers, util_models.RuntimeOptions())
            print('body', res.body)
            if res.body.success:
                print('data', res.body.data)
        except UnretryableException as e:
            # 网络异常
            print(e)
        except TeaException as e:
            # 业务异常
            print(e)
        except Exception as e:
            # 其他异常
            print(e)

if __name__ == '__main__':
    PopGetToken.main(sys.argv[1:])
```

**重要**

1.  **your-ak**和**your-as**可从阿里云官网控制台获取，具体请参见：[链接](https://ram.console.aliyun.com/profile/access-keys)
    
2.  **endPoint**：bailianmodelonchip.cn-beijing.aliyuncs.com
    
3.  GetTokenResponseBodyData需要通过JSON.toJSONString转换成json格式，再下发给设备端，这部分逻辑需要厂商自行实现
    

### **2.3 云端错误码**

**错误码**

**错误说明**

**处理方法**

100007

产品没有额度可激活的设备

购买额度

100008

设备已注册

检查设备唯一标识是否已注册，或修改设备唯一标识

100009

设备未注册

注册设备

100010

请求时间需要五分钟内

修改请求时间重新提交

100011

签名为空

检查请求签名数据

100012

设备唯一标识最长32个字符

检查设备唯一标识长度

100013

设备名称无效

设备名称包含非法字符

100023

设备已禁用

百炼平台-设备管理，启用设备

100025

设备已激活不能重复注册

百炼平台-设备管理，重置设备后注册

100032

接入模式不匹配

检查应用接入模式，根据LICENSE和后付费模式修改SDK调用

100033

设备已过额度激活有效期

重新购买额度

200014

额度已耗尽

重新购买额度

200021

设备当日调用量达到最大限制

购买加油包

200022

额度已过期

重新购买额度

300002

请求百炼网关获取令牌失败

检查应用配置

500001

加密数据和请求参数值不匹配

检查加密参数和请求参数值

500002

解密失败

检查加密数据

## 3\. 设备端接口说明

### **3.1. SDK获取**

不同芯片平台需要使用对应平台的toolchain进行编译，目前百炼已经支持的芯片清单，可直接下载SDK。

如果是新的芯片平台，请联系阿里云销售寻求技术支持

**SDK目录结构**

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

**说明**

-   include目录下包含使用SDK所需要的头文件，需要将该目录添加至工程头文件目录下。
    
-   libqwen\_sdk.a包含SDK核心代码，必须加载。
    
-   libc\_license.a包含license模式相关代码，如使用license模式接入必须加载，如使用后付费模式接入不能加载该库。
    
-   libhal\_dummy.a包含dummy hal代码，用于SDK未适配前检查编译环境用，在完成hal移植后建议删除该库。
    
-   libqwen\_test.a包含测试代码，自动化测试过程需要加载该库，正式生产时需要去除。
    
-   libtinycrypt.a包含加解密依赖接口，如果平台未集成该三方库则必须加载。
    
-   libcjson.a包含SDK相关依赖接口，如果平台未集成该三方库则必须加载。
    

### **3.2. 厂商完成HAL层开发**

SDK中抽象了HAL层，需要各个厂商在自己的芯片平台上完成对应的开发

#### **3.2.1. 内存**

```
/**
 * util_malloc - 分配指定大小的内存块。
 * @size: 需要分配的内存大小，以字节为单位。
 *
 * 本函数通过调用标准库函数malloc来分配内存，目的是为了提供一个更健壮的内存分配方法。
 * 它可能包含了额外的错误检查或者内存管理策略，以提高程序的稳定性和性能。
 * 
 * 返回值： 返回指向所分配内存的指针，如果内存分配失败，则返回NULL。
 */
void * util_malloc(int32_t size);

/**
 * 释放动态分配的内存。
 * 
 * 本函数旨在释放之前通过动态分配获得的内存空间，以避免内存泄漏。
 * 它接受一个指向动态分配内存区域的指针，并将其设置为NULL，以防止悬挂指针的出现。
 * 
 * @param ptr 指向动态分配内存区域的指针。如果为NULL，函数将不执行任何操作。
 *            在释放内存后，此指针将被设置为NULL。
 */
void util_free(void *ptr);
```

**警告**

内存数模块为阿里提供的SDK所依赖的模块，需要各厂商在自己的硬件平台上实现

#### **3.2.2. 随机数模块**

```
/**
 * 初始化随机数生成器
 * 
 * @param seed 用于初始化随机数生成器的种子值
 * 
 * @return 返回初始化结果，0表示成功，非0表示失败
 * 
 * 此函数通过对随机数生成器进行初始化，以确保后续生成的随机数序列具有良好的随机性
 * 种子值的选择对生成的随机数序列有重要影响，相同的种子值会生成相同的随机数序列
 */
int32_t util_random_init(uint32_t seed);

/**
 * 生成一个随机数
 * 
 * @return 返回生成的随机数
 * 
 * 在调用此函数之前，应确保随机数生成器已经通过util_random_init函数成功初始化
 * 此函数生成的随机数是基于初始化时提供的种子值产生的
 */
uint32_t util_random(void);
```

**警告**

随机数模块为阿里提供的SDK所依赖的模块，需要各厂商在自己的硬件平台上实现

#### **3.2.3. 存储模块**

```
/**
 * @brief擦除存储器
 * 
 * 该函数用于擦除存储器中的所有数据。在调用此函数之前，应确保不再需要存储器中的任何信息，
 * 因为擦除操作将删除所有数据，且此操作不可逆。
 * 
 * @return int32_t 返回擦除操作的结果。如果返回值为0，表示擦除成功；如果返回值非0，表示擦除过程中出现错误。
 */
int32_t util_storage_erase(void);

/**
 * @brief存储数据到存储器
 * 
 * 该函数将指定的数据存储到存储器中。在调用此函数之前，应确保数据的正确性和完整性，
 * 因为存储操作将覆盖存储器中的现有数据。
 * 
 * @param data 指向要存储的数据的指针。数据类型为uint8_t，即无符号的8位整数。
 * @param size 要存储的数据的大小，以字节为单位。数据类型为uint32_t，即无符号的32位整数。
 * @return int32_t 返回存储操作的结果。如果返回值为0，表示存储成功；如果返回值非0，表示存储过程中出现错误。
 */
int32_t util_storage_storage(uint8_t *data, uint32_t size);

/**
 * @brief从存储器加载数据
 * 
 * 该函数从存储器中加载指定大小的数据。在调用此函数之前，应确保提供的数据指针指向的内存区域足够大，
 * 以容纳从存储器加载的数据。
 * 
 * @param data 指向用于存储从存储器加载的数据的缓冲区的指针。数据类型为uint8_t，即无符号的8位整数。
 * @param size 要加载的数据的大小，以字节为单位。数据类型为uint32_t，即无符号的32位整数。
 * @return int32_t 返回加载操作的结果。如果返回值为0，表示加载成功；如果返回值非0，表示加载过程中出现错误。
 */
int32_t util_storage_load(uint8_t *data, uint32_t size);
```

**警告**

存储模块为阿里提供的SDK所依赖的模块，需要各厂商在自己的硬件平台上实现

#### **3.2.4. 时间模块**

```
/**
 * 获取当前时间戳（毫秒级）
 * 
 * 此函数用于获取当前的时间戳，精确到毫秒该时间戳通常用于计算时间差、
 * 记录事件发生时间等场景
 * 
 * 返回：当前时间戳（毫秒级）
 */
int64_t util_now_ms(void);

/**
 * 毫秒级睡眠函数
 * 
 * 此函数使当前线程暂停执行指定毫秒数，用于控制程序执行节奏、等待事件发生等
 * 
 * 参数 ms：需要暂停的毫秒数
 */
void util_msleep(uint32_t ms);

/**
 * 获取当前时间戳
 * 
 * 此函数用于获取当前的时间戳，即从1970年1月1日00:00:00 UTC开始到现在的毫秒数
 * 它没有输入参数，返回一个int64_t类型的值，代表当前的时间戳
 * 
 * @return int64_t 当前时间戳，单位为毫秒
 */
int64_t util_get_timestamp(void);

/**
 * 检查时间戳功能是否已初始化
 * 
 * 此函数用于检查时间戳相关功能是否已经初始化如果返回真（非零），则表示
 * 时间戳功能可用；如果返回假（零），则可能需要进行初始化操作或者避免使用时间戳功能
 * 
 * 返回：如果时间戳功能已初始化，则返回非零，否则返回零
 */
uint8_t util_timestamp_inited(void);
```

**警告**

时间模块为阿里提供的SDK所依赖的模块，需要各厂商在自己的硬件平台上实现

#### **3.2.5. 互斥锁模块**

```
/* 互斥锁结构体定义 */
typedef struct _util_mutex_t {
    void *mutex_handle; /* 互斥锁句柄，具体实现依赖于平台 */
} util_mutex_t;

/*****************************************************
 * Function: util_mutex_create
 * Description: 创建一个互斥锁对象。
 * Parameter: 无。
 * Return: util_mutex_t * --- 返回指向互斥锁结构体的指针。
 ****************************************************/
util_mutex_t * util_mutex_create(void);

/*****************************************************
 * Function: util_mutex_delete
 * Description: 删除指定的互斥锁对象。
 * Parameter:
 *     mutex --- 指向互斥锁结构体的指针。
 * Return: 无。
 ****************************************************/
void util_mutex_delete(util_mutex_t *mutex);

/*****************************************************
 * Function: util_mutex_lock
 * Description: 对指定的互斥锁进行加锁操作，带超时机制。
 * Parameter:
 *     mutex --- 指向互斥锁结构体的指针。
 *     timeout --- 加锁等待超时的时间，单位为毫秒(ms)，可设为 MUTEX_WAIT_FOREVER 表示无限等待。
 * Return: int32_t --- 返回操作结果(util_result_t)。
 ****************************************************/
int32_t util_mutex_lock(util_mutex_t *mutex, int32_t timeout);

/*****************************************************
 * Function: util_mutex_unlock
 * Description: 对指定的互斥锁进行解锁操作。
 * Parameter:
 *     mutex --- 指向互斥锁结构体的指针。
 * Return: int32_t --- 返回操作结果(util_result_t)。
 ****************************************************/
int32_t util_mutex_unlock(util_mutex_t *mutex);
```

**警告**

互斥锁模块为阿里提供的SDK所依赖的模块，需要各厂商在自己的硬件平台上实现

#### **3.2.6. HAL层移植验收标准**

在实现以上各模块之后，再加载libqwen\_test.a，在主程序中直接调用接口qwen\_sdk\_test接口，就会对以上工作模块进行测试，输出日志可查看测试结果。

将输出日志反馈给阿里云进行确认。

测试成功的输出日志示例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1975660571/p966580.png)

### **3.3. 设备端业务逻辑对接**

**说明**

本SDK兼容license模式与后付费模式

-   当加载libc\_license.a时为license模式
    
-   当不加载libc\_license.a时为后付费模式。
    

**重要**

加载libc\_license.a需要添加编译选项强制加载库中所有符号

以ARM平台编译参数为例，需要做如下配置

```
# 链接器标志
LDFLAGS += -L./YourLibPath \
          -Wl,--whole-archive \
          -lc_license \
          -Wl,--no-whole-archive \
```

**重要**

当使用后付费模式时，在连接多模态网关前，需要在设备上写入API Key或通过用户自有服务获取临时API Key，推荐使用临时API Key方案。

获取临时API Key的方法请参考：[生成临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。

**警告**

当使用license模式（全托管模式）时，需在设备端写入API Key，开发者需自行确保API Key存储及应用安全。

当使用后付费模式时，如在设备上写入API Key，开发者需自行确保API Key存储及应用安全。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9629836671/p1036191.png)

**说明**

对应的模块可参考图中标记的示例代码1-示例代码6，在详细接口说明中找到对应的示例代码

#### **3.3.1. 初始化接口**

```
/**
 * @brief 初始化MMI
 * 
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_sdk_init(void);

/**
 * @brief 配置MMI模块参数
 *
 * 此函数用于初始化MMI模块的各项配置参数，包括事件回调、工作模式、文本模式、
 * 音色设置、音频流模式以及缓冲区大小等
 * 
 * @param config 指向mmi_user_config_t结构体的指针，包含配置参数
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_config(mmi_user_config_t *config);
```

示例代码1

```
#include "c_mmi.h"

mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

// 初始化SDK
c_mmi_sdk_init();

// 必须要配置evt_cb，否则会导致sdk运行异常
mmi_config.evt_cb = _mmi_event_callback;  // 注册事件回调函数，详细说明见下文
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
// 设置音色，需要在 c_mmi_config 后调用
c_mmi_set_voice_id("longxiaochun_v2");
```

#### **3.3.2. 产品信息配置接口**

```
/**
 * @brief 检查设备是否已注册
 * 
 * @return uint8_t 设备注册状态
 *         - 0: 设备未注册
 *         - 1: 设备已注册
 */
uint8_t c_license_device_is_registered(void);

/**
 * @brief 重置配置
 * 
 * 此函数用于清除所有已保存的设备配置信息
 * 调用此函数后，配置将恢复为默认状态，需要重新设置相关参数
 * 
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_reset(void);

/**
 * @brief 保存配置
 * 
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_save(void);

/**
 * @brief 设置AppId
 * 
 * 此函数用于设置AppId，完成设置后需要调用c_mmi_storage_save进行保存
 * 
 * @param app_id_str AppId，由阿里云颁发，字符串格式
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_set_app_id_str(char *app_id_str);

/**
 * @brief 设置ApiKey
 * 
 * 此函数用于设置ApiKey，完成设置后需要调用c_mmi_storage_save进行保存
 * 
 * @param api_key 通过百炼平台获取
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_set_api_key(char *api_key);

/**
 * @brief 设置WorkSpaceId
 * 
 * 此函数用于设置WorkSpaceId，完成设置后需要调用c_mmi_storage_save进行保存
 * 
 * @param ws_id WorkSpaceId，通过百炼平台获取
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_set_ws_id(char *ws_id);

/**
 * @brief 设置设备名称DeviceName
 * 
 * 此函数用于设置设备名称DeviceName，完成设置后需要调用c_mmi_storage_save进行保存
 * 
 * @param dn 设备名称DeviceName，用户可自行设定，长度不超过32字符
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_storage_set_device_name(char *device_name);

/**
 * @brief 设置AppSecret
 * 此函数用于设置AppSecret，完成设置后需要调用c_mmi_storage_save进行保存
 * 
 * @param app_secret AppSecret，由阿里云颁发，字符串格式
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_license_set_app_secret_str(char *app_secret);

/**
 * @brief 初始化mmi
 * 
 * 该函数用于初始化mmi，仅后付费模式需要调用该接口
 * 
 * @param workspace WorkSpaceId，通过百炼平台获取
 * @param app_id AppId，由阿里云颁发，字符串格式
 * @param api_key 通过百炼平台获取
 * 
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_mmi_init(char *workspace, char *app_id, char *api_key);
```

示例代码2.1 后付费模式配置，

```
#include "c_mmi.h"

// 预置AppId
c_mmi_storage_set_app_id_str("Your AppId");
// 预置WorkspaceId
c_mmi_storage_set_ws_id("Your WorkspaceId");
// 预置ApiKey，使用临时ApiKey时可以不用设置该参数
c_mmi_storage_set_api_key("Your ApiKey");
// 预置DeviceName
c_mmi_set_device_name("Your DeviceName");
// 保存配置信息
c_mmi_storage_save();
// 初始化mmi
c_mmi_init("Your WorkspaceId", "Your AppId", "Your ApiKey or Temporary ApiKey");
```

示例代码2.2 License模式配置

```
#include "c_mmi.h"
#include "lib_c_license.h"

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
```

#### **3.3.3. 设备注册接口（后付费模式无需实现该流程）**

```
/**
 * @brief 生成注册字符串
 * 
 * @param buffer 用于存储生成的注册字符串的缓冲区
 * @param buffer_size 缓冲区大小
 * @param time_ms_str 时间戳字符串，单位为毫秒
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_license_gen_register_str(char *buffer, uint32_t buffer_size, char *time_ms_str);

/**
 * @brief 解析云端的设备注册响应信息。
 * 
 * @param rsp_str 指向设备注册响应字符串的指针。
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_license_analyze_register_rsp(char *rsp_str);
```

示例代码3

```
#include "lib_c_license.h"

#define REQ_BUFFER_SIZE  (1024)

char req[REQ_BUFFER_SIZE];
char time_ms_str[14];

if (c_license_device_is_registered() == 0) {
    snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
    // 根据时间戳timestamp，生成注册信息字串req
    c_license_gen_register_str(req, sizeof(req), time_ms_str);
    // 获取设备注册信息，http接口需客户自行实现
    char *rsp = dummy_http_request(req);
    // 解析并完成注册
    int32_t err = c_license_analyze_register_rsp(rsp);
    if (err) {
        return err;
    }
    // 注册成功后需调用存储接口保存注册信息
    c_mmi_storage_save();
}
```

**说明**

**关于示例代码中dummy\_http\_request接口**

-   半托管模式下，该dummy\_http\_request应访问客户已有的设备管理服务端提供的http接口，来间接完成设备端注册
    
-   全托管模式下，该dummy\_http\_request应访问阿里云提供的设备管理服务接口完成设备端注册
    
    -   使用全托管模式时，接入信息如下：
        
        Host: bailian.multimodalagent.aliyuncs.com
        
        Register API: /api/device/v1/register
        

设备端SDK生成的请求数据包示例

```
{
    "appId": "<YOUR APP ID>",
    "deviceName": "<YOUR DEVICE NAME>",
    "nonce": "<YOUR NONCE>",
    "requestTime": "1753326620619",
    "sdkVersion": "0.3.2",
    "signature": "<YOUR SIGNATURE>"
}
```

设备端收到云端透传的数据包示例（如下数据是http回应报文中的data字段）

```
{
  "nonce": "<YOUR NONCE>",
  "responseTime": "1753326621269",
  "appId": "<YOUR APP ID>",
  "deviceName": "<YOUR DEVICE NAME>",
  "signature": "<YOUR SIGNATURE>"
}
```

**说明**

1.  http\_request需客户自行实现，负责从客户云端接收返回的数据
    
2.  最终传递给c\_device\_analyze\_register\_rsp的时候，需要保持rsp示例数据相同的格式
    

#### **3.3.4. 获取交互令牌接口（后付费模式无需实现该流程）**

```
/**
 * @brief 检查token是否已过期。
 * 
 * @return uint8_t 返回1表示token有效，0表示token已过期。
 */
uint8_t c_license_is_token_expire(void);

/**
 * @brief 生成获取token的请求数据。
 *
 * 此函数根据提供的参数生成获取token的请求字符串，用于向服务器请求访问令牌。
 *
 * @param buffer 用于存储生成的请求字符串的缓冲区
 * @param buffer_size 缓冲区的大小
 * @param time_ms_str 时间戳字符串，单位为毫秒
 * @param api_key API密钥字符串，半托管模式api_key设置为NULL
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_license_gen_get_token_str(char *buffer, uint32_t buffer_size, char *time_ms_str, char *api_key);

/**
 * @brief 解析登录响应数据。
 *
 * 解析登录响应字符串，并触发事件：
 * - C_MMI_EVENT_USER_CONFIG: 用户配置初始化
 * - C_MMI_EVENT_DATA_INIT: 数据初始化完成
 *
 * @param rsp_str 包含登录响应的字符串
 * @return int32_t 返回操作结果，0表示成功，非0表示失败
 */
int32_t c_license_analyze_get_token_rsp(char *rsp_str);
```

示例代码4

```
#include "lib_c_license.h"

#define REQ_BUFFER_SIZE  (1024)

char req[REQ_BUFFER_SIZE];
char time_ms_str[14];
char api_key[36] = { 0 };

snprintf(time_ms_str, sizeof(time_ms_str), "%" PRId64, util_get_timestamp());
c_mmi_storage_get_api_key(api_key);
// 根据服务端下发时间戳timestamp，生成注册信息字串req
// 使用全托管模式必须要有api_key
c_license_gen_get_token_str(req, sizeof(req), time_ms_str, api_key);
// 使用半托管模式可以传入NULL
// c_license_gen_get_token_str(req, sizeof(req), time_ms_str, NULL);
// 获取服务端返回设备信息，该接口需客户自行实现
char *rsp = dummy_http_request(req);
// 解析交互令牌
int32_t err = c_license_analyze_get_token_rsp(rsp);
if (err) {
    return err;
}
```

**说明**

**关于示例代码中dummy\_http\_request接口**

-   半托管模式下，该dummy\_http\_request应访问客户已有的设备管理服务端提供的http接口，来间接获取token
    
-   全托管模式下，该dummy\_http\_request应访问阿里云提供的设备管理服务接口完成设备端注册
    
    -   使用全托管模式时，接入信息如下：
        
        Host: bailian.multimodalagent.aliyuncs.com
        
        Register API: /api/token/v1/getToken
        

设备端SDK生成的请求数据包示例

```
{
    "appId":"<YOUR APP ID>",
    "deviceName":"<YOUR DEVICE NAME>",
    "payMode":"LICENSE",
    "requestTime":"1753327457730",
    "sdkVersion":"0.3.2",
    "tokenType":"MMI",
    "signature": "<YOUR SIGNATURE>"
}
```

云端补充完tokenKey字段后，再将请求发给阿里云Pop接口

```
{
    "appId":"<YOUR APP ID>",
    "deviceName":"<YOUR DEVICE NAME>",
    "payMode":"LICENSE",
    "requestTime":"1753327457730",
    "sdkVersion":"0.3.2",
    "tokenType":"MMI",
    "signature": "<YOUR SIGNATURE>",
    "tokenKey": "<YOUR TOKEN KEY>"
}
```

**重要**

当设备将SDK生成数据传输至云端后，在云端需要添加对应的tokenKey字段后，才能访问阿里云提供的接口获取令牌，设备端尽量不存储TokenKey，避免泄露

设备端收到云端透传的数据包示例

```
{
    "nonce": "<YOUR NONCE>",
    "responseTime": "1753327458081",
    "appId": "<YOUR APP ID>",
    "deviceName": "<YOUR DEVICE NAME>",
    "requestIp": "<YOUR IP>",
    "signature": "<YOUR SIGNATURE>"
}
```

**说明**

1.  http\_request需客户自行实现，负责从客户云端接收返回的数据
    
2.  最终传递给c\_mmi\_analyze\_rsp的时候，需要保持rsp示例数据相同的格式
    

#### **3.3.5. 建立业务连接**

```
/**
 * @brief 获取WSS服务器主机名字符串。
 *
 * 此函数返回WSS服务器主机名字符串。
 * 
 * @return char* 返回指向WSS服务器主机名字符串的指针
 */
char *c_mmi_get_wss_host(void);

/**
 * @brief 获取WSS服务器端口字符串。
 *
 * 此函数返回WSS服务器端口字符串。
 * 
 * @return char* 返回指向WSS服务器端口字符串的指针
 */
char *c_mmi_get_wss_port(void);

/**
 * @brief 获取WSS服务API路径字符串。
 *
 * 此函数返回WSS服务API路径字符串。
 * 
 * @return char* 返回指向WSS服务API路径字符串的指针
 */
char *c_mmi_get_wss_api(void);

/**
 * @brief 获取WSS请求头信息字符串。
 *
 * 此函数返回WSS请求头信息字符串。
 * 
 * @return char* 
 *         返回指向WSS请求头信息字符串的指针
 */
char *c_mmi_get_wss_header(void);
```

示例代码5

```
#include "c_mmi.h"

char *wss_host = c_mmi_get_wss_host();
char *wss_port = c_mmi_get_wss_port();
char *wss_api = c_mmi_get_wss_api();
char *wss_header = c_mmi_get_wss_header();

// 建立wss连接，dummy_wss_connect接口需客户自行实现
WSS_HANDLE *wss = dummy_wss_connect(wss_host, wss_port, wss_api, wss_header);
```

**重要**

本 SDK 与云端的 websocket 通信需要建立 TLS隧道，用户需自行做如下配置：

-   TLS 版本要求TLS1.2 或以上
    
-   开启SNI（SERVER NAME INDICATION）
    
-   配置CA证书（GlobalSign Root CA - R3）
    
-   务必通过这三个接口获取websocket建联所需要的端口，API，和header
    
-   wss\_connect、wss\_register\_recv\_func、wss\_register\_send\_func、wss\_send等相关的接口可复用各模商或芯片已有方案，需客户自行实现
    

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

#### **3.3.7. 事件回调**

```
enum {
    C_MMI_EVENT_USER_CONFIG,        // 用户对于sdk的配置应该在该事件回调中实现，如音频缓冲区大小、工作模式、音色等
    C_MMI_EVENT_DATA_INIT,	    // 当SDK完成初始化后触发该事件，可在该事件回调中开始建立业务连接
    C_MMI_EVENT_SPEECH_READY,	    // 当正确建立WSS连接后触发该事件，在push和tap模式下仅在该事件后才可以调用speech start
    C_MMI_EVENT_SPEECH_PREPARE,     // 当SDK已准备好可以开始新一轮对话时触发此事件
    C_MMI_EVENT_SPEECH_START,       // 当SDK开始进行音频上行时触发此事件
    C_MMI_EVENT_SPEECH_RESTART,     // 当SDK重新开始进行音频上行时触发此事件
    C_MMI_EVENT_DATA_DEINIT,	    // 当SDK注销后触发此事件

    C_MMI_EVENT_ASR_START,	    // 当ASR开始返回数据时触发此事件
    C_MMI_EVENT_ASR_INCOMPLETE,	    // 此事件返回尚未完成ASR的文本数据（全量）
    C_MMI_EVENT_ASR_COMPLETE,	    // 此事件返回完成ASR的全部文本数据（全量）
    C_MMI_EVENT_ASR_END,	    // 当ASR结束时触发此事件

    C_MMI_EVENT_LLM_INCOMPLETE,	    // 此事件返回尚未处理完成的LLM文本数据（全量）
    C_MMI_EVENT_LLM_COMPLETE,	    // 此事件返回处理完成的LLM全部文本数据（全量）

    C_MMI_EVENT_TTS_START,          // 当开始音频下行时触发此事件
    C_MMI_EVENT_TTS_END,	    // 当音频完成下行时触发此事件

    C_MMI_EVENT_HEARTBEAT,	    // 当SDK收到云端心跳回复时触发此事件
};

/**
 * @brief mmi事件回调函数类型
 *
 * 当mmi模块发生状态变化或事件时触发的回调函数
 * 
 * @param event 事件类型，取值为C_MMI_EVENT_xxx系列宏定义
 * @param param 事件参数，根据事件类型不同指向不同数据结构
 * @return int32_t 返回0表示处理成功，非0表示处理失败
 */
typedef int32_t(*c_mmi_event_callback)(uint32_t event, void *param);
```

**说明**

该回调接口的注册是在初始化阶段c\_mmi\_config配置的时候注册的

#### **3.3.8. 多模态数据交互**

```
/**
 * @brief 向录音缓冲区写入数据
 *
 * @param data 待写入的数据指针
 * @param size 数据长度（字节）
 * @return uint32_t 实际写入的字节数
 */
uint32_t c_mmi_put_recorder_data(uint8_t *data, uint32_t size);

/**
 * @brief 从播放缓冲区读取数据
 *
 * @param data 用于存储读取数据的缓冲区
 * @param size 可用缓冲区大小（字节）
 * @return uint32_t 实际读取的字节数
 */
uint32_t c_mmi_get_player_data(uint8_t *data, uint32_t size);

/**
 * @brief 获取需要通过websocket发送的数据
 * 
 * 本函数用于根据指定的类型获取数据，准备通过websocket进行发送
 * 它会根据传入的类型参数，将相应类型的数据填充到提供的数据缓冲区中
 * 
 * @param opcode 用于返回websocket数据类型，如：WS_DATA_TYPE_TEXT、WS_DATA_TYPE_BINARY
 * @param data 指向一个uint8_t数组的指针，该数组用于存储获取的数据
 * @param size 表示数据数组的最大容量，以字节为单位
 * @return 返回实际填充到数据数组中的字节数
 */
uint32_t c_mmi_get_send_data(uint8_t *opcode, uint8_t *data, uint32_t size);

/**
 * @brief 分析接收到的websocket数据函数
 * 
 * 此函数根据提供的数据类型和数据内容，分析接收到的数据包
 * 它的主要作用是解析数据内容，以便进一步处理或使用
 * 
 * @param opcode websocket数据类型，如：WS_DATA_TYPE_TEXT、WS_DATA_TYPE_BINARY
 * @param data 指向接收到的数据的指针，数据的内容将根据type参数进行解析
 * @param size 数据的长度，以字节为单位，用于确定数据的范围
 * @return 返回实际解析的字节数
 */
uint32_t c_mmi_analyze_recv_data(uint8_t opcode, uint8_t *data, uint32_t size);
```

示例代码6

```
int dummy_wss_task_recv(void)
{
    int opcode;
    char payload_data[8 * 1024];
    int recv_size;

    while(1){
        // 通过websocket接收服务端下行数据
        dummy_wss_recv(&opcode, payload_data, &recv_size);
        if(recv_size)
            // 将接收服务端下行数据送入SDK进行解析
            c_mmi_analyze_recv_data(opcode, payload_data, recv_size);
        else
            util_msleep(10);
    }
    return 0;
}

int dummy_wss_task_send(void)
{
    uint8_t opcode;
    uint8_t payload_data[8 * 1024];
    uint32_t size;

    while(1){
        // 从SDK获取打包好的payload数据
        size = c_mmi_get_send_data(&opcode, payload_data, sizeof(payload_data));
        if (size == 0) {
            util_msleep(10);
        } else {
            // 将payload数据传入websocket发送函数，自行打包帧头进行发送
            dummy_wss_send(opcode, data, size);
        }
    }
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
```

**说明**

在c\_mmi\_analyze\_recv\_data接口中会在SDK内部触发各种事件回调，回调到\_mmi\_event\_callback中，再由用户自己处理
