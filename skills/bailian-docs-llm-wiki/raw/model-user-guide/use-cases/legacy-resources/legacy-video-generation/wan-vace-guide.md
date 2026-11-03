# 视频编辑2.1

万相视频编辑统一模型支持 多模态输入 （文本/图像/视频），可实现 多图参考、视频重绘、局部编辑、视频延展、画面扩展 五大核心能力。

## 适用范围

-   各地域支持的模型有所差异，且资源相互独立。各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。
-   调用时，确保**模型、Endpoint URL 和 API Key 均属于同一地域**，跨地域调用将会失败。

**说明**本文的示例代码适用于**北京地域**。

## 核心能力

### 多图参考

**功能介绍：**支持最多 **3张**参考图像，可包括主体与背景（如人物、动物、服饰、场景等）。模型将多张图片融合生成连贯的视频内容。

**参数设置：**

-   `function`：必须设为 `image_reference`。
-   `ref_images_url`：URL数组，支持输入1～3张参考图。
-   `obj_or_bg`：标识每张图为主体（obj）还是背景（bg），与`ref_images_url`长度一致。

**输入提示词**

**输入参考图1（参考主体）**

**输入参考图2（参考背景）**

**输出视频**

视频中，一位女孩自晨雾缭绕的**古老森林深处款款走出**，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当她站定，环顾四周葱郁林木时，她**脸上绽放出惊喜与喜悦交织的笑容**。这一幕，定格在了光影交错的瞬间，记录下她与大自然的美妙邂逅。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2786951571/p955656.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2786951571/p955657.png)

