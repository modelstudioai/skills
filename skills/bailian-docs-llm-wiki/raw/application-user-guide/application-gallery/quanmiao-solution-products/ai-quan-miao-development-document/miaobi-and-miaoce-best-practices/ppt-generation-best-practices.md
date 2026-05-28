# PPT生成最佳实践

本文提供**PPT生成**链路API的最佳实践，帮助您快速入门并开发您自己的业务应用。

**重要**

**调用前须知：**

请通过本地环境直接调用 PPT 流式接口，避免使用阿里云 OpenAPI。

## 1 环境准备

### **后端**

-   点击[PPT生成下单地址](https://common-buy.aliyun.com/?spm=a2c4g.11186623.0.0.24c66c00ZsOBpm&commodityCode=sfm_pptgeneration_public_cn)开通服务；
    
-   [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)；
    
-   [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)；
    
-   引入妙笔SDK [注意获取最新SDK版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)。
    

Java

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>1.0.104</version>
</dependency>
```

Python

```
alibabacloud-tea-openapi-sse==1.0.2
```

JavaScript

```
"@alicloud/openapi-core": "^1.0.2",
"@alicloud/tea-typescript": "^1.7.1",
"@alicloud/openapi-client": "^0.4.12",
```

### **前端**

-   资源地址：https://quanmiao-public.oss-cn-beijing.aliyuncs.com/quanmiao-sdk/v2.0.0/index.js；
    
-   特殊配置：接口请求需要支持refer属性；
    

## **分步骤调用操作步骤**

### **step1：生成PPT大纲**

Java

```
public static AsyncClient getClient() {
    if (client == null) {
        synchronized (ClientHelper.class) {
            if (client == null) {
                StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId("access-key-id")
                            .accessKeySecret("access-key-secret")
                            .build()
            );
            client = AsyncClient.builder()
                    .region("cn-beijing")
                    .credentialsProvider(provider)
                    .serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3))
                    .overrideConfiguration(
                            ClientOverrideConfiguration.create()
                                    .setProtocol("HTTPS")
                                    .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                    )
                    .build();
            }
        }
    }
    return client;
}

AsyncClient client = getClient();
RunPptOutlineGenerationRequest runRequest = RunPptOutlineGenerationRequest.builder()
      .workspaceId(workspaceId)
      .prompt("生成一个关于消防主题的ppt")
      .build();

ResponseIterator<RunPptOutlineGenerationResponseBody> iterator = client.runPptOutlineGenerationWithResponseIterable(runRequest).iterator();
while (iterator.hasNext()) {
    RunPptOutlineGenerationResponseBody event = iterator.next();
    System.out.println(new Date() + " === " + JSON.toJSONString(event));
}
```

Python

```
# 前置要求：
# 1、python版本：3.7+；
# 2、安装依赖：pip3 install alibabacloud-tea-openapi-sse==1.0.2
import os

from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_util_sse import models as util_models
import asyncio
import json

biz_param = ('{"WorkspaceId":"llm-xxxxxx","Prompt":"生成一个关于消防主题的ppt"}')

class AiMiaoBi:
    def __init__(self) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document\_detail/378659.html。
        self.access_key_id = os.environ['accessKeyId']
        self.access_key_secret = os.environ['accessKeySecret']
        # 以上字段请改成实际的值。
        self.endpoint = 'aimiaobi.cn-beijing.aliyuncs.com'
        self._client = None
        self._api_info = self._create_api_info()
        self._runtime = util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = self._create_client(self.access_key_id, self.access_key_secret, self.endpoint)

    def _create_client(
            self,
            access_key_id: str,
            access_key_secret: str,
            endpoint: str,
    ) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint
        )
        return OpenApiClient(config)

    def _create_api_info(self) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称
            action='RunPptOutlineGeneration',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/quanmiao/aimiaosou/runPptOutlineGeneration',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='sse'
        )
        return params

    async def do_sse_query(self):
        if biz_param == '':
            param = {}
        else:
            param: dict = json.loads(biz_param)

        request = open_api_models.OpenApiRequest(
            body=param
        )
        sse_receiver = self._client.call_sse_api_async(params=self._api_info, request=request, runtime=self._runtime)
        return sse_receiver

# 接口调用
async def run():
    aiMiaoBi = AiMiaoBi()
    async for res in await aiMiaoBi.do_sse_query():
        try:
            data = json.loads(res.get('event').data)
            print(data)
        except json.JSONDecodeError:
            print('------json.JSONDecodeError--------')
            print(res.get('headers'))
            print(res.get('event').data)
            print('------json.JSONDecodeError-end--------')
            continue
    print('------end--------')

