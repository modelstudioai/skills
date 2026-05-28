# 妙搜API最佳实践

本文提供妙搜链路 API的最佳示例，帮助您快速入门并开发您自己的业务应用。

## 一、妙搜功能概述

## **1.1、一句话说明**

妙搜内置“互联网搜索”，可以供通用领域知识、信息智能搜索生成，为了应对更多领域、企业知识的搜索生成，我们提供了“通过API引入数据源”和“上传文件用作数据源”的集成能力。通过以下接口可以配置和管理企业API和知识。[控制台入口](https://aimiaobi.console.aliyun.com/?productCode=p_broadscope_search)：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7377257371/p908375.png)

## **1.2、产品页面展示**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7377257371/p908376.png)

### **1.2.1、数据源管理**

#### **控制台入口**

对应“**数据源管理**”菜单：此菜单下为数据接入说明，支持PaaS API方式维护数据源和数据集下知识。

#### **功能说明**

维护数据源，可以是多个，供“智能搜索”模块搜索获取知识。支持的数据源类型目前有三种：

-   **系统内置数据源**：系统内置，不支持修改，目前内置“互联网搜索”，支持互联网通用领域的网站数据搜索；
    
-   **通过API引入数据源**：企业提供搜索API，妙搜提供大模型能力并整合，目前需联系后台技术维护，暂未开放自定义；
    
-   **上传文件用作数据源**：企业提供知识，妙搜提供搜索和大模型能力，可以通过“数据源管理”下数据集相关API维护索引和索引中知识。
    

#### **API：**[数据源管理](https://alidocs.dingtalk.com/i/nodes/Qnp9zOoBVBDEydnQUNwzpGZ281DK0g6l?utm_medium=dingdoc_doc_plugin_url&utm_source=dingdoc_doc)

### **1.2.2、系统配置->通用/媒资搜索信源**

#### **控制台入口**

对应“**系统配置**”菜单下“**通用搜索信源**”、“**媒资搜索信源**”两个tab。

#### **功能说明**

维护“智能搜索”模块两个tab下索引的启用与否、召回文章、chunk（片段）条数。

#### **API：**[系统配置-信源管理](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/)

### **1.2.3、智能搜索**

#### **控制台入口**

-   妙搜首页下多模态搜索框。![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7377257371/p908377.png)
    
-   妙笔首页右上角**搜索素材**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0391743471/p936052.png)
    

#### **功能说明**

深度服务通用领域，影视、媒体、营销、影视、媒体等行业的多模态搜索。

#### **API：**[智能搜索](https://alidocs.dingtalk.com/i/nodes/jb9Y4gmKWrx9eo4dCmZqdNrjJGXn6lpz)

chatconfig.SearchSource 字段下配置“数据源（信源）”。

## **二、PaasAPI整体对接方案**

## 2.1、方案概览

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7377257371/p908378.png)

## **2.2、接口明细**

-   [妙搜-数据源](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/)：维护企业知识
    
    -   [数据源-创建](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdataset)
        
    -   [数据源-详情](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdataset)
        
    -   [数据源-修改](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedataset)
        
    -   [ListDatasets - 数据源-列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasets)
        
    -   [DeleteDataset - 数据源-删除](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedataset)
        
    -   [数据源-添加文档到数据集](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-adddatasetdocument)
        
    -   [数据源-获取文档详情](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasetdocument)
        
    -   [数据源-修改文档](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedatasetdocument)
        
    -   [数据源-文档列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasetdocuments)
        
    -   [数据源-搜索文档](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-searchdatasetdocuments)
        
    -   [DeleteDatasetDocument - 数据源-删除数据集文档](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedatasetdocument)
        
-   [系统配置-信源管理](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/)：配置信源，可以通过控制台配置
    
    -   [SaveDataSourceOrderConfig - 保存信源权重配置](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savedatasourceorderconfig)
        
    -   [GetDataSourceOrderConfig - 获取信源配置权重数据](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasourceorderconfig)
        
