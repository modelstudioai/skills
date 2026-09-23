# Android错误码说明和错误处理

在Android SDK接入上，分为端侧错误和服务端错误两类，返回的错误类型需要分别处理。所有错误都通过onErrorReceived 接口回调。

### 端侧错误

常见主要是由于网络原因导致的报错。常见报错如：

```
TYError(key=0, message={"header":{"local_task_id":"ba29ac78ddbd42a7b7e8cfb7f0765461","name":"TaskFailed","status":51,"status_text":""}})
TYError(key=0, message={"header":{"local_task_id":"ca9682dc849742c0a1480712d0d8d9cc","name":"TaskFailed","status":315,"status_text":" GetInetAddressByHostname timeout host=dashscope.aliyuncs.com timeout=5000 host=dashscope.aliyuncs.com port=443 ip= sockfd=121"}})
TYError(key=0, message={"header":{"local_task_id":"951786d3b94141969374402653cc4412","name":"TaskFailed","status":301,"status_text":" Got bad status host=poc-dashscope.aliyuncs.com line=HTTP/1.1 401 Unauthorized\r\n token=123"}})
```

此类错误为端侧报错，需要重新启动对话。

### 云端报错

错误码列表参考[多模态交互套件-错误码](raw/application-user-guide/application-gallery/multimodal-products/multimodal-api-references/multimodal-error-code.md)

常见主要原因是服务端错误或者是端侧错误调用导致的服务端报错。常见报错如：

```
TYError(key=0, message={"header":{"attributes":{},"error_code":"InternalAsrError","error_message":"Internal asr error","event":"task-failed","local_task_id":"454dcf408a334d1caa2c839dfa10a1f5","task_id":"6a0d507a5b494790a309d4ec68c91ae5"},"payload":{}})

TYError(key=0, message={"header":{"attributes":{},"event":"result-generated","local_task_id":"cc51a165b06841f48884b4915f7c7a29","task_id":"0b0a901e931b437cb2a8cda1aabe8ba4"},"payload":{"output":{"dialog_id":"82b86095-0eb8-4054-83a6-0666b3773f97","error_code":500,"error_message":"SOCKET_TIMEOUT_EXCEPTION: Read timed out","error_name":"InternalLLMError","event":"Error","llm_request_id":"6a56caf7d51349b79316e23303ab55ee","round_id":"0b1a4cd88b4b48b49c311a8c69f9d921"}}})

TYError(key=0, message={"header":{"attributes":{},"error_code":"TooManyInterrupt","error_message":"Send too many RequestToRespond or RequestToSpeak directives in a short time!","event":"task-failed","local_task_id":"bb33ae5b96f74a6986cc546e5003311e","task_id":"cef8f005d9494ab190911adf5b21aee1"},"payload":{}}})
```

服务端错误有两种类型：

1.  错误消息在header中，为不可恢复的错误，需要重新启动对话。
2.  错误消息在payload中，为可恢复错误，对话会自动切回LIstening状态，可以继续执行。

### 错误处理

```
public void onErrorReceived(@NonNull TYError errorInfo) {
            Log.e(TAG, "收到错误: " + errorInfo);
            com.alibaba.fastjson.JSONObject errorJson = (com.alibaba.fastjson.JSONObject) JSON.parse(errorInfo.getMessage());
            com.alibaba.fastjson.JSONObject header = null;
            com.alibaba.fastjson.JSONObject payload = null;
            boolean needRestart = false;
            if (errorJson != null && errorJson.containsKey("header")) {
                header = errorJson.getJSONObject("header");
                if (header != null && header.containsKey("name") && header.getString("name").equals("TaskFailed")) {
                // 客户端错误，需要重连
                    String errorCode = header.getString("status");
                    String errorMsg = header.getString("status_text");
                    needRestart = true;
                }
                if (header != null && header.containsKey("event") && header.getString("event").equals("task-failed")) {
                    // 服务端错误，不能恢复，需要重连
                    String errorCode = header.getString("error_code");
                    String errorMsg = header.getString("error_message");
                    needRestart = true;
                }
            }
            if (errorJson != null && errorJson.containsKey("payload")) {
                payload = errorJson.getJSONObject("payload");
                if (payload != null && payload.containsKey("output") ) {
                    //服务端错误，错误消息在payload中，可以恢复
                    com.alibaba.fastjson.JSONObject output = payload.getJSONObject("output");
                    if (output != null && output.containsKey("event") && output.getString("event").equals("Error")) {
                        String errorCode = output.getString("error_code");
                        String errorMsg = output.getString("error_message");
                        needRestart = false;
                    }
                }
            }
            printErrorMessage(errorCode, errorMsg); //打印错误消息
            if (needRestart) {
                restartConversation(); //重启对话
            }
        }
```
