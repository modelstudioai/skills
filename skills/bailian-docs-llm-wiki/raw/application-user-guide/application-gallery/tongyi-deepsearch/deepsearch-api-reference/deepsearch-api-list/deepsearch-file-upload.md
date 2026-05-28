# 上传文件

可基于如下动态文件操作接口能力获取处理好的文件信息，支持智能体应用的 API 调用通过 parameters.agent\_options.session\_files 参数完成“动态文档解析”工具的文件数据注入。

## **文件上传凭证**

获取临时动态文件上传凭证，用于后续提交文档解析的操作。

### **请求语法**

```
POST /deep-search-agent/file/lease/apply HTTP/1.1
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

input.request\_id

str

否

请求ID（业务自定义）

input.file\_name

str

是

待上传文件名称

input.file\_md5

str

是

待上传文件 md5

input.file\_size

int

是

待上传文件大小

parameters

object

是

配置参数字段，该接口下留空 {}

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

请求ID（业务自定义）

output.result

object

是

文件处理结果

output.result.headers

map\[str, str\]

是

用于上传文件的 headers 信息

output.result.lease\_id

str

是

凭证ID

output.result.pre\_signed\_url

str

是

oss预签名地址

### **示例**

#### **请求示例**

```
{
    "input": {
        "request_id": "8d1c3d50-b761-4730-ac1a-27a248fa08b5",
        "file_name": "深度搜索测试文档.txt",
        "file_md5": "****",
        "file_size": 512
    },
    "parameters": {},
    "stream": false
}
```

#### **返回示例**

```
{
    "code": "200",
    "message": "Success",
    "output": {
        "request_id": "8d1c3d50-b761-4730-ac1a-27a248fa08b5",
        "result": {
            "headers": {
                "Content-Type": "text/plain",
                "x-bailian-extra": "MTU***U5Mw=="
            },
            "lease_id": "c00863829e***8218548747",
            "pre_signed_url": "https://das***center.oss-cn-beijing.aliyuncs.com***b71234fae68.1758218548747.txt?Exp***"
        }
    }
}
```

## **上传文件**

上传文件需要在端侧由用户自行完成，基于文件上传凭证，如何上传文件可参考如下代码。

```
import requests
from http import HTTPStatus

headers = {
    "Content-Type": "$output.result.headers['Content-Type']",
    "x-bailian-extra": "$output.result.headers['x-bailian-extra']"
}
pre_signed_url = "$output.result.pre_signed_url"

file_path = "深度搜索测试文档.txt"
with open(file_path, 'rb') as file:
    response = requests.put(pre_signed_url, data=file, headers=headers)
    if response.status_code == HTTPStatus.OK:
        print("文件上传成功")
    else:
        print(f"文件上传失败，{response.status_code}")
```

## **提交文件解析**

应用临时动态文件上传完成后，可基于文件上传凭证提交文档解析。

### **请求语法**

```
POST /deep-search-agent/file/parse/submit HTTP/1.1
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

input.request\_id

str

否

请求ID（业务自定义）

input.lease\_id

str

是

已上传文件凭证ID

parameters

object

是

配置参数字段，该接口下留空 {}

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

请求ID（业务自定义）

output.result

array\[object\]

是

文件处理结果

output.result.file\_id

str

是

已提交解析任务文件ID

### **示例**

#### **请求示例**

```
{
    "input": {
        "request_id": "4fc80fa9-b66a-4c6a-9dab-1a79ecd972f2",
        "lease_id": "c00863829e***8218548747"
    },
    "parameters": {}
}
```

#### **返回示例**

```
{
    "code": "200",
    "message": "Success",
    "output": {
        "request_id": "4fc80fa9-b66a-4c6a-9dab-1a79ecd972f2",
        "result": [
            {
                "file_id": "file_session_ec4803e***409"                
            }
        ]
    }
}
```

## **获取解析状态**

应用临时动态文件提交文档解析后，可获通过文件ID查询文件解析状态。

### **请求语法**