-   [妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)：端到端智能搜索生成推理能力
    
    -   [妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)
        
    -   [ListSearchTasks - 查询妙搜搜索生成历史任务列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtasks)
        
    -   [ListSearchTaskDialogues - 查询妙搜搜索生成任务详情列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialogues)
        
    -   [ListSearchTaskDialogueDatas - 查询搜索生成任务对话详情中数据列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialoguedatas)
        

## 三、PaasAPI对接示例

## **3.1、前提条件**

-   阿里云账号已开通本产品；
    
-   获得AgentKey、AccessKeyId、AccessKeySecret：[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)；
    
-   获取WorkSpaceId [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)；
    
-   引入妙笔SDK [注意获取最新sdk版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)；
    

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>1.0.30</version>
</dependency>
```

-   引入三方依赖：本文SSE示例采用okhttp开源三方组件，如果使用示例代码需要引入如下pom。
    

```
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.9.1</version>
</dependency>

<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp-sse</artifactId>
    <version>4.9.1</version>
</dependency>
```

## **3.2、管控API（HTTP）-**ListDatasets

### **准备：**

-   阿里云账号已开通产品；
    
-   获取AccessKey：对应示例中 ALIBABA\_CLOUD\_ACCESS\_KEY\_ID；
    
-   获取AccessKeySecret：对应示例中 ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET；
    
-   获取WorkspaceId：对应示例中 WorkspaceId。
    

### **接口说明**

-   妙搜-数据源列表接口。
    

### **接口文档**

-   [ListDatasets - 数据源-列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasets)。
    

### **在线调试**

[ListDatasets\_AI妙笔\_API调试-阿里云OpenAPI开发者门户](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDatasets)。

### **调用示例**

-   Java-SDK：
    

```
// This file is auto-generated, don't edit it. Thanks.
package demo;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.core.http.HttpClient;
import com.aliyun.core.http.HttpMethod;
import com.aliyun.core.http.ProxyOptions;
import com.aliyun.httpcomponent.httpclient.ApacheAsyncHttpClientBuilder;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import com.aliyun.sdk.service.aimiaobi20230801.*;
import com.google.gson.Gson;
import darabonba.core.RequestConfiguration;
import darabonba.core.client.ClientOverrideConfiguration;
import darabonba.core.utils.CommonUtil;
import darabonba.core.TeaPair;

//import javax.net.ssl.KeyManager;
//import javax.net.ssl.X509TrustManager;
import java.net.InetSocketAddress;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.io.*;

