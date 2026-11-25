# 对话文件管理

深度搜索应用支持按 session\_id 维护对话文件目录树：可基于临时文件ID和文件/目录元信息更新目录树，也可删除文件并获取目录树信息，该能力仅适用于法律阅卷场景。

<a id="更新session文件"></a>

<a id="24a789ab3b1d4"></a>

## 更新session文件

支持创建 session\_id 维度文件目录树信息，增强模型在特定场景下对文件的理解能力，需要基于已解析成功的临时动态文件 ID、目录及文件元信息自行构建。

<a id="请求语法"></a>

<a id="fb3725f2a6g14"></a>

### 请求语法

<a id="code-block"></a>

```http
POST /deep-search-agent/session/files/upsert HTTP/1.1
```

<a id="请求参数"></a>

<a id="764bba3785jy4"></a>

### 请求参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| input | object | 是 | 请求参数 |
| input.request\_id | str | 否 | 请求ID（业务） |
| input.chat\_id | str | 否 | 对话ID |
| input.session\_id | str | 是 | 会话ID |
| input.files | array\[object\] | 是 | 已完成解析的文件信息集合 |
| input.files.file\_id | str | 是 | 文件ID |
| input.files.file\_name | str | 是 | 文件名 |
| input.files.file\_path | str | 是 | 完整文件路径 |
| input.files.type | str | 是 | 类型（取值：file/dir） |
| input.files.index\_order | int | 是 | 排序 |
| parameters | object | 是 | 配置参数，该接口下留空 {} |

<a id="返回参数"></a>

<a id="b2221587ffxt1"></a>

### 返回参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| code | str | 是 | 状态码（成功：200） |
| message | str | 是 | 状态信息 |
| output | object | 是 | 输出参数 |
| output.request\_id | str | 否 | 请求ID |
| output.chat\_id | str | 否 | 对话ID |
| output.session\_id | str | 否 | 会话ID |
| output.result | array\[object\] | 是 | 更新处理结果 |
| output.result.\[0\].status | bool | 是 | 更新处理状态 |

<a id="示例"></a>

<a id="9658186abfu20"></a>

### 示例

<a id="请求示例"></a>

<a id="f842698af5y13"></a>

#### 请求示例

<a id="code-block-2"></a>

```json
{
    "input": {
        "session_id": "18220***66b3",
        "files":[
            {
                "file_id": "file_session_e93***17301",
                "file_name": "测试文档.txt",
                "file_path": "评测/测试文档.txt",
                "type": "file",
                "index_order": 0
            }
        ]
    },
    "parameters": {
    }
}
```

<a id="返回示例"></a>

<a id="33cd52baa8krp"></a>

#### 返回示例

<a id="code-block-3"></a>

```json
{
    "code": "200",
    "message": "Success"
    "output": {
        "request_id": "bbe29140-766b-4caf-8558-2c703d9cb641",
        "result": {
            "status": true
        }
    }
}
```

<a id="删除session文件"></a>

<a id="3e1a0e1baecq7"></a>

## 删除session文件

支持删除 session\_id 维度文件目录树中的文件信息

<a id="服务接口"></a>

<a id="RQaTU"></a>

### 服务接口

支持删除 session\_id 维度文件目录树信息。

<a id="请求语法-2"></a>

<a id="0f8e418f22xod"></a>

### 请求语法

<a id="code-block-4"></a>

```http
POST /deep-search-agent/session/files/delete HTTP/1.1
```

<a id="请求参数-2"></a>

<a id="cc988e6d8c538"></a>

### 请求参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| 字段 | 类型 | 是否必须 | 说明 |
| input | object | 是 | 请求参数 |
| input.request\_id | str | 否 | 请求ID（业务） |
| input.chat\_id | str | 否 | 对话ID |
| input.session\_id | str | 是 | 会话ID |
| input.file\_ids | array\[str\] | 是 | 文件ID集合 |
| parameters | object | 是 | 配置参数，该接口下留空 {} |

<a id="返回参数-2"></a>

<a id="cf516632fer8j"></a>

### 返回参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| code | str | 是 | 状态码（成功：200） |
| message | str | 是 | 状态信息 |
| output | object | 是 | 输出参数 |
| output.request\_id | str | 否 | 请求ID |
| output.chat\_id | str | 否 | 对话ID |
| output.session\_id | str | 否 | 会话ID |
| output.result | array\[object\] | 是 | 更新处理结果 |
| output.result.\[0\].status | bool | 是 | 更新处理状态 |

<a id="示例-2"></a>

<a id="3a0e2c8ef6snn"></a>

### 示例

<a id="请求示例-2"></a>

<a id="cb0112f469573"></a>

#### 请求示例

<a id="code-block-5"></a>

```json
{
    "input": {
        "session_id": "18220***66b3",
        "file_ids":[
            "file_session_e93***17301"
        ]
    },
    "parameters": {
    }
}
```