在调用前，先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx2.1-vace-plus",
    "input": {
        "function": "image_reference",
        "prompt": "视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她脸上绽放出惊喜与喜悦交织的笑容。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。",
        "ref_images_url": [
            "http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png",
            "http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png"
        ]
    },
    "parameters": {
        "prompt_extend": true,
        "obj_or_bg": ["obj","bg"],
        "size": "1280*720"
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### Python

```
import os
import requests
import time

# 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")
headers = {"X-DashScope-Async": "enable", "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def create_task():
    """创建视频合成任务，返回 task_id"""
    try:
        resp = requests.post(
            f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers={
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "wanx2.1-vace-plus",
                "input": {
                    "function": "image_reference",
                    "prompt": "视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她脸上绽放出惊喜与喜悦交织的笑容。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。",
                    "ref_images_url": [
                        "http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png",
                        "http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png"
                    ]
                },
                "parameters": {"prompt_extend": True, "obj_or_bg": ["obj", "bg"], "size": "1280*720"}
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

def poll_result(task_id):
    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()["output"]
            status = data["task_status"]
            print(f"Status: {status}")

            if status == "SUCCEEDED":
                return data["video_url"]
            elif status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
            time.sleep(15)
        except requests.RequestException as e:
            print(f"轮询异常: {e}，15秒后重试...")
            time.sleep(15)

if __name__ == "__main__":
    task_id = create_task()
    print(f"任务ID: {task_id}")
    video_url = poll_result(task_id)
    print(f"\n视频生成成功: {video_url}")
```

#### Java

```
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;

public class VideoSynthesis {
    // 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
    static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

    static {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalStateException("未设置 DASHSCOPE_API_KEY");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        // 启用HTTP Keep-Alive（JVM默认已开启，显式设置更可靠）
        System.setProperty("http.keepAlive", "true");
        System.setProperty("http.maxConnections", "20");
    }

    public static boolean isValidUserUrl(String urlString) {
        try {
            URL url = new URL(urlString);
            // 检查协议是否为安全协议
            String protocol = url.getProtocol();
            if (!"https".equalsIgnoreCase(protocol) && !"http".equalsIgnoreCase(protocol)) {
                return false;
            }

            return true;
        } catch (Exception e) {
            System.err.println("无效的URL: " + e.getMessage());
            return false;
        }
    }

    // 通用HTTP POST请求
    private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
    }

    // 通用HTTP GET请求
    private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
    }

    // 创建连接（复用连接参数）
    private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        // 配置连接属性
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);  // 30秒连接超时
        conn.setReadTimeout(60000);     // 60秒读取超时
        conn.setInstanceFollowRedirects(true);  // 允许重定向

        // 设置通用Header
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
            conn.setRequestProperty(entry.getKey(), entry.getValue());
        }

        // 异步任务专用Header
        if (path.contains("video-synthesis")) {
            conn.setRequestProperty("X-DashScope-Async", "enable");
        }

        // 设置内容类型和接受类型
        conn.setRequestProperty("Accept", "application/json");

        return conn;
    }

    // 读取响应（自动处理错误流）
    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
                ? conn.getInputStream()
                : conn.getErrorStream();

        if (is == null) {
            throw new IOException("无法获取响应流，响应码: " + conn.getResponseCode());
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append("\n");  // 添加换行符以保持原始格式
            }
            return sb.toString();
        }
    }

    // 步骤1：创建任务
    public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
                .put("model", "wanx2.1-vace-plus")
                .put("input", new JSONObject()
                        .put("function", "image_reference")
                        .put("prompt", "视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她脸上绽放出惊喜与喜悦交织的笑容。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。")
                        .put("ref_images_url", new JSONArray()
                                .put("http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png")
                                .put("http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png")))
                .put("parameters", new JSONObject()
                        .put("prompt_extend", true)
                        .put("obj_or_bg", new JSONArray().put("obj").put("bg"))
                        .put("size", "1280*720"));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        // 检查响应是否包含错误信息
        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
            String errorMessage = jsonResponse.optString("message", "未知错误");
            throw new RuntimeException("创建任务失败: " + errorMessage + ", 详细信息: " + resp);
        }
        JSONObject output = jsonResponse.getJSONObject("output");
        return output.getString("task_id");
    }

    // 步骤2：轮询结果（15秒间隔，无次数限制）
    public static String pollResult(String taskId) throws Exception {
        while (true) {
            String resp = httpGet("/tasks/" + taskId);
            JSONObject responseJson = new JSONObject(resp);

            // 验证响应结构
            if (!responseJson.has("output")) {
                throw new RuntimeException("API响应缺少'output'字段: " + resp);
            }

            JSONObject output = responseJson.getJSONObject("output");
            String status = output.getString("task_status");
            System.out.println("Status: " + status);

            if ("SUCCEEDED".equals(status)) {
                return output.getString("video_url");
            } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
                String message = output.optString("message", "未知错误");
                throw new RuntimeException("任务失败: " + message + ", 任务ID: " + taskId + ", 详细信息: " + resp);
            }
            Thread.sleep(15000);
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("正在创建视频合成任务...");
            String taskId = createTask();
            System.out.println("任务创建成功，Task ID: " + taskId);
            System.out.println("正在轮询任务结果...");
            String videoUrl = pollResult(taskId);
            System.out.println("视频URL: " + videoUrl);
        } catch (Exception e) {
            System.err.println("发生错误: " + e.getMessage());
            e.printStackTrace(); // 打印完整的堆栈跟踪以便调试
        }
    }

}
```

### 视频重绘

**功能介绍**：从输入视频中提取主体姿态与动作、构图与运动轮廓或线稿结构,结合文本提示词生成具有相同动态特征的新视频。还支持通过参考图像替换原视频中的主体。

**参数设置：**

-   `function`： 必须设为 `video_repainting`。
    
-   `video_url`：**必填**。输入视频的URL地址（MP4格式，≤50MB，≤5秒）。
    
-   `control_condition`：**必填**。设置视频特征提取的方式，决定了新视频保留原视频的哪些特征。
    
    -   `posebodyface`：提取脸部表情和肢体动作（保留面部表情细节）。
    -   `posebody`：仅提取肢体动作，不含脸部（仅控制身体动作）。
    -   `depth`：提取构图和运动轮廓（保留场景结构）。
    -   `scribble`：提取线稿结构（保留线稿边缘细节）。
-   `strength`：可选。控制特征提取的强度，范围 \[0.0, 1.0\]，默认 1.0。数值越大越贴近原视频，数值越小生成越自由。
    
-   `ref_images_url`：可选。传入1张参考图像URL，用于替换输入视频中的主体。
    

**输入提示词**

**输入视频**

**输出视频**

视频展示了一辆黑色的**蒸汽朋克风格汽车**，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx2.1-vace-plus",
    "input": {
        "function": "video_repainting",
        "prompt": "视频展示了一辆黑色的蒸汽朋克风格汽车，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味。",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"
    },
    "parameters": {
        "prompt_extend": false,
        "control_condition": "depth"
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### Python

```
import os
import requests
import time

# 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

def create_task():
    """创建视频重绘任务，返回 task_id"""
    try:
        resp = requests.post(
            f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers={
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "wanx2.1-vace-plus",
                "input": {
                    "function": "video_repainting",
                    "prompt": "视频展示了一辆黑色的蒸汽朋克风格汽车，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味。",
                    "video_url": "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"
                },
                "parameters": {
                    "prompt_extend": False, # 视频重绘建议关闭prompt智能改写
                    "control_condition": "depth" # 可选: posebodyface, posebody, depth, scribble
                }
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

def poll_result(task_id):
    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()["output"]
            status = data["task_status"]
            print(f"Status: {status}")

            if status == "SUCCEEDED":
                return data["video_url"]
            elif status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
            time.sleep(15)
        except requests.RequestException as e:
            print(f"轮询异常: {e}，15秒后重试...")
            time.sleep(15)

if __name__ == "__main__":
    task_id = create_task()
    print(f"任务ID: {task_id}")
    video_url = poll_result(task_id)
    print(f"\n视频生成成功: {video_url}")
```

#### Java

```
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;

public class VideoRepainting {
    // 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
    static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

    static {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalStateException("未设置 DASHSCOPE_API_KEY");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
        System.setProperty("http.maxConnections", "20");
    }

    // 通用HTTP POST请求
    private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
    }

    // 通用HTTP GET请求
    private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
    }

    // 创建连接
    private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        conn.setInstanceFollowRedirects(true);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
            conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
            conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        conn.setRequestProperty("Accept", "application/json");
        return conn;
    }

    // 读取响应
    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
                ? conn.getInputStream()
                : conn.getErrorStream();
        if (is == null) throw new IOException("无法获取响应流，响应码: " + conn.getResponseCode());
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line).append("\n");
            }
            return sb.toString();
        }
    }

    // 步骤1：创建视频重绘任务
    public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
                .put("model", "wanx2.1-vace-plus")
                .put("input", new JSONObject()
                        .put("function", "video_repainting")
                        .put("prompt", "视频展示了一辆黑色的蒸汽朋克风格汽车，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味。")
                        .put("video_url", "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"))
                .put("parameters", new JSONObject()
                        .put("prompt_extend", false)
                        .put("control_condition", "depth"));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
            String errorMessage = jsonResponse.optString("message", "未知错误");
            throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
    }

    // 步骤2：轮询结果
    public static String pollResult(String taskId) throws Exception {
        while (true) {
            String resp = httpGet("/tasks/" + taskId);
            JSONObject output = new JSONObject(resp).getJSONObject("output");
            String status = output.getString("task_status");
            System.out.println("Status: " + status);

            if ("SUCCEEDED".equals(status)) {
                return output.getString("video_url");
            } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
                throw new RuntimeException("任务失败: " + output.optString("message", "未知错误"));
            }
            Thread.sleep(15000);
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("正在创建视频重绘任务...");
            String taskId = createTask();
            System.out.println("任务创建成功，Task ID: " + taskId);
            System.out.println("正在轮询任务结果...");
            String videoUrl = pollResult(taskId);
            System.out.println("视频URL: " + videoUrl);
        } catch (Exception e) {
            System.err.println("发生错误: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

### 局部编辑

**功能介绍：**对视频指定区域进行精细化编辑，支持元素增删改和主体背景替换。上传掩码图像指定编辑区域，模型将自动跟踪目标并融合生成内容。

**参数设置：**

-   `function`：必须设为 `video_edit`。
    
-   `video_url`：**必填**。输入原视频的URL地址。
    
-   `mask_image_url`：可选。与 `mask_video_url` 二选一，推荐使用此参数。输入掩码图像URL，白色区域代表需要编辑的部分，黑色区域保留不变。
    
-   `mask_frame_id`：可选。配合 `mask_image_url` 使用，指定掩码对应视频的哪一帧（默认第1帧）。
    
-   `mask_type`：可选。指定编辑区域的行为方式：
    
    -   `tracking`（默认）：编辑区域会根据目标物体的运动轨迹自动跟随。
    -   `fixed`：编辑区域保持固定位置不变。
-   `expand_ratio`：可选。`仅当 mask_type` 为 `tracking` 时生效。
    
    -   作用：设置掩码区域向外扩展的比例。取值范围\[0.0, 1.0\]，默认值为 0.05。
    -   说明：数值越小，掩码越贴合目标；数值越大，掩码扩展范围越广。
-   `ref_images_url`：可选。传入1张参考图像URL，用于将编辑区域的内容替换为该参考图的内容。
    

**输入提示词**

**输入视频**

**输入掩码图像**

**输出视频**

视频展示了一家巴黎风情的法式咖啡馆，一只**穿着西装的狮子**优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。

![mask](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3778351571/p955179.png)

> 白色区域表示编辑区域

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx2.1-vace-plus",
    "input": {
        "function": "video_edit",
        "prompt": "视频展示了一家巴黎风情的法式咖啡馆，一只穿着西装的狮子优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。",
        "mask_image_url": "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4",
        "mask_frame_id": 1
    },
    "parameters": {
        "prompt_extend": false,
        "mask_type": "tracking",
        "expand_ratio": 0.05
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### Python

> 安装依赖：pip install requests。

```
import os
import requests
import time

# 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

def create_task():
    """创建局部编辑任务，返回 task_id"""
    try:
        resp = requests.post(
            f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers={
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "wanx2.1-vace-plus",
                "input": {
                    "function": "video_edit",
                    "prompt": "视频展示了一家巴黎风情的法式咖啡馆，一只穿着西装的狮子优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。",
                    "mask_image_url": "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png",
                    "video_url": "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4",
                    "mask_frame_id": 1 # 掩码对应的视频帧索引
                },
                "parameters": {
                    "prompt_extend": False,
                    "mask_type": "tracking", # 跟踪模式
                    "expand_ratio": 0.05
                }
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

def poll_result(task_id):
    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()["output"]
            status = data["task_status"]
            print(f"Status: {status}")

            if status == "SUCCEEDED":
                return data["video_url"]
            elif status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
            time.sleep(15)
        except requests.RequestException as e:
            print(f"轮询异常: {e}，15秒后重试...")
            time.sleep(15)

if __name__ == "__main__":
    task_id = create_task()
    print(f"任务ID: {task_id}")
    video_url = poll_result(task_id)
    print(f"\n视频生成成功: {video_url}")
```

#### Java

```
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;

public class VideoRegionalEdit {
    // 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
    static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

    static {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalStateException("未设置 DASHSCOPE_API_KEY");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
    }

    private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
    }

    private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
    }

    private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
            conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
            conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
    }

    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line).append("\n");
            return sb.toString();
        }
    }

    // 步骤1：创建局部编辑任务
    public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
                .put("model", "wanx2.1-vace-plus")
                .put("input", new JSONObject()
                        .put("function", "video_edit")
                        .put("prompt", "视频展示了一家巴黎风情的法式咖啡馆，一只穿着西装的狮子优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。")
                        .put("mask_image_url", "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png")
                        .put("video_url", "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4")
                        .put("mask_frame_id", 1))
                .put("parameters", new JSONObject()
                        .put("prompt_extend", false)
                        .put("mask_type", "tracking")
                        .put("expand_ratio", 0.05));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
            String errorMessage = jsonResponse.optString("message", "未知错误");
            throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
    }

    // 步骤2：轮询结果
    public static String pollResult(String taskId) throws Exception {
        while (true) {
            String resp = httpGet("/tasks/" + taskId);
            JSONObject output = new JSONObject(resp).getJSONObject("output");
            String status = output.getString("task_status");
            System.out.println("Status: " + status);

            if ("SUCCEEDED".equals(status)) return output.getString("video_url");
            else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                throw new RuntimeException("任务失败: " + output.optString("message"));
            Thread.sleep(15000);
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("正在创建局部编辑任务...");
            String taskId = createTask();
            System.out.println("任务创建成功，Task ID: " + taskId);
            String videoUrl = pollResult(taskId);
            System.out.println("视频URL: " + videoUrl);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 视频延展

**功能介绍：**基于输入的图像或视频片段，预测并生成具有连续性的后续内容。支持“首帧/首片段”向后延展，或“尾帧/尾片段”向前延展。最终生成的视频总时长固定为5秒。

**参数设置：**

-   `function`：必须设为 `video_extension`。
    
-   `prompt`：**必填**。描述期望生成的延展内容。
    
-   `first_clip_url`：可选。输入首段视频URL（≤3秒），模型将基于此片段向后延续生成视频。
    
-   `last_clip_url`：可选。输入尾段视频URL（≤3秒），模型将基于此片段向前倒推生成视频。
    
-   `first_frame_url`：可选，输入首帧图像的 URL 地址。基于首帧图像向后延展。
    
-   `last_frame_url`：可选，输入尾帧图像的 URL 地址。基于尾帧图像向前延展。
    
    > **注意**：first\_clip\_url、last\_clip\_url、first\_frame\_url、last\_frame\_url 四个参数中，**必须至少提供一项**作为输入。
    

**输入提示词**

**输入首片段视频（1秒）**

**输出视频（延长后的视频为5秒）**

一只戴着墨镜的**狗在街道上滑滑板**，3D卡通。

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx2.1-vace-plus",
    "input": {
        "function": "video_extension",
        "prompt": "一只戴着墨镜的狗在街道上滑滑板，3D卡通。",
        "first_clip_url": "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"
    },
    "parameters": {
        "prompt_extend": false
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### Python

```
import os
import requests
import time

# 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

def create_task():
    """创建视频延展任务，返回 task_id"""
    try:
        resp = requests.post(
            f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers={
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "wanx2.1-vace-plus",
                "input": {
                    "function": "video_extension",
                    "prompt": "一只戴着墨镜的狗在街道上滑滑板，3D卡通。",
                    "first_clip_url": "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"
                },
                "parameters": {
                    "prompt_extend": False
                }
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

def poll_result(task_id):
    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()["output"]
            status = data["task_status"]
            print(f"Status: {status}")

            if status == "SUCCEEDED":
                return data["video_url"]
            elif status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
            time.sleep(15)
        except requests.RequestException as e:
            print(f"轮询异常: {e}，15秒后重试...")
            time.sleep(15)

if __name__ == "__main__":
    task_id = create_task()
    print(f"任务ID: {task_id}")
    video_url = poll_result(task_id)
    print(f"\n视频生成成功: {video_url}")
```

#### Java

```
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;

public class VideoExtension {
    // 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
    static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

    static {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalStateException("未设置 DASHSCOPE_API_KEY");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
    }

    private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
    }

    private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
    }

    private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
            conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
            conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
    }

    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line).append("\n");
            return sb.toString();
        }
    }

    // 步骤1：创建视频延展任务
    public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
                .put("model", "wanx2.1-vace-plus")
                .put("input", new JSONObject()
                        .put("function", "video_extension")
                        .put("prompt", "一只戴着墨镜的狗在街道上滑滑板，3D卡通。")
                        .put("first_clip_url", "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"))
                .put("parameters", new JSONObject()
                        .put("prompt_extend", false));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
            String errorMessage = jsonResponse.optString("message", "未知错误");
            throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
    }

    // 步骤2：轮询结果
    public static String pollResult(String taskId) throws Exception {
        while (true) {
            String resp = httpGet("/tasks/" + taskId);
            JSONObject output = new JSONObject(resp).getJSONObject("output");
            String status = output.getString("task_status");
            System.out.println("Status: " + status);

            if ("SUCCEEDED".equals(status)) return output.getString("video_url");
            else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                throw new RuntimeException("任务失败: " + output.optString("message"));
            Thread.sleep(15000);
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("正在创建视频延展任务...");
            String taskId = createTask();
            System.out.println("任务创建成功，Task ID: " + taskId);
            String videoUrl = pollResult(taskId);
            System.out.println("视频URL: " + videoUrl);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 视频画面扩展

**功能介绍：** 在视频的上下左右四个方向上，根据提示词按比例扩展画面内容，保持视频主体的连贯性和背景的自然融合。

**参数设置：**

-   `function`：必须设为 `video_outpainting`。
-   `video_url`：**必填**。输入原视频的URL地址。
-   `top_scale`：可选。向上扩展比例，范围 \[1.0, 2.0\]，默认值为1.0（不扩展）。
-   `bottom_scale`：可选。向下扩展比例，范围 \[1.0, 2.0\]，默认值为1.0。
-   `left_scale`：可选。向左扩展比例，范围 \[1.0, 2.0\]，默认值为1.0。
-   `right_scale`：可选。向右扩展比例，范围 \[1.0, 2.0\]，默认值为1.0。

> **示例**：设置 `left_scale` 为 1.5，表示左侧画面将扩展为原宽度的1.5倍。

**输入提示词**

**输入视频**

**输出视频**

一位优雅的女士正在激情演奏小提琴，**她身后是一支完整的交响乐团**。

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx2.1-vace-plus",
    "input": {
        "function": "video_outpainting",
        "prompt": "一位优雅的女士正在激情演奏小提琴，她身后是一支完整的交响乐团。",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"
    },
    "parameters": {
        "prompt_extend": false,
        "top_scale": 1.5,
        "bottom_scale": 1.5,
        "left_scale": 1.5,
        "right_scale": 1.5
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### Python

```
import os
import requests
import time

# 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

def create_task():
    """创建视频画面扩展任务，返回 task_id"""
    try:
        resp = requests.post(
            f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers={
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "wanx2.1-vace-plus",
                "input": {
                    "function": "video_outpainting",
                    "prompt": "一位优雅的女士正在激情演奏小提琴，她身后是一支完整的交响乐团。",
                    "video_url": "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"
                },
                "parameters": {
                    "prompt_extend": False,
                    "top_scale": 1.5,    # 上方扩展比例
                    "bottom_scale": 1.5, # 下方扩展比例
                    "left_scale": 1.5,   # 左方扩展比例
                    "right_scale": 1.5   # 右方扩展比例
                }
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

def poll_result(task_id):
    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()["output"]
            status = data["task_status"]
            print(f"Status: {status}")

            if status == "SUCCEEDED":
                return data["video_url"]
            elif status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
            time.sleep(15)
        except requests.RequestException as e:
            print(f"轮询异常: {e}，15秒后重试...")
            time.sleep(15)

if __name__ == "__main__":
    task_id = create_task()
    print(f"任务ID: {task_id}")
    video_url = poll_result(task_id)
    print(f"\n视频生成成功: {video_url}")
```

#### Java

```
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;

public class VideoOutpainting {
    // 以下为华北2（北京）地域的URL，请将{WorkspaceId}替换为真实的业务空间ID。各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
    static final String BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
    private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

    static {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalStateException("未设置 DASHSCOPE_API_KEY");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
    }

    private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
    }

    private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
    }

    private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
            conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
            conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
    }

    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
           while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append("\n");
            }
            return sb.toString();
        }
    }

    // 步骤1：创建视频画面扩展任务
    public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
                .put("model", "wanx2.1-vace-plus")
                .put("input", new JSONObject()
                        .put("function", "video_outpainting")
                        .put("prompt", "一位优雅的女士正在激情演奏小提琴，她身后是一支完整的交响乐团。")
                        .put("video_url", "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"))
                .put("parameters", new JSONObject()
                        .put("prompt_extend", false)
                        .put("top_scale", 1.5)
                        .put("bottom_scale", 1.5)
                        .put("left_scale", 1.5)
                        .put("right_scale", 1.5));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
            String errorMessage = jsonResponse.optString("message", "未知错误");
            throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
    }

    // 步骤2：轮询结果
    public static String pollResult(String taskId) throws Exception {
        while (true) {
            String resp = httpGet("/tasks/" + taskId);
            JSONObject output = new JSONObject(resp).getJSONObject("output");
            String status = output.getString("task_status");
            System.out.println("Status: " + status);

            if ("SUCCEEDED".equals(status)) return output.getString("video_url");
            else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                throw new RuntimeException("任务失败: " + output.optString("message"));
            Thread.sleep(15000);
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("正在创建视频画面扩展任务...");
            String taskId = createTask();
            System.out.println("任务创建成功，Task ID: " + taskId);
            String videoUrl = pollResult(taskId);
            System.out.println("视频URL: " + videoUrl);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 如何输入图像和视频

### 输入图像

-   **图像数量**：根据[所选功能](https://help.aliyun.com/zh/model-studio/wan-vace-guide#14662a4c30k7g)传入对应数量的图像。
    
-   **输入方式**：
    
    -   **公网URL**：支持 HTTP 或 HTTPS 协议。示例：[](https://xxxx/xxx.png)[https://xxxx/xxx.png](https://xxxx/xxx.png)。
    -   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。示例：oss://dashscope-instant/xxx/xxx.png。

### 输入视频

-   **视频数量**：根据[所选功能](https://help.aliyun.com/zh/model-studio/wan-vace-guide#14662a4c30k7g)传入对应数量的视频。
    
-   **输入方式**：
    
    -   **公网URL**：支持 HTTP 或 HTTPS 协议。示例：[](https://xxxx/xxx.mp4)[https://xxxx/xxx.mp4](https://xxxx/xxx.mp4)。
    -   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。示例：oss://dashscope-instant/xxx/xxx.mp4。

## 输出视频

-   **视频数量**：1个。
    
-   **视频规格**：分辨率总像素固定为720P，帧率30fps，格式为MP4（H.264 编码）。
    
-   **视频URL有效期**：**24小时**。
    
-   **视频尺寸**：根据所选功能不同而有所差异。
    
    -   **多图参考 / 局部编辑**：
        
        -   输出固定为 720P 规格。
        -   具体宽高由请求参数 [size](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md) 决定。
    -   **视频重绘 / 视频延展 / 视频画面扩展**：
        
        -   若输入视频分辨率 ≤ 720P：保持原始分辨率输出。
        -   若输入视频分辨率 > 720P：保持宽高比不变，按比例缩放至 720P 输出。

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#89e9be041ek81)。
    
-   模型限流请参见[万相系列](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入不计费，输出计费。按成功生成的 **视频秒数** 计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
    -   通用视频编辑还支持[节省计划](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

## API文档

[通用视频编辑API参考](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)

## 常见问题

#### Q：多图参考功能最多支持几张图片?

A：最多支持3张参考图像。若超过3张，仅保留前3张作为输入。建议主体图像使用纯色背景以便更好突出主体，背景图像不包含任何主体对象。

#### Q: 视频重绘时什么情况下应该关闭prompt智能改写?

A: 当文本描述与输入视频内容不一致时，模型可能产生误解。建议手动关闭智能改写`prompt_extend=false`，并在prompt中提供清晰、具体的画面描述，以提升生成一致性与准确性。

#### Q：局部编辑功能中，掩码图像和掩码视频有什么区别?

A：掩码图像`mask_image_url`与掩码视频`mask_video_url`二选一填写。**推荐优先使用掩码图像**，只需指定一帧的编辑区域，系统会自动跟踪目标。