public class ListDatasets {
    public static void main(String[] args) throws Exception {

        // HttpClient Configuration
        /*HttpClient httpClient = new ApacheAsyncHttpClientBuilder()
                .connectionTimeout(Duration.ofSeconds(10)) // Set the connection timeout time, the default is 10 seconds
                .responseTimeout(Duration.ofSeconds(10)) // Set the response timeout time, the default is 20 seconds
                .maxConnections(128) // Set the connection pool size
                .maxIdleTimeOut(Duration.ofSeconds(50)) // Set the connection pool timeout, the default is 30 seconds
                // Configure the proxy
                .proxy(new ProxyOptions(ProxyOptions.Type.HTTP, new InetSocketAddress("<YOUR-PROXY-HOSTNAME>", 9001))
                        .setCredentials("<YOUR-PROXY-USERNAME>", "<YOUR-PROXY-PASSWORD>"))
                // If it is an https connection, you need to configure the certificate, or ignore the certificate(.ignoreSSL(true))
                .x509TrustManagers(new X509TrustManager[]{})
                .keyManagers(new KeyManager[]{})
                .ignoreSSL(false)
                .build();*/

        // Configure Credentials authentication information, including ak, secret, token
        StaticCredentialProvider provider = StaticCredentialProvider.create(Credential.builder()
                // Please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are set.
                .accessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .accessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
                //.securityToken(System.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")) // use STS token
                .build());

        // Configure the Client
        AsyncClient client = AsyncClient.builder()
                .region("cn-beijing") // Region ID
                //.httpClient(httpClient) // Use the configured HttpClient, otherwise use the default HttpClient (Apache HttpClient)
                .credentialsProvider(provider)
                //.serviceConfiguration(Configuration.create()) // Service-level configuration
                // Client-level configuration rewrite, can set Endpoint, Http request parameters, etc.
                .overrideConfiguration(
                        ClientOverrideConfiguration.create()
                                  // Endpoint 请参考 https://api.aliyun.com/product/AiMiaoBi
                                .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                        //.setConnectTimeout(Duration.ofSeconds(30))
                )
                .build();

        // Parameter settings for API request
        ListDatasetsRequest listDatasetsRequest = ListDatasetsRequest..workspaceId(workspaceId).builder()
                // Request-level configuration rewrite, can set Http request parameters, etc.
                // .requestConfiguration(RequestConfiguration.create().setHttpHeaders(new HttpHeaders()))
                .build();

        // Asynchronously get the return value of the API request
        CompletableFuture<ListDatasetsResponse> response = client.listDatasets(listDatasetsRequest);
        // Synchronously get the return value of the API request
        ListDatasetsResponse resp = response.get();
        System.out.println(new Gson().toJson(resp));
        // Asynchronous processing of return values
        /*response.thenAccept(resp -> {
            System.out.println(new Gson().toJson(resp));
        }).exceptionally(throwable -> { // Handling exceptions
            System.out.println(throwable.getMessage());
            return null;
        });*/

        // Finally, close the client
        client.close();
    }

}
```

## **3.3、推理API（HTTP-SSE）**\-RunSearchGeneration 

### **准备**

-   阿里云账号已开通产品；
    
-   获取AccessKey：对应示例中 ALIBABA\_CLOUD\_ACCESS\_KEY\_ID；
    
-   获取AccessKeySecret：对应示例中 ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET；
    
-   获取WorkspaceId：对应示例中 WorkspaceId。
    

### **接口说明**

-   妙搜-智能搜索接口。
    

### **接口文档**

-   [妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)。
    

### **调用示例**

-   Java-SDK：
    

```
package com.aliyun.sdk.service.demo;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunSearchGenerationRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunSearchGenerationResponseBody;
import com.google.gson.Gson;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;
import org.junit.Test;
import java.util.Arrays;

public class RunSearchGenerationTest {

    //accessKeyId
    String accessKeyId = System.getenv("accessKeyId");

    //accessKeySecret
    String accessKeySecret = System.getenv("accessKeySecret");
    String workspaceId = System.getenv("workspaceId");