```
POST /deep-search-agent/file/parse/status HTTP/1.1
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

input.request\_id

str

否

请求ID（业务自定义）

input.file\_ids

list\[str\]

是

已提交解析任务文件ID集合

parameters

object

是

配置参数字段，该接口下留空 {}

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

请求ID（业务自定义）

output.result

array\[object\]

是

文件处理结果

output.result.\[0\].status

str

是

已提交解析任务文件的处理状态

### **文件状态**

```
文件status包括以下状态：
- 说明：必须等到状态为 FILE_IS_READY 才能进行问答。

- 文件解析
● INIT: 待解析。
● PARSING: 解析中。
● PARSE_SUCCESS：解析完成。
● PARSE_FAILED：解析失败。

- 索引构建
● SAFE_CHECKING: 安全检测中。
● SAFE_CHECK_FAILED: 安全检测失败。
● INDEX_BUILDING：索引构建中。
● INDEX_BUILD_SUCCESS：索引构建成功。
● INDEX_BUILDING_FAILED：索引构建失败。
● INDEX_DELETED：文件索引已删除。
● FILE_IS_READY：文件准备完毕。
● FILE_EXPIRED：文件过期。
```

### **示例**

#### **请求示例**

```
{
    "input": {
        "request_id": "bbe29140-766b-4caf-8558-2c703d9cb641",
        "file_ids": [
            "file_session_ec4803e***409"
        ]
    },
    "parameters": {}
}
```

#### **返回示例**

```
{
    "code": "200",
    "message": "Success",
    "output": {
        "request_id": "bbe29140-766b-4caf-8558-2c703d9cb641",
        "result": [
            {
                "status": "FILE_IS_READY"                
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
import time
import hashlib
import requests

from http import HTTPStatus

apply_lease_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/lease/apply"
submit_file_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/parse/submit"
parse_status_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/parse/status"

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

def get_file_upload_info(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise Exception("file not exists")
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    file_md5 = md5.hexdigest()
    return {"file_name": file_name, "file_size": file_size, "md5": file_md5}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python deep_search_demo.py <file_path>")
        exit(1)

    file_path = sys.argv[1]
    file_info = get_file_upload_info(file_path)
    file_name: str = file_info["file_name"]
    file_size: int = file_info["file_size"]
    file_md5: str = file_info["md5"]

    # 1. 申请租约
    apply_lease_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "file_name": file_name,
            "file_size": file_size,
            "file_md5": file_md5
        },
        "parameters": {}
    }
    response = requests.post(apply_lease_url, json=apply_lease_params, headers=headers)
    lease_data = {}
    if response.status_code == HTTPStatus.OK:
        print("1. Lease applied successfully.")
        lease_data = response.json()["output"]["result"]
        print(json.dumps(lease_data, indent=2, ensure_ascii=False))
    else:
        print(f'code={response.status_code}')
        exit(1)

    # 2. 上传文件
    upload_headers = lease_data["headers"]
    lease_id = lease_data["lease_id"]
    pre_signed_url = lease_data["pre_signed_url"]
    with open(file_path, 'rb') as file:
        # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
        response = requests.put(pre_signed_url, data=file, headers=upload_headers)
    if response.status_code == HTTPStatus.OK:
        print("2. File uploaded successfully.")
    else:
        print(f"Failed to upload the file. ResponseCode: {response.status_code}")
        exit(1)

    # 3.提交解析
    submit_file_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "lease_id": lease_data["lease_id"]
        },
        "parameters": {}
    }
    response = requests.post(submit_file_url, json=submit_file_params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        print("3. File submit parse successfully.")
        submit_data = response.json()["output"]["result"][0]
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        submit_data = response.json()
        print(f'response={response.json()}')
        print(f'code={response.status_code}')
        exit(1)

    # 4.获取解析状态
    parse_status_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "file_ids": [
                submit_data["file_id"]
            ]
        },
        "parameters": {}
    }
    _start_time = time.time()
    while True:
        response = requests.post(parse_status_url, json=parse_status_params, headers=headers)
        _process_time = time.time() - _start_time
        if response.status_code == HTTPStatus.OK:
            parse_status = response.json()["output"]["result"]
            print(json.dumps(parse_status, indent=2, ensure_ascii=False))
            file_status = parse_status[0]["status"]
            print(f"4. Check file process status: {file_status}. process time: {_process_time}")
            if file_status == "FILE_IS_READY":
                print("5. File process successfully.")
                exit(0)
        else:
            print(f'response={response.json()}')
            print(f'code={response.status_code}')
        try:
            if _process_time > 1800:
                print(f'file process timeout[>1800s]: {_process_time}')
                exit(1)
            time.sleep(10)
        except Exception as e:
            pass
