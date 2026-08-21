# 文档内容审核

本文为您介绍通义数据挖掘文档内容审核API的语法及示例。

## **请求语法**

```
POST /zhiwen-chat/audit HTTP/1.1
```

## **请求参数**

**名称**

**类型**

**必填**

**描述**

**示例值**

capabilityType

string

是

能力类型

文档内容审核：CONTENT\_REVIEW

CONTENT\_REVIEW

userPrompt

string

是

提示词

你是一名经验丰富的高级文档审核专家，精通风险识别、合规性检查、事实核查和专业沟通。你的审核标准极为严格，注重细节，并能提供具有建设性的修改建议。你的任务是针对提供的文档，进行一次全面、深入的审核。你需要识别文档中存在的各种问题，生成一份结构化的审核报告。

fileIdList

array

是

文档ID列表

\[

"file\_zhiwen\_XXX"

\]

stream

boolean

是

是否流式返回

true

## **返回参数**

**名称**

**类型**

**描述**

output

object

\-choices

array

\-finishReason

string

结束原因

\-message

object

消息体

\-role

string

角色

\-content

string

消息内容

requestId

string

请求ID

usage

object

token使用信息

\-inputTokens

int

输入token数量

\-outputTokens

int

输出token数量

\-totalTokens

int

总token数量

## **示例**

### **调用示例**

Python

```
import os
import requests

'''
API名称：内容审核
API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-chat/audit
环境要求：Python >= 3.7
'''

url = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-chat/audit"
request_headers = {
    "Authorization": os.environ.get("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
    "Content-Type": "application/json"
}
# 内容审核 CONTENT_REVIEW
request_body = {
    "capabilityType": "CONTENT_REVIEW",
    "userPrompt": "你是一名经验丰富的高级文档审核专家，精通风险识别、合规性检查、事实核查和专业沟通。你的审核标准极为严格，注重细节，并能提供具有建设性的修改建议。你的任务是针对提供的文档，进行一次全面、深入的审核。你需要识别文档中存在的各种问题，生成一份结构化的审核报告。",
    "stream": True,
    "fileIdList": [
        "file_zhiwen_XXX"  # 替换为你的文档ID
    ]
}

with requests.post(url, json=request_body, headers=request_headers) as response:
    if request_body["stream"]:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    print("Received:", line[5:].strip())
    else:
        print("Received:", response.json())
```

Java

```
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import org.apache.http.HttpEntity;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import java.util.HashMap;
import java.util.Map;

/**
 * API名称：内容审核
 * API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-chat/audit
 * 环境要求：Java 8及以上
 */
public class AuditDemo {
    // Step 1. API 地址和配置
    private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");   // 填写百炼平台的 API KEY
    private static final String API_URL = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-chat/audit";
    private static final String CHARSET = "UTF-8";
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws IOException, InterruptedException {
        // Step 2. 请求参数配置
        // 文档上传API  返回的fileId字段（格式：file_zhiwen_XXX）
        String fileId = "file_zhiwen_XXX";
        // 自定义Prompt：可根据业务需求修改，示例可参考通义智文轻应用[效果调试]页面
        String userPrompt = "你是一名经验丰富的高级文档审核专家，精通风险识别、合规性检查、事实核查和专业沟通。你的审核标准极为严格，注重细节，并能提供具有建设性的修改建议。你的任务是针对提供的文档，进行一次全面、深入的审核。你需要识别文档中存在的各种问题，生成一份结构化的审核报告。";
        // 是否流式：本示例采用流式输出，可根据业务进行配置
        boolean isStreaming = true;

        // Step 3. 构建请求体
        Map<String, Object> requestBodyMap = new HashMap<>();
        requestBodyMap.put("capabilityType", "CONTENT_REVIEW");
        requestBodyMap.put("userPrompt", userPrompt);
        requestBodyMap.put("stream", isStreaming);
        requestBodyMap.put("fileIdList", new String[]{fileId});
        String requestBody = objectMapper.writeValueAsString(requestBodyMap);

        // Step 4. 配置请求超时时间
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(30 * 1000).build();

        // Step 5. 执行请求，根据业务需要选择：流式请求 或 非流式请求
        try (CloseableHttpClient httpClient = HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .build()) {

            // 构造 HTTP POST 请求
            HttpPost httpPost = new HttpPost(API_URL);
            buildRequestHeaders(httpPost, requestBody);

            // 执行请求：本示例采用流式输出，可根据业务配置stream参数
            buildStreamingRequest(httpClient, httpPost); // 流式请求
            // buildNonStreamingRequest(httpClient, httpPost); // 非流式请求
        }
    }

    /**
     * 构建通用请求头
     *
     * @param httpPost HTTP请求对象
     * @param requestBody 请求体字符串
     */
    private static void buildRequestHeaders(HttpPost httpPost, String requestBody) {
        httpPost.setHeader("Authorization", API_KEY);
        httpPost.setHeader("Content-Type", "application/json");
        httpPost.setEntity(new StringEntity(requestBody, CHARSET));
    }

    /**
     * 构建流式请求
     * @param client HTTP客户端
     * @param httpPost HTTP请求对象
     * @return 异步执行的CompletableFuture对象
     */
    private static void buildStreamingRequest(CloseableHttpClient client, HttpPost httpPost) {
        System.out.println("流式请求:");
        try (CloseableHttpResponse response = client.execute(httpPost)) {
            HttpEntity entity = response.getEntity();
            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode == 200 && entity != null) {
                try (InputStream inputStream = entity.getContent();
                     BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        if (line.startsWith("data:")) {
                            String json = line.substring(5).trim();
                            System.out.println(json);
                        }
                    }
                }
            } else {
                String errorBody = EntityUtils.toString(response.getEntity());
                System.err.println("请求失败: " + errorBody);
            }
        } catch (IOException e) {
            System.err.println("请求失败: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * 构建非流式请求
     * @param client HTTP客户端
     * @param httpPost HTTP请求对象
     * @throws IOException 当网络请求或数据读取发生错误时
     */
    private static void buildNonStreamingRequest(CloseableHttpClient client, HttpPost httpPost) throws IOException {
        System.out.println("非流式请求:");
        try (CloseableHttpResponse response = client.execute(httpPost)) {
            HttpEntity entity = response.getEntity();
            if (entity == null) {
                System.err.println("响应体为空");
                return;
            }
            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode == 200 && entity != null){
                String responseBody = EntityUtils.toString(entity);
                System.out.println(responseBody);
            }else{
                String errorBody = EntityUtils.toString(entity);
                System.err.println("请求失败: " + errorBody);
            }
        }catch (IOException e) {
            System.err.println("请求失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

### **正常返回示例**

`JSON`格式

```
{
  "output": {
    "choices": [{
      "finishReason": "stop",
      "message": {
        "role": "assistant",
        "content": "**文档审核报告：《XXX.pdf》**\n文档内容审核结果。\n**注**：本报告基于提供的文本内容生成，实际审核可能需结合完整文档及上下文进一步细化。"
      }
    }]
  },
  "requestId": "08bd24d4-6c85-9b2e-9ead-c9480b4b1651",
  "usage": {
    "inputTokens": 100,
    "outputTokens": 100,
    "totalTokens": 200
  }
}
```

## **错误码**

请参见[错误码-通义数据挖掘](https://help.aliyun.com/zh/model-studio/docmining-error-code)。
