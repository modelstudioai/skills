# 获取API Key

使用阿里云百炼的大模型或应用前，请先获取API Key作为鉴权凭证。

**说明**

本文介绍的是百炼按量付费的 API Key。如果您使用的是 Token Plan 或 Coding Plan，请使用对应的专属 API Key（以`sk-sp-`开头），获取方式请参见[Token Plan API Key](https://help.aliyun.com/zh/model-studio/token-plan-quickstart#tp04-h-step2)和[Coding Plan 的 API Key](https://help.aliyun.com/zh/model-studio/coding-plan#2531c37fd64f9)。

## **获取API Key**

**重要**

需使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)，或具备`管理员`或`API-Key`[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)的[子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。

## 华北2（北京）、新加坡等地域

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)首页，在页面右上角选择**华北2（北京）**、 **新加坡**、**日本（东京）**、**德国（法兰克福）**地域，进入[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)页面，单击**创建API Key**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属业务空间**：建议选择默认业务空间。
        
    -   **描述**（可选，最多200字符）：输入描述信息，方便后续识别该 API Key 的用途。
        
    -   **权限**：建议选择**全部**，若有更精细的权限控制需求，可以选择**自定义**来控制可访问 IP 和 可访问模型。
        
    
    **如何选择 API Key 的权限配置？**
    
    阿里云百炼提供两种类型的权限配置，请根据实际需求进行选择：
    
    -   **全部**：授予该 API Key 调用所有模型与应用的权限。
        
    -   **自定义**：可配置访问 **IP 白名单**和可访问**模型范围**。
        
        > IP 白名单默认设置：IPv4 （`0.0.0.0/0`）和 IPv6 （仅北京地域支持）全部放通。
        
        > IP 白名单支持设置最多 **20** 个 IPv4、IPv6 的地址或网段。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9729022871/p1083262.png)
    
3.  创建成功后，弹窗会显示完整的 API Key 和 API Host（服务端点地址）。请立即复制或下载保存，注意妥善保管，任何获取到该密钥的人都能以您的身份发起服务请求并产生费用。关闭弹窗后将**无法再次查看或复制**明文 API Key。如果丢失，请重置或创建新的密钥。
    
    > 主账号可查看所有业务空间下的 API Key；子账号只能查看已加入业务空间中的 API Key。
    

## 美国（弗吉尼亚）地域

1.  前往[阿里云百炼控制台](https://modelstudio.console.aliyun.com/us-east-1)首页，在页面右上角切换到**美国（弗吉尼亚）**地域，进入**API Key**管理页面，单击**创建API Key**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属业务空间**：建议选择默认业务空间。
        
    -   **描述**（可选，最多200字符）：输入描述信息，方便后续识别该 API Key 的用途。
        
3.  创建成功后，弹窗会显示完整的 API Key。请立即复制并妥善保存，关闭弹窗后将无法再次查看完整的 API Key。
    
4.  在API Key列表中，点击API Key旁的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8412544571/p994217.png)图标可复制脱敏后的API Key。
    
    > 主账号可查看所有业务空间下的 API Key；子账号只能查看已加入业务空间中的 API Key。
    

**API Key 管理操作**

在 API Key 列表中，您可以对已有 API Key 执行以下操作：

-   **编辑**：修改 API Key 的描述和权限配置。
    
-   **删除**：永久删除该 API Key，删除后不可恢复。
    
-   **禁用**（美国（弗吉尼亚）地域除外）：暂停该 API Key 的使用，不影响密钥保存，可随时重新启用。
    
-   **重置**（美国（弗吉尼亚）地域除外）：生成新的密钥值，旧密钥立即失效。
    

**何时选择其他归属账号或业务空间？**

如果您有团队协作或成本分摊需求，可以了解以下概念：

-   **归属业务空间**：用于隔离不同项目或团队的资源和权限。若需管控某类用户可调用的模型，或对模型调用的费用进行分账，请创建/选择列表中的子业务空间。
    