    public AsyncClient getAsyncClient() {
        return AsyncClient.builder().region("cn-beijing")
                .credentialsProvider(StaticCredentialProvider.create(Credential.builder().accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build()))
                .serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3))
                .overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com"))
                .build();
    }
    
    @Test
    public void testRunSearchGeneration() {
        AsyncClient client = getAsyncClient();
        RunSearchGenerationRequest request = RunSearchGenerationRequest.builder()
                .workspaceId(workspaceId)
                .prompt("杭州亚运会")
                .chatConfig(RunSearchGenerationRequest.ChatConfig.builder()
                        .searchParam(RunSearchGenerationRequest.SearchParam.builder()
                                .searchSources(Arrays.asList(
                                        RunSearchGenerationRequest.SearchSources.builder()
                                                .code("SystemSearch")
                                                .datasetName("QuarkCommonNews")
                                                .build()
                                        )
                                ).build())
                        .build())
                .build();
        ResponseIterable<RunSearchGenerationResponseBody> responseIterable = client.runSearchGenerationWithResponseIterable(request);
        ResponseIterator<RunSearchGenerationResponseBody> iterator = responseIterable.iterator();
        while (iterator.hasNext()) {
            RunSearchGenerationResponseBody event = iterator.next();
            System.out.println("data:\n" + new Gson().toJson(event));
        }

        System.out.println("请求成功的请求头值：");
        System.out.println("code: " + responseIterable.getStatusCode());
        System.out.println("headers: " + responseIterable.getHeaders());
    }
}
```

-   python：
    

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

biz_param = ('{"WorkspaceId":"${llm-xxx}","Prompt":"测试","AgentContext": {"BizContext": {"SkipCurrentSupplement":true}}}')

class AiMiaoBi:
    def __init__(self) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        self.access_key_id = os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
        self.access_key_secret = os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
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
            action='RunSearchGeneration',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/quanmiao/aimiaosou/runSearchGeneration',
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

### **响应示例**

```
id:32c02e8e-3498-4765-878e-2125fd5e7caa
event:task-finished
data:{
    "payload": {
        "output": {
            "agentContext": {
                "bizContext": {
                    "prompt": "杭州亚运会吉祥物",
                    "currentStep": "search",
                    "nextStep": "generate",
                    "searchKeywords": [
                        "杭州",
                        "亚运会",
                        "吉祥物"
                    ],
                    "supplementEnable": false,
                    "supplementDataType": "searchQuery",
                    "searchQueryList": [
                        "杭州亚运会吉祥物"
                    ],
                    "multimodalMediaSelection": {},
                    "generatedContent": {
                        "textSearchResult": {
                            "total": 10,
                            "searchQuery": "杭州亚运会吉祥物",
                            "searchResult": [
                                {
                                    "docUuid": "53558a72452efbe881f41e81bd6138fe",
                                    "chunks": [
                                        "AI知识君全网内容智能分析杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，分别是琮琮、莲莲和宸宸。\n1. \n琮琮：代表位于浙江省杭州市余杭区瓶窑镇内的良渚古城遗址。它的名字来源于良渚古城遗址出土的代表性文物玉琮，具有坚强刚毅、敦厚善良、体魄强健和热情奔放四大美好寓意。\n2. \n莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。\n3. 宸宸：代表世界上里程最长、工程量最大的古代运河京杭大运河。宸宸这一名字源于京杭大运河上的著名建筑拱宸桥，其寓意为机智勇敢、聪慧灵动、乐观向上、积极进取。\n",
                                        "2. \n莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。\n3. 宸宸：代表世界上里程最长、工程量最大的古代运河京杭大运河。宸宸这一名字源于京杭大运河上的著名建筑拱宸桥，其寓意为机智勇敢、聪慧灵动、乐观向上、积极进取。",
                                        "3. 宸宸：代表世界上里程最长、工程量最大的古代运河京杭大运河。宸宸这一名字源于京杭大运河上的著名建筑拱宸桥，其寓意为机智勇敢、聪慧灵动、乐观向上、积极进取。\n参考来源[1]琮琮（杭州第19届亚运会吉祥物）_百度百科百度百科[2]杭州亚运会吉祥物分别代表什么 一文详解2022年亚运会吉祥物美好寓意qtx.com\n杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，分别是琮琮、莲莲和宸宸。\n1. \n琮琮：代表位于浙江省杭州市余杭区瓶窑镇内的良渚古城遗址。它的名字来源于良渚古城遗址出土的代表性文物玉琮，具有坚强刚毅、敦厚善良、体魄强健和热情奔放四大美好寓意。\n2. \n莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。\n"
                                    ],
                                    "searchSourceType": "SystemSearch",
                                    "searchSource": "QuarkCommonNews",
                                    "searchSourceName": "互联网搜索",
                                    "pubTime": "2024-08-09 05:48:52",
                                    "source": "百度百科",
                                    "title": "杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，分别是琮琮、莲莲和宸宸。<",
                                    "content": "AI知识君全网内容智能分析杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，分别是琮琮、莲莲和宸宸。\n1. \n琮琮：代表位于浙江省杭州市余杭区瓶窑镇内的良渚古城遗址。它的名字来源于良渚古城遗址出土的代表性文物玉琮，具有坚强刚毅、敦厚善良、体魄强健和热情奔放四大美好寓意。\n2. \n莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。\n3. 宸宸：代表世界上里程最长、工程量最大的古代运河京杭大运河。宸宸这一名字源于京杭大运河上的著名建筑拱宸桥，其寓意为机智勇敢、聪慧灵动、乐观向上、积极进取。\n参考来源[1]琮琮（杭州第19届亚运会吉祥物）_百度百科百度百科[2]杭州亚运会吉祥物分别代表什么 一文详解2022年亚运会吉祥物美好寓意qtx.com\n杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，分别是琮琮、莲莲和宸宸。\n1. \n琮琮：代表位于浙江省杭州市余杭区瓶窑镇内的良渚古城遗址。它的名字来源于良渚古城遗址出土的代表性文物玉琮，具有坚强刚毅、敦厚善良、体魄强健和热情奔放四大美好寓意。\n2. \n莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。\n3. 宸宸：代表世界上里程最长、工程量最大的古代运河京杭大运河。宸宸这一名字源于京杭大运河上的著名建筑拱宸桥，其寓意为机智勇敢、聪慧灵动、乐观向上、积极进取。",
                                    "url": "https://page.sm.cn/blm/midpage-317/index?h=v7.wenda_llm.quark.cn&id=24_bef1416cd6f6aedf89355fa42e67cb20&from=kkframenew",
                                    "summary": "杭州第19届亚运会的吉祥物是三个造型活泼可爱且又充满时代活力的机器人形象，<em>分别是琮琮、莲莲和宸宸</em>。<br>1. 琮琮：代表位于浙江省杭州市余杭区瓶窑镇内的良渚古城遗址。它的名字来源于良渚古城遗址出土的代表性文物玉琮，具有坚强刚毅、敦厚善良、体魄强健和热情奔放四大美好寓意。<br>2. 莲莲：代表杭州的城市名片西湖，结合吉祥物莲莲身上的主色调，人们自然会想到西湖上的接天莲叶。这一吉祥物形象除了寓意纯洁善良、活泼可爱、热情好客、美丽动人外，还寄托了莲花那高贵、纯洁的美好品质。<br",
                                    "select": true
                                }
                            ]
                        }
                    }
                },
                "agentName": "PlannerAgent"
            }
        },
        "usage": {
            "totalTokens": 693
        }
    },
    "header": {
        "sessionId": "32c02e8e-3498-4765-878e-2125fd5e7caa",
        "taskId": "67a91c00-54aa-4684-8eb3-cb9951cb8382",
        "event": "task-finished",
        "eventInfo": "生成完成"
    }
}
```

**说明**

关注event:task-finished：标识搜索生成完成。

### **简单的demo示例**

根据不同的使用场景设计了demo示例，您可以使用当前示例进行使用。

##### **总结生成答案+数据源-互联网搜索**

```
{
    "prompt": "杭州亚运会吉祥物是什么"
}

