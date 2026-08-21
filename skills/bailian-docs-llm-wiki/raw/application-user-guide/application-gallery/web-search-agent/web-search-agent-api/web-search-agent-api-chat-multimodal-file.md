# 多模态文件操作

使用联网搜索多模态能力时，可以通过如下文件接口，将需要与联网搜索 agent 交互的图片提前上传到 OSS 处，在进行联网问答时，使用已经提前上传到 OSS 图片 url， 可以提供更流畅的问答体验。

## **获取预签名 OSS 上传地址**

获取与签名 OSS 上传地址，可以将图片上传至该地址

```
POST /web-search-agent/file/upload/apply HTTP/1.1
```

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.session\_id

str

是

文件操作

session id（业务自定义）

input.files

array

是

待上传文件列表

input.files\[\].file\_name

str

是

文件名称

input.files\[\].file\_size

int

是

文件大小(字节)

input.files\[\].content\_type

str

是

文件 MIME

类型

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

Agent

选项配置

parameters.agent\_options.agent\_id

str

是

Agent ID

### **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID

output.result

object

是

文件处理结果

output.result.upload\_tasks

array

是

上传任务列表

output.result.upload\_tasks\[\].file\_id

str

是

文件 ID

output.result.upload\_tasks\[\].file\_name

str

是

文件名称

output.result.upload\_tasks\[\].upload\_url

str

是

OSS

预签名上传地址

output.result.upload\_tasks\[\].expire\_at

int

是

上传 URL

过期时间(Unix 时间戳)，默认 1 小时

## **执行上传**

在获取到 OSS 预签名上传地址后，可以通过如下操作将本地文件上传到对应的地址。其中，${output.result.upload\_tasks\[\].upload\_url}为通过调用**获取预签名 OSS 上传地址** 接口获取到对应文件的OSS 预签名上传地址。

```
curl -X PUT -T ./path/to/test.jpg -H "Content-Type: image/jpeg" ${output.result.upload_tasks[].upload_url}
```

## **回调获取文件上传的状态**

调用文件上传回调，查看文件上传的结果，即是否成功。

```
POST /web-search-agent/file/upload/callback HTTP/1.1
```

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.session\_id

str

是

文件操作

session id（业务自定义）

input.file\_id

str

是

文件

ID(获取上传 URL 时返回)

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

Agent

选项配置

parameters.agent\_options.agent\_id

str

是

Agent ID

### **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID

output.result

object

是

处理结果

output.result.status

str

是

上传状态(成功:SUCCESS)

## **获取文件上传的信息**

查看已经上传文件的状态信息

```
POST /web-search-agent/file/info/get HTTP/1.1
```

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.session\_id

str

是

文件操作

session id（业务自定义）

input.file\_ids

array\[str\]

是

文件 ID 列表

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

Agent

选项配置

parameters.agent\_options.agent\_id

str

是

Agent ID

### **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID

output.result

object

是

处理结果

output.result\[\].file\_id

str

是

文件 ID

output.result\[\].file\_name

str

是

文件名称

output.result\[\].file\_size

int

是

文件大小(字节)

output.result\[\].content\_type

str

是

文件 MIME

类型

output.result\[\].preview\_url

str

是

文件预览地址(OSS

预签名 URL)

output.result\[\].expire\_at

int

是

预览 URL

过期时间(Unix 时间戳)

output.result\[\].status

str

是

文件状态(如:done)

## **删除文件**

删除已上传的文件

```
POST /web-search-agent/file/delete HTTP/1.1
```

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.session\_id

str

是

文件操作

session id（业务自定义）

input.file\_ids

array\[str\]

是

文件 ID 列表

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

Agent

选项配置

parameters.agent\_options.agent\_id

str

是

Agent ID

### **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID

output.result

object

是

处理结果

output.result\[\].status

str

是

删除状态(成功:SUCCESS)

## **调用示例**

Python