<a id="返回示例-2"></a>

<a id="964268f259wjw"></a>

#### 返回示例

<a id="code-block-6"></a>

```json
{
    "code": "200",
    "message": "Success"
    "output": {
        "request_id": "bbe29140-766b-4caf-8558-2c703d9cb641",
        "result": {
            "status": true
        }
    }
}
```

<a id="获取session文件"></a>

<a id="c5ed6a23d9yd6"></a>

## 获取session文件

支持获取 session\_id 维度文件目录树信息。

<a id="请求语法-3"></a>

<a id="040534d8c1z7g"></a>

### 请求语法

<a id="code-block-7"></a>

```http
POST /deep-search-agent/session/files/list HTTP/1.1
```

<a id="请求参数-3"></a>

<a id="b6b67a48f90zd"></a>

### 请求参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| input | object | 是 | 请求参数 |
| input.request\_id | str | 否 | 请求ID（业务） |
| input.chat\_id | str | 否 | 对话ID |
| input.session\_id | str | 是 | 会话ID |
| input.page\_number | int | 否 | 分页参数，页码 |
| input.page\_size | int | 否 | 分页参数，每页数量 |
| parameters | object | 是 | 配置参数，该接口下留空 {} |

<a id="返回参数-3"></a>

<a id="55b51fb6c81aw"></a>

### 返回参数

| 参数名 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| code | str | 是 | 状态码（成功：200） |
| message | str | 是 | 状态信息 |
| output | object | 是 | 输出参数 |
| output.request\_id | str | 否 | 请求ID |
| output.chat\_id | str | 否 | 对话ID |
| output.session\_id | str | 否 | 会话ID |
| output.result | object | 是 | 更新处理结果 |
| output.result.total | int | 是 | 命中总数 |
| output.result.files | array\[object\] | 是 | 文件列表信息 |
| output.result.files.\[0\].file\_id | str | 是 | 文件ID |
| output.result.files.\[0\].file\_name | str | 是 | 文件名 |
| output.result.files.\[0\].file\_path | str | 是 | 文件路径 |
| output.result.files.\[0\].type | str | 是 | 类型（取值：file/dir） |
| output.result.files.\[0\].index\_order | int | 是 | 排序 |

<a id="示例-3"></a>

<a id="497e1a3fd3uk2"></a>

### 示例

<a id="请求示例-3"></a>

<a id="93402a92f4lat"></a>

#### 请求示例

<a id="code-block-8"></a>

```json
{
    "input": {
        "session_id": "18220***66b3",
        "page_number": 1,
        "page_size": 10
    },
    "parameters": {
    }
}
```

<a id="返回示例-3"></a>

<a id="452c4b230ez1x"></a>

#### 返回示例

<a id="code-block-9"></a>

```json
{
    "code": "200",
    "message": "Success"
    "output": {
        "request_id": "bbe29140-766b-4caf-8558-2c703d9cb641",
        "result": {
            "total": 0,
            "files": []
        }
    }
}
```

<a id="调用示例"></a>

<a id="ab0dc25cccefs"></a>

## 调用示例

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import os
import sys
import uuid
import json
from copy import deepcopy

import requests

from http import HTTPStatus

list_session_files_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/list"
upsert_session_files_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/upsert"
delete_session_files_url = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/delete"

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python operate_session_files.py <session_id>")
        exit(1)

    session_id = sys.argv[1]

    # 1. 获取测试 session 文件
    list_session_files_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "session_id": session_id
        },
        "parameters": {}
    }
    response = requests.post(list_session_files_url, json=list_session_files_params, headers=headers)
    session_files_data = {}
    if response.status_code == HTTPStatus.OK:
        print("1. List session files successfully.")
        session_files_data = response.json()["output"]["result"]
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f'code={response.status_code}')
        exit(1)

    # 2. 更新测试 session 文件
    files = session_files_data["files"]
    temp_file = None
    for file in files:
        if '测试/' in file["file_path"]:
            temp_file = file
    if temp_file is None:
        temp_file = deepcopy(files[0])
        temp_file["file_id"] = temp_file["file_id"] + "_test"
        temp_file["file_path"] = "测试/" + temp_file["file_path"]
        files.append(temp_file)

    upsert_session_files_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "session_id": session_id,
            "files": files
        },
        "parameters": {}
    }
    response = requests.post(upsert_session_files_url, json=upsert_session_files_params, headers=headers)
    upsert_data = {}
    if response.status_code == HTTPStatus.OK:
        print("2. Upsert session files successfully.")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f'code={response.status_code}')
        exit(1)

    # 3. 删除测试 session 文件
    delete_session_files_params = {
        "request_id": str(uuid.uuid4()),
        "input": {
            "session_id": session_id,
            "file_ids": [
                temp_file["file_id"]
            ]
        },
        "parameters": {}
    }
    response = requests.post(delete_session_files_url, json=delete_session_files_params, headers=headers)
    delete_data = {}
    if response.status_code == HTTPStatus.OK:
        print("3. Delete session files successfully.")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f'code={response.status_code}')
        exit(1)