if __name__ == '__main__':
    asyncio.run(run())
```

JavaScript

```
'use strict';
var __asyncValues = (this && this.__asyncValues) || function (o) {
    if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
    var m = o[Symbol.asyncIterator], i;
    return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
    function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
    function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
};

const OpenApi = require('@alicloud/openapi-core');
const Dara = require('@darabonba/typescript');
class Client {
    /**
     * 使用AK&SK初始化账号Client
     * @return Client
     * @throws Exception
     */
    static createClient() {
        let config = new OpenApi.$OpenApiUtil.Config({
            accessKeyId: 'xxxx',
            accessKeySecret: 'xxxx',
        });
        config.endpoint = `aimiaobi.cn-beijing.aliyuncs.com`;
        return new OpenApi.default(config);
    }
    /**
     * API 相关
     * @param path params
     * @return OpenApi.Params
     */
    static createApiInfo() {
        let params = new OpenApi.$OpenApiUtil.Params({
            // 接口名称
            action: 'RunPptOutlineGeneration',
            // 接口版本
            version: '2023-08-01',
            // 接口协议
            protocol: 'HTTPS',
            // 接口 HTTP 方法
            method: 'POST',
            authType: 'AK',
            style: 'V3',
            // 接口 PATH
            pathname: `/quanmiao/miaosou/runPptOutlineGeneration`,
            // 接口请求体内容格式
            reqBodyType: 'json',
            // 接口响应体内容格式
            bodyType: 'sse',
        });
        return params;
    }