```

Java

```
import java.io.*;
import java.net.*;
import java.util.*;
import java.nio.file.*;
import java.security.MessageDigest;
import com.alibaba.fastjson.*;
import java.nio.charset.StandardCharsets;

public class DeepSearchDemo {
    private static final String APPLY_LEASE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/lease/apply";
    private static final String SUBMIT_FILE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/parse/submit";
    private static final String PARSE_STATUS_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/file/parse/status";

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.out.println("usage: java DeepSearchDemo <file_path>");
            System.exit(1);
        }

        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.out.println("please set and DASHSCOPE_API_KEY environment variable");
            System.exit(1);
        }

        String filePath = args[0];
        File file = new File(filePath);
        if (!file.exists()) {
            throw new Exception("file not exists");
        }
        String fileName = file.getName();
        long fileSize = file.length();
        String fileMd5 = calculateMD5(filePath);

        // 1. 申请租约
        Map<String, Object> applyLeaseParams = new HashMap<>();
        applyLeaseParams.put("request_id", UUID.randomUUID().toString());
        // input
        Map<String, Object> applyLeaseInput = new HashMap<>();
        applyLeaseInput.put("file_name", fileName);
        applyLeaseInput.put("file_size", fileSize);
        applyLeaseInput.put("file_md5", fileMd5);

        applyLeaseParams.put("input", applyLeaseInput);
        applyLeaseParams.put("parameters", new HashMap<>());

        // HTTP 请求
        URL applyLeaseUrl = new URL(APPLY_LEASE_URL);
        HttpURLConnection applyLeaseConn = (HttpURLConnection) applyLeaseUrl.openConnection();
        applyLeaseConn.setRequestMethod("POST");
        applyLeaseConn.setDoOutput(true);
        applyLeaseConn.setRequestProperty("Authorization", "Bearer " + apiKey);
        applyLeaseConn.setRequestProperty("Content-Type", "application/json");

        // 发送 body
        try (OutputStream os = applyLeaseConn.getOutputStream()) {
            os.write(JSON.toJSONString(applyLeaseParams).getBytes(StandardCharsets.UTF_8));
        }

        JSONObject leaseData = null;
        if (applyLeaseConn.getResponseCode() == HttpURLConnection.HTTP_OK) {
            System.out.println("1. Lease applied successfully.");
            String responseBody;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(applyLeaseConn.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                responseBody = sb.toString();
            }
            JSONObject respJson = JSON.parseObject(responseBody);
            leaseData = respJson.getJSONObject("output").getJSONObject("result");
            System.out.println(leaseData.toJSONString());
        } else {
            System.out.println("code=" + applyLeaseConn.getResponseCode());
            // 打印错误响应
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(applyLeaseConn.getErrorStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
                System.exit(1);
            }
        }

        // 2. 上传文件
        String uploadHeaders = leaseData.getString("headers");
        String preSignedUrl = leaseData.getString("pre_signed_url");

        URL uploadUrl = new URL(preSignedUrl);
        HttpURLConnection uploadConn = (HttpURLConnection) uploadUrl.openConnection();
        uploadConn.setRequestMethod("PUT");
        uploadConn.setDoOutput(true);
        JSONObject uploadHeadersObject = JSON.parseObject(uploadHeaders);
        for (Map.Entry<String, Object> entry : uploadHeadersObject.entrySet()) {
            uploadConn.setRequestProperty(entry.getKey(), entry.getValue().toString());
        }
        try (OutputStream os = uploadConn.getOutputStream(); InputStream fis = Files.newInputStream(Paths.get(filePath))) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
        }

        if (uploadConn.getResponseCode() == HttpURLConnection.HTTP_OK) {
            System.out.println("2. File uploaded successfully.");
        } else {
            System.out.println("Failed to upload the file. ResponseCode: " + uploadConn.getResponseCode());
            System.exit(1);
        }

        // 3. 提交解析
        Map<String, Object> submitFileParams = new HashMap<>();
        submitFileParams.put("request_id", UUID.randomUUID().toString());
        // input
        Map<String, Object> submitFileInput = new HashMap<>();
        submitFileInput.put("lease_id", leaseData.getString("lease_id"));

        submitFileParams.put("input", submitFileInput);
        submitFileParams.put("parameters", new HashMap<>());

        URL submitFileUrl = new URL(SUBMIT_FILE_URL);
        HttpURLConnection submitFileConn = (HttpURLConnection) submitFileUrl.openConnection();
        submitFileConn.setRequestMethod("POST");
        submitFileConn.setDoOutput(true);
        submitFileConn.setRequestProperty("Authorization", "Bearer " + apiKey);
        submitFileConn.setRequestProperty("Content-Type", "application/json");

        try (OutputStream os = submitFileConn.getOutputStream()) {
            os.write(JSON.toJSONString(submitFileParams).getBytes(StandardCharsets.UTF_8));
        }

        JSONObject submitData = null;
        if (submitFileConn.getResponseCode() == HttpURLConnection.HTTP_OK) {
            System.out.println("3. File submit parse successfully.");
            String responseBody;
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(submitFileConn.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                responseBody = sb.toString();
            }
            JSONObject respJson = JSON.parseObject(responseBody);
            submitData = respJson.getJSONObject("output").getJSONObject("result");
            System.out.println(submitData.toJSONString());
        } else {
            System.out.println("code=" + submitFileConn.getResponseCode());
            System.exit(1);
        }

        // 4. 获取解析状态
        Map<String, Object> parseStatusParams = new HashMap<>();
        parseStatusParams.put("request_id", UUID.randomUUID().toString());
        // input
        Map<String, Object> parseStatusInput = new HashMap<>();
        parseStatusInput.put("file_ids", new JSONArray().fluentAdd(submitData.getString("file_id")));
        long startTime = System.currentTimeMillis();
        while (true) {
            URL parseStatusUrl = new URL(PARSE_STATUS_URL);
            HttpURLConnection parseStatusConn = (HttpURLConnection) parseStatusUrl.openConnection();
            parseStatusConn.setRequestMethod("POST");
            parseStatusConn.setDoOutput(true);
            parseStatusConn.setRequestProperty("Authorization", "Bearer " + apiKey);
            parseStatusConn.setRequestProperty("Content-Type", "application/json");

            try (OutputStream os = parseStatusConn.getOutputStream()) {
                os.write(JSON.toJSONString(parseStatusParams).getBytes(StandardCharsets.UTF_8));
            }

            JSONArray parseStatusData = null;
            if (parseStatusConn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                String responseBody;
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(parseStatusConn.getInputStream(), StandardCharsets.UTF_8))) {
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    responseBody = sb.toString();
                }
                JSONObject respJson = JSON.parseObject(responseBody);
                parseStatusData = respJson.getJSONObject("output").getJSONArray("result");
                System.out.println(parseStatusData.toJSONString());
                String fileStatus = parseStatusData.getJSONObject(0).getString("status");
                if ("FILE_IS_READY".equals(fileStatus)) {
                    System.out.println("5. File process successfully.");
                    System.exit(0);
                }
            } else {
                System.out.println("code=" + parseStatusConn.getResponseCode());
            }
            long processTime = (System.currentTimeMillis() - startTime) / 1000;
            if (processTime > 1800) {
                System.out.println("file process timeout[>1800s]: " + processTime);
                System.exit(1);
            }
            Thread.sleep(10000);
        }
    }

    private static String calculateMD5(String filePath) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (InputStream is = Files.newInputStream(Paths.get(filePath))) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                md.update(buffer, 0, bytesRead);
            }
        }
        byte[] digest = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

}
```