- 明确指定：总结生成答案+数据源-互联网搜索
{
    "prompt": "杭州亚运会吉祥物是什么",
    "chatConfig": {
        "generateTechnology": "copilotReference",
        "searchModels": [
            "TextGenerate"
        ],
        "searchParam": {
            "searchSources": [
                {
                    "code": "SystemSearch",
                    "datasetName": "QuarkCommonNews"
                }
            ]
        }
    }
}
```

##### **总结生成答案+数据源-互联网搜索+跳过反问**

```
{
    "prompt": "杭州亚运会吉祥物是什么",
    "chatConfig": {
        "generateTechnology": "copilotReference",
        "searchModels": [
            "TextGenerate"
        ],
        "searchParam": {
            "searchSources": [
                {
                    "code": "SystemSearch",
                    "datasetName": "QuarkCommonNews"
                }
            ]
        }
    },
    "AgentContext": {
    	"BizContext": {
    		"SkipCurrentSupplement": true
    	}
    }
}
```

##### **原文语句回答+数据源-互联网搜索**

```
{
    "prompt": "杭州亚运会吉祥物是什么",
    "chatConfig": {
        "generateTechnology": "copilotReference",
        "searchModels": [
            "ExcerptGenerate"
        ],
        "searchParam": {
            "searchSources": [
                {
                    "code": "SystemSearch",
                    "datasetName": "QuarkCommonNews"
                }
            ]
        }
    }
}
```

##### **按时间线总结+数据源-互联网搜索**

```
{
    "prompt": "杭州亚运会吉祥物是什么",
    "chatConfig": {
        "generateTechnology": "copilotReference",
        "searchModels": [
            "TimelineGenerate"
        ],
        "searchParam": {
            "searchSources": [
                {
                    "code": "SystemSearch",
                    "datasetName": "QuarkCommonNews"
                }
            ]
        }
    }
}
```

##### **媒资搜索+精准搜索+数据源-互联网搜索**

```
{
    "prompt": "杭州亚运会吉祥物是什么",
    "chatConfig": {
        "generateTechnology": "copilotPrecise",
        "searchModels": [
            "PreciseSearch"
        ],
        "searchParam": {
            "searchSources": [
                {
                    "code": "SystemSearch",
                    "datasetName": "QuarkCommonNews"
                }
            ]
        }
    }
}
```

## 四、业务场景最佳实践

## **4.1、场景一：**互联网智能搜索

### **场景说明**

无企业专属知识，走互联网通用领域知识进行智能搜索生成。

### **技术对接步骤**

1.  配置信源：
    
    1.  [1.2.2、系统配置->通用/媒资搜索信源](#bc74145d52kp3)下配置“互联网搜索”的开启&条数。
        
2.  对接智能搜索API：
    
    1.  [1.2.3、智能搜索](#6bb0f44e32hfy)下API，指定“互联网搜索”数据集作为搜索源。
        

## 4.2、场景二：企业搜索API智能搜索

### 场景说明

企业有自己的搜索能力（可以是企业知识库搜索，也可以是三方通用领域搜索等），并提供了搜索API，可以用三方企业搜索API接入，加持妙搜大模型能力后，实现灵活的企业级智能搜索生成。

### **技术对接步骤：**

1.  准备三方企业搜索API：
    
    1.  按照推荐的API模板提供API（非标、或不支持的鉴权需要定开）：[三方搜索API模板](https://help.aliyun.com/zh/model-studio/third-party-search-api-template)。
        
2.  配置三方企业搜索API：
    
    1.  提供账号、API定义给技术团队后台维护（未来会开放自定义三方API的维护能力）。
        
3.  配置信源：
    
    1.  [1.2.2、系统配置->通用/媒资搜索信源](#bc74145d52kp3)下配置对应索引的开启&条数。
        
4.  对接智能搜索API：
    
    1.  [1.2.3、智能搜索](#6bb0f44e32hfy)模块下API，指定对应数据集作为搜索源。
        

## **4.3、场景三：上传文件用作数据源**

### **场景说明：**

有企业知识需要语义构建索引，或已有企业知识搜索能力效果不理想，可以考虑直接通过妙搜构建企业知识库语义索引，用来企业知识库智能搜索生成。

### **技术对接步骤：**

1.  数据对接：通过[1.2.1、数据源管理](#20c3204988kwk)模块下维护企业知识语义索引。
    
    1.  如果是poc或者临时固定数据集构建，可以联系技术团队后台批量导入。
        
2.  通过API构建：
    
    1.  数据集-新增接口：初始化一个新的数据集（全局一次）可以手动（curl）一次性提前创建好；
        
    2.  数据集-添加文档数据接口：往步骤i创建的数据集中添加企业知识。
        
3.  配置信源：
    
    1.  [1.2.2、系统配置->通用/媒资搜索信源](#bc74145d52kp3)下配置对应索引的开启&条数。
        
4.  对接智能搜索API：
    
    1.  [1.2.3、智能搜索](#6bb0f44e32hfy)模块下API，指定对应数据集作为搜索源。