详情请参见[API Key 权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f2704153a055r)以及[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

## **配置API Key到环境变量**

建议您把API Key配置到环境变量，从而避免在代码里显式地配置API Key，降低泄漏风险。

## Linux系统

### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  执行以下命令来将环境变量设置追加到`~/.bashrc` 文件中。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
    ```
    
    也可以手动修改`~/.bashrc` 文件。
    
    **手动修改**
    
    执行以下命令，打开`~/.bashrc` 文件。
    
    ```
    nano ~/.bashrc
    ```
    
    在配置文件中添加以下内容。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
    在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
    
2.  执行以下命令，使变更生效。
    
    ```
    source ~/.bashrc
    ```
    
3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

## macOS系统

### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  在终端中执行以下命令，查看默认Shell类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据默认Shell类型进行操作。
    
    #### **Zsh**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.zshrc` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
        ```
        
        也可以手动修改`~/.zshrc` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.zshrc
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.zshrc
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    
    #### **Bash**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.bash_profile` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bash_profile
        ```
        
        也可以手动修改`~/.bash_profile` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.bash_profile
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.bash_profile
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    

### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

> 以下命令适用于 Zsh 和 Bash。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

## Windows系统

在Windows系统中，您可以通过系统属性、CMD或PowerShell配置环境变量。

### **系统属性**

**说明**

-   此方式配置的环境变量永久生效。
    
-   修改系统环境变量需具备管理员权限。
    
-   配置环境变量后不会立即影响已经打开的命令窗口、IDE或其他正在运行的应用程序。您需要重新启动这些程序或者打开新的命令行使环境变量生效。
    

1.  在Windows系统桌面中按`Win+Q`键，在搜索框中搜索**编辑系统环境变量**，单击打开**系统属性**界面。
    
2.  在**系统属性**窗口，单击**环境变量**，然后在**系统变量**区域下单击**新建**，**变量名**填入`DASHSCOPE_API_KEY`，**变量值**填入您的DashScope API Key。
    
3.  依次单击三个窗口的**确定**，关闭系统属性配置页面，完成环境变量配置。
    
4.  打开CMD（命令提示符）窗口或Windows PowerShell窗口，执行如下命令检查环境变量是否生效。
    
    -   CMD查询命令：
        
        ```
        echo %DASHSCOPE_API_KEY%
        ```
        ```
        Microsoft Windows [版本 10.0.19045.5371]
        (c) Microsoft Corporation。保留所有权利。
        C:\Windows\system32>echo %DASHSCOPE_API_KEY%
        sk-ee16697?fe4
        C:\Windows\system32>
        ```
        
    -   Windows PowerShell查询命令：
        
        ```
        echo $env:DASHSCOPE_API_KEY
        ```
        ```
        Windows PowerShell
        版权所有 (C) Microsoft Corporation。保留所有权利。
        尝试新的跨平台 PowerShell https://aka.ms/pscore6
        PS C:\Windows\system32> echo $env:DASHSCOPE_API_KEY
        sk-ee166797fe40xxx
        PS C:\Windows\system32>
        ```
        

### **CMD**

#### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在CMD中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  打开一个新的CMD窗口。
    
3.  在新的CMD窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo %DASHSCOPE_API_KEY%
    ```
    

#### **添加临时性环境变量**

如果您仅希望在当前会话中使用该环境变量，可以在CMD中运行以下命令。

```
REM 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo %DASHSCOPE_API_KEY%
```

### **PowerShell**

#### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在PowerShell中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的PowerShell窗口。
    
3.  在新的PowerShell窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo $env:DASHSCOPE_API_KEY
    ```
    

### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以在PowerShell中运行以下命令。

```
# 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo $env:DASHSCOPE_API_KEY
```

## **使用API Key**

-   **方式一：在**[**第三方工具**](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)**中调用模型**
    
    常用工具配置：[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)、[Cline](https://help.aliyun.com/zh/model-studio/cline)、[Claude Code](https://help.aliyun.com/zh/model-studio/claude-code)、[Dify](https://help.aliyun.com/zh/model-studio/dify)、[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)。
    
-   **方式二：通过代码调用模型**
    
    通过代码[首次调用千问API](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)，建议[配置API Key到环境变量](#section-env-var-config)，以避免硬编码在代码中导致泄露风险。
    

**说明**

通过代码或第三方工具调用模型时，除 API Key 外还需指定**服务端点**（即创建成功弹窗中显示的 **API Host**，对应 SDK 或 HTTP 请求中的 `base_url`）。百炼同时提供 **OpenAI 兼容**与 **Anthropic 兼容**两种协议的接口，两种协议的 `base_url` 不同，且会随地域变化，请以对应接口文档中的说明为准：

-   OpenAI 兼容协议：[OpenAI兼容-Chat](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)
    
-   Anthropic 兼容协议：[Anthropic兼容-Messages](https://help.aliyun.com/zh/model-studio/anthropic-api-messages)
    

请勿以任何方式公开API Key，避免因未经授权的使用导致安全风险或资金损失。

## **API Key 安全升级说明**

百炼已对按量付费 API Key 生成和存储机制进行安全升级（美国（弗吉尼亚）地域除外）。升级前已创建的`sk-`开头的 API Key 可继续正常使用，不受影响。升级后新创建的 API Key 统一以`sk-ws`开头。

下表列出了升级前后 API Key 的主要差异。

**对比项**

**升级前创建的 API Key**

**升级后创建的 API Key**

**Key 格式**

以 `sk-` 开头，长度较短（约 32 位）

以 `sk-ws` 开头，长度较长

**明文查看**

可在控制台随时复制完整明文

仅在创建时展示一次明文，关闭弹窗后无法再次查看。如果丢失，请进行重置或重新创建

**调用能力**

可正常调用模型，功能不受影响

可正常调用模型，与升级前功能完全一致

**建议操作**

建议创建新密钥替换旧密钥，以获得更完善的安全保障

创建后请立即复制保存，妥善保管

## **通过 API 管理 API Key**

除在控制台操作外，阿里云百炼还提供 OpenAPI，支持以编程方式创建、查询、编辑、删除、启用、禁用和重置 API Key，便于将 API Key 的管理集成到自动化运维流程中。

**说明**

调用以下接口需使用阿里云账号的 AccessKey 进行签名认证（而非 API Key 本身），并具备相应的 RAM 权限。您可以在各接口的 OpenAPI 开发者门户页面在线调试，也可以通过各语言的阿里云 SDK 调用。

**接口**

**说明**

[CreateApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/CreateApiKey)

创建 API Key。

[GetApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetApiKey)

查询指定 API Key 的信息。

[ListApiKeys](https://api.aliyun.com/api/ModelStudio/2026-02-10/ListApiKeys)

查询 API Key 列表。

[UpdateApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/UpdateApiKey)

编辑 API Key，如修改描述与权限配置。

[DeleteApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/DeleteApiKey)

删除 API Key，删除后不可恢复。

[EnableApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/EnableApiKey)

启用 API Key（美国（弗吉尼亚）地域除外）。

[DisableApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/DisableApiKey)

禁用 API Key，不影响密钥保存，可随时重新启用（美国（弗吉尼亚）地域除外）。

[ResetApiKey](https://api.aliyun.com/api/ModelStudio/2026-02-10/ResetApiKey)

重置 API Key，生成新的密钥值，旧密钥立即失效（美国（弗吉尼亚）地域除外）。

## API Key权限说明

API Key的调用权限完全由其**归属业务空间**决定。**同一空间内的API Key权限相同**，无需为不同模型（如文生文、文生图、语音合成）创建不同的API Key。

-   **默认业务空间下的API Key：**可调用所有标准模型，以及默认业务空间内的[应用](https://help.aliyun.com/zh/model-studio/application-introduction)。
    
-   **子业务空间下的API Key：**可调用该子业务空间已获得[授权](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)的标准模型，以及该子业务空间内的应用。
    

**调用在阿里云百炼**[**调优后的模型**](https://help.aliyun.com/zh/model-studio/model-training-overview)**：**此类模型部署成功后，仅能用其所在业务空间的API Key调用，无需[授权](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)。

**说明**

您可以在**创建API Key** 或点击已有 API Key 操作列的**编辑**时，将**权限**切换为**自定义**，即可配置：

> 仅 美国（弗吉尼亚）地域 不支持以下配置

-   **IP 访问白名单**：仅允许名单内的 IP 使用该 API Key 发起调用（支持 IPv4、IPv6 与网段）。
    
-   **访问权限范围**：为该API Key 勾选可访问的模型或应用；未勾选的资源无法通过此API Key 调用。
    

## **API Key时效性说明**

创建的API Key没有失效日期，手动删除后即失效。

若需为第三方应用或用户提供临时访问权限，或需严格控制敏感数据访问、删除等高风险操作，可[生成临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（有效期60秒），避免暴露长期有效的API Key，降低泄露风险。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

**Q：单个主账号下最多能创建多少个API Key？**

A：对于华北2（北京）、新加坡、日本（东京）和德国（法兰克福）地域，每个主账号在每个地域最多可创建50个API Key。

对于美国（弗吉尼亚）地域，每个归属账号（包括主账号）最多可创建20个API Key。

**Q：RAM用户被删除后，其创建的API Key是否依然可用？**

A：在RAM控制台中[禁用或删除RAM用户](https://help.aliyun.com/zh/ram/user-guide/delete-a-ram-user)后，其创建的所有API Key均将失效，无法再用于模型调用。

**Q：用echo命令确认环境变量设置成功了，为什么运行代码还是提示找不到API Key？**

A：具体原因如下：

-   情况一：**没有设置永久性环境变量**。临时环境变量只在当前终端会话有效，对于已经启动的 IDE 或其他应用程序并不会生效。请参考本文中设置永久性环境变量的方法。
    
-   情况二：**没有重启IDE、命令行工具或应用**。
    
    -   通常需要重启IDE（如VS Code）或命令行工具，使其能够加载最新的环境变量。
        
    -   如果在部署应用后设置了环境变量，可能需要重启应用服务，让应用能够重新加载环境变量。
        
-   情况三：**需要在配置文件添加环境变量**。如果您的应用是通过服务管理器（如systemd、supervisord）启动的，可能需要在服务管理器的配置文件中添加环境变量。
    
-   情况四：**用了sudo命令**。如果使用`sudo python xx.py`运行脚本，可能会遗漏当前用户环境变量，因为`sudo`默认不继承所有环境变量。您可采用`sudo -E python xx.py`命令，其中的`-E` 参数确保环境变量被传递。如有权限执行该脚本，可以直接执行 `python xx.py`。