```
# coding=utf-8

import os
import json
import requests

from http import HTTPStatus

# 基础 URL
BASE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent"

# 四个接口 URL
get_upload_url = f"{BASE_URL}/file/upload/apply"
upload_callback = f"{BASE_URL}/file/upload/callback"
get_file_info = f"{BASE_URL}/file/info/get"
delete_file = f"{BASE_URL}/file/delete"

# 请求头
headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

# Agent 配置参数
AGENT_OPTIONS = {
    "agent_id": "aid-xxx",
}

def call_get_upload_url(session_id: str, files: list) -> dict:
    """
    获取文件上传 URL
    
    Args:
        session_id: 会话 ID
        files: 文件列表，每个文件包含 file_name, file_size, content_type, file_ext
    
    Returns:
        上传任务信息，包含 upload_tasks 列表
    """
    params = {
        "input": {
            "session_id": session_id,
            "files": files
        },
        "parameters": {
            "agent_options": AGENT_OPTIONS
        }
    }
    
    response = requests.post(get_upload_url, json=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        result = response.json()
        print("获取上传 URL 成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result["output"]["result"]
    else:
        print(f'获取上传 URL 失败: code={response.status_code}')
        print(f'response={response.text}')
        raise Exception(f"获取上传 URL 失败: {response.status_code}")

def call_upload_callback(session_id: str, file_id: str) -> dict:
    """
    文件上传完成后的回调
    
    Args:
        session_id: 会话 ID
        file_id: 文件 ID
    
    Returns:
        回调结果，包含 status
    """
    params = {
        "input": {
            "session_id": session_id,
            "file_id": file_id
        },
        "parameters": {
            "agent_options": AGENT_OPTIONS
        }
    }
    
    response = requests.post(upload_callback, json=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        result = response.json()
        print("上传回调成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result["output"]["result"]
    else:
        print(f'上传回调失败: code={response.status_code}')
        print(f'response={response.text}')
        raise Exception(f"上传回调失败: {response.status_code}")

def call_get_file_info(session_id: str, file_ids: list) -> dict:
    """
    获取文件信息
    
    Args:
        session_id: 会话 ID
        file_ids: 文件 ID 列表
    
    Returns:
        文件信息列表，包含 file_name, file_size, content_type, preview_url 等
    """
    params = {
        "input": {
            "session_id": session_id,
            "file_ids": file_ids
        },
        "parameters": {
            "agent_options": AGENT_OPTIONS
        }
    }
    
    response = requests.post(get_file_info, json=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        result = response.json()
        print("获取文件信息成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result["output"]["result"]
    else:
        print(f'获取文件信息失败: code={response.status_code}')
        print(f'response={response.text}')
        raise Exception(f"获取文件信息失败: {response.status_code}")

def call_delete_file(session_id: str, file_ids: list) -> dict:
    """
    删除文件
    
    Args:
        session_id: 会话 ID
        file_ids: 待删除的文件 ID 列表
    
    Returns:
        删除结果，包含 status
    """
    params = {
        "input": {
            "session_id": session_id,
            "file_ids": file_ids
        },
        "parameters": {
            "agent_options": AGENT_OPTIONS
        }
    }
    
    response = requests.post(delete_file, json=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        result = response.json()
        print("删除文件成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result["output"]["result"]
    else:
        print(f'删除文件失败: code={response.status_code}')
        print(f'response={response.text}')
        raise Exception(f"删除文件失败: {response.status_code}")

if __name__ == "__main__":
    # 示例用法
    SESSION_ID = "session-456"
    
    # 1. 获取上传 URL
    print("=" * 50)
    print("1. 获取上传 URL")
    print("=" * 50)
    upload_result = call_get_upload_url(SESSION_ID, [
        {
            "file_name": "test_1.jpg",
            "file_size": 1024000,
            "content_type": "image/jpeg",
            "file_ext": "jpg"
        }
    ])
    
    # 从结果中获取 upload_tasks
    upload_tasks = upload_result.get("upload_tasks", [])
    if upload_tasks:
        task = upload_tasks[0]
        file_id = task["file_id"]
        upload_url = task["upload_url"]
        print(f"\nfile_id: {file_id}")
        print(f"upload_url: {upload_url}")
        
        # 2. 实际上传文件（使用 PUT 方法上传到 OSS）
        print("\n" + "=" * 50)
        print("2. 上传文件到 OSS")
        print("=" * 50)
        # 这里需要实际的文件数据进行上传
        # with open("test_1.jpg", "rb") as f:
        #     response = requests.put(upload_url, data=f)
        #     if response.status_code == HTTPStatus.OK:
        #         print("文件上传成功")
        
        # 3. 上传完成后回调
        print("\n" + "=" * 50)
        print("3. 上传回调")
        print("=" * 50)
        callback_result = call_upload_callback(SESSION_ID, file_id)
        
        # 4. 获取文件信息
        print("\n" + "=" * 50)
        print("4. 获取文件信息")
        print("=" * 50)
        file_info = call_get_file_info(SESSION_ID, [file_id])
        
        # 5. 删除文件（可选）
        print("\n" + "=" * 50)
        print("5. 删除文件")
        print("=" * 50)
        delete_result = call_delete_file(SESSION_ID, [file_id])
```

