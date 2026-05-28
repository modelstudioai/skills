# 生成报告导出

深度搜索应用生成结果报告文件 (md、html、pdf) 的获取。

## **请求语法**

```
POST /deep-search-agent/file/expose HTTP/1.1
```

## **请求参数**

**参数名**

**类型**

**是否必须**

**默认值**

**说明**

input

object

是

输入字段

input.request\_id

str

否

请求ID（业务自定义）

input.writing\_result\_path

str

是

None

文件路径

input.writing\_result\_type

str

是

"html\_url"

获取类型，可选\[html, html\_url, md, md\_url, pdf\_url\]

parameters

object

是

配置参数字段，该接口下留空 {}

## **示例**

### **请求示例**

```
{
    "input": {
        "request_id": "b4d140f0-07b4-90cb-b13d-b29c9ac37fda",
        "writing_result_path": "msearch/agents/files/upload/5c81a***7da1151",
        "writing_result_type": "html_url"
    },
    "parameters": {}
}
```

### **返回示例**

```
{
    "code": "200",
    "message": "Success",
    "output": {
        "request_id": "b4d140f0-07b4-90cb-b13d-b29c9ac37fda",
        "result": [
            {
                "text": "https://***.aliyuncs.com/***/agents/files/upload/5c81a***7da1151.html?***",
                "type": "html_url"
            }
        ]
    }
}
```

## **调用示例**

Python

```
# coding=utf-8

import os
import sys
import uuid
import json
import requests

from http import HTTPStatus

file_expose_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/expose"

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

def get_file_export_info(file_path: str) -> dict:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("please set DASHSCOPE_API_KEY environment variable")
        exit(1)

    # 文件导出
    file_expose_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "writing_result_path": file_path,
            "writing_result_type": "html_url"
        },
        "parameters": {}
    }
    response = requests.post(file_expose_url, json=file_expose_params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        print("file exported successfully.")
        export_info = response.json()["output"]["result"]
        return export_info
    else:
        print(f'code={response.status_code}')
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python deep_search_demo.py <file_path>")
        exit(1)

    file_path = sys.argv[1]
    export_info = get_file_export_info(file_path)
    print(json.dumps(export_info, indent=2, ensure_ascii=False))
```

Java

```
import java.io.*;
import java.net.*;
import java.util.*;
import com.alibaba.fastjson.*;
import java.nio.charset.StandardCharsets;

public class DeepSearchDemo {

    private static final String FILE_EXPOSE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/expose";

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("usage: java DeepSearchDemo <file_path>");
            System.exit(1);
        }

        String filePath = args[0];
        try {
            JSONArray exportInfo = getFileExportInfo(filePath);
            System.out.println(exportInfo.toJSONString());
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    public static JSONArray getFileExportInfo(String filePath) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null) {
            System.out.println("please set DASHSCOPE_API_KEY environment variable");
            System.exit(1);
        }

        // 构造参数
        Map<String, Object> params = new HashMap<>();
        params.put("request_id", UUID.randomUUID().toString());
        // input
        Map<String, Object> input = new HashMap<>();
        input.put("writing_result_path", filePath);
        input.put("writing_result_type", "html_url");
        // parameters
        Map<String, Object> parameters = new HashMap<>();

        params.put("input", input);
        params.put("parameters", parameters);

        String body = JSON.toJSONString(params);

        // HTTP 请求
        URL apiUrl = new URL(FILE_EXPOSE_URL);
        HttpURLConnection conn = (HttpURLConnection) apiUrl.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.setRequestProperty("Authorization", "Bearer " + apiKey);
        conn.setRequestProperty("Content-Type", "application/json");

        // 发送 body
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes(StandardCharsets.UTF_8));
        }

        int statusCode = conn.getResponseCode();
        if (statusCode == 200) {
            System.out.println("file exported successfully.");
            String responseBody;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                responseBody = sb.toString();
            }
            
            JSONObject respJson = JSON.parseObject(responseBody);

            return respJson.getJSONObject("output").getJSONArray("result");
        } else {
            System.out.println("code=" + statusCode);
            // 打印错误响应
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getErrorStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            }
            return null;
        }
    }
}
```