```

<a id="fig-code-group-java-tab"></a>

java

<a id="code-code-group-java"></a>

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.UUID;

public class DeepSearchDemo {

    private static final String LIST_SESSION_FILES_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/list";
    private static final String UPSERT_SESSION_FILES_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/upsert";
    private static final String DELETE_SESSION_FILES_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/session/files/delete";

    private static final String DASHSCOPE_API_KEY = System.getenv("DASHSCOPE_API_KEY");

    private static JSONObject buildListParams(String sessionId) {
        JSONObject input = new JSONObject();
        input.put("session_id", sessionId);

        JSONObject params = new JSONObject();
        params.put("input", input);
        params.put("request_id", UUID.randomUUID().toString());
        params.put("parameters", new JSONObject());

        return params;
    }

    private static JSONObject buildUpsertParams(String sessionId, JSONArray files) {
        JSONObject input = new JSONObject();
        input.put("session_id", sessionId);
        input.put("files", files);

        JSONObject params = new JSONObject();
        params.put("input", input);
        params.put("request_id", UUID.randomUUID().toString());
        params.put("parameters", new JSONObject());

        return params;
    }

    private static JSONObject buildDeleteParams(String sessionId, JSONArray fileIds) {
        JSONObject input = new JSONObject();
        input.put("session_id", sessionId);
        input.put("file_ids", fileIds);

        JSONObject params = new JSONObject();
        params.put("input", input);
        params.put("request_id", UUID.randomUUID().toString());
        params.put("parameters", new JSONObject());

        return params;
    }

    private static JSONObject sendPostRequest(String url, JSONObject body) throws Exception {
        URL urlObj = new URL(url);
        HttpURLConnection conn = (HttpURLConnection) urlObj.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.setDoInput(true);
        conn.setRequestProperty("Authorization", "Bearer " + DASHSCOPE_API_KEY);
        conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");
        conn.setRequestProperty("Accept", "application/json");
        conn.setRequestProperty("User-Agent", "Java Client");

        try (DataOutputStream os = new DataOutputStream(conn.getOutputStream())) {
            os.write(JSON.toJSONString(body).getBytes("UTF-8"));
            os.flush();
        }
        int responseCode = conn.getResponseCode();

        // 读取响应
        StringBuilder response = new StringBuilder();
        BufferedReader reader;
        if (responseCode >= 200 && responseCode < 300) {
            reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        } else {
            reader = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
        }
        String inputLine;
        while ((inputLine = reader.readLine()) != null) {
            response.append(inputLine);
        }
        reader.close();
        if (responseCode != 200) {
            System.err.println("Error response code: " + responseCode);
            System.out.println("Response: " + response.toString());
            System.exit(1);
        }

        return JSON.parseObject(response.toString());
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.out.println("usage: java DeepSearchDemo <session_id>");
            System.exit(1);
        }

        String sessionId = args[0];

        // 1. List session files
        JSONObject listResponse = sendPostRequest(LIST_SESSION_FILES_URL, buildListParams(sessionId));
        JSONObject result = listResponse.getJSONObject("output").getJSONObject("result");
        System.out.println("1. List session files successfully.");
        System.out.println(JSON.toJSONString(result, true));

        // 2. Upsert session files
        JSONArray files = result.getJSONArray("files");
        JSONObject tempFile = null;
        for (int i = 0; i < files.size(); i++) {
            JSONObject file = files.getJSONObject(i);
            if (file.getString("file_path").contains("测试/")) {
                tempFile = file;
                break;
            }
        }
        if (tempFile == null) {
            tempFile = new JSONObject().fluentPutAll(files.getJSONObject(0));
            tempFile.put("file_id", tempFile.getString("file_id") + "_test");
            tempFile.put("file_path", "测试/" + tempFile.getString("file_path"));
            files.add(tempFile);
        }
        JSONObject upsertResponse = sendPostRequest(UPSERT_SESSION_FILES_URL, buildUpsertParams(sessionId, files));
        result = upsertResponse.getJSONObject("output").getJSONObject("result");
        System.out.println("2. Upsert session files successfully.");
        System.out.println(JSON.toJSONString(result, true));

        // 3. Delete session files
        JSONArray fileIds = new JSONArray();
        fileIds.add(tempFile.getString("file_id"));

        JSONObject deleteResponse = sendPostRequest(DELETE_SESSION_FILES_URL, buildDeleteParams(sessionId, fileIds));
        result = deleteResponse.getJSONObject("output").getJSONObject("result");
        System.out.println("3. Delete session files successfully.");
        System.out.println(JSON.toJSONString(result, true));
    }

}
```