Java

```
import java.io.*;
import java.net.*;
import java.util.*;
import com.alibaba.fastjson2.*;
import java.nio.charset.StandardCharsets;

public class FileApiDemo {
    private static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent";
    private static final String GET_UPLOAD_URL = BASE_URL + "/file/upload/apply";
    private static final String UPLOAD_CALLBACK = BASE_URL + "/file/upload/callback";
    private static final String GET_FILE_INFO = BASE_URL + "/file/info/get";
    private static final String DELETE_FILE = BASE_URL + "/file/delete";

    private static final String AGENT_ID = "aid-2ea101badcd5438c8798794d6e47f6f9";

    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.out.println("please set DASHSCOPE_API_KEY environment variable");
            System.exit(1);
        }

        String sessionId = "session-456";

        // 1. 获取上传 URL
        System.out.println("=" .repeat(50));
        System.out.println("1. 获取上传 URL");
        System.out.println("=".repeat(50));
        JSONObject uploadResult = callGetUploadUrl(apiKey, sessionId);
        JSONObject uploadTask = uploadResult.getJSONArray("upload_tasks").getJSONObject(0);
        String fileId = uploadTask.getString("file_id");
        String uploadUrl = uploadTask.getString("upload_url");
        String fileName = uploadTask.getString("file_name");
        System.out.println("file_id: " + fileId);
        System.out.println("upload_url: " + uploadUrl);

        // 2. 上传文件到 OSS（使用 PUT 方法）
        System.out.println("\n" + "=".repeat(50));
        System.out.println("2. 上传文件到 OSS");
        System.out.println("=".repeat(50));
        // 实际上传需要使用真实文件
        // uploadFileToOss(uploadUrl, filePath);
        System.out.println("文件上传示例（需替换为真实文件路径）");

        // 3. 上传回调
        System.out.println("\n" + "=".repeat(50));
        System.out.println("3. 上传回调");
        System.out.println("=".repeat(50));
        JSONObject callbackResult = callUploadCallback(apiKey, sessionId, fileId);
        System.out.println("callback status: " + callbackResult.getString("status"));

        // 4. 获取文件信息
        System.out.println("\n" + "=".repeat(50));
        System.out.println("4. 获取文件信息");
        System.out.println("=".repeat(50));
        JSONArray fileInfoResult = callGetFileInfo(apiKey, sessionId, Arrays.asList(fileId));
        System.out.println("file info: " + fileInfoResult.toJSONString());

        // 5. 删除文件
        System.out.println("\n" + "=".repeat(50));
        System.out.println("5. 删除文件");
        System.out.println("=".repeat(50));
        JSONObject deleteResult = callDeleteFile(apiKey, sessionId, Arrays.asList(fileId));
        System.out.println("delete status: " + deleteResult.getString("status"));
    }

    /**
     * 获取文件上传 URL
     */
    public static JSONObject callGetUploadUrl(String apiKey, String sessionId) throws Exception {
        Map<String, Object> params = new HashMap<>();
        params.put("input", new HashMap<String, Object>() {{
            put("session_id", sessionId);
            put("files", new JSONArray().fluentAdd(new HashMap<String, Object>() {{
                put("file_name", "test_1.jpg");
                put("file_size", 1024000);
                put("content_type", "image/jpeg");
                put("file_ext", "jpg");
            }}));
        }});
        params.put("parameters", new HashMap<String, Object>() {{
            put("agent_options", buildAgentOptions());
        }});

        return doPost(apiKey, GET_UPLOAD_URL, params).getJSONObject("output").getJSONObject("result");
    }

    /**
     * 文件上传回调
     */
    public static JSONObject callUploadCallback(String apiKey, String sessionId, String fileId) throws Exception {
        Map<String, Object> params = new HashMap<>();
        params.put("input", new HashMap<String, Object>() {{
            put("session_id", sessionId);
            put("file_id", fileId);
        }});
        params.put("parameters", new HashMap<String, Object>() {{
            put("agent_options", buildAgentOptions());
        }});

        return doPost(apiKey, UPLOAD_CALLBACK, params).getJSONObject("output").getJSONObject("result");
    }

    /**
     * 获取文件信息
     */
    public static JSONArray callGetFileInfo(String apiKey, String sessionId, List<String> fileIds) throws Exception {
        Map<String, Object> params = new HashMap<>();
        params.put("input", new HashMap<String, Object>() {{
            put("session_id", sessionId);
            put("file_ids", new JSONArray(fileIds));
        }});
        params.put("parameters", new HashMap<String, Object>() {{
            put("agent_options", buildAgentOptions());
        }});

        return doPost(apiKey, GET_FILE_INFO, params).getJSONObject("output").getJSONArray("result");
    }

    /**
     * 删除文件
     */
    public static JSONObject callDeleteFile(String apiKey, String sessionId, List<String> fileIds) throws Exception {
        Map<String, Object> params = new HashMap<>();
        params.put("input", new HashMap<String, Object>() {{
            put("session_id", sessionId);
            put("file_ids", new JSONArray(fileIds));
        }});
        params.put("parameters", new HashMap<String, Object>() {{
            put("agent_options", buildAgentOptions());
        }});

        return doPost(apiKey, DELETE_FILE, params).getJSONObject("output").getJSONObject("result");
    }

    /**
     * 构建 Agent 选项
     */
    private static Map<String, Object> buildAgentOptions() {
        return new HashMap<String, Object>() {{
            put("agent_id", AGENT_ID);
        }};
    }

    /**
     * 发送 POST 请求
     */
    private static JSONObject doPost(String apiKey, String urlStr, Map<String, Object> params) throws Exception {
        URL url = new URL(urlStr);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.setRequestProperty("Authorization", "Bearer " + apiKey);
        conn.setRequestProperty("Content-Type", "application/json");

        try (OutputStream os = conn.getOutputStream()) {
            os.write(JSON.toJSONString(params).getBytes(StandardCharsets.UTF_8));
        }

        if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
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
            System.out.println(respJson.toJSONString());
            return respJson;
        } else {
            System.out.println("code=" + conn.getResponseCode());
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getErrorStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            }
            throw new Exception("请求失败: " + conn.getResponseCode());
        }
    }

    /**
     * 上传文件到 OSS（PUT 方法）
     */
    private static void uploadFileToOss(String uploadUrl, String filePath) throws Exception {
        URL url = new URL(uploadUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("PUT");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream();
             InputStream fis = new FileInputStream(filePath)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
        }

        if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
            System.out.println("文件上传成功");
        } else {
            System.out.println("文件上传失败: " + conn.getResponseCode());
        }
    }
}
```