    static async main(args) {
        var _a, e_1, _b, _c;
        let client = Client.createClient();
        let params = Client.createApiInfo();
        let body = { };
        body['WorkspaceId'] = 'llm-xxxxx';
        body['Prompt'] = '生成一个关于消防主题的ppt';
        let request = new OpenApi.$OpenApiUtil.OpenApiRequest({
            body: body,
        });
        try {
            let response = await client.callSSEApi(params, request, new Dara.RuntimeOptions({"readTimeout": 60000, "connectTimeout": 60000}));
            //console.log(response);
            try {
                for (var _d = true, response_1 = __asyncValues(response), response_1_1; response_1_1 = await response_1.next(), _a = response_1_1.done, !_a; _d = true) {
                    _c = response_1_1.value;
                    _d = false;
                    const value = _c;
                    console.log('-'.repeat(30));
                    console.log(value.event);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (!_d && !_a && (_b = response_1.return)) await _b.call(response_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        catch (error) {
            console.log(error);
        }
    }
}
exports.Client = Client;
Client.main(process.argv.slice(2));
```

### **step2：生成PPT内容**

#### [获取PPT组件配置](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptconfig) -- 获取编辑PPT作品所需的code信息

```
AsyncClient client = ClientHelper.getClient();
GetPptConfigRequest request = GetPptConfigRequest.builder()
      .workspaceId(workspaceId)
      .build();
CompletableFuture<GetPptConfigResponse> future = client.getPptConfig(request);
try {
    GetPptConfigResponse response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

#### [初始化PPT创建操作](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreationv2) **-- 获取生成PPT过程中所需参数**

-   **温馨提示：**这个接口涉及到扣费，请注意费用
    
-   **提供信息：**
    
    1.  下发用于初始化“PPT生成”的前端组件的signature；
        
    2.  针对不同场景下发需要的其他参数（如PPT流程ID、作品ID、任务ID）。
        

## **3 创作场景说明**

### **场景一：全链路创建生成PPT**

一站式SaaS解决方案，最接近控制台的SaaS全量功能，可全部交由前端SDK完成。

#### **step1：初始化创建PPT的会话**

##### **后端：**

通过[初始化PPT创建操作](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreationv2)接口初始化创建PPT的会话，如下为示例代码：

```
taskId = "xxxx";

AsyncClient client = ClientHelper.getClient();
InitiatePptCreationV2Request request = InitiatePptCreationV2Request.builder()
      .workspaceId(workspaceId)
      .taskId(taskId)
      .outline("# 中国传统文化艺术的魅力")
      .isMobile(true) // 是否是移动端，按需填入
      .build();
CompletableFuture<InitiatePptCreationV2Response> future = client.initiatePptCreationV2(request);
try {
    InitiatePptCreationV2Response response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

##### **前端：**

全局加载初始化quanmiao-sdk，如下为示例代码：

```
const SDK_URL = "https://quanmiao-public.oss-cn-beijing.aliyuncs.com/quanmiao-sdk/v2.0.0/index.js";
const script = document.createElement('script');
script.src = SDK_URL;
script.async = true;
document.body.appendChild(script);
```

业务链路中调用创建API（后续编辑 / 查看链路参考【场景三】），如下为示例代码：

```
// 确保SDK已经加载完
await window.Quanmiao.createPPT({
    appkey: 'your appkey', // 必填，由服务端API获取
    signature: 'your signature', // 必填，由服务端API获取
    container: document.getElementById('XXX'), // 必填，挂载容器DOM元素
    content: 'PPT大纲内容' , // 必填
    speaker: 'PPT主讲人', // 非必填，默认为 'XXX'
    isMobile: true, // 是否使用移动端模式。非必填，默认为false
    onMessage(type, data) {
      if (type === 'SET_PPT_MAKING_STATUS') {
        if (data?.status === '1') {
          // 正在生成中
        }
        if (data?.status === '0') {
          // 生成完成
        }
      }
      if (type === 'GENERATE_PPT_SUCCESS') {
        // 这里可以拿到PPT的作品id：data?.id
        console.log('作品id', data?.id);
      }
    },
  });
} catch (e) {
  console.log('调用PPT SDK err=>', e);
  message.error(e?.msg || e?.message || '操作异常');
}
```

#### **step2：**绑定PPT作品数据 -- 基于step1中前端SDK获取到的作品id

```
taskId = "6831f55d-fa3b-4592-b3fd-bdf47ca2ab96";

AsyncClient client = ClientHelper.getClient();
BindPptArtifactRequest request = BindPptArtifactRequest.builder()
      .workspaceId(workspaceId)
      .taskId(taskId)
      .artifactId(12345)
      .build();

CompletableFuture<BindPptArtifactResponse> future = client.bindPptArtifact(request);
try {
    BindPptArtifactResponse response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

### **场景二：基于客户定制模板，开始生成PPT**

#### **step1：定制模板 -- 通过全妙官方渠道联系我们**

可以通过[查询企业专属PPT模板列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listenterpriseppttemplates)获取测试模板，试用当前场景效果

#### **step2：基于已有模板生成PPT内容**

##### **后端：**

通过后端API按需获取对应参数，下发参数及示例代码如下：

-   pptProcessId -- 对应前端SDK入参aipptTaskId；
    
-   signature；
    

```
AsyncClient client = ClientHelper.getClient();
InitiatePptCreationV2Request request = InitiatePptCreationV2Request.builder()
        .workspaceId(workspaceId)
        .taskId(UUID.randomUUID().toString())
        .processType(1) //注意这里的类型
        .isMobile(true) // 是否是移动端，按需填入
        .outline("#说说中国传统文化艺术的魅力\n##1. 传统文化艺术的源远流长\n###1.1 中国古代艺术发展历程\n####1.1.1 古代绘画艺术的演变\n- 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。\n- 唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。\n")
        .build();

CompletableFuture<InitiatePptCreationV2Response> future = client.initiatePptCreationV2  (request);
try {
    InitiatePptCreationV2Response response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

##### **前端：**

业务链路中调用创建API（后续编辑 / 查看链路参考【场景三】），如下为示例代码：

```
// 确保SDK已经加载完
await window.Quanmiao.createPPT({
    appkey: 'your appkey', // 必填，由服务端API获取
    signature: 'your signature', // 必填，由服务端API获取
    container: document.getElementById('XXX'), // 必填，挂载容器DOM元素
    content: ' PPT大纲内容' , // 必填
    speaker: 'PPT主讲人', // 非必填，默认为 'XXX'
    isMobile: true, // 是否使用移动端模式。非必填，默认为false
    templateId: 88888, // 模板id
    aipptTaskId: 88888888, // 创建生成任务id -- 由服务端API获取；当前链路需填入
    isEnterprise: false,// 是否为企业模板 -- 传入了模板id的时候才生效，默认是true；如果传入的模板是全妙内置模板（非用户自有的企业模板），需要传入false进行覆盖生效
    onMessage(type, data) {
      if (type === 'SET_PPT_MAKING_STATUS') {
        if (data?.status === '1') {
          // 正在生成中
        }
        if (data?.status === '0') {
          // 生成完成
        }
      }
      if (type === 'GENERATE_PPT_SUCCESS') {
        // 这里可以拿到PPT的作品id：data?.id
        console.log('作品id', data?.id);
      }
    },
  });
} catch (e) {
  console.log('调用PPT SDK err=>', e);
  message.error(e?.msg || e?.message || '操作异常');
}
```

### **场景三：云端完成**PPT作品的创建，跳转前端界面编辑 / 查看作品

#### **step1：（**后端**）**完成PPT作品的创建

下发参数：

-   pptProcessId
    
-   pptArtifactId -- 对应前端SDK入参作品id
    

由于该场景涉及大量计算操作，RT较高，所以进行了异步设计。用户需要通过GetPptInfo接口获取对应的数据，然后再进行后续操作。

1.  初始化，如下为代码示例：
    

```
AsyncClient client = ClientHelper.getClient();
InitiatePptCreationV2Request request = InitiatePptCreationV2Request.builder()
        .workspaceId(workspaceId)
        .taskId(UUID.randomUUID().toString())
        .processType(2) //注意这里的类型
        .outline("#说说中国传统文化艺术的魅力\n##1. 传统文化艺术的源远流长\n###1.1 中国古代艺术发展历程\n####1.1.1 古代绘画艺术的演变\n- 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。\n- 唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。\n")
        .build();

CompletableFuture<InitiatePptCreationV2Response> future = client.initiatePptCreationV2  (request);
try {
    InitiatePptCreationV2Response response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

2.  轮询pptArtifactId，如下为代码示例：
    

```
AsyncClient client = ClientHelper.getClient();
GetPptInfoRequest request = GetPptInfoRequest.builder()
        .workspaceId(PublicConfig.get("workspace-id"))
        .taskId(taskId)
        .build();
CompletableFuture<GetPptInfoResponse> future = client.getPptInfo(request);
try {
    GetPptInfoResponse response = future.get();
    System.out.println("getPptInfo result: " + JSON.toJSONString(response));
    GetPptInfoResponseBody.Data data = response.getBody().getData();
    return GetPptInfoResp.builder()
            .taskId(data.getTaskId())
            .pptProcessId(data.getPptProcessId())
            .pptArtifactId(data.getPptArtifactId())
            .exportTaskId(data.getExportTaskId())
            .exportFileLink(data.getExportFileLink())
            .query(data.getQuery())
            .build();
} catch (InterruptedException e) {
    e.printStackTrace();
} catch (ExecutionException e) {
    e.printStackTrace();
}
return null;
```

#### **step2：（前端）界面编辑 / 查看作品**

```
// 确保SDK已经加载完
await window.Quanmiao.editPPT({
  appkey: 'your appkey', // 必填，由服务端API获取
  code: 'your code', // 必填，由服务端API获取
  container: document.getElementById('XXX'), // 必填，挂载容器DOM元素
  id: 88888, // 作品id，必填；从服务端API获取，也可从前端生成步骤获取
  isMobile: true, // 是否使用移动端模式。非必填，默认为false
  editorModel: false // 是否是编辑模式。默认是true
});
```

### **场景四：全云端完成**PPT作品的创建 -- 轮询任务过程 及 最终作品下载链接

由云端完成PPT作品的创建和导出，下发exportTaskId（导出任务ID）。

用户根据exportTaskId调用 [查询PPT导出任务的结果](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptartifactexportresult)进行轮询，获取PPT文件的下载地址。

异步设计，同【场景三】。

1.  获取导出任务的ID，如下为代码示例：
    

```
AsyncClient client = ClientHelper.getClient();
InitiatePptCreationV2Request request = InitiatePptCreationV2Request.builder()
        .workspaceId(workspaceId)
        .taskId(UUID.randomUUID().toString())
        .processType(3) //注意这里的类型
        .outline("#说说中国传统文化艺术的魅力\n##1. 传统文化艺术的源远流长\n###1.1 中国古代艺术发展历程\n####1.1.1 古代绘画艺术的演变\n- 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。\n- 唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。\n")
        .build();

CompletableFuture<InitiatePptCreationV2Response> future = client.initiatePptCreationV2  (request);
try {
    InitiatePptCreationV2Response response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

2.  轮询exportTaskId，如下为代码示例：
    

```
AsyncClient client = ClientHelper.getClient();
GetPptInfoRequest request = GetPptInfoRequest.builder()
        .workspaceId(PublicConfig.get("workspace-id"))
        .taskId(taskId)
        .build();
CompletableFuture<GetPptInfoResponse> future = client.getPptInfo(request);
try {
    GetPptInfoResponse response = future.get();
    System.out.println("getPptInfo result: " + JSON.toJSONString(response));
    GetPptInfoResponseBody.Data data = response.getBody().getData();
    return GetPptInfoResp.builder()
            .taskId(data.getTaskId())
            .pptProcessId(data.getPptProcessId())
            .pptArtifactId(data.getPptArtifactId())
            .exportTaskId(data.getExportTaskId())
            .exportFileLink(data.getExportFileLink())
            .query(data.getQuery())
            .build();
} catch (InterruptedException e) {
    e.printStackTrace();
} catch (ExecutionException e) {
    e.printStackTrace();
}
return null;
```

3.  轮询任务结果，如下为示例代码：
    

```
AsyncClient client = MyClientHelper.getClient();
GetPptArtifactExportResultRequest request = GetPptArtifactExportResultRequest.builder()
        .workspaceId(workspaceId)
        .exportTaskId("2dxxx529c-b065-43ff-a04d-xxx")
        .build();

for(int i = 0; i < 30; i++) {
    CompletableFuture<GetPptArtifactExportResultResponse> future = client.getPptArtifactExportResult(request);
    try {
        GetPptArtifactExportResultResponse response = future.get();
        System.out.println("result: " + JSON.toJSONString(response));
    } catch (InterruptedException e) {
        throw new RuntimeException(e);
    } catch (ExecutionException e) {
        throw new RuntimeException(e);
    }
    
    try {
        Thread.sleep(3000L);
    } catch (InterruptedException e) {
        throw new RuntimeException(e);
    }
}
```

### **场景五：全云端完成PPT作品的创建 -- 只轮询最终**作品下载链接

由云端完成PPT作品的创建和导出，下发文件链接。

异步设计，同【场景三】。

1.  获取导出任务的ID，如下为示例代码：
    

```
AsyncClient client = ClientHelper.getClient();
InitiatePptCreationV2Request request = InitiatePptCreationV2Request.builder()
        .workspaceId(workspaceId)
        .taskId(UUID.randomUUID().toString())
        .processType(4) //注意这里的类型
        .outline("#说说中国传统文化艺术的魅力\n##1. 传统文化艺术的源远流长\n###1.1 中国古代艺术发展历程\n####1.1.1 古代绘画艺术的演变\n- 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。\n- 唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。\n")
        .build();

CompletableFuture<InitiatePptCreationV2Response> future = client.initiatePptCreationV2  (request);
try {
    InitiatePptCreationV2Response response = future.get();
    System.out.println("result: " + JSON.toJSONString(response));
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} catch (ExecutionException e) {
    throw new RuntimeException(e);
}
```

2.  轮询exportFileLink，如下为示例代码：
    

```
AsyncClient client = ClientHelper.getClient();
GetPptInfoRequest request = GetPptInfoRequest.builder()
        .workspaceId(PublicConfig.get("workspace-id"))
        .taskId(taskId)
        .build();
CompletableFuture<GetPptInfoResponse> future = client.getPptInfo(request);
try {
    GetPptInfoResponse response = future.get();
    System.out.println("getPptInfo result: " + JSON.toJSONString(response));
    GetPptInfoResponseBody.Data data = response.getBody().getData();
    return GetPptInfoResp.builder()
            .taskId(data.getTaskId())
            .pptProcessId(data.getPptProcessId())
            .pptArtifactId(data.getPptArtifactId())
            .exportTaskId(data.getExportTaskId())
            .exportFileLink(data.getExportFileLink())
            .query(data.getQuery())
            .build();
} catch (InterruptedException e) {
    e.printStackTrace();
} catch (ExecutionException e) {
    e.printStackTrace();
}
return null;
```

## **4 一键调用示例**

为提升开发效率和使用体验，我们已提供完整的Demo示例代码，支持用户一键调用，便于快速集成与调试，

##### **后端：**

Demo示例可下载如下文档：

-   Java：[ppt-generation-demo.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260515/uwacwg/ppt-generation-demo.zip)；
    
-   Python：[ppt-generation-demo-py.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260515/gcnidg/ppt-generation-demo-py.zip)。
    

本地网页端口：[http://localhost:8080/ppt](http://localhost:8080/ppt)。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3754149771/p1074831.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3754149771/p1074833.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3754149771/p1074832.png)

##### **前端示例：**

以下是前端配置参考示例代码，填入相关接口参数后，本地服务启动界面即可快速查看效果，Demo示例可下载如下文档：

[ppt-frontend-demo.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260521/bwowfo/ppt-frontend-demo.zip)

示例效果（具体调试信息，请关注控制台打印信息）：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3754149771/p1074834.png)

## **5 其他**

前端SDK销毁：

**重要**

业务处理过程中谨慎调用，一般离开界面处理即可

```
windows.Quanmiao.deleteIframe();
```
