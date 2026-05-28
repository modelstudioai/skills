# 文档删除

本文为您介绍通义数据挖掘文档删除API的语法及示例。

## **请求语法**

```
POST /zhiwen-file/delete_file HTTP/1.1
```

## **请求参数**

**名称**

**类型**

**必填**

**描述**

**示例值**

fileId

string

是

要删除的文档ID

file\_zhiwen\_XXX

## **返回参数**

**名称**

**类型**

**描述**

code

int

状态码

request\_id

string

请求ID

success

boolean

是否成功

message

string

响应消息

## **示例**

### **调用示例**

Python

```
import os
import requests
from http import HTTPStatus

'''
API名称：文档删除
API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/delete_file
环境要求：Python >= 3.7
'''

url = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/delete_file"
request_headers = {
    "Authorization": os.environ.get("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
    "Content-Type": "application/json"
}

response = requests.post(url,
                         json={
                             "fileId": "file_zhiwen_5f6e46d308a145b182c4bf1b788cea07_10035945"
                         },
                         headers=request_headers)

if response.status_code == HTTPStatus.OK:
    print(response.json())
else:
    print(f'response={response.json()}')
    print(f'code={response.status_code}')
```

Java

```
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpResponse;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * API名称：文档删除
 * API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/delete_file
 * 环境要求：Java 8及以上
 */
public class FileDeleteDemo {
    // Step 1. API 地址和配置
    private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");    // 填写百炼平台的 API KEY
    private static final String API_URL = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/delete_file";
    private static final String CHARSET = "UTF-8";
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws IOException {
        // Step 2. 请求参数配置
        // 文档上传API  返回的fileId字段（格式：file_zhiwen_XXX）
        String fileId = "file_zhiwen_XXX";

        // Step 3. 构建请求体
        Map<String, String> requestBodyMap = new HashMap<>();
        requestBodyMap.put("fileId", fileId);
        String requestBody = objectMapper.writeValueAsString(requestBodyMap);

        // Step 4. 配置请求超时时间
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(30 * 1000).build();

        // Step 5. 执行删除文档请求
        try (CloseableHttpClient httpClient = HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .build()) {
            // 构造 HTTP POST 请求
            HttpPost httpPost = new HttpPost(API_URL);
            buildRequestHeaders(httpPost, requestBody);
            HttpResponse response = httpClient.execute(httpPost);

            // 检查响应状态码
            if (response.getStatusLine().getStatusCode() == 200) {
                System.out.println("文档删除成功: " + fileId);
            } else {
                System.out.println("文档删除失败: " + fileId);
            }
        }catch (Exception e) {
            System.err.println("删除文档时发生异常: " + e.getMessage());
            e.printStackTrace();
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
}
```

### **正常返回示例**

`JSON`格式

```
{
  "code": 200,
  "request_id": "1a022107-2b41-979f-a730-59b43d3ada2c",
  "success": true,
  "message": "成功"
}
```

## **错误码**

请参见[错误码-通义数据挖掘](https://help.aliyun.com/zh/model-studio/docmining-error-code)。
