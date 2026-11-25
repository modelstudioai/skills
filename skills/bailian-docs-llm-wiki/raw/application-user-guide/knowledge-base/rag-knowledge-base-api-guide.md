# 知识库API指南

阿里云百炼知识库提供开放的API接口，便于您快速接入现有业务系统，实现自动化操作，并应对复杂的检索需求。

> **重要**
>
> 本文档仅适用于文档搜索类知识库。

> **重要**
>
> 知识库相关功能在中国站仅支持**华北2（北京）**地域，在国际站仅支持**新加坡**地域开通和使用，其他地域如德国（法兰克福）等均不支持知识库功能。

<a id="前置步骤"></a>

<a id="71fcfbd434agq"></a>

## 前置步骤

1.  [子账号](../application-permission-management/application-permission-management-overview.md)（主账号不需要）需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management)（AliyunBailianDataFullAccess策略），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)，然后才能通过阿里云API操作知识库。
    
    > 子账号只能操作已加入业务空间中的知识库；主账号可操作所有业务空间下的知识库。
    
2.  安装最新版[阿里云百炼SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29&language=python-tea&tab=primer-doc)，以调用知识库相关的阿里云API。如何安装请参考[阿里云SDK开发参考](https://help.aliyun.com/sdk/developer-reference/)目录下文档。
    
    > 如果SDK不能满足需求，可以通过[签名机制](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)（较为复杂）HTTP请求知识库的相关接口。具体对接方式请参见[API概览](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-overview)。
    
3.  [获取AccessKey和AccessKey Secret](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)以及[业务空间 ID](https://help.aliyun.com/zh/model-studio/use-workspace)，并将它们配置到系统环境变量，以运行示例代码。以Linux操作系统为例：
    
    > 如果您使用了 IDE 或其他辅助开发插件，需自行将ALIBABA\_CLOUD\_ACCESS\_KEY\_ID、ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET和WORKSPACE\_ID变量配置到相应的开发环境中。
    

<a id="code-block"></a>

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID='您的阿里云访问密钥ID'
export ALIBABA_CLOUD_ACCESS_KEY_SECRET='您的阿里云访问密钥密码'
export WORKSPACE_ID='您的阿里云百炼业务空间ID'
```

4.  准备好示例知识文档[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250428/tfewui/%E9%98%BF%E9%87%8C%E4%BA%91%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，用于创建知识库。

<a id="accordion-完整示例代码"></a>

完整示例代码

<a id="sec-tabs"></a>

<a id="创建知识库"></a>

<a id="创建知识库-h4"></a>

#### 创建知识库

> **重要**
>
> -   在调用本示例之前，请务必完成上述所有[前置步骤](rag-knowledge-base-api-guide.md#71fcfbd434agq)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
> -   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
import time

import requests
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")

    return len(missing_vars) == 0

def calculate_md5(file_path: str) -> str:
    """
    计算文件的MD5值。

    参数:
        file_path (str): 文件本地路径。

    返回:
        str: 文件的MD5值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, "rb") as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

def get_file_size(file_path: str) -> int:
    """
    获取文件大小（以字节为单位）。
    参数:
        file_path (str): 文件本地路径。
    返回:
        int: 文件大小（以字节为单位）。
    """
    return os.path.getsize(file_path)

# 初始化客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 申请文件上传租约
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)

# 上传文件到临时存储
def upload_file(pre_signed_url, headers, file_path):
    """
    将文件上传到阿里云百炼服务。
    参数:
        pre_signed_url (str): 上传租约中的 URL。
        headers (dict): 上传请求的头部。
        file_path (str): 文件本地路径。
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    upload_headers = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    }
    response = requests.put(pre_signed_url, data=file_content, headers=upload_headers)
    response.raise_for_status()

# 添加文件到类目中
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)

# 查询文件的解析状态
def describe_file(client, workspace_id, file_id):
    """
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)

# 初始化知识库（索引）
def create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type):
    """
    在阿里云百炼服务中创建知识库（初始化）。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。
        name (str): 知识库名称。
        structure_type (str): 知识库的数据类型。
        source_type (str): 应用数据的数据类型，支持类目类型和文件类型。
        sink_type (str): 知识库的向量存储类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        name=name,
        source_type=source_type,
        sink_type=sink_type,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.create_index_with_options(workspace_id, request, headers, runtime)

# 提交索引任务
def submit_index(client, workspace_id, index_id):
    """
    向阿里云百炼服务提交索引任务。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)

# 等待索引任务完成
def get_index_job_status(client, workspace_id, job_id, index_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

def create_knowledge_base(
        file_path: str,
        workspace_id: str,
        name: str
):
    """
    使用阿里云百炼服务创建知识库。
    参数:
        file_path (str): 文件本地路径。
        workspace_id (str): 业务空间ID。
        name (str): 知识库名称。
    返回:
        str or None: 如果成功，返回知识库ID；否则返回None。
    """
    # 设置默认值
    category_id = 'default'
    parser = 'DASHSCOPE_DOCMIND'
    source_type = 'DATA_CENTER_FILE'
    structure_type = 'unstructured'
    sink_type = 'DEFAULT'
    try:
        # 步骤1：初始化客户端（Client）
        print("步骤1：初始化Client")
        client = create_client()
        # 步骤2：准备文件信息
        print("步骤2：准备文件信息")
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        # 步骤3：申请上传租约
        print("步骤3：向阿里云百炼申请上传租约")
        lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        # 步骤4：上传文件
        print("步骤4：上传文件到阿里云百炼")
        upload_file(upload_url, upload_headers, file_path)
        # 步骤5：将文件添加到服务器
        print("步骤5：将文件添加到阿里云百炼服务器")
        add_response = add_file(client, lease_id, parser, category_id, workspace_id)
        file_id = add_response.body.data.file_id
        # 步骤6：检查文件状态
        print("步骤6：检查阿里云百炼中的文件状态")
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"当前文件状态：{status}")
            if status == 'INIT':
                print("文件待解析，请稍候...")
            elif status == 'PARSING':
                print("文件解析中，请稍候...")
            elif status == 'PARSE_SUCCESS':
                print("文件解析完成！")
                break
            else:
                print(f"未知的文件状态：{status}，请联系技术支持。")
                return None
            time.sleep(5)
        # 步骤7：初始化知识库
        print("步骤7：在阿里云百炼中初始化知识库")
        index_response = create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type)
        index_id = index_response.body.data.id
        # 步骤8：提交索引任务
        print("步骤8：向阿里云百炼提交索引任务")
        submit_response = submit_index(client, workspace_id, index_id)
        job_id = submit_response.body.data.id
        # 步骤9：获取索引任务状态
        print("步骤9：获取阿里云百炼索引任务状态")
        while True:
            get_index_job_status_response = get_index_job_status(client, workspace_id, job_id, index_id)
            status = get_index_job_status_response.body.data.status
            print(f"当前索引任务状态：{status}")
            if status == 'COMPLETED':
                break
            time.sleep(5)
        print("阿里云百炼知识库创建成功！")
        return index_id
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    file_path = input("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
    kb_name = input("请为您的知识库输入一个名称：")
    workspace_id = os.environ.get('WORKSPACE_ID')
    create_knowledge_base(file_path, workspace_id, kb_name)

if __name__ == '__main__':
    main()
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class KnowledgeBaseCreate {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 计算文件的MD5值。
     *
     * @param filePath 文件本地路径
     * @return 文件的MD5值
     * @throws Exception 如果计算过程中发生错误
     */
    public static String calculateMD5(String filePath) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(filePath)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesRead);
            }
        }
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param filePath 文件本地路径
     * @return 文件大小（以字节为单位）
     */
    public static String getFileSize(String filePath) {
        File file = new File(filePath);
        long fileSize = file.length();
        return String.valueOf(fileSize);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return 配置好的客户端对象
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param client      客户端对象
     * @param categoryId  类目ID
     * @param fileName    文件名称
     * @param fileMd5     文件的MD5值
     * @param fileSize    文件大小（以字节为单位）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
        applyFileUploadLeaseRequest.setFileName(fileName);
        applyFileUploadLeaseRequest.setMd5(fileMd5);
        applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
        applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        return applyFileUploadLeaseResponse;
    }

    /**
     * 上传文件到临时存储。
     *
     * @param preSignedUrl 上传租约中的 URL
     * @param headers      上传请求的头部
     * @param filePath     文件本地路径
     * @throws Exception 如果上传过程中发生错误
     */
    public static void uploadFile(String preSignedUrl, Map<String, String> headers, String filePath) throws Exception {
        File file = new File(filePath);
        if (!file.exists() || !file.isFile()) {
            throw new IllegalArgumentException("文件不存在或不是普通文件: " + filePath);
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            URL url = new URL(preSignedUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("PUT");
            conn.setDoOutput(true);

            // 设置上传请求头
            conn.setRequestProperty("X-bailian-extra", headers.get("X-bailian-extra"));
            conn.setRequestProperty("Content-Type", headers.get("Content-Type"));

            // 分块读取并上传文件
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                conn.getOutputStream().write(buffer, 0, bytesRead);
            }

            int responseCode = conn.getResponseCode();
            if (responseCode != 200) {
                throw new RuntimeException("上传失败: " + responseCode);
            }
        }
    }

    /**
     * 将文件添加到类目中。
     *
     * @param client      客户端对象
     * @param leaseId     租约ID
     * @param parser      用于文件的解析器
     * @param categoryId  类目ID
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
        addFileRequest.setLeaseId(leaseId);
        addFileRequest.setParser(parser);
        addFileRequest.setCategoryId(categoryId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应对象
     */
    public static DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 在阿里云百炼服务中创建知识库（初始化）。
     *
     * @param client        客户端对象
     * @param workspaceId   业务空间ID
     * @param fileId        文件ID
     * @param name          知识库名称
     * @param structureType 知识库的数据类型
     * @param sourceType    应用数据的数据类型，支持类目类型和文件类型
     * @param sinkType      知识库的向量存储类型
     * @return 阿里云百炼服务的响应对象
     */
    public static CreateIndexResponse createIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId, String name, String structureType, String sourceType, String sinkType) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.CreateIndexRequest createIndexRequest = new com.aliyun.bailian20231229.models.CreateIndexRequest();
        createIndexRequest.setStructureType(structureType);
        createIndexRequest.setName(name);
        createIndexRequest.setSourceType(sourceType);
        createIndexRequest.setSinkType(sinkType);
        createIndexRequest.setDocumentIds(Collections.singletonList(fileId));
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.createIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
    }

    /**
     * 向阿里云百炼服务提交索引任务。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static SubmitIndexJobResponse submitIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.SubmitIndexJobRequest submitIndexJobRequest = new com.aliyun.bailian20231229.models.SubmitIndexJobRequest();
        submitIndexJobRequest.setIndexId(indexId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.submitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param jobId       任务ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
        getIndexJobStatusRequest.setIndexId(indexId);
        getIndexJobStatusRequest.setJobId(jobId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        GetIndexJobStatusResponse getIndexJobStatusResponse = null;
        getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        return getIndexJobStatusResponse;
    }

    /**
     * 使用阿里云百炼服务创建知识库。
     *
     * @param filePath    文件本地路径
     * @param workspaceId 业务空间ID
     * @param name        知识库名称
     * @return 如果成功，返回知识库ID；否则返回 null
     */
    public static String createKnowledgeBase(String filePath, String workspaceId, String name) {
        // 设置默认值
        String categoryId = "default";
        String parser = "DASHSCOPE_DOCMIND";
        String sourceType = "DATA_CENTER_FILE";
        String structureType = "unstructured";
        String sinkType = "DEFAULT";
        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：初始化Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：准备文件信息
            System.out.println("步骤2：准备文件信息");
            String fileName = new File(filePath).getName();
            String fileMd5 = calculateMD5(filePath);
            String fileSize = getFileSize(filePath);

            // 步骤3：申请上传租约
            System.out.println("步骤3：向阿里云百炼申请上传租约");
            ApplyFileUploadLeaseResponse leaseResponse = applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            String leaseId = leaseResponse.getBody().getData().getFileUploadLeaseId();
            String uploadUrl = leaseResponse.getBody().getData().getParam().getUrl();
            Object uploadHeaders = leaseResponse.getBody().getData().getParam().getHeaders();

            // 步骤4：上传文件
            System.out.println("步骤4：上传文件到阿里云百炼");
            // 请自行安装jackson-databind
            // 将上一步的uploadHeaders转换为Map(Key-Value形式)
            ObjectMapper mapper = new ObjectMapper();
            Map<String, String> uploadHeadersMap = (Map<String, String>) mapper.readValue(mapper.writeValueAsString(uploadHeaders), Map.class);
            uploadFile(uploadUrl, uploadHeadersMap, filePath);

            // 步骤5：将文件添加到服务器
            System.out.println("步骤5：将文件添加到阿里云百炼服务器");
            AddFileResponse addResponse = addFile(client, leaseId, parser, categoryId, workspaceId);
            String fileId = addResponse.getBody().getData().getFileId();

            // 步骤6：检查文件状态
            System.out.println("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                DescribeFileResponse describeResponse = describeFile(client, workspaceId, fileId);
                String status = describeResponse.getBody().getData().getStatus();
                System.out.println("当前文件状态：" + status);

                if (status.equals("INIT")) {
                    System.out.println("文件待解析，请稍候...");
                } else if (status.equals("PARSING")) {
                    System.out.println("文件解析中，请稍候...");
                } else if (status.equals("PARSE_SUCCESS")) {
                    System.out.println("文件解析完成！");
                    break;
                } else {
                    System.out.println("未知的文件状态：" + status + "，请联系技术支持。");
                    return null;
                }
                TimeUnit.SECONDS.sleep(5);
            }

            // 步骤7：初始化知识库
            System.out.println("步骤7：在阿里云百炼中创建知识库");
            CreateIndexResponse indexResponse = createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
            String indexId = indexResponse.getBody().getData().getId();

            // 步骤8：提交索引任务
            System.out.println("步骤8：向阿里云百炼提交索引任务");
            SubmitIndexJobResponse submitResponse = submitIndex(client, workspaceId, indexId);
            String jobId = submitResponse.getBody().getData().getId();

            // 步骤9：获取索引任务状态
            System.out.println("步骤9：获取阿里云百炼索引任务状态");
            while (true) {
                GetIndexJobStatusResponse getStatusResponse = getIndexJobStatus(client, workspaceId, jobId, indexId);
                String status = getStatusResponse.getBody().getData().getStatus();
                System.out.println("当前索引任务状态：" + status);

                if (status.equals("COMPLETED")) {
                    break;
                }
                TimeUnit.SECONDS.sleep(5);
            }

            System.out.println("阿里云百炼知识库创建成功！");
            return indexId;

        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        if (!checkEnvironmentVariables()) {
            return;
        }

        System.out.print("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        String filePath = scanner.nextLine();

        System.out.print("请为您的知识库输入一个名称：");
        String kbName = scanner.nextLine();

        String workspaceId = System.getenv("WORKSPACE_ID");
        String result = createKnowledgeBase(filePath, workspaceId, kbName);
        if (result != null) {
            System.out.println("知识库ID: " + result);
        }
    }
}
```

<a id="fig-code-group-php-tab"></a>

PHP

<a id="code-code-group-php"></a>

```php
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\AddFileRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ApplyFileUploadLeaseRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\CreateIndexRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\SubmitIndexJobRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\GetIndexJobStatusRequest;

class KnowledgeBaseCreate {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 计算文件的MD5值。
     *
     * @param string $filePath 文件本地路径。
     * @return string 文件的MD5值。
     */
    public static function calculateMd5($filePath) {
        $md5Hash = hash_init("md5");
        $handle = fopen($filePath, "rb");
        while (!feof($handle)) {
            $chunk = fread($handle, 4096);
            hash_update($md5Hash, $chunk);
        }
        fclose($handle);
        return hash_final($md5Hash);
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param string $filePath 文件本地路径。
     * @return int 文件大小（以字节为单位）。
     */
    public static function getFileSize($filePath) {
        return (string)filesize($filePath);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $categoryId 类目ID。
     * @param string $fileName 文件名称。
     * @param string $fileMd5 文件的MD5值。
     * @param int $fileSize 文件大小（以字节为单位）。
     * @param string $workspaceId 业务空间ID。
     * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
     */
    public static function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
        $headers = [];
        $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
            "fileName" => $fileName,
            "md5" => $fileMd5,
            "sizeInBytes" => $fileSize
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
    }

    /**
     * 上传文件到临时存储。
    *
    * @param string $preSignedUrl 上传租约中的 URL。
    * @param array $headers 上传请求的头部。
    * @param string $filePath 文件本地路径。
    */
    public static function uploadFile($preSignedUrl, $headers, $filePath) {
        $fileContent = file_get_contents($filePath);
        // 设置上传请求头
        $uploadHeaders = [
            "X-bailian-extra" => $headers["X-bailian-extra"],
            "Content-Type" => $headers["Content-Type"]
        ];
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_map(function($key, $value) {
            return "$key: $value";
        }, array_keys($uploadHeaders), $uploadHeaders));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpCode != 200) {
            throw new Exception("上传失败: " . curl_error($ch));
        }
        curl_close($ch);
    }

    /**
     * 将文件添加到类目中。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $leaseId 租约ID。
     * @param string $parser 用于文件的解析器。
     * @param string $categoryId 类目ID。
     * @param string $workspaceId 业务空间ID。
     * @return AddFileResponse 阿里云百炼服务的响应。
     */
    public static function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
        $headers = [];
        $addFileRequest = new AddFileRequest([
            "leaseId" => $leaseId,
            "parser" => $parser,
            "categoryId" => $categoryId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @return DescribeFileResponse 阿里云百炼服务的响应。
     */
    public static function describeFile($client, $workspaceId, $fileId) {
        $headers = [];
        $runtime = new RuntimeOptions([]);
        return $client->describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
    }

    /**
     * 在阿里云百炼服务中创建知识库（初始化）。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @param string $name 知识库名称。
     * @param string $structureType 知识库的数据类型。
     * @param string $sourceType 应用数据的数据类型，支持类目类型和文件类型。
     * @param string $sinkType 知识库的向量存储类型。
     * @return CreateIndexResponse 阿里云百炼服务的响应。
     */
    public static function createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType) {
        $headers = [];
        $createIndexRequest = new CreateIndexRequest([
            "structureType" => $structureType,
            "name" => $name,
            "sourceType" => $sourceType,
            "documentIds" => [
                $fileId
            ],
            "sinkType" => $sinkType
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->createIndexWithOptions($workspaceId, $createIndexRequest, $headers, $runtime);
    }

    /**
     * 向阿里云百炼服务提交索引任务。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @return SubmitIndexJobResponse 阿里云百炼服务的响应。
     */
    public static function submitIndex($client, $workspaceId, $indexId) {
        $headers = [];
        $submitIndexJobRequest = new SubmitIndexJobRequest([
            'indexId' => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->submitIndexJobWithOptions($workspaceId, $submitIndexJobRequest, $headers, $runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @param string $jobId 任务ID。
     * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
     */
    public static function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
        $headers = [];
        $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
            'indexId' => $indexId,
            'jobId' => $jobId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务创建知识库。
     *
     * @param string $filePath 文件本地路径。
     * @param string $workspaceId 业务空间ID。
     * @param string $name 知识库名称。
     * @return string|null 如果成功，返回知识库ID；否则返回null。
     */
    public static function createKnowledgeBase($filePath, $workspaceId, $name) {
        // 设置默认值
        $categoryId = 'default';
        $parser = 'DASHSCOPE_DOCMIND';
        $sourceType = 'DATA_CENTER_FILE';
        $structureType = 'unstructured';
        $sinkType = 'DEFAULT';
        try {
            // 步骤1：初始化客户端（Client）
            echo "步骤1：初始化Client\n";
            $client = self::createClient();

            // 步骤2：准备文件信息
            echo "步骤2：准备文件信息\n";
            $fileName = basename($filePath);
            $fileMd5 = self::calculateMd5($filePath);
            $fileSize = self::getFileSize($filePath);

            // 步骤3：申请上传租约
            echo "步骤3：向阿里云百炼申请上传租约\n";
            $leaseResponse = self::applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId);
            $leaseId = $leaseResponse->body->data->fileUploadLeaseId;
            $uploadUrl = $leaseResponse->body->data->param->url;
            $uploadHeaders = $leaseResponse->body->data->param->headers;
            $uploadHeadersMap = json_decode(json_encode($uploadHeaders), true);

            // 步骤4：上传文件
            echo "步骤4：上传文件到阿里云百炼\n";
            self::uploadFile($uploadUrl, $uploadHeadersMap, $filePath);

            // 步骤5：将文件添加到服务器
            echo "步骤5：将文件添加到阿里云百炼服务器\n";
            $addResponse = self::addFile($client, $leaseId, $parser, $categoryId, $workspaceId);
            $fileId = $addResponse->body->data->fileId;
            // 步骤6：检查文件状态
            echo "步骤6：检查阿里云百炼中的文件状态\n";
            while (true) {
                $describeResponse = self::describeFile($client, $workspaceId, $fileId);
                $status = $describeResponse->body->data->status;
                echo "当前文件状态：$status\n";
                if ($status == 'INIT') {
                    echo "文件待解析，请稍候...\n";
                } elseif ($status == 'PARSING') {
                    echo "文件解析中，请稍候...\n";
                } elseif ($status == 'PARSE_SUCCESS') {
                    echo "文件解析完成！\n";
                    break;
                } else {
                    echo "未知的文件状态：$status, 请联系技术支持。\n";
                    return null;
                }
                sleep(5);
            }

            // 步骤7：初始化知识库
            echo "步骤7：在阿里云百炼中初始化知识库\n";
            $indexResponse = self::createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType);
            $indexId = $indexResponse->body->data->id;

            // 步骤8：提交索引任务
            echo "步骤8：向阿里云百炼提交索引任务\n";
            $submitResponse = self::submitIndex($client, $workspaceId, $indexId);
            $jobId = $submitResponse->body->data->id;

            // 步骤9：获取索引任务状态
            echo "步骤9：获取阿里云百炼索引任务状态\n";
            while (true) {
                $getIndexJobStatusResponse = self::getIndexJobStatus($client, $workspaceId, $jobId, $indexId);
                $status = $getIndexJobStatusResponse->body->data->status;
                echo "当前索引任务状态：$status\n";
                if ($status == 'COMPLETED') {
                    break;
                }
                sleep(5);
            }
            echo "阿里云百炼知识库创建成功！\n";
            return $indexId;
        } catch (Exception $e) {
            echo "发生错误：{$e->getMessage()}\n";
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }
        $filePath = readline("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        $kbName = readline("请为您的知识库输入一个名称：");
        $workspaceId = getenv('WORKSPACE_ID');
        $result = self::createKnowledgeBase($filePath, $workspaceId, $kbName);
       if ($result) {
           echo "知识库ID: $result\n";
       } else {
           echo "知识库创建失败。\n";
       }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseCreate::main(array_slice($argv, 1));
```

<a id="fig-code-group-node-js-tab"></a>

Node.js

<a id="code-code-group-node-js"></a>

```javascript
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const crypto = require('crypto');

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbCreate {

  /**
   * 检查并提示设置必要的环境变量
   * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
   */
  static checkEnvironmentVariables() {
    const requiredVars = {
      'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
      'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
      'WORKSPACE_ID': '阿里云百炼业务空间ID'
    };

    const missing = [];
    for (const [varName, desc] of Object.entries(requiredVars)) {
      if (!process.env[varName]) {
        console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
        missing.push(varName);
      }
    }
    return missing.length === 0;
  }

  /**
   * 计算文件的MD5值
   * @param {string} filePath - 文件本地路径
   * @returns {Promise<string>} - 文件的MD5值
   */
  static async calculateMD5(filePath) {
    const hash = crypto.createHash('md5');
    const stream = fs.createReadStream(filePath);

    return new Promise((resolve, reject) => {
      stream.on('data', chunk => hash.update(chunk));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', reject);
    });
  }

  /**
   * 获取文件大小（以字节为单位），返回字符串格式
   * @param {string} filePath - 文件本地路径
   * @returns {string} - 文件大小（如 "123456"）
   */
  static getFileSize(filePath) {
    try {
      const stats = fs.statSync(filePath);
      return stats.size.toString();
    } catch (err) {
      console.error(`获取文件大小失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 创建并配置客户端（Client）
   * @return Client
   * @throws Exception
   */
  static createClient() {
    const config = new OpenApi.Config({
      accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
      accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
    });
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
    config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
    return new bailian20231229.default(config);
  }

  /**
   * 申请文件上传租约
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} categoryId - 类目ID
   * @param {string} fileName - 文件名称
   * @param {string} fileMd5 - 文件的MD5值
   * @param {string} fileSize - 文件大小（以字节为单位）
   * @param {string} workspaceId - 业务空间ID
   * @returns {Promise<bailian20231229.ApplyFileUploadLeaseResponse>} - 阿里云百炼服务的响应
   */
  static async applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
    const headers = {};
    const req = new bailian20231229.ApplyFileUploadLeaseRequest({
      md5: fileMd5,
      fileName,
      sizeInBytes: fileSize
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.applyFileUploadLeaseWithOptions(
      categoryId,
      workspaceId,
      req,
      headers,
      runtime
    );
  }

  /**
   * 上传文件到临时存储
   * @param {string} preSignedUrl - 上传租约中的URL
   * @param {Object} headers - 上传请求的头部
   * @param {string} filePath - 文件本地路径
   */
  static async uploadFile(preSignedUrl, headers, filePath) {
    const uploadHeaders = {
      "X-bailian-extra": headers["X-bailian-extra"],
      "Content-Type": headers["Content-Type"]
    };
    const stream = fs.createReadStream(filePath);
    try {
      await axios.put(preSignedUrl, stream, { headers: uploadHeaders });
    } catch (e) {
      throw new Error(`上传失败: ${e.message}`);
    }
  }

  /**
   * 添加文件到类目中
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} leaseId - 租约ID
   * @param {string} parser - 用于文件的解析器
   * @param {string} categoryId - 类目ID
   * @param {string} workspaceId - 业务空间ID
   * @returns {Promise<bailian20231229.AddFileResponse>} - 阿里云百炼服务的响应
   */
  static async addFile(client, leaseId, parser, categoryId, workspaceId) {
    const headers = {};
    const req = new bailian20231229.AddFileRequest({
      leaseId,
      parser,
      categoryId
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.addFileWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 查询文件的解析状态
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} fileId - 文件ID
   * @returns {Promise<bailian20231229.DescribeFileResponse>} - 阿里云百炼服务的响应
   */
  static async describeFile(client, workspaceId, fileId) {
    const headers = {};
    const runtime = new Util.RuntimeOptions({});
    return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
  }

  /**
   * 初始化知识库（索引）
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} fileId - 文件ID
   * @param {string} name - 知识库名称
   * @param {string} structureType - 知识库的数据类型
   * @param {string} sourceType - 应用数据的数据类型，支持类目类型和文件类型
   * @param {string} sinkType - 知识库的向量存储类型
   * @returns {Promise<bailian20231229.CreateIndexResponse>} - 阿里云百炼服务的响应
   */
  static async createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType) {
    const headers = {};
    const req = new bailian20231229.CreateIndexRequest({
      name,
      structureType,
      documentIds: [fileId],
      sourceType,
      sinkType
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.createIndexWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 提交索引任务
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} indexId - 知识库ID
   * @returns {Promise<bailian20231229.SubmitIndexJobResponse>} - 阿里云百炼服务的响应
   */
  static async submitIndex(client, workspaceId, indexId) {
    const headers = {};
    const req = new bailian20231229.SubmitIndexJobRequest({ indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.submitIndexJobWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 查询索引任务状态
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} jobId - 任务ID
   * @param {string} indexId - 知识库ID
   * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
   */
  static async getIndexJobStatus(client, workspaceId, jobId, indexId) {
    const headers = {};
    const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 创建知识库
   * @param {string} filePath - 文件本地路径
   * @param {string} workspaceId - 业务空间ID
   * @param {string} name - 知识库名称
   * @returns {Promise<string | null>} - 如果成功，返回知识库ID；否则返回null
   */
  static async createKnowledgeBase(filePath, workspaceId, name) {
    const categoryId = 'default';
    const parser = 'DASHSCOPE_DOCMIND';
    const sourceType = 'DATA_CENTER_FILE';
    const structureType = 'unstructured';
    const sinkType = 'DEFAULT';

    try {
      console.log("步骤1：初始化Client");
      const client = this.createClient();

      console.log("步骤2：准备文件信息");
      const fileName = path.basename(filePath);
      const fileMd5 = await this.calculateMD5(filePath);
      const fileSize = this.getFileSize(filePath);

      console.log("步骤3：向阿里云百炼申请上传租约")
      const leaseRes = await this.applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
      const leaseId = leaseRes.body.data.fileUploadLeaseId;
      const uploadUrl = leaseRes.body.data.param.url;
      const uploadHeaders = leaseRes.body.data.param.headers;

      console.log("步骤4：上传文件到阿里云百炼")
      await this.uploadFile(uploadUrl, uploadHeaders, filePath);

      console.log("步骤5：将文件添加到阿里云百炼服务器")
      const addRes = await this.addFile(client, leaseId, parser, categoryId, workspaceId);
      const fileId = addRes.body.data.fileId;

      console.log("步骤6：检查阿里云百炼中的文件状态")
      while (true) {
        const descRes = await this.describeFile(client, workspaceId, fileId);
        const status = descRes.body.data.status;
        console.log(`当前文件状态：${status}`);

        if (status === 'INIT') console.log("文件待解析，请稍候...");
        else if (status === 'PARSING') console.log("文件解析中，请稍候...");
        else if (status === 'PARSE_SUCCESS') break;
        else {
          console.error(`未知的文件状态：${status}，请联系技术支持。`);
          return null;
        }
        await this.sleep(5);
      }

      console.log("步骤7：在阿里云百炼中初始化知识库")
      const indexRes = await this.createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
      const indexId = indexRes.body.data.id;

      console.log("步骤8：向阿里云百炼提交索引任务")
      const submitRes = await this.submitIndex(client, workspaceId, indexId);
      const jobId = submitRes.body.data.id;

      console.log("步骤9：获取阿里云百炼索引任务状态")
      while (true) {
        const jobRes = await this.getIndexJobStatus(client, workspaceId, jobId, indexId);
        const status = jobRes.body.data.status;
        console.log(`当前索引任务状态：${status}`);
        if (status === 'COMPLETED') break;
        await this.sleep(5);
      }
      console.log("阿里云百炼知识库创建成功！");
      return indexId;
    } catch (e) {
      console.error(`发生错误：${e.message}`);
      return null;
    }
  }

  /**
   * 等待指定时间（秒）
   * @param {number} seconds - 等待时间（秒）
   * @returns {Promise<void>}
   */
  static sleep(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
  }

  static async main(args) {
    if (!this.checkEnvironmentVariables()) {
      console.log("环境变量校验未通过。");
      return;
    }

    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    try {
      const filePath = await new Promise((resolve, reject) => {
        readline.question("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：", (ans) => {
          ans.trim() ? resolve(ans) : reject(new Error("路径不能为空"));
        });
      });
      const kbName = await new Promise((resolve, reject) => {
        readline.question("请为您的知识库输入一个名称：", (ans) => {
          ans.trim() ? resolve(ans) : reject(new Error("知识库名称不能为空"));
        });
      });
      const workspaceId = process.env.WORKSPACE_ID;

      const result = await KbCreate.createKnowledgeBase(filePath, workspaceId, kbName);
      if (result) console.log(`知识库ID: ${result}`);
      else console.log("知识库创建失败。");
    } catch (err) {
      console.error(err.message);
    } finally {
      readline.close();
    }
  }
}

exports.KbCreate = KbCreate;
KbCreate.main(process.argv.slice(2));
```

<a id="fig-code-group-c-tab"></a>

C#

<a id="code-code-group-c"></a>

```csharp
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseCreate
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 计算文件的MD5值。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件的MD5值</returns>
        /// <exception cref="Exception">计算过程中发生错误时抛出异常</exception>
        public static string CalculateMD5(string filePath)
        {
            using (var md5 = MD5.Create())
            {
                using (var stream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    byte[] hashBytes = md5.ComputeHash(stream);
                    StringBuilder sb = new StringBuilder();
                    foreach (byte b in hashBytes)
                    {
                        sb.Append(b.ToString("x2"));
                    }
                    return sb.ToString();
                }
            }
        }

        /// <summary>
        /// 获取文件大小（以字节为单位）。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件大小（以字节为单位）</returns>
        public static string GetFileSize(string filePath)
        {
            var file = new FileInfo(filePath);
            return file.Length.ToString();
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址.
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 申请文件上传租约。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="fileName">文件名称</param>
        /// <param name="fileMd5">文件的MD5值</param>
        /// <param name="fileSize">文件大小（以字节为单位）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string categoryId,
            string fileName,
            string fileMd5,
            string fileSize,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
            {
                FileName = fileName,
                Md5 = fileMd5,
                SizeInBytes = fileSize
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        }

        /// <summary>
        /// 上传文件到临时存储。
        /// </summary>
        /// <param name="preSignedUrl">上传租约中的 URL</param>
        /// <param name="headers">上传请求的头部</param>
        /// <param name="filePath">文件本地路径</param>
        /// <exception cref="Exception">上传过程中发生错误时抛出异常</exception>
        public static void UploadFile(string preSignedUrl, Dictionary<string, string> headers, string filePath)
        {
            var file = new FileInfo(filePath);
            if (!File.Exists(filePath))
            {
                throw new ArgumentException($"文件不存在或不是普通文件: {filePath}");
            }

            using (var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                var url = new Uri(preSignedUrl);
                var conn = (HttpWebRequest)WebRequest.Create(url);
                conn.Method = "PUT";
                conn.ContentType = headers["Content-Type"];
                conn.Headers.Add("X-bailian-extra", headers["X-bailian-extra"]);

                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fs.Read(buffer, 0, buffer.Length)) > 0)
                {
                    conn.GetRequestStream().Write(buffer, 0, bytesRead);
                }

                using (var response = (HttpWebResponse)conn.GetResponse())
                {
                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        throw new Exception($"上传失败: {response.StatusCode}");
                    }
                }
            }
        }

        /// <summary>
        /// 将文件添加到类目中。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="leaseId">租约ID</param>
        /// <param name="parser">用于文件的解析器</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string leaseId,
            string parser,
            string categoryId,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
            {
                LeaseId = leaseId,
                Parser = parser,
                CategoryId = categoryId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
        }

        /// <summary>
        /// 查询文件的基本信息。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
        }

        /// <summary>
        /// 在阿里云百炼服务中创建知识库（初始化）。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <param name="name">知识库名称</param>
        /// <param name="structureType">知识库的数据类型</param>
        /// <param name="sourceType">应用数据的数据类型，支持类目类型和文件类型</param>
        /// <param name="sinkType">知识库的向量存储类型</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexResponse CreateIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId,
            string name,
            string structureType,
            string sourceType,
            string sinkType)
        {
            var headers = new Dictionary<string, string>() { };
            var createIndexRequest = new AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexRequest
            {
                StructureType = structureType,
                Name = name,
                SourceType = sourceType,
                SinkType = sinkType,
                DocumentIds = new List<string> { fileId }
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.CreateIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
        }

        /// <summary>
        /// 向阿里云百炼服务提交索引任务。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobResponse SubmitIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var submitIndexJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobRequest
            {
                IndexId = indexId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.SubmitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
        }

        /// <summary>
        /// 查询索引任务状态。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="jobId">任务ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string jobId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
            {
                IndexId = indexId,
                JobId = jobId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务创建知识库。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="name">知识库名称</param>
        /// <returns>如果成功，返回知识库ID；否则返回 null</returns>
        public static string CreateKnowledgeBase(string filePath, string workspaceId, string name)
        {
            // 设置默认值
            string categoryId = "default";
            string parser = "DASHSCOPE_DOCMIND";
            string sourceType = "DATA_CENTER_FILE";
            string structureType = "unstructured";
            string sinkType = "DEFAULT";

            try
            {
                Console.WriteLine("步骤1：初始化Client");
                AlibabaCloud.SDK.Bailian20231229.Client client = CreateClient();

                Console.WriteLine("步骤2：准备文件信息");
                var fileInfo = new FileInfo(filePath);
                string fileName = fileInfo.Name;
                string fileMd5 = CalculateMD5(filePath);
                string fileSize = GetFileSize(filePath);

                Console.WriteLine("步骤3：向阿里云百炼申请上传租约");
                Bailian20231229.Models.ApplyFileUploadLeaseResponse leaseResponse = ApplyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
                string leaseId = leaseResponse.Body.Data.FileUploadLeaseId;
                string uploadUrl = leaseResponse.Body.Data.Param.Url;
                var uploadHeaders = leaseResponse.Body.Data.Param.Headers;

                Console.WriteLine("步骤4：上传文件到阿里云百炼");
                // 请自行安装Newtonsoft.Json
                var uploadHeadersMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(JsonConvert.SerializeObject(uploadHeaders));
                UploadFile(uploadUrl, uploadHeadersMap, filePath);

                Console.WriteLine("步骤5：将文件添加到阿里云百炼服务器");
                Bailian20231229.Models.AddFileResponse addResponse = AddFile(client, leaseId, parser, categoryId, workspaceId);
                string fileId = addResponse.Body.Data.FileId;

                Console.WriteLine("步骤6：检查阿里云百炼中的文件状态");
                while (true)
                {
                    Bailian20231229.Models.DescribeFileResponse describeResponse = DescribeFile(client, workspaceId, fileId);
                    string status = describeResponse.Body.Data.Status;
                    Console.WriteLine($"当前文件状态：{status}");

                    if (status == "INIT")
                    {
                        Console.WriteLine("文件待解析，请稍候...");
                    }
                    else if (status == "PARSING")
                    {
                        Console.WriteLine("文件解析中，请稍候...");
                    }
                    else if (status == "PARSE_SUCCESS")
                    {
                        Console.WriteLine("文件解析完成！");
                        break;
                    }
                    else
                    {
                        Console.WriteLine($"未知的文件状态：{status}，请联系技术支持。");
                        return null;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤7：在阿里云百炼中创建知识库");
                Bailian20231229.Models.CreateIndexResponse indexResponse = CreateIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
                string indexId = indexResponse.Body.Data.Id;

                Console.WriteLine("步骤8：向阿里云百炼提交索引任务");
                Bailian20231229.Models.SubmitIndexJobResponse submitResponse = SubmitIndex(client, workspaceId, indexId);
                string jobId = submitResponse.Body.Data.Id;

                Console.WriteLine("步骤9：获取阿里云百炼索引任务状态");
                while (true)
                {
                    Bailian20231229.Models.GetIndexJobStatusResponse getStatusResponse = GetIndexJobStatus(client, workspaceId, jobId, indexId);
                    string status = getStatusResponse.Body.Data.Status;
                    Console.WriteLine($"当前索引任务状态：{status}");

                    if (status == "COMPLETED")
                    {
                        break;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("阿里云百炼知识库创建成功！");
                return indexId;

            }
            catch (Exception ex)
            {
                Console.WriteLine($"发生错误：{ex.Message}");
                Console.WriteLine("错误详情: " + ex.StackTrace);
                return null;
            }
        }

        /// <summary>
        /// 主函数。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                return;
            }

            Console.Write("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
            string filePath = Console.ReadLine();

            Console.Write("请为您的知识库输入一个名称：");
            string kbName = Console.ReadLine();

            string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
            string result = CreateKnowledgeBase(filePath, workspaceId, kbName);
            if (result != null)
            {
                Console.WriteLine($"知识库ID: {result}");
            }
        }
    }
}
```

<a id="fig-code-group-go-tab"></a>

Go

<a id="code-code-group-go"></a>

```go
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
	"github.com/go-resty/resty/v2"
)

// CheckEnvironmentVariables 检查并提示设置必要的环境变量。
func CheckEnvironmentVariables() bool {
	// 必要的环境变量及其描述.
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// CalculateMD5 计算文件的MD5值。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件的MD5值。
//   - error: 错误信息.
func CalculateMD5(filePath string) (_result string, _err error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	md5Hash := md5.New()
	_, err = io.Copy(md5Hash, file)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", md5Hash.Sum(nil)), nil
}

// GetFileSize 获取文件大小（以字节为单位）。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件大小（以字节为单位）。
//   - error: 错误信息。
func GetFileSize(filePath string) (_result string, _err error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%d", info.Size()), nil
}

// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}

// UploadFile 将文件上传到阿里云百炼服务。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	body, err := io.ReadAll(file)
	if err != nil {
		return err
	}

	client := resty.New()
	uploadHeaders := map[string]string{
		"X-bailian-extra": headers["X-bailian-extra"],
		"Content-Type":    headers["Content-Type"],
	}

	resp, err := client.R().
		SetHeaders(uploadHeaders).
		SetBody(body).
		Put(preSignedUrl)

	if err != nil {
		return err
	}

	if resp.IsError() {
		return fmt.Errorf("HTTP 错误: %d", resp.StatusCode())
	}

	return nil
}

// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}

// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - any: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}

// CreateIndex 在阿里云百炼服务中创建知识库（初始化）。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//   - name (string): 知识库名称。
//   - structureType (string): 知识库的数据类型。
//   - sourceType (string): 应用数据的数据类型，支持类目类型和文件类型。
//   - sinkType (string): 知识库的向量存储类型。
//
// 返回:
//   - *bailian20231229.CreateIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func CreateIndex(client *bailian20231229.Client, workspaceId, fileId, name, structureType, sourceType, sinkType string) (_result *bailian20231229.CreateIndexResponse, _err error) {
	headers := make(map[string]*string)
	createIndexRequest := &bailian20231229.CreateIndexRequest{
		StructureType: tea.String(structureType),
		Name:          tea.String(name),
		SourceType:    tea.String(sourceType),
		SinkType:      tea.String(sinkType),
		DocumentIds:   []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.CreateIndexWithOptions(tea.String(workspaceId), createIndexRequest, headers, runtime)
}

// SubmitIndex 提交索引任务。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.SubmitIndexJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.SubmitIndexJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexJobRequest := &bailian20231229.SubmitIndexJobRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexJobWithOptions(tea.String(workspaceId), submitIndexJobRequest, headers, runtime)
}

// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}

// CreateKnowledgeBase 使用阿里云百炼服务创建知识库。
//
// 参数:
//   - filePath (string): 文件本地路径。
//   - workspaceId (string): 业务空间ID。
//   - name (string): 知识库名称。
//
// 返回:
//   - string or nil: 如果成功，返回知识库ID；否则返回nil。
//   - error: 错误信息。
func CreateKnowledgeBase(filePath, workspaceId, name string) (_result string, _err error) {
	categoryId := "default"
	parser := "DASHSCOPE_DOCMIND"
	sourceType := "DATA_CENTER_FILE"
	structureType := "unstructured"
	sinkType := "DEFAULT"

	fmt.Println("步骤1：初始化Client")
	client, err := CreateClient()
	if err != nil {
		return "", err
	}

	fmt.Println("步骤2：准备文件信息")
	fileName := filepath.Base(filePath)
	fileMD5, err := CalculateMD5(filePath)
	if err != nil {
		return "", err
	}
	fileSizeStr, err := GetFileSize(filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤3：向阿里云百炼申请上传租约")
	leaseResponse, err := ApplyLease(client, categoryId, fileName, fileMD5, fileSizeStr, workspaceId)
	if err != nil {
		return "", err
	}

	leaseId := tea.StringValue(leaseResponse.Body.Data.FileUploadLeaseId)
	uploadURL := tea.StringValue(leaseResponse.Body.Data.Param.Url)
	uploadHeaders := leaseResponse.Body.Data.Param.Headers

	jsonData, err := json.Marshal(uploadHeaders)
	if err != nil {
		return "", err
	}

	var uploadHeadersMap map[string]string
	err = json.Unmarshal(jsonData, &uploadHeadersMap)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤4：上传文件到阿里云百炼")
	err = UploadFile(uploadURL, uploadHeadersMap, filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤5：将文件添加到阿里云百炼服务器")
	addResponse, err := AddFile(client, leaseId, parser, categoryId, workspaceId)
	if err != nil {
		return "", err
	}
	fileID := tea.StringValue(addResponse.Body.Data.FileId)

	fmt.Println("步骤6：检查阿里云百炼中的文件状态")
	for {
		describeResponse, err := DescribeFile(client, workspaceId, fileID)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(describeResponse.Body.Data.Status)
		fmt.Printf("当前文件状态：%s\n", status)

		if status == "INIT" {
			fmt.Println("文件待解析，请稍候...")
		} else if status == "PARSING" {
			fmt.Println("文件解析中，请稍候...")
		} else if status == "PARSE_SUCCESS" {
			fmt.Println("文件解析完成！")
			break
		} else {
			fmt.Printf("未知的文件状态：%s，请联系技术支持。\n", status)
			return "", fmt.Errorf("unknown document status: %s", status)
		}
		time.Sleep(5 * time.Second)
	}

	fmt.Println("步骤7：在阿里云百炼中初始化知识库")
	indexResponse, err := CreateIndex(client, workspaceId, fileID, name, structureType, sourceType, sinkType)
	if err != nil {
		return "", err
	}
	indexID := tea.StringValue(indexResponse.Body.Data.Id)

	fmt.Println("步骤8：向阿里云百炼提交索引任务")
	submitResponse, err := SubmitIndex(client, workspaceId, indexID)
	if err != nil {
		return "", err
	}
	jobID := tea.StringValue(submitResponse.Body.Data.Id)

	fmt.Println("步骤9：获取阿里云百炼索引任务状态")
	for {
		getIndexJobStatusResponse, err := GetIndexJobStatus(client, workspaceId, jobID, indexID)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(getIndexJobStatusResponse.Body.Data.Status)
		fmt.Printf("当前索引任务状态：%s\n", status)

		if status == "COMPLETED" {
			break
		}
		time.Sleep(5 * time.Second)
	}

	fmt.Println("阿里云百炼知识库创建成功！")
	return indexID, nil
}

// 主函数。
func main() {
	if !CheckEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}
	// 创建 scanner 用于读取输入
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
	filePath, _ := reader.ReadString('\n')
	filePath = strings.TrimSpace(filePath)
	fmt.Print("请为您的知识库输入一个名称：")
	kbName, _ := reader.ReadString('\n')
	kbName = strings.TrimSpace(kbName)
	workspaceID := os.Getenv("WORKSPACE_ID")
	indexID, err := CreateKnowledgeBase(filePath, workspaceID, kbName)
	if err != nil {
		fmt.Printf("发生错误：%v\n", err)
		return
	}
	fmt.Printf("知识库创建成功，ID为：%s\n", indexID)
}
```

<a id="检索知识库"></a>

<a id="检索知识库-h4"></a>

#### 检索知识库

> **重要**
>
> -   在调用本示例之前，请务必完成上述所有[前置步骤](rag-knowledge-base-api-guide.md#71fcfbd434agq)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
> -   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
# 示例代码仅供参考，请勿在生产环境中直接使用
import os

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")

    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
        # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 检索知识库
def retrieve_index(client, workspace_id, index_id, query):
    """
    在指定的知识库中检索信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        query (str): 检索query。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
    runtime = util_models.RuntimeOptions()
    return client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)

def main():
    """
    使用阿里云百炼服务检索知识库。

    返回:
        str or None: 如果成功，返回检索召回的文本切片；否则返回 None。
    """
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    try:
        print("步骤1：创建Client")
        client = create_client()
        print("步骤2：检索知识库")
        index_id = input("请输入知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        query = input("请输入检索query：")
        workspace_id = os.environ.get('WORKSPACE_ID')
        resp = retrieve_index(client, workspace_id, index_id, query)
        result = UtilClient.to_jsonstring(resp.body)
        print(result)
    except Exception as e:
        print(f"发生错误：{e}")
        return None

if __name__ == '__main__':
    main()
```

<a id="fig-code-group-2-java-tab"></a>

Java

<a id="code-code-group-2-java"></a>

```java
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.aliyun.teautil.models.RuntimeOptions;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.*;

public class KnowledgeBaseRetrieve {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return 配置好的客户端对象
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 在指定的知识库中检索信息。
     *
     * @param client         客户端对象（bailian20231229Client）
     * @param workspaceId    业务空间ID
     * @param indexId        知识库ID
     * @param query          检索查询语句
     * @return               阿里云百炼服务的响应
     */
    public static RetrieveResponse retrieveIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String query) throws Exception {
        RetrieveRequest retrieveRequest = new RetrieveRequest();
        retrieveRequest.setIndexId(indexId);
        retrieveRequest.setQuery(query);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.retrieveWithOptions(workspaceId, retrieveRequest, null, runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库。
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：创建Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：检索知识库
            System.out.println("步骤2：检索知识库");
            Scanner scanner = new Scanner(System.in);
            System.out.print("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            String indexId = scanner.nextLine();
            System.out.print("请输入检索query：");
            String query = scanner.nextLine();
            String workspaceId = System.getenv("WORKSPACE_ID");
            RetrieveResponse resp = retrieveIndex(client, workspaceId, indexId, query);

            // 请自行安装jackson-databind。将响应体responsebody转换为 JSON 字符串
            ObjectMapper mapper = new ObjectMapper();
            String result = mapper.writeValueAsString(resp.getBody());
            System.out.println(result);
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
        }
    }
}
```

<a id="fig-code-group-2-php-tab"></a>

PHP

<a id="code-code-group-2-php"></a>

```php
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\RetrieveRequest;

class KnowledgeBaseRetrieve {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

     /**
     * 在指定的知识库中检索信息。
     *
     * @param Bailian $client 客户端对象（Client）。
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $query 检索查询语句
     * @return RetrieveResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function retrieveIndex($client, $workspaceId, $indexId, $query) {
        $headers = [];
        $retrieveRequest = new RetrieveRequest([
            "query" => $query,
            "indexId" => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->retrieveWithOptions($workspaceId, $retrieveRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }

        try {
            // 步骤1：创建Client
            echo "步骤1：创建Client\n";
            $client = self::createClient();

            // 步骤2：检索知识库
            echo "步骤2：检索知识库\n";
            $indexId = readline("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            $query = readline("请输入检索query：");
            $workspaceId = getenv("WORKSPACE_ID");
            // 调用检索方法
            $resp = self::retrieveIndex($client, $workspaceId, $indexId, $query);
            // 将响应体responsebody转换为 JSON 字符串
            $result = json_encode($resp->body, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
            echo $result . "\n";
        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseRetrieve::main(array_slice($argv, 1));
```

<a id="fig-code-group-2-node-js-tab"></a>

Node.js

<a id="code-code-group-2-node-js"></a>

```javascript
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbRetrieve {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }
        return missing.length === 0;
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new bailian20231229.default(config);
    }

    /**
     * 在指定的知识库中检索信息
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @param {string} indexId 知识库ID
     * @param {string} query 检索query
     * @returns {Promise<bailian20231229.RetrieveResponse>} 阿里云百炼服务的响应
     */
    static async retrieveIndex(client, workspaceId, indexId, query) {
        const headers = {};
        const req = new bailian20231229.RetrieveRequest({
            indexId,
            query
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.retrieveWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库
     */
    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            console.log("步骤1：创建Client")
            const client = this.createClient();

            console.log("步骤2：检索知识库")
            const indexId = await new Promise((resolve, reject) => {
                // 知识库ID即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取
                readline.question("请输入知识库ID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("知识库ID不能为空"));
                });
            });
            const query = await new Promise((resolve, reject) => {
                readline.question("请输入检索query：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("检索query不能为空"));
                });
            });
            const workspaceId = process.env.WORKSPACE_ID;
            const resp = await this.retrieveIndex(client, workspaceId, indexId, query);
            const result = JSON.stringify(resp.body);
            console.log(result);
        } catch (err) {
            console.error(`发生错误：${err.message}`);
            return;
        } finally {
            readline.close();
        }
    }
}

exports.KbRetrieve = KbRetrieve;
KbRetrieve.main(process.argv.slice(2));
```

<a id="fig-code-group-2-c-tab"></a>

C#

<a id="code-code-group-2-c"></a>

```csharp
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseRetrieve
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 在指定的知识库中检索信息。
        /// </summary>
        /// <param name="client">客户端对象（bailian20231229Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="query">检索查询语句</param>
        /// <returns>阿里云百炼服务的响应</returns>
        /// <exception cref="Exception">如果调用失败</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.RetrieveResponse RetrieveIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string query)
        {
            var headers = new Dictionary<string, string>() { };
            var retrieveRequest = new AlibabaCloud.SDK.Bailian20231229.Models.RetrieveRequest
            {
                IndexId = indexId,
                Query = query
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.RetrieveWithOptions(workspaceId, retrieveRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务检索知识库。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }

            try
            {
                // 步骤1：初始化客户端（Client）
                Console.WriteLine("步骤1：创建Client");
                Bailian20231229.Client client = CreateClient();

                // 步骤2：检索知识库
                Console.WriteLine("步骤2：检索知识库");
                Console.Write("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                string indexId = Console.ReadLine();
                Console.Write("请输入检索query：");
                string query = Console.ReadLine();
                string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                Bailian20231229.Models.RetrieveResponse resp = RetrieveIndex(client, workspaceId, indexId, query);

                // 请自行安装Newtonsoft.Json。将响应体responsebody转换为 JSON 字符串
                var mapper = new JsonSerializerSettings { Formatting = Formatting.Indented };
                string result = JsonConvert.SerializeObject(resp.Body, mapper);
                Console.WriteLine(result);
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
            }
        }
    }
}
```

<a id="fig-code-group-2-go-tab"></a>

Go

<a id="code-code-group-2-go"></a>

```go
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

// checkEnvironmentVariables 检查并提示设置必要的环境变量。
func checkEnvironmentVariables() bool {
	// 必要的环境变量及其描述。
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// createClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func createClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// retrieveIndex 在指定的知识库中检索信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - query（string）: 检索查询语句
//
// 返回:
//   - *bailian20231229.RetrieveResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func retrieveIndex(client *bailian20231229.Client, workspaceId, indexId, query string) (*bailian20231229.RetrieveResponse, error) {
	headers := make(map[string]*string)
	request := &bailian20231229.RetrieveRequest{
		IndexId: tea.String(indexId),
		Query:   tea.String(query),
	}
	runtime := &util.RuntimeOptions{}
	return client.RetrieveWithOptions(tea.String(workspaceId), request, headers, runtime)
}

// 主函数。
func main() {
	if !checkEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}

	// 步骤1：初始化客户端（Client）
	fmt.Println("步骤1：创建Client")
	client, err := createClient()
	if err != nil {
		fmt.Println("创建客户端失败:", err)
		return
	}

	// 步骤2：检索知识库
	fmt.Println("步骤2：检索知识库")
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入知识库ID：") // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
	indexId, _ := reader.ReadString('\n')
	indexId = strings.TrimSpace(indexId)
	fmt.Print("请输入检索query：")
	query, _ := reader.ReadString('\n')
	query = strings.TrimSpace(query)
	workspaceId := os.Getenv("WORKSPACE_ID")
	resp, err := retrieveIndex(client, workspaceId, indexId, query)
	if err != nil {
		fmt.Printf("检索失败：%v\n", err)
		return
	}
        fmt.Println(resp.Body)
}
```

<a id="更新知识库"></a>

<a id="更新知识库-h4"></a>

#### 更新知识库

> **重要**
>
> -   在调用本示例之前，请务必完成上述所有[前置步骤](rag-knowledge-base-api-guide.md#71fcfbd434agq)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
> -   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

Python

<a id="code-code-group-3-python"></a>

```python
# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
import time

import requests
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")

    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

def calculate_md5(file_path: str) -> str:
    """
    计算文件的MD5值。

    参数:
        file_path (str): 文件本地路径。

    返回:
        str: 文件的MD5值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, "rb") as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

def get_file_size(file_path: str) -> int:
    """
    获取文件大小（以字节为单位）。
    参数:
        file_path (str): 文件本地路径。
    返回:
        int: 文件大小（以字节为单位）。
    """
    return os.path.getsize(file_path)

# 申请文件上传租约
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)

# 上传文件到临时存储
def upload_file(pre_signed_url, headers, file_path):
    """
    将文件上传到阿里云百炼服务。
    参数:
        pre_signed_url (str): 上传租约中的 URL。
        headers (dict): 上传请求的头部。
        file_path (str): 文件本地路径。
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    upload_headers = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    }
    response = requests.put(pre_signed_url, data=file_content, headers=upload_headers)
    response.raise_for_status()

# 添加文件到类目中
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)

# 查询文件的解析状态
def describe_file(client, workspace_id, file_id):
    """
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)

# 提交追加文件任务
def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type):
    """
    向一个文档搜索类知识库追加导入已解析的文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。
        source_type(str): 数据类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request,
                                                              headers, runtime)

# 等待追加任务完成
def get_index_job_status(client, workspace_id, job_id, index_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

# 删除旧文件
def delete_index_document(client, workspace_id, index_id, file_id):
    """
    从指定的文档搜索类知识库中永久删除一个或多个文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_document_request = bailian_20231229_models.DeleteIndexDocumentRequest(
        index_id=index_id,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_document_with_options(workspace_id, delete_index_document_request, headers, runtime)

def update_knowledge_base(
        file_path: str,
        workspace_id: str,
        index_id: str,
        old_file_id: str
):
    """
    使用阿里云百炼服务更新知识库。
    参数:
        file_path (str): 文件（更新后的）的实际本地路径。
        workspace_id (str): 业务空间ID。
        index_id (str): 需要更新的知识库ID。
        old_file_id (str): 需要更新的文件的FileID。
    返回:
        str or None: 如果成功，返回知识库ID；否则返回None。
    """
    # 设置默认值
    category_id = 'default'
    parser = 'DASHSCOPE_DOCMIND'
    source_type = 'DATA_CENTER_FILE'
    try:
        # 步骤1：创建客户端（Client）
        print("步骤1：创建Client")
        client = create_client()
        # 步骤2：准备文件信息
        print("步骤2：准备文件信息")
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        # 步骤3：申请上传租约
        print("步骤3：向阿里云百炼申请上传租约")
        lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        # 步骤4：上传文件到临时存储
        print("步骤4：上传文件到临时存储")
        upload_file(upload_url, upload_headers, file_path)
        # 步骤5：添加文件到类目中
        print("步骤5：添加文件到类目中")
        add_response = add_file(client, lease_id, parser, category_id, workspace_id)
        file_id = add_response.body.data.file_id
        # 步骤6：检查文件状态
        print("步骤6：检查阿里云百炼中的文件状态")
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"当前文件状态：{status}")
            if status == 'INIT':
                print("文件待解析，请稍候...")
            elif status == 'PARSING':
                print("文件解析中，请稍候...")
            elif status == 'PARSE_SUCCESS':
                print("文件解析完成！")
                break
            else:
                print(f"未知的文件状态：{status}，请联系技术支持。")
                return None
            time.sleep(5)
        # 步骤7：提交追加文件任务
        print("步骤7：提交追加文件任务")
        index_add_response = submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type)
        job_id = index_add_response.body.data.id
        # 步骤8：获取索引任务状态
        print("步骤8：等待追加任务完成")
        while True:
            get_index_job_status_response = get_index_job_status(client, workspace_id, job_id, index_id)
            status = get_index_job_status_response.body.data.status
            print(f"当前索引任务状态：{status}")
            if status == 'COMPLETED':
                break
            time.sleep(5)
        print("步骤9：删除旧文件")
        delete_index_document(client, workspace_id, index_id, old_file_id)
        print("阿里云百炼知识库更新成功！")
        return index_id
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    file_path = input("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
    index_id = input("请输入需要更新的知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
    old_file_id = input("请输入需要更新的文件的 FileID：")  # 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
    workspace_id = os.environ.get('WORKSPACE_ID')
    update_knowledge_base(file_path, workspace_id, index_id, old_file_id)

if __name__ == '__main__':
    main()
```

<a id="fig-code-group-3-java-tab"></a>

Java

<a id="code-code-group-3-java"></a>

```java
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.*;
import com.aliyun.teautil.models.RuntimeOptions;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.*;

public class KnowledgeBaseUpdate {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 创建并配置客户端（Client）
     *
     * @return 配置好的客户端（Client）
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 计算文件的MD5值
     *
     * @param filePath 文件本地路径
     * @return 文件的MD5值
     */
    public static String calculateMD5(String filePath) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(filePath)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesRead);
            }
        }
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    /**
     * 获取文件大小（以字节为单位）
     *
     * @param filePath 文件本地路径
     * @return 文件大小（以字节为单位）
     */
    public static String getFileSize(String filePath) {
        File file = new File(filePath);
        long fileSize = file.length();
        return String.valueOf(fileSize);
    }

    /**
     * 申请文件上传租约。
     *
     * @param client      客户端对象
     * @param categoryId  类目ID
     * @param fileName    文件名称
     * @param fileMd5     文件的MD5值
     * @param fileSize    文件大小（以字节为单位）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
        applyFileUploadLeaseRequest.setFileName(fileName);
        applyFileUploadLeaseRequest.setMd5(fileMd5);
        applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
        applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        return applyFileUploadLeaseResponse;
    }

    /**
     * 上传文件到临时存储。
     *
     * @param preSignedUrl 上传租约中的 URL
     * @param headers      上传请求的头部
     * @param filePath     文件本地路径
     * @throws Exception 如果上传过程中发生错误
     */
    public static void uploadFile(String preSignedUrl, Map<String, String> headers, String filePath) throws Exception {
        File file = new File(filePath);
        if (!file.exists() || !file.isFile()) {
            throw new IllegalArgumentException("文件不存在或不是普通文件: " + filePath);
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            URL url = new URL(preSignedUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("PUT");
            conn.setDoOutput(true);

            // 设置上传请求头
            conn.setRequestProperty("X-bailian-extra", headers.get("X-bailian-extra"));
            conn.setRequestProperty("Content-Type", headers.get("Content-Type"));

            // 分块读取并上传文件
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                conn.getOutputStream().write(buffer, 0, bytesRead);
            }

            int responseCode = conn.getResponseCode();
            if (responseCode != 200) {
                throw new RuntimeException("上传失败: " + responseCode);
            }
        }
    }

    /**
     * 将文件添加到类目中。
     *
     * @param client      客户端对象
     * @param leaseId     租约ID
     * @param parser      用于文件的解析器
     * @param categoryId  类目ID
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
        addFileRequest.setLeaseId(leaseId);
        addFileRequest.setParser(parser);
        addFileRequest.setCategoryId(categoryId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应对象
     */
    public static DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 向一个文档搜索类知识库追加导入已解析的文件
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @param fileId      文件ID
     * @param sourceType  数据类型
     * @return 阿里云百炼服务的响应
     */
    public static SubmitIndexAddDocumentsJobResponse submitIndexAddDocumentsJob(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId, String sourceType) throws Exception {
        Map<String, String> headers = new HashMap<>();
        SubmitIndexAddDocumentsJobRequest submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest();
        submitIndexAddDocumentsJobRequest.setIndexId(indexId);
        submitIndexAddDocumentsJobRequest.setDocumentIds(Collections.singletonList(fileId));
        submitIndexAddDocumentsJobRequest.setSourceType(sourceType);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.submitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param jobId       任务ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
        getIndexJobStatusRequest.setIndexId(indexId);
        getIndexJobStatusRequest.setJobId(jobId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        GetIndexJobStatusResponse getIndexJobStatusResponse = null;
        getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        return getIndexJobStatusResponse;
    }

    /**
     * 从指定的文档搜索类知识库中永久删除一个或多个文件
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应
     */
    public static DeleteIndexDocumentResponse deleteIndexDocument(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        DeleteIndexDocumentRequest deleteIndexDocumentRequest = new DeleteIndexDocumentRequest();
        deleteIndexDocumentRequest.setIndexId(indexId);
        deleteIndexDocumentRequest.setDocumentIds(Collections.singletonList(fileId));
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.deleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     *
     * @param filePath    文件（更新后的）的实际本地路径
     * @param workspaceId 业务空间ID
     * @param indexId     需要更新的知识库ID
     * @param oldFileId   需要更新的文件的FileID
     * @return 如果成功，返回知识库ID；否则返回 null
     */
    public static String updateKnowledgeBase(String filePath, String workspaceId, String indexId, String oldFileId) {
        // 设置默认值
        String categoryId = "default";
        String parser = "DASHSCOPE_DOCMIND";
        String sourceType = "DATA_CENTER_FILE";
        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：创建Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：准备文件信息（更新后的文件）
            System.out.println("步骤2：准备文件信息");
            String fileName = Paths.get(filePath).getFileName().toString();
            String fileMd5 = calculateMD5(filePath);
            String fileSize = getFileSize(filePath);

            // 步骤3：申请上传租约
            System.out.println("步骤3：向阿里云百炼申请上传租约");
            ApplyFileUploadLeaseResponse leaseResponse = applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            String leaseId = leaseResponse.getBody().getData().getFileUploadLeaseId();
            String uploadUrl = leaseResponse.getBody().getData().getParam().getUrl();
            Object uploadHeaders = leaseResponse.getBody().getData().getParam().getHeaders();

            // 步骤4：上传文件到临时存储
            System.out.println("步骤4：上传文件到临时存储");
            // 请自行安装jackson-databind
            // 将上一步的uploadHeaders转换为Map(Key-Value形式)
            ObjectMapper mapper = new ObjectMapper();
            Map<String, String> uploadHeadersMap = (Map<String, String>) mapper.readValue(mapper.writeValueAsString(uploadHeaders), Map.class);
            uploadFile(uploadUrl, uploadHeadersMap, filePath);

            // 步骤5：添加文件到类目中
            System.out.println("步骤5：添加文件到类目中");
            AddFileResponse addResponse = addFile(client, leaseId, parser, categoryId, workspaceId);
            String fileId = addResponse.getBody().getData().getFileId();

            // 步骤6：检查更新后的文件状态
            System.out.println("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                DescribeFileResponse describeResponse = describeFile(client, workspaceId, fileId);
                String status = describeResponse.getBody().getData().getStatus();
                System.out.println("当前文件状态：" + status);
                if ("INIT".equals(status)) {
                    System.out.println("文件待解析，请稍候...");
                } else if ("PARSING".equals(status)) {
                    System.out.println("文件解析中，请稍候...");
                } else if ("PARSE_SUCCESS".equals(status)) {
                    System.out.println("文件解析完成！");
                    break;
                } else {
                    System.out.println("未知的文件状态：" + status + "，请联系技术支持。");
                    return null;
                }
                Thread.sleep(5000);
            }

            // 步骤7：提交追加文件任务
            System.out.println("步骤7：提交追加文件任务");
            SubmitIndexAddDocumentsJobResponse indexAddResponse = submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
            String jobId = indexAddResponse.getBody().getData().getId();

            // 步骤8：等待追加任务完成
            System.out.println("步骤8：等待追加任务完成");
            while (true) {
                GetIndexJobStatusResponse jobStatusResponse = getIndexJobStatus(client, workspaceId, jobId, indexId);
                String status = jobStatusResponse.getBody().getData().getStatus();
                System.out.println("当前索引任务状态：" + status);
                if ("COMPLETED".equals(status)) {
                    break;
                }
                Thread.sleep(5000);
            }

            // 步骤9：删除旧文件
            System.out.println("步骤9：删除旧文件");
            deleteIndexDocument(client, workspaceId, indexId, oldFileId);

            System.out.println("阿里云百炼知识库更新成功！");
            return indexId;
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        String filePath = scanner.nextLine();

        System.out.print("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        String indexId = scanner.nextLine(); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。

        System.out.print("请输入需要更新的文件的 FileID：");
        String oldFileId = scanner.nextLine();

        String workspaceId = System.getenv("WORKSPACE_ID");
        String result = updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
        if (result != null) {
            System.out.println("知识库更新成功，返回知识库ID: " + result);
        } else {
            System.out.println("知识库更新失败。");
        }
    }
}
```

<a id="fig-code-group-3-php-tab"></a>

PHP

<a id="code-code-group-3-php"></a>

```php
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\AddFileRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ApplyFileUploadLeaseRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\DeleteIndexDocumentRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\GetIndexJobStatusRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\SubmitIndexAddDocumentsJobRequest;

class KnowledgeBaseUpdate {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 计算文件的MD5值。
     *
     * @param string $filePath 文件本地路径。
     * @return string 文件的MD5值。
     */
    public static function calculateMd5($filePath) {
        $md5Hash = hash_init("md5");
        $handle = fopen($filePath, "rb");
        while (!feof($handle)) {
            $chunk = fread($handle, 4096);
            hash_update($md5Hash, $chunk);
        }
        fclose($handle);
        return hash_final($md5Hash);
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param string $filePath 文件本地路径。
     * @return int 文件大小（以字节为单位）。
     */
    public static function getFileSize($filePath) {
        return (string)filesize($filePath);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $categoryId 类目ID。
     * @param string $fileName 文件名称。
     * @param string $fileMd5 文件的MD5值。
     * @param int $fileSize 文件大小（以字节为单位）。
     * @param string $workspaceId 业务空间ID。
     * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
     */
    public static function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
        $headers = [];
        $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
            "fileName" => $fileName,
            "md5" => $fileMd5,
            "sizeInBytes" => $fileSize
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
    }

    /**
     * 上传文件到临时存储。
    *
    * @param string $preSignedUrl 上传租约中的 URL。
    * @param array $headers 上传请求的头部。
    * @param string $filePath 文件本地路径。
    */
    public static function uploadFile($preSignedUrl, $headers, $filePath) {
        $fileContent = file_get_contents($filePath);
        // 设置上传请求头
        $uploadHeaders = [
            "X-bailian-extra" => $headers["X-bailian-extra"],
            "Content-Type" => $headers["Content-Type"]
        ];
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_map(function($key, $value) {
            return "$key: $value";
        }, array_keys($uploadHeaders), $uploadHeaders));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpCode != 200) {
            throw new Exception("上传失败: " . curl_error($ch));
        }
        curl_close($ch);
    }

    /**
     * 将文件添加到类目中。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $leaseId 租约ID。
     * @param string $parser 用于文件的解析器。
     * @param string $categoryId 类目ID。
     * @param string $workspaceId 业务空间ID。
     * @return AddFileResponse 阿里云百炼服务的响应。
     */
    public static function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
        $headers = [];
        $addFileRequest = new AddFileRequest([
            "leaseId" => $leaseId,
            "parser" => $parser,
            "categoryId" => $categoryId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @return DescribeFileResponse 阿里云百炼服务的响应。
     */
    public static function describeFile($client, $workspaceId, $fileId) {
        $headers = [];
        $runtime = new RuntimeOptions([]);
        return $client->describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
    }

    /**
     * 向一个文档搜索类知识库追加导入已解析的文件
     *
     * @param Bailian $client 客户端对象
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $fileId 文件ID
     * @param string $sourceType 数据类型
     * @return SubmitIndexAddDocumentsJobResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType) {
        $headers = [];
        $submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest([
            "indexId" =>$indexId,
            "sourceType" => $sourceType,
            "documentIds" => [
                $fileId
            ]
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->submitIndexAddDocumentsJobWithOptions($workspaceId, $submitIndexAddDocumentsJobRequest, $headers, $runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @param string $jobId 任务ID。
     * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
     */
    public static function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
        $headers = [];
        $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
            'indexId' => $indexId,
            'jobId' => $jobId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
    }

    /**
     * 从指定的文档搜索类知识库中永久删除文件
     *
     * @param Bailian $client 客户端对象
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $fileId 文件ID
     * @return mixed 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function deleteIndexDocument($client, $workspaceId, $indexId, $fileId) {
        $headers = [];
        $deleteIndexDocumentRequest = new DeleteIndexDocumentRequest([
            "indexId" => $indexId,
            "documentIds" => [
                $fileId
            ]
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->deleteIndexDocumentWithOptions($workspaceId, $deleteIndexDocumentRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     *
     * @param string $filePath 文件（更新后的）的实际本地路径
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 需要更新的知识库ID
     * @param string $oldFileId 需要更新的文件的FileID
     * @return string| null 如果成功，返回知识库ID；否则返回 null
     */
    public static function updateKnowledgeBase($filePath, $workspaceId, $indexId, $oldFileId) {
        $categoryId = "default";
        $parser = "DASHSCOPE_DOCMIND";
        $sourceType = "DATA_CENTER_FILE";

        try {
            // 步骤1：创建Client
            echo "步骤1：创建Client\n";
            $client = self::createClient();

            // 步骤2：准备文件信息
            echo "步骤2：准备文件信息\n";
            $fileName = basename($filePath);
            $fileMd5 = self::calculateMD5($filePath);
            $fileSize = self::getFileSize($filePath);

            // 步骤3：申请上传租约
            echo "步骤3：向阿里云百炼申请上传租约\n";
            $leaseResponse = self::applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId);
            $leaseId = $leaseResponse->body->data->fileUploadLeaseId;
            $uploadUrl = $leaseResponse->body->data->param->url;
            $uploadHeaders = $leaseResponse->body->data->param->headers;
            $uploadHeadersMap = json_decode(json_encode($uploadHeaders), true);

            // 步骤4：上传文件到临时存储
            echo "步骤4：上传文件到临时存储\n";
            self::uploadFile($uploadUrl, $uploadHeadersMap, $filePath);

            // 步骤5：添加文件到类目中
            echo "步骤5：添加文件到类目中\n";
            $addResponse = self::addFile($client, $leaseId, $parser, $categoryId, $workspaceId);
            $fileId = $addResponse->body->data->fileId;

            // 步骤6：检查文件状态
            echo "步骤6：检查阿里云百炼中的文件状态\n";
            while (true) {
                $describeResponse = self::describeFile($client, $workspaceId, $fileId);
                $status = $describeResponse->body->data->status;
                echo "当前文件状态：" . $status . "\n";

                if ($status === "INIT") {
                    echo "文件待解析，请稍候...\n";
                } elseif ($status === "PARSING") {
                    echo "文件解析中，请稍候...\n";
                } elseif ($status === "PARSE_SUCCESS") {
                    echo "文件解析完成！\n";
                    break;
                } else {
                    echo "未知的文件状态：" . $status . "，请联系技术支持。\n";
                    return null;
                }
                sleep(5);
            }

            // 步骤7：提交追加文件任务
            echo "步骤7：提交追加文件任务\n";
            $indexAddResponse = self::submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType);
            $jobId = $indexAddResponse->body->data->id;

            // 步骤8：等待任务完成
            echo "步骤8：等待追加任务完成\n";
            while (true) {
                $jobStatusResponse = self::getIndexJobStatus($client, $workspaceId, $jobId, $indexId);
                $status = $jobStatusResponse->body->data->status;
                echo "当前索引任务状态：" . $status . "\n";

                if ($status === "COMPLETED") {
                    break;
                }
                sleep(5);
            }

            // 步骤9：删除旧文件
            echo "步骤9：删除旧文件\n";
            self::deleteIndexDocument($client, $workspaceId, $indexId, $oldFileId);

            echo "阿里云百炼知识库更新成功！\n";
            return $indexId;

        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }
        $filePath = readline("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        $indexId = readline("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        $oldFileId = readline("请输入需要更新的文件的 FileID："); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
        $workspaceId = getenv('WORKSPACE_ID');
        $result = self::updateKnowledgeBase($filePath, $workspaceId, $indexId, $oldFileId);

        if ($result !== null) {
            echo "知识库更新成功，返回知识库ID: " . $result . "\n";
        } else {
            echo "知识库更新失败。\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseUpdate::main(array_slice($argv, 1));
```

<a id="fig-code-group-3-node-js-tab"></a>

Node.js

<a id="code-code-group-3-node-js"></a>

```javascript
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const crypto = require('crypto');

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbUpdate {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }
        return missing.length === 0;
    }

    /**
     * 计算文件的MD5值
     * @param {string} filePath - 文件本地路径
     * @returns {Promise<string>} - 文件的MD5值
     */
    static async calculateMD5(filePath) {
        const hash = crypto.createHash('md5');
        const stream = fs.createReadStream(filePath);

        return new Promise((resolve, reject) => {
            stream.on('data', chunk => hash.update(chunk));
            stream.on('end', () => resolve(hash.digest('hex')));
            stream.on('error', reject);
        });
    }

    /**
     * 获取文件大小（以字节为单位），返回字符串格式
     * @param {string} filePath - 文件本地路径
     * @returns {string} - 文件大小（如 "123456"）
     */
    static getFileSize(filePath) {
        try {
            const stats = fs.statSync(filePath);
            return stats.size.toString();
        } catch (err) {
            console.error(`获取文件大小失败: ${err.message}`);
            throw err;
        }
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
        return new bailian20231229.default(config);
    }

    /**
     * 申请文件上传租约
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} categoryId - 类目ID
     * @param {string} fileName - 文件名称
     * @param {string} fileMd5 - 文件的MD5值
     * @param {string} fileSize - 文件大小（以字节为单位）
     * @param {string} workspaceId - 业务空间ID
     * @returns {Promise<bailian20231229.ApplyFileUploadLeaseResponse>} - 阿里云百炼服务的响应
     */
    static async applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
        const headers = {};
        const req = new bailian20231229.ApplyFileUploadLeaseRequest({
            md5: fileMd5,
            fileName,
            sizeInBytes: fileSize
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.applyFileUploadLeaseWithOptions(
            categoryId,
            workspaceId,
            req,
            headers,
            runtime
        );
    }

    /**
     * 上传文件到临时存储
     * @param {string} preSignedUrl - 上传租约中的URL
     * @param {Object} headers - 上传请求的头部
     * @param {string} filePath - 文件本地路径
     */
    static async uploadFile(preSignedUrl, headers, filePath) {
        const uploadHeaders = {
            "X-bailian-extra": headers["X-bailian-extra"],
            "Content-Type": headers["Content-Type"]
        };
        const stream = fs.createReadStream(filePath);
        try {
            await axios.put(preSignedUrl, stream, { headers: uploadHeaders });
        } catch (e) {
            throw new Error(`上传失败: ${e.message}`);
        }
    }

    /**
     * 添加文件到类目中
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} leaseId - 租约ID
     * @param {string} parser - 用于文件的解析器
     * @param {string} categoryId - 类目ID
     * @param {string} workspaceId - 业务空间ID
     * @returns {Promise<bailian20231229.AddFileResponse>} - 阿里云百炼服务的响应
     */
    static async addFile(client, leaseId, parser, categoryId, workspaceId) {
        const headers = {};
        const req = new bailian20231229.AddFileRequest({
            leaseId,
            parser,
            categoryId
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.addFileWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 查询文件的解析状态
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} fileId - 文件ID
     * @returns {Promise<bailian20231229.DescribeFileResponse>} - 阿里云百炼服务的响应
     */
    static async describeFile(client, workspaceId, fileId) {
        const headers = {};
        const runtime = new Util.RuntimeOptions({});
        return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 提交追加文件任务
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 知识库ID
     * @param {string} fileId - 文件ID
     * @param {string} sourceType - 数据类型
     * @returns {Promise<bailian20231229.SubmitIndexAddDocumentsJobResponse>} - 阿里云百炼服务的响应
     */
    static async submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType) {
        const headers = {};
        const req = new bailian20231229.SubmitIndexAddDocumentsJobRequest({
            indexId,
            documentIds: [fileId],
            sourceType,
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.submitIndexAddDocumentsJobWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 查询索引任务状态
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} jobId - 任务ID
     * @param {string} indexId - 知识库ID
     * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
     */
    static async getIndexJobStatus(client, workspaceId, jobId, indexId) {
        const headers = {};
        const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
        const runtime = new Util.RuntimeOptions({});
        return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 删除旧文件
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 知识库ID
     * @param {string} fileId - 文件ID
     * @returns {Promise<bailian20231229.DeleteIndexDocumentResponse>} - 阿里云百炼服务的响应
     */
    static async deleteIndexDocument(client, workspaceId, indexId, fileId) {
        const headers = {};
        const req = new bailian20231229.DeleteIndexDocumentRequest({
            indexId,
            documentIds: [fileId],
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.deleteIndexDocumentWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     * @param {string} filePath - 文件（更新后的）的实际本地路径
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 需要更新的知识库ID
     * @param {string} oldFileId - 需要更新的文件的FileID
     * @returns {Promise<string | null>} - 如果成功，返回知识库ID；否则返回null
     */
    static async updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId) {
        const categoryId = 'default';
        const parser = 'DASHSCOPE_DOCMIND';
        const sourceType = 'DATA_CENTER_FILE';

        try {
            console.log("步骤1：创建Client");
            const client = this.createClient();

            console.log("步骤2：准备文件信息");
            const fileName = path.basename(filePath);
            const fileMd5 = await this.calculateMD5(filePath);
            const fileSize = this.getFileSize(filePath);

            console.log("步骤3：向阿里云百炼申请上传租约");
            const leaseRes = await this.applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            const leaseId = leaseRes.body.data.fileUploadLeaseId;
            const uploadUrl = leaseRes.body.data.param.url;
            const uploadHeaders = leaseRes.body.data.param.headers;

            console.log("步骤4：上传文件到临时存储");
            await this.uploadFile(uploadUrl, uploadHeaders, filePath);

            console.log("步骤5：添加文件到类目中");
            const addRes = await this.addFile(client, leaseId, parser, categoryId, workspaceId);
            const fileId = addRes.body.data.fileId;

            console.log("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                const descRes = await this.describeFile(client, workspaceId, fileId);
                const status = descRes.body.data.status;
                console.log(`当前文件状态：${status}`);

                if (status === 'INIT') {
                    console.log("文件待解析，请稍候...");
                } else if (status === 'PARSING') {
                    console.log("文件解析中，请稍候...");
                } else if (status === 'PARSE_SUCCESS') {
                    console.log("文件解析完成！");
                    break;
                } else {
                    console.error(`未知的文件状态：${status}，请联系技术支持。`);
                    return null;
                }
                await this.sleep(5);
            }

            console.log("步骤7：提交追加文件任务");
            const indexAddResponse = await this.submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
            const jobId = indexAddResponse.body.data.id;

            console.log("步骤8：等待追加任务完成");
            while (true) {
                const getJobStatusResponse = await this.getIndexJobStatus(client, workspaceId, jobId, indexId);
                const status = getJobStatusResponse.body.data.status;
                console.log(`当前索引任务状态：${status}`);
                if (status === 'COMPLETED') {
                    break;
                }
                await this.sleep(5);
            }

            console.log("步骤9：删除旧文件");
            await this.deleteIndexDocument(client, workspaceId, indexId, oldFileId);

            console.log("阿里云百炼知识库更新成功！");
            return indexId;
        } catch (e) {
            console.error(`发生错误：${e.message}`);
            return null;
        }
    }

    /**
     * 等待指定时间（秒）
     * @param {number} seconds - 等待时间（秒）
     * @returns {Promise<void>}
     */
    static sleep(seconds) {
        return new Promise(resolve => setTimeout(resolve, seconds * 1000));
    }

    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            const filePath = await new Promise((resolve, reject) => {
                readline.question("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("路径不能为空"));
                });
            });
            const indexId = await new Promise((resolve, reject) => {
                // 知识库ID即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                readline.question("请输入需要更新的知识库ID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("知识库ID不能为空"));
                });
            });
            const oldFileId = await new Promise((resolve, reject) => {
                // FileId即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
                readline.question("请输入需要更新的文件的 FileID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("FileID不能为空"));
                });
            });
            const workspaceId = process.env.WORKSPACE_ID;

            const result = await this.updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
            if (result) console.log(`知识库ID: ${result}`);
            else console.log("知识库更新失败。");
        } catch (err) {
            console.error(err.message);
        } finally {
            readline.close();
        }
    }
}

exports.KbUpdate = KbUpdate;
KbUpdate.main(process.argv.slice(2));
```

<a id="fig-code-group-3-c-tab"></a>

C#

<a id="code-code-group-3-c"></a>

```csharp
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;

using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseUpdate
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 计算文件的MD5值。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件的MD5值</returns>
        /// <exception cref="Exception">计算过程中发生错误时抛出异常</exception>
        public static string CalculateMD5(string filePath)
        {
            using (var md5 = MD5.Create())
            {
                using (var stream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    byte[] hashBytes = md5.ComputeHash(stream);
                    StringBuilder sb = new StringBuilder();
                    foreach (byte b in hashBytes)
                    {
                        sb.Append(b.ToString("x2"));
                    }
                    return sb.ToString();
                }
            }
        }

        /// <summary>
        /// 获取文件大小（以字节为单位）。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件大小（以字节为单位）</returns>
        public static string GetFileSize(string filePath)
        {
            var file = new FileInfo(filePath);
            return file.Length.ToString();
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 申请文件上传租约。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="fileName">文件名称</param>
        /// <param name="fileMd5">文件的MD5值</param>
        /// <param name="fileSize">文件大小（以字节为单位）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string categoryId,
            string fileName,
            string fileMd5,
            string fileSize,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
            {
                FileName = fileName,
                Md5 = fileMd5,
                SizeInBytes = fileSize
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        }

        /// <summary>
        /// 上传文件到临时存储。
        /// </summary>
        /// <param name="preSignedUrl">上传租约中的 URL</param>
        /// <param name="headers">上传请求的头部</param>
        /// <param name="filePath">文件本地路径</param>
        /// <exception cref="Exception">上传过程中发生错误时抛出异常</exception>
        public static void UploadFile(string preSignedUrl, Dictionary<string, string> headers, string filePath)
        {
            var file = new FileInfo(filePath);
            if (!File.Exists(filePath))
            {
                throw new ArgumentException($"文件不存在或不是普通文件: {filePath}");
            }

            using (var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                var url = new Uri(preSignedUrl);
                var conn = (HttpWebRequest)WebRequest.Create(url);
                conn.Method = "PUT";
                conn.ContentType = headers["Content-Type"];
                conn.Headers.Add("X-bailian-extra", headers["X-bailian-extra"]);

                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fs.Read(buffer, 0, buffer.Length)) > 0)
                {
                    conn.GetRequestStream().Write(buffer, 0, bytesRead);
                }

                using (var response = (HttpWebResponse)conn.GetResponse())
                {
                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        throw new Exception($"上传失败: {response.StatusCode}");
                    }
                }
            }
        }

        /// <summary>
        /// 将文件添加到类目中。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="leaseId">租约ID</param>
        /// <param name="parser">用于文件的解析器</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string leaseId,
            string parser,
            string categoryId,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
            {
                LeaseId = leaseId,
                Parser = parser,
                CategoryId = categoryId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
        }

        /// <summary>
        /// 查询文件的基本信息。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
        }

        /// <summary>
        /// 向一个文档搜索类知识库追加导入已解析的文件
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="fileId">文件ID</param>
        /// <param name="sourceType">数据类型</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse SubmitIndexAddDocumentsJob(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string fileId,
            string sourceType)
        {
            var headers = new Dictionary<string, string>() { };
            var submitIndexAddDocumentsJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobRequest
            {
                IndexId = indexId,
                DocumentIds = new List<string> { fileId },
                SourceType = sourceType
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.SubmitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
        }

        /// <summary>
        /// 查询索引任务状态。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="jobId">任务ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string jobId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
            {
                IndexId = indexId,
                JobId = jobId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        }

        /// <summary>
        /// 从指定的文档搜索类知识库中永久删除一个或多个文件
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentResponse DeleteIndexDocument(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var deleteIndexDocumentRequest = new AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentRequest
            {
                IndexId = indexId,
                DocumentIds = new List<string> { fileId }
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DeleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务更新知识库
        /// </summary>
        /// <param name="filePath">文件（更新后的）的实际本地路径</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">需要更新的知识库ID</param>
        /// <param name="oldFileId">需要更新的文件的FileID</param>
        /// <returns>如果成功，返回知识库ID；否则返回 null</returns>
        public static string UpdateKnowledgeBase(string filePath, string workspaceId, string indexId, string oldFileId)
        {
            // 设置默认值
            string categoryId = "default";
            string parser = "DASHSCOPE_DOCMIND";
            string sourceType = "DATA_CENTER_FILE";

            try
            {
                Console.WriteLine("步骤1：创建Client");
                var client = CreateClient();

                Console.WriteLine("步骤2：准备文件信息");
                string fileName = Path.GetFileName(filePath);
                string fileMd5 = CalculateMD5(filePath);
                string fileSize = GetFileSize(filePath);

                Console.WriteLine("步骤3：向阿里云百炼申请上传租约");
                Bailian20231229.Models.ApplyFileUploadLeaseResponse leaseResponse = ApplyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
                string leaseId = leaseResponse.Body.Data.FileUploadLeaseId;
                string uploadUrl = leaseResponse.Body.Data.Param.Url;
                var uploadHeaders = leaseResponse.Body.Data.Param.Headers;

                Console.WriteLine("步骤4：上传文件到临时存储");
                // 请自行安装Newtonsoft.Json
                var uploadHeadersMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(JsonConvert.SerializeObject(uploadHeaders));
                UploadFile(uploadUrl, uploadHeadersMap, filePath);

                Console.WriteLine("步骤5：添加文件到类目中");
                Bailian20231229.Models.AddFileResponse addResponse = AddFile(client, leaseId, parser, categoryId, workspaceId);
                string fileId = addResponse.Body.Data.FileId;

                Console.WriteLine("步骤6：检查阿里云百炼中的文件状态");
                while (true)
                {
                    Bailian20231229.Models.DescribeFileResponse describeResponse = DescribeFile(client, workspaceId, fileId);
                    string status = describeResponse.Body.Data.Status;
                    Console.WriteLine("当前文件状态：" + status);
                    if ("INIT".Equals(status))
                    {
                        Console.WriteLine("文件待解析，请稍候...");
                    }
                    else if ("PARSING".Equals(status))
                    {
                        Console.WriteLine("文件解析中，请稍候...");
                    }
                    else if ("PARSE_SUCCESS".Equals(status))
                    {
                        Console.WriteLine("文件解析完成！");
                        break;
                    }
                    else
                    {
                        Console.WriteLine("未知的文件状态：" + status + "，请联系技术支持。");
                        return null;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤7：提交追加文件任务");
                Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse indexAddResponse = SubmitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
                string jobId = indexAddResponse.Body.Data.Id;

                Console.WriteLine("步骤8：等待追加任务完成");
                while (true)
                {
                    Bailian20231229.Models.GetIndexJobStatusResponse jobStatusResponse = GetIndexJobStatus(client, workspaceId, jobId, indexId);
                    string status = jobStatusResponse.Body.Data.Status;
                    Console.WriteLine("当前索引任务状态：" + status);
                    if ("COMPLETED".Equals(status))
                    {
                        break;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤9：删除旧文件");
                DeleteIndexDocument(client, workspaceId, indexId, oldFileId);

                Console.WriteLine("阿里云百炼知识库更新成功！");
                return indexId;
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
                return null;
            }
        }

        /// <summary>
        /// 主函数。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }

            Console.Write("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
            string filePath = Console.ReadLine();

            Console.Write("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            string indexId = Console.ReadLine();

            Console.Write("请输入需要更新的文件的 FileID："); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
            string oldFileId = Console.ReadLine();

            string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
            string result = UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
            if (result != null)
            {
                Console.WriteLine("知识库更新成功，返回知识库ID: " + result);
            }
            else
            {
                Console.WriteLine("知识库更新失败。");
            }
        }
    }
}
```

<a id="fig-code-group-3-go-tab"></a>

Go

<a id="code-code-group-3-go"></a>

```go
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
	"github.com/go-resty/resty/v2"
)

// CheckEnvironmentVariables 检查并提示设置必要的环境变量。
func CheckEnvironmentVariables() bool {
	// 必要的环境变量及其描述。
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// CalculateMD5 计算文件的MD5值。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件的MD5值。
//   - error: 错误信息。
func CalculateMD5(filePath string) (_result string, _err error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	md5Hash := md5.New()
	_, err = io.Copy(md5Hash, file)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", md5Hash.Sum(nil)), nil
}

// GetFileSize 获取文件大小（以字节为单位）。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件大小（以字节为单位）。
//   - error: 错误信息。
func GetFileSize(filePath string) (_result string, _err error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%d", info.Size()), nil
}

// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}

// UploadFile 将文件上传到阿里云百炼服务。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	body, err := io.ReadAll(file)
	if err != nil {
		return err
	}

	client := resty.New()
	uploadHeaders := map[string]string{
		"X-bailian-extra": headers["X-bailian-extra"],
		"Content-Type":    headers["Content-Type"],
	}

	resp, err := client.R().
		SetHeaders(uploadHeaders).
		SetBody(body).
		Put(preSignedUrl)

	if err != nil {
		return err
	}

	if resp.IsError() {
		return fmt.Errorf("HTTP 错误: %d", resp.StatusCode())
	}

	return nil
}

// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}

// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DescribeFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}

// SubmitIndexAddDocumentsJob 向一个文档搜索类知识库追加导入已解析的文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - fileId(string): 文件ID。
//   - sourceType(string): 数据类型。
//
// 返回:
//   - *bailian20231229.SubmitIndexAddDocumentsJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndexAddDocumentsJob(client *bailian20231229.Client, workspaceId, indexId, fileId, sourceType string) (_result *bailian20231229.SubmitIndexAddDocumentsJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexAddDocumentsJobRequest := &bailian20231229.SubmitIndexAddDocumentsJobRequest{
		IndexId:     tea.String(indexId),
		SourceType:  tea.String(sourceType),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexAddDocumentsJobWithOptions(tea.String(workspaceId), submitIndexAddDocumentsJobRequest, headers, runtime)
}

// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}

// DeleteIndexDocument 从指定的文档搜索类知识库中永久删除一个或多个文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexDocumentResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DeleteIndexDocument(client *bailian20231229.Client, workspaceId, indexId, fileId string) (*bailian20231229.DeleteIndexDocumentResponse, error) {
	headers := make(map[string]*string)
	deleteIndexDocumentRequest := &bailian20231229.DeleteIndexDocumentRequest{
		IndexId:     tea.String(indexId),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexDocumentWithOptions(tea.String(workspaceId), deleteIndexDocumentRequest, headers, runtime)
}

// UpdateKnowledgeBase 使用阿里云百炼服务更新知识库。
//
// 参数:
//   - filePath (string): 文件（更新后的）的实际本地路径。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 需要更新的知识库ID。
//   - oldFileId (string): 需要更新的文件的FileID。
//
// 返回:
//   - string: 如果成功，返回知识库ID；否则返回空字符串。
//   - error: 错误信息。
func UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId string) (_result string, _err error) {
	// 设置默认值
	categoryId := "default"
	parser := "DASHSCOPE_DOCMIND"
	sourceType := "DATA_CENTER_FILE"

	fmt.Println("步骤1：创建Client")
	client, err := CreateClient()
	if err != nil {
		return "", err
	}

	fmt.Println("步骤2：准备文件信息")
	fileName := filepath.Base(filePath)
	fileMD5, err := CalculateMD5(filePath)
	if err != nil {
		return "", err
	}
	fileSizeStr, err := GetFileSize(filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤3：向阿里云百炼申请上传租约")
	leaseResponse, err := ApplyLease(client, categoryId, fileName, fileMD5, fileSizeStr, workspaceId)
	if err != nil {
		return "", err
	}

	leaseId := tea.StringValue(leaseResponse.Body.Data.FileUploadLeaseId)
	uploadURL := tea.StringValue(leaseResponse.Body.Data.Param.Url)
	uploadHeaders := leaseResponse.Body.Data.Param.Headers

	jsonData, err := json.Marshal(uploadHeaders)
	if err != nil {
		return "", err
	}

	var uploadHeadersMap map[string]string
	err = json.Unmarshal(jsonData, &uploadHeadersMap)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤4：上传文件到临时存储")
	err = UploadFile(uploadURL, uploadHeadersMap, filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤5：添加文件到类目中")
	addResponse, err := AddFile(client, leaseId, parser, categoryId, workspaceId)
	if err != nil {
		return "", err
	}
	fileId := tea.StringValue(addResponse.Body.Data.FileId)

	fmt.Println("步骤6：检查阿里云百炼中的文件状态")
	for {
		describeResponse, err := DescribeFile(client, workspaceId, fileId)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(describeResponse.Body.Data.Status)
		fmt.Printf("当前文件状态：%s\n", status)

		if status == "INIT" {
			fmt.Println("文件待解析，请稍候...")
		} else if status == "PARSING" {
			fmt.Println("文件解析中，请稍候...")
		} else if status == "PARSE_SUCCESS" {
			fmt.Println("文件解析完成！")
			break
		} else {
			fmt.Printf("未知的文件状态：%s，请联系技术支持。\n", status)
			return "", fmt.Errorf("unknown document status: %s", status)
		}
		time.Sleep(5 * time.Second)
	}

	// 提交追加文件任务
	fmt.Println("步骤7：提交追加文件任务")
	indexAddResponse, err := SubmitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType)
	if err != nil {
		return "", err
	}
	jobId := tea.StringValue(indexAddResponse.Body.Data.Id)

	// 等待任务完成
	fmt.Println("步骤8：等待追加任务完成")
	for {
		getIndexJobStatusResponse, err := GetIndexJobStatus(client, workspaceId, jobId, indexId)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(getIndexJobStatusResponse.Body.Data.Status)
		fmt.Printf("当前索引任务状态：%s\n", status)

		if status == "COMPLETED" {
			break
		}
		time.Sleep(5 * time.Second)
	}

	// 删除旧文件
	fmt.Println("步骤9：删除旧文件")
	_, err = DeleteIndexDocument(client, workspaceId, indexId, oldFileId)
	if err != nil {
		return "", err
	}

	fmt.Println("阿里云百炼知识库更新成功！")
	return indexId, nil
}

// 主函数。
func main() {
	if !CheckEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}
	// 创建 scanner 用于读取输入
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
	filePath, _ := reader.ReadString('\n')
	filePath = strings.TrimSpace(filePath)

	fmt.Print("请输入需要更新的知识库ID：") // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
	indexId, _ := reader.ReadString('\n')
	indexId = strings.TrimSpace(indexId)

	fmt.Print("请输入需要更新的文件的 FileID：") // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
	oldFileId, _ := reader.ReadString('\n')
	oldFileId = strings.TrimSpace(oldFileId)

	workspaceId := os.Getenv("WORKSPACE_ID")
	result, err := UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId)
	if err != nil {
		fmt.Printf("发生错误：%v\n", err)
		return
	}

	if result != "" {
		fmt.Printf("知识库更新成功，返回知识库ID: %s\n", result)
	} else {
		fmt.Println("知识库更新失败。")
	}
}
```

<a id="管理知识库"></a>

<a id="管理知识库-h4"></a>

#### 管理知识库

> **重要**
>
> -   在调用本示例之前，请务必完成上述所有[前置步骤](rag-knowledge-base-api-guide.md#71fcfbd434agq)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
> -   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-python-tab"></a>

Python

<a id="code-code-group-4-python"></a>

```python
# 示例代码仅供参考，请勿在生产环境中直接使用
import os

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")

    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 查看知识库
def list_indices(client, workspace_id):
    """
    获取指定业务空间下一个或多个知识库的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    runtime = util_models.RuntimeOptions()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)

# 删除知识库
def delete_index(client, workspace_id, index_id):
    """
    永久性删除指定的知识库。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_request = bailian_20231229_models.DeleteIndexRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_with_options(workspace_id, delete_index_request, headers, runtime)

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    try:
        start_option = input(
            "请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：")
        if start_option == '1':
            # 查看知识库
            print("\n执行查看知识库")
            workspace_id = os.environ.get('WORKSPACE_ID')
            client = create_client()
            list_indices_response = list_indices(client, workspace_id)
            print(UtilClient.to_jsonstring(list_indices_response.body.data))
        elif start_option == '2':
            print("\n执行删除知识库")
            workspace_id = os.environ.get('WORKSPACE_ID')
            index_id = input("请输入知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            # 删除前二次确认
            while True:
                confirm = input(f"您确定要永久性删除该知识库 {index_id} 吗？(y/n): ").strip().lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    print("已取消删除操作。")
                    return
                else:
                    print("无效输入，请输入 y 或 n。")
            client = create_client()
            resp = delete_index(client, workspace_id, index_id)
            if resp.body.status == '200':
                print(f"知识库{index_id}删除成功！")
            else:
                err_info = UtilClient.to_jsonstring(resp.body)
                print(f"发生错误：{err_info}")
        else:
            print("无效的选项，程序退出。")
            return
    except Exception as e:
        print(f"发生错误：{e}")
        return

if __name__ == '__main__':
    main()
```

<a id="fig-code-group-4-java-tab"></a>

Java

<a id="code-code-group-4-java"></a>

```java
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.DeleteIndexResponse;
import com.aliyun.bailian20231229.models.ListIndicesResponse;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.*;

public class KnowledgeBaseManage {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 创建并配置客户端（Client）
     *
     * @return 配置好的客户端（Client）
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.credentials.Client credential = new com.aliyun.credentials.Client();
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setCredential(credential);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应
     */
    public static ListIndicesResponse listIndices(com.aliyun.bailian20231229.Client client, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ListIndicesRequest listIndicesRequest = new com.aliyun.bailian20231229.models.ListIndicesRequest();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
    }

    /**
     * 永久性删除指定的知识库
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应
     */
    public static DeleteIndexResponse deleteIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.DeleteIndexRequest deleteIndexRequest = new com.aliyun.bailian20231229.models.DeleteIndexRequest();
        deleteIndexRequest.setIndexId(indexId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
    }

    /**
     * 主函数
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        try {
            Scanner scanner = new Scanner(System.in);
            System.out.print("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：");
            String startOption = scanner.nextLine();
            com.aliyun.bailian20231229.Client client = createClient();
            if (startOption.equals("1")) {
                // 查看知识库
                System.out.println("\n执行查看知识库");
                String workspaceId = System.getenv("WORKSPACE_ID");
                ListIndicesResponse response = listIndices(client, workspaceId);
                // 请自行安装jackson-databind。将响应转换为 JSON 字符串
                ObjectMapper mapper = new ObjectMapper();
                String result = mapper.writeValueAsString(response.getBody().getData());
                System.out.println(result);
            } else if (startOption.equals("2")) {
                System.out.println("\n执行删除知识库");
                String workspaceId = System.getenv("WORKSPACE_ID");
                System.out.print("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                String indexId = scanner.nextLine();
                // 删除前二次确认
                boolean confirm = false;
                while (!confirm) {
                    System.out.print("您确定要永久性删除该知识库 " + indexId + " 吗？(y/n): ");
                    String input = scanner.nextLine().trim().toLowerCase();
                    if (input.equals("y")) {
                        confirm = true;
                    } else if (input.equals("n")) {
                        System.out.println("已取消删除操作。");
                        return;
                    } else {
                        System.out.println("无效输入，请输入 y 或 n。");
                    }
                }
                DeleteIndexResponse resp = deleteIndex(client, workspaceId, indexId);
                if (resp.getBody().getStatus().equals("200")) {
                    System.out.println("知识库" + indexId + "删除成功！");
                } else {
                    ObjectMapper mapper = new ObjectMapper();
                    System.out.println("发生错误：" + mapper.writeValueAsString(resp.getBody()));
                }
            } else {
                System.out.println("无效的选项，程序退出。");
            }
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
        }
    }
}
```

<a id="fig-code-group-4-php-tab"></a>

PHP

<a id="code-code-group-4-php"></a>

```php
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\DeleteIndexRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ListIndicesRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;

class KnowledgeBaseManage {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

     /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     *
     * @param Bailian $client 客户端对象（Client）
     * @param string $workspaceId 业务空间ID
     * @return ListIndicesResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function listIndices($client, $workspaceId) {
        $headers = [];
        $listIndicesRequest = new ListIndicesRequest([]);
        $runtime = new RuntimeOptions([]);
        // 调用客户端方法
        return $client->listIndicesWithOptions($workspaceId, $listIndicesRequest, $headers, $runtime);
    }

    /**
     * 永久性删除指定的知识库
     *
     * @param Bailian $client 客户端对象（Client）
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @return mixed 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function deleteIndex($client, $workspaceId, $indexId) {
        $headers = [];
        $deleteIndexRequest = new DeleteIndexRequest([
            "indexId" => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->deleteIndexWithOptions($workspaceId, $deleteIndexRequest, $headers, $runtime);
    }

    /**
     * 主函数
     */
    public static function main($args) {
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }

        try {
            echo "请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：";
            $startOption = trim(fgets(STDIN));
            $client = self::createClient();
            if ($startOption === "1") {
                // 查看知识库
                echo "\n执行查看知识库\n";
                $workspaceId = getenv("WORKSPACE_ID");
                $response = self::listIndices($client, $workspaceId);
                // 将响应转换为 JSON 字符串
                $result = json_encode($response->body->data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
                echo $result . "\n";
            } elseif ($startOption === "2") {
                echo "\n执行删除知识库\n";
                $workspaceId = getenv("WORKSPACE_ID");
                $indexId = readline("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                // 删除前二次确认
                while (true) {
                    $confirm = strtolower(trim(readline("您确定要永久性删除该知识库 $indexId 吗？(y/n): ")));
                    if ($confirm === 'y') {
                        break;
                    } elseif ($confirm === 'n') {
                        echo "已取消删除操作。\n";
                        return;
                    } else {
                        echo "无效输入，请输入 y 或 n。\n";
                    }
                }
                $response = self::deleteIndex($client, $workspaceId, $indexId);
                if ($response->body->status == "200")
                    echo "知识库" . $indexId . "删除成功！\n";
                else
                    echo "发生错误：" . json_encode($response->body) . "\n";
            } else {
                echo "无效的选项，程序退出。\n";
            }
        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseManage::main(array_slice($argv, 1));
```

<a id="fig-code-group-4-node-js-tab"></a>

Node.js

<a id="code-code-group-4-node-js"></a>

```javascript
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbManage {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }

        return missing.length === 0;
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new bailian20231229.default(config);
    }

    /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @returns {Promise<bailian20231229.ListIndicesResponse>} 阿里云百炼服务的响应
     */
    static async listIndices(client, workspaceId) {
        const headers = {};
        const listIndicesRequest = new bailian20231229.ListIndicesRequest();
        const runtime = new Util.RuntimeOptions({});
        return await client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
    }

    /**
     * 永久性删除指定的知识库
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @param {string} indexId 知识库ID
     * @returns {Promise<bailian20231229.DeleteIndexResponse>} 阿里云百炼服务的响应
     */
    static async deleteIndex(client, workspaceId, indexId) {
        const headers = {};
        const deleteIndexRequest = new bailian20231229.DeleteIndexRequest({
            indexId
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务执行操作（查看或删除知识库）
     */
    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            const startOption = await new Promise((resolve) => {
                readline.question("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：", (ans) => {
                    resolve(ans.trim());
                });
            });

            if (startOption === '1') {
                console.log("\n执行查看知识库");
                const workspaceId = process.env.WORKSPACE_ID;
                const client = this.createClient();
                const response = await this.listIndices(client, workspaceId);
                console.log(JSON.stringify(response.body.data));
            } else if (startOption === '2') {
                console.log("\n执行删除知识库");
                const workspaceId = process.env.WORKSPACE_ID;
                const indexId = await new Promise((resolve) => {
                    readline.question("请输入知识库ID：", (ans) => { // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                        resolve(ans.trim());
                    });
                });
                // 删除前二次确认
                let confirm = '';
                while (confirm !== 'y' && confirm !== 'n') {
                    confirm = (await new Promise((resolve) => {
                        readline.question(`您确定要永久性删除该知识库 ${indexId} 吗？(y/n): `, (ans) => {
                            resolve(ans.trim().toLowerCase());
                        });
                    })).toLowerCase();
                    if (confirm === 'n') {
                        console.log("已取消删除操作。");
                        return;
                    } else if (confirm !== 'y') {
                        console.log("无效输入，请输入 y 或 n。");
                    }
                }
                const client = this.createClient();
                const resp = await this.deleteIndex(client, workspaceId, indexId);
                if (resp.body.status == '200')
                    console.log(`知识库${indexId}删除成功！`);
                else {
                    const errInfo = JSON.stringify(resp.body);
                    console.error(`发生错误：${errInfo}`)
                }
            } else {
                console.log("无效的选项，程序退出。");
            }
        } catch (err) {
            console.error(`发生错误：${err.message}`);
        } finally {
            readline.close();
        }
    }
}

exports.KbManage = KbManage;
KbManage.main(process.argv.slice(2));
```

<a id="fig-code-group-4-c-tab"></a>

C#

<a id="code-code-group-4-c"></a>

```csharp
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseManage
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 获取指定业务空间下一个或多个知识库的详细信息。
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ListIndicesResponse ListIndices(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var listIndicesRequest = new Bailian20231229.Models.ListIndicesRequest();
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ListIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
        }

        /// <summary>
        /// 永久性删除指定的知识库。
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexResponse DeleteIndex(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId, string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var deleteIndexRequest = new Bailian20231229.Models.DeleteIndexRequest
            {
                IndexId = indexId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DeleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
        }

        /// <summary>
        /// 主函数
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }
            try
            {
                Console.Write("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：");
                string startOption = Console.ReadLine();
                if (startOption == "1")
                {
                    Console.WriteLine("\n执行查看知识库");
                    string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                    Bailian20231229.Client client = CreateClient();
                    Bailian20231229.Models.ListIndicesResponse listIndicesResponse = ListIndices(client, workspaceId);
                    // 请自行安装Newtonsoft.Json。将响应对象转为 JSON 字符串输出
                    var json = JsonConvert.SerializeObject(listIndicesResponse.Body.Data, Formatting.Indented);
                    Console.WriteLine(json);
                }
                else if (startOption == "2")
                {
                    Console.WriteLine("\n执行删除知识库");
                    string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                    Console.Write("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                    string indexId = Console.ReadLine();
                    // 删除前二次确认
                    while (true)
                    {
                        Console.Write($"您确定要永久性删除该知识库 {indexId} 吗？(y/n): ");
                        string confirm = Console.ReadLine()?.ToLower();
                        if (confirm == "y")
                        {
                            break;
                        }
                        else if (confirm == "n")
                        {
                            Console.WriteLine("已取消删除操作。");
                            return;
                        }
                        else
                        {
                            Console.WriteLine("无效输入，请输入 y 或 n。");
                        }
                    }
                    Bailian20231229.Client client = CreateClient();
                    Bailian20231229.Models.DeleteIndexResponse resp = DeleteIndex(client, workspaceId, indexId);
                    if (resp.Body.Status == "200")
                    {
                        Console.WriteLine($"知识库{indexId}删除成功！");
                    }
                    else
                    {
                        var mapper = new JsonSerializerSettings { Formatting = Formatting.Indented };
                        string errInfo = JsonConvert.SerializeObject(resp.Body, mapper);
                        Console.WriteLine($"发生错误：{errInfo}");
                    }
                }
                else
                {
                    Console.WriteLine("无效的选项，程序退出。");
                    return;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
            }
        }
    }
}
```

<a id="fig-code-group-4-go-tab"></a>

Go

<a id="code-code-group-4-go"></a>

```go
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

// checkEnvironmentVariables 检查并提示设置必要的环境变量。
func checkEnvironmentVariables() bool {
	// 必要的环境变量及其描述
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// createClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
func createClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// listIndices 获取指定业务空间下一个或多个知识库的详细信息。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//
// 返回:
//   - *bailian20231229.ListIndicesResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func listIndices(client *bailian20231229.Client, workspaceId string) (_result *bailian20231229.ListIndicesResponse, _err error) {
	headers := make(map[string]*string)
	listIndicesRequest := &bailian20231229.ListIndicesRequest{}
	runtime := &util.RuntimeOptions{}
	return client.ListIndicesWithOptions(tea.String(workspaceId), listIndicesRequest, headers, runtime)
}

// deleteIndex 永久性删除指定的知识库。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//   - indexId     string: 知识库ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func deleteIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.DeleteIndexResponse, _err error) {
	headers := make(map[string]*string)
	deleteIndexRequest := &bailian20231229.DeleteIndexRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexWithOptions(tea.String(workspaceId), deleteIndexRequest, headers, runtime)

}

// 主函数。
func main() {
	if !checkEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}

	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：")

	// 确保读取输入
	if !scanner.Scan() {
		fmt.Println("无法读取输入。")
		return
	}
	startOption := scanner.Text()

	client, err := createClient()
	if err != nil {
		fmt.Println("创建客户端失败:", err)
		return
	}

	if strings.TrimSpace(startOption) == "1" {
		fmt.Println("\n执行查看知识库")
		workspaceId := os.Getenv("WORKSPACE_ID")
		resp, err := listIndices(client, workspaceId)
		if err != nil {
			fmt.Println("获取知识库列表失败:", err)
			return
		}
		fmt.Printf("知识库列表:\n%+v\n", resp.Body.Data)
	} else if strings.TrimSpace(startOption) == "2" {
		fmt.Println("\n执行删除知识库")
		workspaceId := os.Getenv("WORKSPACE_ID")
		fmt.Print("请输入知识库ID：")
		if !scanner.Scan() {
			fmt.Println("无法读取知识库ID。")
			return
		}
		indexId := scanner.Text()
		for {
			fmt.Printf("您确定要永久性删除该知识库 %s 吗？(y/n): ", indexId)
			if !scanner.Scan() {
				fmt.Println("无法读取确认输入。")
				return
			}
			confirm := strings.ToLower(strings.TrimSpace(scanner.Text()))

			if confirm == "y" {
				break
			} else if confirm == "n" {
				fmt.Println("已取消删除操作。")
				return
			} else {
				fmt.Println("无效输入，请输入 y 或 n。")
			}
		}
		resp, err := deleteIndex(client, workspaceId, indexId)
		if err != nil {
			fmt.Println("删除知识库失败:", err)
		} else {
			if tea.StringValue(resp.Body.Status) == "200" {
				fmt.Printf("知识库 %s 删除成功！\n", indexId)
			} else {
				fmt.Println(resp.Body)
			}
		}
	} else {
		fmt.Println("无效的选项，程序退出。")
	}
}
```

<a id="切片管理"></a>

<a id="切片管理-h4"></a>

#### 切片管理

> **重要**
>
> -   在调用本示例之前，请务必完成上述所有[前置步骤](rag-knowledge-base-api-guide.md#71fcfbd434agq)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
> -   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。

<a id="fig-code-group-5"></a>

<a id="fig-code-group-5-python-tab"></a>

Python

<a id="code-code-group-5-python"></a>

```python
# 示例代码仅供参考，请勿在生产环境中直接使用
import os
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_bailian20231229 import models as bailian_models
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions

def create_client():
    config = Config(
        access_key_id=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        endpoint="bailian.cn-beijing.aliyuncs.com"
    )
    return bailian20231229Client(config)

def list_chunks(client, workspace_id, index_id, page_num=1, page_size=10):
    """列出切片"""
    request = bailian_models.ListChunksRequest(
        index_id=index_id,
        page_num=page_num,
        page_size=page_size,
    )
    runtime = RuntimeOptions()
    response = client.list_chunks_with_options(workspace_id, request, {}, runtime)
    return response.body

def update_chunk(client, workspace_id, pipeline_id, data_id, chunk_id, content, title=None):
    """更新切片内容"""
    request = bailian_models.UpdateChunkRequest(
        pipeline_id=pipeline_id,
        data_id=data_id,
        chunk_id=chunk_id,
        is_displayed_chunk_content=True,
        content=content,
    )
    if title:
        request.title = title
    runtime = RuntimeOptions()
    response = client.update_chunk_with_options(workspace_id, request, {}, runtime)
    return response.body

def delete_chunk(client, workspace_id, pipeline_id, chunk_ids):
    """删除切片"""
    request = bailian_models.DeleteChunkRequest(
        pipeline_id=pipeline_id,
        chunk_ids=chunk_ids,
    )
    runtime = RuntimeOptions()
    response = client.delete_chunk_with_options(workspace_id, request, {}, runtime)
    return response.body

def main():
    workspace_id = os.environ.get("WORKSPACE_ID")
    index_id = "YOUR_INDEX_ID"
    pipeline_id = "YOUR_INDEX_ID"

    client = create_client()

    # 列出切片
    result = list_chunks(client, workspace_id, index_id)
    print(f"Total chunks: {result.data.total}")
    nodes = result.data.nodes or []
    for i, node in enumerate(nodes):
        meta = node.metadata
        chunk_id = meta.get("_id", "")
        doc_id = meta.get("doc_id", "")
        print(f"  [{i}] chunk_id={chunk_id}, doc_id={doc_id}")

    if not nodes:
        print("No chunks found.")
        return

    # 更新切片
    target = nodes[0]
    target_meta = target.metadata
    target_chunk_id = target_meta.get("_id")
    target_data_id = target_meta.get("doc_id")
    update_result = update_chunk(
        client, workspace_id, pipeline_id,
        data_id=target_data_id,
        chunk_id=target_chunk_id,
        content="更新后的切片内容",
    )
    print(f"Update success: {update_result.success}")

    # 删除切片
    last_chunk_id = nodes[-1].metadata.get("_id")
    delete_result = delete_chunk(
        client, workspace_id, pipeline_id,
        chunk_ids=[last_chunk_id],
    )
    print(f"Delete success: {delete_result.success}")

if __name__ == "__main__":
    main()
```

<a id="fig-code-group-5-java-tab"></a>

Java

<a id="code-code-group-5-java"></a>

```java
// 示例代码仅供参考，请勿在生产环境中直接使用
package com.example;

import com.aliyun.bailian20231229.Client;
import com.aliyun.bailian20231229.models.*;
import com.aliyun.teaopenapi.models.Config;
import com.aliyun.teautil.models.RuntimeOptions;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class ChunkManagement {

    public static Client createClient() throws Exception {
        Config config = new Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
                .setEndpoint("bailian.cn-beijing.aliyuncs.com");
        return new Client(config);
    }

    /**
     * 列出切片
     */
    public static ListChunksResponse listChunks(Client client, String workspaceId,
                                                 String indexId, Integer pageNum, Integer pageSize) throws Exception {
        ListChunksRequest request = new ListChunksRequest()
                .setIndexId(indexId)
                .setPageNum(pageNum)
                .setPageSize(pageSize);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.listChunksWithOptions(workspaceId, request, new java.util.HashMap<>(), runtime);
    }

    /**
     * 更新切片
     */
    public static UpdateChunkResponse updateChunk(Client client, String workspaceId,
                                                   String pipelineId, String dataId,
                                                   String chunkId, String content) throws Exception {
        UpdateChunkRequest request = new UpdateChunkRequest()
                .setPipelineId(pipelineId)
                .setDataId(dataId)
                .setChunkId(chunkId)
                .setIsDisplayedChunkContent(true)
                .setContent(content);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.updateChunkWithOptions(workspaceId, request, new java.util.HashMap<>(), runtime);
    }

    /**
     * 删除切片
     */
    public static DeleteChunkResponse deleteChunk(Client client, String workspaceId,
                                                   String pipelineId, List<String> chunkIds) throws Exception {
        DeleteChunkRequest request = new DeleteChunkRequest()
                .setPipelineId(pipelineId)
                .setChunkIds(chunkIds);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.deleteChunkWithOptions(workspaceId, request, new java.util.HashMap<>(), runtime);
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        String workspaceId = System.getenv("WORKSPACE_ID");
        String indexId = "YOUR_INDEX_ID";
        String pipelineId = "YOUR_INDEX_ID";

        Client client = createClient();

        // 列出切片
        ListChunksResponse listResp = listChunks(client, workspaceId, indexId, 1, 10);
        ListChunksResponseBody body = listResp.getBody();
        ListChunksResponseBody.ListChunksResponseBodyData data = body.getData();
        System.out.println("Total chunks: " + data.getTotal());

        List<ListChunksResponseBody.ListChunksResponseBodyDataNodes> nodes = data.getNodes();
        if (nodes == null || nodes.isEmpty()) {
            System.out.println("No chunks found.");
            return;
        }

        for (int i = 0; i < nodes.size(); i++) {
            ListChunksResponseBody.ListChunksResponseBodyDataNodes node = nodes.get(i);
            Map<String, Object> metadata = (Map<String, Object>) node.getMetadata();
            String chunkId = metadata != null ? String.valueOf(metadata.get("_id")) : "";
            String docId = metadata != null ? String.valueOf(metadata.get("doc_id")) : "";
            System.out.printf("  [%d] chunk_id=%s, doc_id=%s%n", i, chunkId, docId);
        }

        // 更新切片
        ListChunksResponseBody.ListChunksResponseBodyDataNodes target = nodes.get(0);
        Map<String, Object> targetMeta = (Map<String, Object>) target.getMetadata();
        String targetChunkId = String.valueOf(targetMeta.get("_id"));
        String targetDataId = String.valueOf(targetMeta.get("doc_id"));

        UpdateChunkResponse updateResp = updateChunk(client, workspaceId, pipelineId,
                targetDataId, targetChunkId, "更新后的切片内容");
        System.out.println("Update success: " + updateResp.getBody().getSuccess());

        // 删除切片
        ListChunksResponseBody.ListChunksResponseBodyDataNodes lastNode = nodes.get(nodes.size() - 1);
        Map<String, Object> lastMeta = (Map<String, Object>) lastNode.getMetadata();
        String lastChunkId = String.valueOf(lastMeta.get("_id"));

        DeleteChunkResponse deleteResp = deleteChunk(client, workspaceId, pipelineId,
                Arrays.asList(lastChunkId));
        System.out.println("Delete success: " + deleteResp.getBody().getSuccess());
    }
}
```

<a id="fig-code-group-5-php-tab"></a>

PHP

<a id="code-code-group-5-php"></a>

```php
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
require_once __DIR__ . '/vendor/autoload.php';

use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ListChunksRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\UpdateChunkRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\DeleteChunkRequest;
use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\Dara\Models\RuntimeOptions;

$accessKeyId = getenv('ALIBABA_CLOUD_ACCESS_KEY_ID');
$accessKeySecret = getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET');
$workspaceId = getenv('WORKSPACE_ID');
$indexId = 'YOUR_INDEX_ID';

// 初始化客户端
$config = new Config([
    'accessKeyId' => $accessKeyId,
    'accessKeySecret' => $accessKeySecret,
    'endpoint' => 'bailian.cn-beijing.aliyuncs.com'
]);
$client = new Bailian($config);
$runtime = new RuntimeOptions([]);
$headers = [];

// 列出切片
$request = new ListChunksRequest([
    'indexId' => $indexId,
    'pageNum' => 1,
    'pageSize' => 10
]);
$response = $client->listChunksWithOptions($workspaceId, $request, $headers, $runtime);
$body = $response->body;
echo "Total: " . $body->data->total . "\n";

if ($body->data->nodes && count($body->data->nodes) > 0) {
    $firstNode = $body->data->nodes[0];
    $metadata = $firstNode->metadata;
    $docId = $metadata['doc_id'] ?? '';
    $chunkFullId = $metadata['_id'] ?? '';
    echo "First chunk _id: $chunkFullId\n";

    // 更新切片
    $updateReq = new UpdateChunkRequest([
        'pipelineId' => $indexId,
        'dataId' => $docId,
        'chunkId' => $chunkFullId,
        'isDisplayedChunkContent' => true,
        'content' => '更新后的切片内容'
    ]);
    $updateResp = $client->updateChunkWithOptions($workspaceId, $updateReq, $headers, $runtime);
    echo "Update success: " . ($updateResp->body->success ? 'true' : 'false') . "\n";

    // 删除切片
    $lastNode = $body->data->nodes[count($body->data->nodes) - 1];
    $lastId = $lastNode->metadata['_id'] ?? '';
    $delReq = new DeleteChunkRequest([
        'pipelineId' => $indexId,
        'chunkIds' => [$lastId]
    ]);
    $delResp = $client->deleteChunkWithOptions($workspaceId, $delReq, $headers, $runtime);
    echo "Delete success: " . ($delResp->body->success ? 'true' : 'false') . "\n";
}
```

<a id="fig-code-group-5-node-js-tab"></a>

Node.js

<a id="code-code-group-5-node-js"></a>

```javascript
// 示例代码仅供参考，请勿在生产环境中直接使用
const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');

const WORKSPACE_ID = process.env.WORKSPACE_ID;
const INDEX_ID = 'YOUR_INDEX_ID';

function createClient() {
    const config = new OpenApi.Config({
        accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
        accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        endpoint: 'bailian.cn-beijing.aliyuncs.com'
    });
    return new bailian20231229.default(config);
}

async function listChunks(client) {
    const request = new bailian20231229.ListChunksRequest({
        indexId: INDEX_ID,
        pageNum: 1,
        pageSize: 10
    });
    const runtime = new Util.RuntimeOptions({});
    const response = await client.listChunksWithOptions(WORKSPACE_ID, request, {}, runtime);
    return response.body;
}

async function updateChunk(client, chunkId, dataId, content) {
    const request = new bailian20231229.UpdateChunkRequest({
        pipelineId: INDEX_ID,
        dataId: dataId,
        chunkId: chunkId,
        isDisplayedChunkContent: true,
        content: content
    });
    const runtime = new Util.RuntimeOptions({});
    const response = await client.updateChunkWithOptions(WORKSPACE_ID, request, {}, runtime);
    return response.body;
}

async function deleteChunk(client, chunkId) {
    const request = new bailian20231229.DeleteChunkRequest({
        pipelineId: INDEX_ID,
        chunkIds: [chunkId]
    });
    const runtime = new Util.RuntimeOptions({});
    const response = await client.deleteChunkWithOptions(WORKSPACE_ID, request, {}, runtime);
    return response.body;
}

async function main() {
    const client = createClient();

    // 列出切片
    const listBody = await listChunks(client);
    console.log('Total:', listBody.data?.total);
    const nodes = listBody.data?.nodes || [];

    if (nodes.length === 0) {
        console.log('No chunks found.');
        return;
    }

    for (let i = 0; i < nodes.length; i++) {
        const metadata = nodes[i].metadata || {};
        console.log(`  [${i}] chunk_id=${metadata._id}, doc_id=${metadata.doc_id}`);
    }

    // 更新切片
    const firstMeta = nodes[0].metadata || {};
    const updateResult = await updateChunk(client, firstMeta._id, firstMeta.doc_id, '更新后的切片内容');
    console.log('Update success:', updateResult.success);

    // 删除切片
    const lastMeta = nodes[nodes.length - 1].metadata || {};
    const deleteResult = await deleteChunk(client, lastMeta._id);
    console.log('Delete success:', deleteResult.success);
}

main().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
});
```

<a id="fig-code-group-5-c-tab"></a>

C#

<a id="code-code-group-5-c"></a>

```csharp
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections.Generic;
using AlibabaCloud.SDK.Bailian20231229;
using AlibabaCloud.SDK.Bailian20231229.Models;
using AlibabaCloud.OpenApiClient.Models;
using AlibabaCloud.TeaUtil.Models;

class Program
{
    static Client CreateClient()
    {
        var config = new Config
        {
            AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            Endpoint = "bailian.cn-beijing.aliyuncs.com"
        };
        return new Client(config);
    }

    static void Main(string[] args)
    {
        var client = CreateClient();
        var workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
        var indexId = "YOUR_INDEX_ID";
        var headers = new Dictionary<string, string>();
        var runtime = new RuntimeOptions();

        // 列出切片
        var listReq = new ListChunksRequest
        {
            IndexId = indexId,
            PageNum = 1,
            PageSize = 10
        };
        var listResp = client.ListChunksWithOptions(workspaceId, listReq, headers, runtime);
        Console.WriteLine($"Total: {listResp.Body.Data?.Total}");

        if (listResp.Body.Data?.Nodes == null || listResp.Body.Data.Nodes.Count == 0)
        {
            Console.WriteLine("No chunks found.");
            return;
        }

        for (int i = 0; i < listResp.Body.Data.Nodes.Count; i++)
        {
            var node = listResp.Body.Data.Nodes[i];
            var metadata = node.Metadata as Dictionary<string, object>;
            var chunkId = metadata?.ContainsKey("_id") == true ? metadata["_id"]?.ToString() : "";
            var docId = metadata?.ContainsKey("doc_id") == true ? metadata["doc_id"]?.ToString() : "";
            Console.WriteLine($"  [{i}] chunk_id={chunkId}, doc_id={docId}");
        }

        // 更新切片
        var firstNode = listResp.Body.Data.Nodes[0];
        var firstMeta = firstNode.Metadata as Dictionary<string, object>;
        var targetChunkId = firstMeta?["_id"]?.ToString() ?? "";
        var targetDataId = firstMeta?["doc_id"]?.ToString() ?? "";

        var updateReq = new UpdateChunkRequest
        {
            PipelineId = indexId,
            DataId = targetDataId,
            ChunkId = targetChunkId,
            IsDisplayedChunkContent = true,
            Content = "更新后的切片内容"
        };
        var updateResp = client.UpdateChunkWithOptions(workspaceId, updateReq, headers, runtime);
        Console.WriteLine($"Update success: {updateResp.Body.Success}");

        // 删除切片
        var lastNode = listResp.Body.Data.Nodes[listResp.Body.Data.Nodes.Count - 1];
        var lastMeta = lastNode.Metadata as Dictionary<string, object>;
        var lastChunkId = lastMeta?["_id"]?.ToString() ?? "";

        var delReq = new DeleteChunkRequest
        {
            PipelineId = indexId,
            ChunkIds = new List<string> { lastChunkId }
        };
        var delResp = client.DeleteChunkWithOptions(workspaceId, delReq, headers, runtime);
        Console.WriteLine($"Delete success: {delResp.Body.Success}");
    }
}
```

<a id="fig-code-group-5-go-tab"></a>

Go

<a id="code-code-group-5-go"></a>

```go
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"fmt"
	"os"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

func CreateClient() (*bailian20231229.Client, error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
		Endpoint:        tea.String("bailian.cn-beijing.aliyuncs.com"),
	}
	return bailian20231229.NewClient(config)
}

func ListChunks(client *bailian20231229.Client, workspaceId string, indexId string) (*bailian20231229.ListChunksResponseBody, error) {
	req := &bailian20231229.ListChunksRequest{
		IndexId:  tea.String(indexId),
		PageNum:  tea.Int32(1),
		PageSize: tea.Int32(10),
	}
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	resp, err := client.ListChunksWithOptions(tea.String(workspaceId), req, headers, runtime)
	if err != nil {
		return nil, err
	}
	return resp.Body, nil
}

func UpdateChunk(client *bailian20231229.Client, workspaceId string, pipelineId string, chunkId string, dataId string, content string) error {
	req := &bailian20231229.UpdateChunkRequest{
		PipelineId:              tea.String(pipelineId),
		DataId:                  tea.String(dataId),
		ChunkId:                 tea.String(chunkId),
		IsDisplayedChunkContent: tea.Bool(true),
		Content:                 tea.String(content),
	}
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	resp, err := client.UpdateChunkWithOptions(tea.String(workspaceId), req, headers, runtime)
	if err != nil {
		return err
	}
	fmt.Printf("Update success: %v\n", tea.BoolValue(resp.Body.Success))
	return nil
}

func DeleteChunk(client *bailian20231229.Client, workspaceId string, pipelineId string, chunkIds []*string) error {
	req := &bailian20231229.DeleteChunkRequest{
		PipelineId: tea.String(pipelineId),
		ChunkIds:   chunkIds,
	}
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	resp, err := client.DeleteChunkWithOptions(tea.String(workspaceId), req, headers, runtime)
	if err != nil {
		return err
	}
	fmt.Printf("Delete success: %v\n", tea.BoolValue(resp.Body.Success))
	return nil
}

func main() {
	client, err := CreateClient()
	if err != nil {
		fmt.Printf("Error creating client: %v\n", err)
		os.Exit(1)
	}
	workspaceId := os.Getenv("WORKSPACE_ID")
	indexId := "YOUR_INDEX_ID"

	// 列出切片
	body, err := ListChunks(client, workspaceId, indexId)
	if err != nil {
		fmt.Printf("Error listing chunks: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Total chunks: %d\n", tea.Int64Value(body.Data.Total))

	// 更新切片
	err = UpdateChunk(client, workspaceId, indexId, "YOUR_CHUNK_ID", "YOUR_DOC_ID", "更新后的切片内容")
	if err != nil {
		fmt.Printf("Error updating chunk: %v\n", err)
	}

	// 删除切片
	err = DeleteChunk(client, workspaceId, indexId, []*string{tea.String("YOUR_CHUNK_ID")})
	if err != nil {
		fmt.Printf("Error deleting chunk: %v\n", err)
	}
}
```

<a id="创建知识库-2"></a>

<a id="f5b417e92ajyd"></a>

## 创建知识库

接下来通过示例，引导您在给定的业务空间下创建一个文档搜索类知识库。

<table><tbody><tr><td><a id="a8ce8e7788gmh"></a><h3>1. 初始化客户端</h3><p>在开始上传文件和创建知识库之前，您需要使用<a href="rag-knowledge-base-api-guide.md#71fcfbd434agq">配置好的AccessKey和AccessKey Secret</a>初始化客户端（Client），以完成身份验证和接入点<code>endpoint</code>配置。</p><ul><li><strong>公网接入地址：</strong><blockquote><p>请确保您的客户端可以访问公网。</p></blockquote><ul><li>公有云：<code>bailian.cn-beijing.aliyuncs.com</code></li></ul></li><li><strong>VPC接入地址：</strong><blockquote><p>若您的客户端部署在阿里云北京地域<code>cn-beijing</code>（公有云），且处于<a href="https://help.aliyun.com/zh/vpc/what-is-vpc">VPC</a>网络环境中，可以使用以下VPC接入地址（不支持跨地域访问）。</p></blockquote><ul><li>公有云：<code>bailian-vpc.cn-beijing.aliyuncs.com</code></li></ul></li></ul><p>创建完成后，您将得到一个Client对象，用于后续的 API 调用。</p></td><td><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>def create_client() -&gt; bailian20231229Client:
    &quot;&quot;&quot;
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    &quot;&quot;&quot;
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)
</code></pre></div><a id="fig-code-group-6-java-tab"></a>Java<div><a id="code-code-group-6-java"></a><pre class="language-java"><code>/**
 * 初始化客户端（Client）。
 *
 * @return 配置好的客户端对象
 */
public com.aliyun.bailian20231229.Client createClient() throws Exception {
    com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
            .setAccessKeyId(System.getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_ID&quot;))
            .setAccessKeySecret(System.getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_SECRET&quot;));
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = &quot;bailian.cn-beijing.aliyuncs.com&quot;;
    return new com.aliyun.bailian20231229.Client(config);
}
</code></pre></div><a id="fig-code-group-6-php-tab"></a>PHP<div><a id="code-code-group-6-php"></a><pre class="language-php"><code>/**
 * 初始化客户端（Client）。
 *
 * @return Bailian 配置好的客户端对象（Client）。
 */
public function createClient(){
    $config = new Config([
        &quot;accessKeyId&quot; =&gt; getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_ID&quot;),
        &quot;accessKeySecret&quot; =&gt; getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_SECRET&quot;)
    ]);
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    $config-&gt;endpoint = 'bailian.cn-beijing.aliyuncs.com';
    return new Bailian($config);
}
</code></pre></div><a id="fig-code-group-6-node-js-tab"></a>Node.js<div><a id="code-code-group-6-node-js"></a><pre class="language-javascript"><code>/**
 * 创建并配置客户端（Client）
 * @return Client
 * @throws Exception
 */
function createClient() {
  const config = new OpenApi.Config({
    accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
    accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
  });
  // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
  config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
  return new bailian20231229.default(config);
}
</code></pre></div><a id="fig-code-group-6-c-tab"></a>C#<div><a id="code-code-group-6-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 初始化客户端（Client）。
/// &lt;/summary&gt;
/// &lt;returns&gt;配置好的客户端对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;初始化过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
{
    var config = new AlibabaCloud.OpenApiClient.Models.Config
    {
        AccessKeyId = Environment.GetEnvironmentVariable(&quot;ALIBABA_CLOUD_ACCESS_KEY_ID&quot;),
        AccessKeySecret = Environment.GetEnvironmentVariable(&quot;ALIBABA_CLOUD_ACCESS_KEY_SECRET&quot;),
    };
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址.
    config.Endpoint = &quot;bailian.cn-beijing.aliyuncs.com&quot;;
    return new AlibabaCloud.SDK.Bailian20231229.Client(config);
}
</code></pre></div><a id="fig-code-group-6-go-tab"></a>Go<div><a id="code-code-group-6-go"></a><pre class="language-go"><code>// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &amp;openapi.Config{
		AccessKeyId:     tea.String(os.Getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_ID&quot;)),
		AccessKeySecret: tea.String(os.Getenv(&quot;ALIBABA_CLOUD_ACCESS_KEY_SECRET&quot;)),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String(&quot;bailian.cn-beijing.aliyuncs.com&quot;)
	_result = &amp;bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}
</code></pre></div></div></td></tr><tr><td colspan="2"><a id="4b4a1236aalno"></a><h3>2. 上传知识库文件</h3></td></tr><tr><td><a id="30d77d8d0a9n1"></a><h4>2.1. 申请文件上传租约</h4><p>在创建知识库前，您需先将文件上传至<strong>同一业务空间</strong>，作为知识库的知识来源。上传文件前，需调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-applyfileuploadlease">ApplyFileUploadLease接口</a>申请一个文件上传租约。该租约是一个临时的授权，允许您在限定时间内（有效期为分钟级）上传文件。</p><ul><li><p><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></p></li><li><p><strong>category_id：</strong>本示例中，请传入<code>default</code>。阿里云百炼使用类目管理您上传的文件，系统会自动创建一个默认类目。您亦可调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addcategory">AddCategory接口</a>创建新类目，并获取对应的<code>category_id</code>。</p></li><li><p><strong>file_name：</strong>请传入上传文件的名称（包括后缀）。其值必须与实际文件名一致。例如，实际上传文件的文件名为 <code>阿里云百炼系列手机产品介绍.docx</code> 时，<code>file_name</code> 传入 <code>阿里云百炼系列手机产品介绍.docx</code>。</p></li><li><p><strong>file_md5：</strong>请传入上传文件的MD5值（但当前阿里云不对该值进行校验，便于您使用URL地址上传文件）。</p><blockquote><p>以Python为例，MD5值可使用hashlib模块获取。其他语言请参见<a href="rag-knowledge-base-api-guide.md">完整示例代码</a>。</p></blockquote><a id="accordion-代码示例"></a><section><p>代码示例</p><div><a id="code-block-2"></a><pre class="language-python"><code>import hashlib

def calculate_md5(file_path):
    &quot;&quot;&quot;
    计算文件的MD5值。

    参数:
        file_path (str): 文件本地路径。

    返回:
        str: 文件的MD5值。
    &quot;&quot;&quot;
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, &quot;rb&quot;) as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b&quot;&quot;):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

# 使用示例
file_path = &quot;请替换为您需要上传文件的实际本地路径，例如/xxx/xxx/xxx/阿里云百炼系列手机产品介绍.docx&quot;
md5_value = calculate_md5(file_path)
print(f&quot;文件的MD5值为: {md5_value}&quot;)
</code></pre><p>将代码中的<code>file_path</code>变量替换为文件的实际本地路径后运行，即可获取目标文件的MD5值（下方为示例值）：</p><a id="code-block-3"></a><pre class="language-text"><code>文件的MD5值为: 2ef7361ea907f3a1b91e3b9936f5643a
</code></pre></div></section></li><li><p><strong>file_size：</strong>请传入上传文件的字节大小。</p><blockquote><p>以Python为例，该值可使用os模块获取。其他语言请参见<a href="rag-knowledge-base-api-guide.md">完整示例代码</a>。</p></blockquote><a id="accordion-代码示例-2"></a><section><p>代码示例</p><div><a id="code-block-4"></a><pre class="language-python"><code>import os

def get_file_size(file_path: str) -&gt; int:
    &quot;&quot;&quot;
    获取文件的字节大小（以字节为单位）。

    参数:
        file_path (str): 文件的实际本地路径。

    返回:
        int: 文件大小（以字节为单位）。
    &quot;&quot;&quot;
    return os.path.getsize(file_path)

# 使用示例
file_path = &quot;请替换为您需要上传文件的实际本地路径，例如/xxx/xxx/xxx/阿里云百炼系列手机产品介绍.docx&quot;
file_size = get_file_size(file_path)
print(f&quot;文件的字节大小为: {file_size}&quot;)
</code></pre><p>将代码中的<code>file_path</code>变量替换为文件的实际本地路径后运行，即可获取目标文件的字节大小（下方为示例值）：</p><a id="code-block-5"></a><pre class="language-text"><code>文件的字节大小为: 14015
</code></pre></div></section></li></ul><p>申请临时上传租约成功后，您将获得：</p><ul><li><strong>一组临时上传参数：</strong><ul><li><code>Data.FileUploadLeaseId</code></li><li><code>Data.Param.Method</code></li><li><code>Data.Param.Headers</code>中的<code>X-bailian-extra</code></li><li><code>Data.Param.Headers</code>中的<code>Content-Type</code></li></ul></li><li><p><strong>一个临时上传URL：</strong><code>Data.Param.Url</code></p></li></ul><p>您将在下一步中用到它们。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    &quot;&quot;&quot;
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-7-java-tab"></a>Java<div><a id="code-code-group-7-java"></a><pre class="language-java"><code>/**
 * 申请文件上传租约。
 *
 * @param client      客户端对象
 * @param categoryId  类目ID
 * @param fileName    文件名称
 * @param fileMd5     文件的MD5值
 * @param fileSize    文件大小（以字节为单位）
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应对象
 */
public ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
    applyFileUploadLeaseRequest.setFileName(fileName);
    applyFileUploadLeaseRequest.setMd5(fileMd5);
    applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
    applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
    return applyFileUploadLeaseResponse;
}
</code></pre></div><a id="fig-code-group-7-php-tab"></a>PHP<div><a id="code-code-group-7-php"></a><pre class="language-php"><code>/**
 * 申请文件上传租约。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $categoryId 类目ID。
 * @param string $fileName 文件名称。
 * @param string $fileMd5 文件的MD5值。
 * @param int $fileSize 文件大小（以字节为单位）。
 * @param string $workspaceId 业务空间ID。
 * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
 */
public function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
    $headers = [];
    $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
        &quot;fileName&quot; =&gt; $fileName,
        &quot;md5&quot; =&gt; $fileMd5,
        &quot;sizeInBytes&quot; =&gt; $fileSize
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-7-node-js-tab"></a>Node.js<div><a id="code-code-group-7-node-js"></a><pre class="language-javascript"><code>/**
 * 申请文件上传租约
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} categoryId - 类目ID
 * @param {string} fileName - 文件名称
 * @param {string} fileMd5 - 文件的MD5值
 * @param {string} fileSize - 文件大小（以字节为单位）
 * @param {string} workspaceId - 业务空间ID
 * @returns {Promise&lt;bailian20231229.ApplyFileUploadLeaseResponse&gt;} - 阿里云百炼服务的响应
 */
async function applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
  const headers = {};
  const req = new bailian20231229.ApplyFileUploadLeaseRequest({
    md5: fileMd5,
    fileName,
    sizeInBytes: fileSize
 });
 const runtime = new Util.RuntimeOptions({});
 return await client.applyFileUploadLeaseWithOptions(
    categoryId,
    workspaceId,
    req,
    headers,
    runtime
  );
}
</code></pre></div><a id="fig-code-group-7-c-tab"></a>C#<div><a id="code-code-group-7-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 申请文件上传租约。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;categoryId&quot;&gt;类目ID&lt;/param&gt;
/// &lt;param name=&quot;fileName&quot;&gt;文件名称&lt;/param&gt;
/// &lt;param name=&quot;fileMd5&quot;&gt;文件的MD5值&lt;/param&gt;
/// &lt;param name=&quot;fileSize&quot;&gt;文件大小（以字节为单位）&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string categoryId,
    string fileName,
    string fileMd5,
    string fileSize,
    string workspaceId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
    {
        FileName = fileName,
        Md5 = fileMd5,
        SizeInBytes = fileSize
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-7-go-tab"></a>Go<div><a id="code-code-group-7-go"></a><pre class="language-go"><code>// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &amp;bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例"></a><section><p>请求示例</p><div><a id="code-block-6"></a><pre class="language-json"><code>{
  &quot;CategoryId&quot;: &quot;default&quot;,
  &quot;FileName&quot;: &quot;阿里云百炼系列手机产品介绍.docx&quot;,
  &quot;Md5&quot;: &quot;2ef7361ea907f3a1b91e3b9936f5643a&quot;,
  &quot;SizeInBytes&quot;: &quot;14015&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例"></a><section><p>响应示例</p><div><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;RequestId&quot;: &quot;778C0B3B-59C2-5FC1-A947-36EDD1XXXXXX&quot;,
  &quot;Success&quot;: true,
  &quot;Message&quot;: &quot;&quot;,
  &quot;Code&quot;: &quot;success&quot;,
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Data&quot;: {
    &quot;FileUploadLeaseId&quot;: &quot;1e6a159107384782be5e45ac4759b247.1719325231035&quot;,
    &quot;Type&quot;: &quot;HTTP&quot;,
    &quot;Param&quot;: {
      &quot;Method&quot;: &quot;PUT&quot;,
      &quot;Url&quot;: &quot;https://bailian-datahub-data-origin-prod.oss-cn-hangzhou.aliyuncs.com/1005426495169178/10024405/68abd1dea7b6404d8f7d7b9f7fbd332d.1716698936847.pdf?Expires=1716699536&amp;OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Signature=YOUR_SIGNATURE&quot;,
      &quot;Headers&quot;: &quot;        \&quot;X-bailian-extra\&quot;: \&quot;MTAwNTQyNjQ5NTE2OTE3OA==\&quot;,\n        \&quot;Content-Type\&quot;: \&quot;application/pdf\&quot;&quot;
    }
  }
}
</code></pre></div></section></td></tr><tr><td><a id="b02222f5a73qq"></a><h4>2.2. 上传文件到临时存储</h4><p>取得上传租约后，您即可使用租约中的临时上传参数和临时上传URL，将本地存储或可通过公网访问的文件上传至阿里云百炼服务器。请注意，每个业务空间最多支持10万个文件。目前支持上传的格式包括：PDF、DOCX、DOC、TXT、Markdown、PPTX、PPT、XLSX、XLS、HTML、PNG、JPG、JPEG、BMP 和 GIF。</p><ul><li><p><strong>pre_signed_url：</strong>请传入<a href="rag-knowledge-base-api-guide.md">申请文件上传租约</a>时接口返回的<code>Data.Param.Url</code>。</p><blockquote><p>该 URL 为预签名 URL，不支持 FormData 方式上传，需使用二进制方式上传（详见示例代码）。</p></blockquote></li></ul></td><td><div><div><p><strong>重要</strong>本示例不支持在线调试和多语言示例代码生成。</p></div></div><a id="sec-tabs-2"></a><section><a id="本地上传"></a><section><a id="本地上传-h4"></a><h4>本地上传</h4><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>Python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import requests
from urllib.parse import urlparse

def upload_file(pre_signed_url, file_path):
    &quot;&quot;&quot;
    将本地文件上传至临时存储。

    参数:
        pre_signed_url (str): 上传租约中的URL。
        file_path (str): 文件本地路径。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    try:
        # 设置请求头
        headers = {
            &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
            &quot;Content-Type&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
        }

        # 读取文件并上传
        with open(file_path, 'rb') as file:
            # 下方设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            response = requests.put(pre_signed_url, data=file, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print(&quot;File uploaded successfully.&quot;)
        else:
            print(f&quot;Failed to upload the file. ResponseCode: {response.status_code}&quot;)

    except Exception as e:
        print(f&quot;An error occurred: {str(e)}&quot;)

if __name__ == &quot;__main__&quot;:

    pre_signed_url_or_http_url = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;

    # 将本地文件上传至临时存储
    file_path = &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;
    upload_file(pre_signed_url_or_http_url, file_path)
</code></pre></div><a id="fig-code-group-8-java-tab"></a>Java<div><a id="code-code-group-8-java"></a><pre class="language-java"><code>import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadFile {
    public static void uploadFile(String preSignedUrl, String filePath) {
        HttpURLConnection connection = null;
        try {
            // 创建URL对象
            URL url = new URL(preSignedUrl);
            connection = (HttpURLConnection) url.openConnection();
            // 设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            connection.setRequestMethod(&quot;PUT&quot;);
            // 允许向connection输出，因为这个连接是用于上传文件的
            connection.setDoOutput(true);
            connection.setRequestProperty(&quot;X-bailian-extra&quot;, &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;);
            connection.setRequestProperty(&quot;Content-Type&quot;, &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;);
            // 读取文件并通过连接上传
            try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                 FileInputStream fileInputStream = new FileInputStream(filePath)) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
                outStream.flush();
            }
            // 检查响应
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 文件上传成功处理
                System.out.println(&quot;File uploaded successfully.&quot;);
            } else {
                // 文件上传失败处理
                System.out.println(&quot;Failed to upload the file. ResponseCode: &quot; + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    public static void main(String[] args) {
        String preSignedUrlOrHttpUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;
        // 将本地文件上传至临时存储
        String filePath = &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;;
        uploadFile(preSignedUrlOrHttpUrl, filePath);
    }
}
</code></pre></div><a id="fig-code-group-8-php-tab"></a>PHP<div><a id="code-code-group-8-php"></a><pre class="language-php"><code>&lt;?php

/**
 * 将本地文件上传至临时存储
 *
 * @param string $preSignedUrl 从 ApplyFileUploadLease 接口获取的预签名 URL 或 HTTP 地址
 * @param array $headers 包含 &quot;X-bailian-extra&quot; 和 &quot;Content-Type&quot; 的请求头数组
 * @param string $filePath 本地文件路径
 * @throws Exception 如果上传失败
 */
function uploadFile($preSignedUrl, $headers, $filePath) {
    // 读取文件内容
    $fileContent = file_get_contents($filePath);
    if ($fileContent === false) {
        throw new Exception(&quot;无法读取文件: &quot; . $filePath);
    }

    // 初始化 cURL 会话
    $ch = curl_init();

    // 设置 cURL 选项
    curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;PUT&quot;); // 使用 PUT 方法
    curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent); // 设置请求体为文件内容
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // 返回响应结果而不是直接输出

    // 构建请求头
    $uploadHeaders = [
        &quot;X-bailian-extra: &quot; . $headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type: &quot; . $headers[&quot;Content-Type&quot;]
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $uploadHeaders);

    // 执行请求
    $response = curl_exec($ch);

    // 获取 HTTP 响应码
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // 关闭 cURL 会话
    curl_close($ch);

    // 检查响应码
    if ($httpCode != 200) {
        throw new Exception(&quot;上传失败，HTTP 状态码: &quot; . $httpCode . &quot;，错误信息: &quot; . $response);
    }

    // 上传成功
    echo &quot;File uploaded successfully.\n&quot;;
}

/**
 * 主函数：本地文件上传
 */
function main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    $preSignedUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    $headers = [
        &quot;X-bailian-extra&quot; =&gt; &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot; =&gt; &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
    ];

    // 将本地文件上传至临时存储
    $filePath = &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;;

    try {
        uploadFile($preSignedUrl, $headers, $filePath);
    } catch (Exception $e) {
        echo &quot;Error: &quot; . $e-&gt;getMessage() . &quot;\n&quot;;
    }
}

// 调用主函数
main();

?&gt;
</code></pre></div><a id="fig-code-group-8-node-js-tab"></a>Node.js<div><a id="code-code-group-8-node-js"></a><pre class="language-javascript"><code>const fs = require('fs');
const axios = require('axios');

/**
 * 将本地文件上传至临时存储
 *
 * @param {string} preSignedUrl - 上传租约中的URL
 * @param {Object} headers - 上传请求的头部
 * @param {string} filePath - 文件本地路径
 * @throws {Error} 如果上传失败
 */
async function uploadFile(preSignedUrl, headers, filePath) {
    // 构建上传所需的请求头
    const uploadHeaders = {
        &quot;X-bailian-extra&quot;: headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type&quot;: headers[&quot;Content-Type&quot;]
    };

    // 创建文件读取流
    const fileStream = fs.createReadStream(filePath);

    try {
        // 使用 axios 发送 PUT 请求
        const response = await axios.put(preSignedUrl, fileStream, {
            headers: uploadHeaders
        });

        // 检查响应状态码
        if (response.status === 200) {
            console.log(&quot;File uploaded successfully.&quot;);
        } else {
            console.error(`Failed to upload the file. ResponseCode: ${response.status}`);
            throw new Error(`Upload failed with status code: ${response.status}`);
        }
    } catch (error) {
        // 处理错误
        console.error(&quot;Error during upload:&quot;, error.message);
        throw new Error(`上传失败: ${error.message}`);
    }
}

/**
 * 主函数：本地文件上传
 */
function main() {
    const preSignedUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;

    const headers = {
        &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
    };

    // 将本地文件上传至临时存储
    const filePath = &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;;

    uploadFile(preSignedUrl, headers, filePath)
        .then(() =&gt; {
            console.log(&quot;Upload completed.&quot;);
        })
        .catch((err) =&gt; {
            console.error(&quot;Upload failed:&quot;, err.message);
        });
}

// 调用主函数
main();
</code></pre></div><a id="fig-code-group-8-c-tab"></a>C#<div><a id="code-code-group-8-c"></a><pre class="language-csharp"><code>using System;
using System.IO;
using System.Net;

public class UploadFilExample
{
    public static void UploadFile(string preSignedUrl, string filePath)
    {
        HttpWebRequest connection = null;
        try
        {
            // 创建 URL 对象
            Uri url = new Uri(preSignedUrl);
            connection = (HttpWebRequest)WebRequest.Create(url);
            // 设置请求方法用于文件上传，需与您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Method 字段的值一致
            connection.Method = &quot;PUT&quot;;
            // 允许向 connection 输出，因为这个连接是用于上传文件的
            connection.AllowWriteStreamBuffering = false;
            connection.SendChunked = false;
            // 设置请求头，需与您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中的字段值一致
            connection.Headers[&quot;X-bailian-extra&quot;] = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 X-bailian-extra 字段的值&quot;;
            connection.ContentType = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 Content-Type 字段的值（返回空值时，传空值即可）&quot;;
            // 读取文件并通过连接上传
            using (var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            using (var requestStream = connection.GetRequestStream())
            {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fileStream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    requestStream.Write(buffer, 0, bytesRead);
                }
                requestStream.Flush();
            }
            // 检查响应
            using (HttpWebResponse response = (HttpWebResponse)connection.GetResponse())
            {
                if (response.StatusCode == HttpStatusCode.OK)
                {
                    // 文件上传成功处理
                    Console.WriteLine(&quot;File uploaded successfully.&quot;);
                }
                else
                {
                    // 文件上传失败处理
                    Console.WriteLine($&quot;Failed to upload the file. ResponseCode: {response.StatusCode}&quot;);
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            e.StackTrace.ToString();
        }
        finally
        {
            if (connection != null)
            {
                connection.Abort();
            }
        }
    }

    public static void Main(string[] args)
    {
        string preSignedUrlOrHttpUrl = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值&quot;;
        // 将本地文件上传至临时存储
        string filePath = &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;;
        UploadFile(preSignedUrlOrHttpUrl, filePath);
    }
}
</code></pre></div><a id="fig-code-group-8-go-tab"></a>Go<div><a id="code-code-group-8-go"></a><pre class="language-go"><code>package main

import (
    &quot;fmt&quot;
    &quot;io&quot;
    &quot;os&quot;

    &quot;github.com/go-resty/resty/v2&quot;
)

// UploadFile 将本地文件上传至临时存储。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - error: 如果上传失败返回错误信息，否则返回 nil
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
    // 打开本地文件
    file, err := os.Open(filePath)
    if err != nil {
        return fmt.Errorf(&quot;打开文件失败: %w&quot;, err)
    }
    defer file.Close()

    // 读取内容
    body, err := io.ReadAll(file)
    if err != nil {
        return fmt.Errorf(&quot;读取文件失败: %w&quot;, err)
    }

    // 创建 REST 客户端
    client := resty.New()

    // 构建上传所需的请求头
    uploadHeaders := map[string]string{
        &quot;X-bailian-extra&quot;: headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type&quot;:    headers[&quot;Content-Type&quot;],
    }

    // 发送 PUT 请求
    resp, err := client.R().
        SetHeaders(uploadHeaders).
        SetBody(body).
        Put(preSignedUrl)

    if err != nil {
        return fmt.Errorf(&quot;发送请求失败: %w&quot;, err)
    }

    // 检查 HTTP 响应状态码
    if resp.IsError() {
        return fmt.Errorf(&quot;HTTP 错误: %d&quot;, resp.StatusCode())
    }

    fmt.Println(&quot;File uploaded successfully.&quot;)
    return nil
}

// main 主函数
func main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    preSignedUrl := &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    headers := map[string]string{
        &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot;:    &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;,
    }

    // 将本地文件上传至临时存储
    filePath := &quot;请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）&quot;

    // 调用上传函数
    err := UploadFile(preSignedUrl, headers, filePath)
    if err != nil {
        fmt.Printf(&quot;上传失败: %v\n&quot;, err)
    }
}
</code></pre></div></div></section><a id="url地址上传"></a><section><a id="url地址上传-h4"></a><h4>URL地址上传</h4><blockquote><p>请确保URL公开可访问且指向一个有效的文件。</p></blockquote><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-python-tab"></a>Python<div><a id="code-code-group-9-python"></a><pre class="language-python"><code>import requests
from urllib.parse import urlparse

def upload_file_link(pre_signed_url, source_url_string):
    &quot;&quot;&quot;
    将可通过公网访问的文件上传至临时存储。

    参数:
        pre_signed_url (str): 上传租约中的 URL。
        source_url_string (str): 文件的URL地址。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    try:
        # 设置请求头
        headers = {
            &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
            &quot;Content-Type&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
        }

        # 设置访问文件URL地址的请求方法为GET
        source_response = requests.get(source_url_string)
        if source_response.status_code != 200:
            raise RuntimeError(&quot;Failed to get source file.&quot;)

        # 下方设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
        response = requests.put(pre_signed_url, data=source_response.content, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print(&quot;File uploaded successfully.&quot;)
        else:
            print(f&quot;Failed to upload the file. ResponseCode: {response.status_code}&quot;)

    except Exception as e:
        print(f&quot;An error occurred: {str(e)}&quot;)

if __name__ == &quot;__main__&quot;:

    pre_signed_url_or_http_url = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值（返回空值时，传空值即可）&quot;

    # 文件的URL地址
    source_url = &quot;请替换为您需要上传文件的URL地址&quot;
    upload_file_link(pre_signed_url_or_http_url, source_url)
</code></pre></div><a id="fig-code-group-9-java-tab"></a>Java<div><a id="code-code-group-9-java"></a><pre class="language-java"><code>import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadFile {
    public static void uploadFileLink(String preSignedUrl, String sourceUrlString) {
        HttpURLConnection connection = null;
        try {
            // 创建URL对象
            URL url = new URL(preSignedUrl);
            connection = (HttpURLConnection) url.openConnection();
            // 设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            connection.setRequestMethod(&quot;PUT&quot;);
            // 允许向connection输出，因为这个连接是用于上传文件的
            connection.setDoOutput(true);
            connection.setRequestProperty(&quot;X-bailian-extra&quot;, &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;);
            connection.setRequestProperty(&quot;Content-Type&quot;, &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;);
            URL sourceUrl = new URL(sourceUrlString);
            HttpURLConnection sourceConnection = (HttpURLConnection) sourceUrl.openConnection();
            // 设置访问文件URL地址的请求方法为GET
            sourceConnection.setRequestMethod(&quot;GET&quot;);
            // 获取响应码，200表示请求成功
            int sourceFileResponseCode = sourceConnection.getResponseCode();
            // 从URL地址读取文件并通过连接上传
            if (sourceFileResponseCode != HttpURLConnection.HTTP_OK) {
                throw new RuntimeException(&quot;Failed to get source file.&quot;);
            }
            try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                 InputStream in = new BufferedInputStream(sourceConnection.getInputStream())) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = in.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
                outStream.flush();
            }
            // 检查响应
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 文件上传成功
                System.out.println(&quot;File uploaded successfully.&quot;);
            } else {
                // 文件上传失败
                System.out.println(&quot;Failed to upload the file. ResponseCode: &quot; + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    public static void main(String[] args) {
        String preSignedUrlOrHttpUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;

        String sourceUrl = &quot;请替换为您需要上传文件的URL地址&quot;;
        uploadFileLink(preSignedUrlOrHttpUrl, sourceUrl);
    }
}
</code></pre></div><a id="fig-code-group-9-php-tab"></a>PHP<div><a id="code-code-group-9-php"></a><pre class="language-php"><code>&lt;?php

/**
 * 将可通过公网访问的文件上传至临时存储
 *
 * @param string $preSignedUrl 从 ApplyFileUploadLease 接口获取的预签名 URL 或 HTTP 地址
 * @param array $headers 包含 &quot;X-bailian-extra&quot; 和 &quot;Content-Type&quot; 的请求头数组
 * @param string $sourceUrl 文件的URL地址
 * @throws Exception 如果上传失败
 */
function uploadFile($preSignedUrl, $headers, $sourceUrl) {

    $fileContent = file_get_contents($sourceUrl);
    if ($fileContent === false) {
        throw new Exception(&quot;无法从给定的URL地址下载文件: &quot; . $sourceUrl);
    }
    // 初始化 cURL 会话
    $ch = curl_init();

    // 设置 cURL 选项
    curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;PUT&quot;); // 使用 PUT 方法
    curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent); // 设置请求体为文件内容
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // 返回响应结果而不是直接输出

    // 构建请求头
    $uploadHeaders = [
        &quot;X-bailian-extra: &quot; . $headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type: &quot; . $headers[&quot;Content-Type&quot;]
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $uploadHeaders);

    // 执行请求
    $response = curl_exec($ch);

    // 获取 HTTP 响应码
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // 关闭 cURL 会话
    curl_close($ch);

    // 检查响应码
    if ($httpCode != 200) {
        throw new Exception(&quot;上传失败，HTTP 状态码: &quot; . $httpCode . &quot;，错误信息: &quot; . $response);
    }

    // 上传成功
    echo &quot;File uploaded successfully.\n&quot;;
}

/**
 * 主函数：将可通过公网访问的文件上传至临时存储
 */
function main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    $preSignedUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    $headers = [
        &quot;X-bailian-extra&quot; =&gt; &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot; =&gt; &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
    ];

    $sourceUrl = &quot;请替换为您需要上传文件的URL地址&quot;;

    try {
        uploadFile($preSignedUrl, $headers, $sourceUrl);
    } catch (Exception $e) {
        echo &quot;Error: &quot; . $e-&gt;getMessage() . &quot;\n&quot;;
    }
}

// 调用主函数
main();

?&gt;
</code></pre></div><a id="fig-code-group-9-node-js-tab"></a>Node.js<div><a id="code-code-group-9-node-js"></a><pre class="language-javascript"><code>const axios = require('axios');

/**
 * 将可通过公网访问的文件上传至临时存储
 *
 * @param {string} preSignedUrl - 上传租约中的URL
 * @param {Object} headers - 上传请求的头部
 * @param {string} sourceUrl - 文件的URL地址
 * @throws {Error} 如果上传失败
 */
async function uploadFileFromUrl(preSignedUrl, headers, sourceUrl) {
    // 构建上传所需的请求头
    const uploadHeaders = {
        &quot;X-bailian-extra&quot;: headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type&quot;: headers[&quot;Content-Type&quot;]
    };

    try {
        // 从给定的URL地址下载文件
        const response = await axios.get(sourceUrl, {
            responseType: 'stream'
        });

        // 使用 axios 发送 PUT 请求
        const uploadResponse = await axios.put(preSignedUrl, response.data, {
            headers: uploadHeaders
        });

        // 检查响应状态码
        if (uploadResponse.status === 200) {
            console.log(&quot;File uploaded successfully from URL.&quot;);
        } else {
            console.error(`Failed to upload the file. ResponseCode: ${uploadResponse.status}`);
            throw new Error(`Upload failed with status code: ${uploadResponse.status}`);
        }
    } catch (error) {
        // 处理错误
        console.error(&quot;Error during upload:&quot;, error.message);
        throw new Error(`上传失败: ${error.message}`);
    }
}

/**
 * 主函数：将一个可公开直接下载的文件上传到临时存储
 */
function main() {
    const preSignedUrl = &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;;

    const headers = {
        &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;
    };

    const sourceUrl = &quot;请替换为您需要上传文件的URL地址&quot;;

    uploadFileFromUrl(preSignedUrl, headers, sourceUrl)
        .then(() =&gt; {
            console.log(&quot;Upload completed.&quot;);
        })
        .catch((err) =&gt; {
            console.error(&quot;Upload failed:&quot;, err.message);
        });
}

// 调用主函数
main();
</code></pre></div><a id="fig-code-group-9-c-tab"></a>C#<div><a id="code-code-group-9-c"></a><pre class="language-csharp"><code>using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class UploadFileExample
{
    public static async Task UploadFileFromUrl(string preSignedUrl, string url)
    {
        try
        {
            // 创建 HTTP 客户端从给定的URL地址下载文件
            using (HttpClient httpClient = new HttpClient())
            {
                HttpResponseMessage response = await httpClient.GetAsync(url, HttpCompletionOption.ResponseHeadersRead);
                response.EnsureSuccessStatusCode();

                // 获取文件流
                using (Stream fileStream = await response.Content.ReadAsStreamAsync())
                {
                    // 创建 URL 对象
                    Uri urlObj = new Uri(preSignedUrl);
                    HttpWebRequest connection = (HttpWebRequest)WebRequest.Create(urlObj);

                    // 设置请求方法用于文件上传
                    connection.Method = &quot;PUT&quot;;
                    connection.AllowWriteStreamBuffering = false;
                    connection.SendChunked = false;

                    // 设置请求头（请替换为实际值）
                    connection.Headers[&quot;X-bailian-extra&quot;] = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 X-bailian-extra 字段的值&quot;;
                    connection.ContentType = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 Content-Type 字段的值（返回空值时，传空值即可）&quot;;

                    // 获取请求流并写入文件流
                    using (Stream requestStream = connection.GetRequestStream())
                    {
                        byte[] buffer = new byte[4096];
                        int bytesRead;
                        while ((bytesRead = await fileStream.ReadAsync(buffer, 0, buffer.Length)) &gt; 0)
                        {
                            await requestStream.WriteAsync(buffer, 0, bytesRead);
                        }
                        await requestStream.FlushAsync();
                    }

                    // 检查响应
                    using (HttpWebResponse responseResult = (HttpWebResponse)connection.GetResponse())
                    {
                        if (responseResult.StatusCode == HttpStatusCode.OK)
                        {
                            Console.WriteLine(&quot;File uploaded successfully from URL.&quot;);
                        }
                        else
                        {
                            Console.WriteLine($&quot;Failed to upload the file. ResponseCode: {responseResult.StatusCode}&quot;);
                        }
                    }
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            Console.WriteLine(e.StackTrace);
        }
    }

    public static async Task Main(string[] args)
    {
        string preSignedUrlOrHttpUrl = &quot;请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值&quot;;
        string url = &quot;请替换为您需要上传文件的URL地址&quot;;

        await UploadFileFromUrl(preSignedUrlOrHttpUrl, url);
    }
}
</code></pre></div><a id="fig-code-group-9-go-tab"></a>Go<div><a id="code-code-group-9-go"></a><pre class="language-go"><code>package main

import (
    &quot;fmt&quot;
    &quot;net/http&quot;

    &quot;github.com/go-resty/resty/v2&quot;
)

// UploadFileFromUrl 将可通过公网访问的文件上传至临时存储。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - sourceUrl (string): 文件的URL地址。
//
// 返回:
//   - error: 如果上传失败返回错误信息，否则返回 nil
func UploadFileFromUrl(preSignedUrl string, headers map[string]string, sourceUrl string) error {
    // 从给定的URL地址下载文件
    resp, err := http.Get(sourceUrl)
    if err != nil {
        return fmt.Errorf(&quot;获取文件失败: %w&quot;, err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf(&quot;获取文件失败，状态码: %d&quot;, resp.StatusCode)
    }

    // 创建 REST 客户端
    client := resty.New()

    // 构建上传所需的请求头
    uploadHeaders := map[string]string{
        &quot;X-bailian-extra&quot;: headers[&quot;X-bailian-extra&quot;],
        &quot;Content-Type&quot;:    headers[&quot;Content-Type&quot;],
    }

    // 发送 PUT 请求
    response, err := client.R().
        SetHeaders(uploadHeaders).
        SetBody(resp.Body).
        Put(preSignedUrl)

    if err != nil {
        return fmt.Errorf(&quot;发送请求失败: %w&quot;, err)
    }

    if err != nil {
        return fmt.Errorf(&quot;发送请求失败: %w&quot;, err)
    }

    // 检查 HTTP 响应状态码
    if response.IsError() {
        return fmt.Errorf(&quot;HTTP 错误: %d&quot;, response.StatusCode())
    }

    fmt.Println(&quot;File uploaded successfully from URL.&quot;)
    return nil
}

// main 主函数
func main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    preSignedUrl := &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值&quot;

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    headers := map[string]string{
        &quot;X-bailian-extra&quot;: &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值&quot;,
        &quot;Content-Type&quot;:    &quot;请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）&quot;,
    }

    sourceUrl := &quot;请替换为您需要上传文件的URL地址&quot;

    // 调用上传函数
    err := UploadFileFromUrl(preSignedUrl, headers, sourceUrl)
    if err != nil {
        fmt.Printf(&quot;上传失败: %v\n&quot;, err)
    }
}
</code></pre></div></div></section></section></td></tr><tr><td><a id="50a3954544lxk"></a><h4>2.3. 添加文件到类目中</h4><p>阿里云百炼使用类目管理您上传的文件。因此，接下来您需要调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile">AddFile接口</a>将已上传的文件添加到同一业务空间下的类目中。</p><ul><li><p><strong>parser：</strong>请传入<code>DASHSCOPE_DOCMIND</code>。</p></li><li><p><strong>lease_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">申请文件上传租约</a>时接口返回的<code>Data.FileUploadLeaseId</code>。</p></li><li><p><strong>category_id：</strong>本示例中，请传入<code>default</code>。若您使用了自建类目上传，则需传入对应的<code>category_id</code>。</p><div><div><p><strong>重要</strong>请确保此处传入的<code>CategoryId</code>与<a href="rag-knowledge-base-api-guide.md">申请文件上传租约</a>步骤中使用的<code>CategoryId</code>保持一致，否则会出现<code>Category is mismatched</code>错误。</p></div></div></li></ul><p>完成添加后，阿里云百炼将返回该文件的<code>FileId</code>，并自动开始解析您的文件。同时<code>lease_id</code>（租约ID）随即失效，<strong>请勿再使用相同的租约ID重复提交</strong>。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/AddFile">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/AddFile?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-10"></a><div><a id="fig-code-group-10-python-tab"></a>Python<div><a id="code-code-group-10-python"></a><pre class="language-python"><code>def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    &quot;&quot;&quot;
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-10-java-tab"></a>Java<div><a id="code-code-group-10-java"></a><pre class="language-java"><code>/**
 * 将文件添加到类目中。
 *
 * @param client      客户端对象
 * @param leaseId     租约ID
 * @param parser      用于文件的解析器
 * @param categoryId  类目ID
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应对象
 */
public AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
    addFileRequest.setLeaseId(leaseId);
    addFileRequest.setParser(parser);
    addFileRequest.setCategoryId(categoryId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-10-php-tab"></a>PHP<div><a id="code-code-group-10-php"></a><pre class="language-php"><code>/**
 * 将文件添加到类目中。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $leaseId 租约ID。
 * @param string $parser 用于文件的解析器。
 * @param string $categoryId 类目ID。
 * @param string $workspaceId 业务空间ID。
 * @return AddFileResponse 阿里云百炼服务的响应。
 */
public function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
    $headers = [];
    $addFileRequest = new AddFileRequest([
        &quot;leaseId&quot; =&gt; $leaseId,
        &quot;parser&quot; =&gt; $parser,
        &quot;categoryId&quot; =&gt; $categoryId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-10-node-js-tab"></a>Node.js<div><a id="code-code-group-10-node-js"></a><pre class="language-javascript"><code>/**
 * 添加文件到类目中
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} leaseId - 租约ID
 * @param {string} parser - 用于文件的解析器
 * @param {string} categoryId - 类目ID
 * @param {string} workspaceId - 业务空间ID
 * @returns {Promise&lt;bailian20231229.AddFileResponse&gt;} - 阿里云百炼服务的响应
 */
async function addFile(client, leaseId, parser, categoryId, workspaceId) {
 const headers = {};
 const req = new bailian20231229.AddFileRequest({
  leaseId,
  parser,
  categoryId
});
 const runtime = new Util.RuntimeOptions({});
 return await client.addFileWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-10-c-tab"></a>C#<div><a id="code-code-group-10-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 将文件添加到类目中。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;leaseId&quot;&gt;租约ID&lt;/param&gt;
/// &lt;param name=&quot;parser&quot;&gt;用于文件的解析器&lt;/param&gt;
/// &lt;param name=&quot;categoryId&quot;&gt;类目ID&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string leaseId,
    string parser,
    string categoryId,
    string workspaceId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
    {
        LeaseId = leaseId,
        Parser = parser,
        CategoryId = categoryId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-10-go-tab"></a>Go<div><a id="code-code-group-10-go"></a><pre class="language-go"><code>// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &amp;bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-2"></a><section><p>请求示例</p><div><a id="code-block-8"></a><pre class="language-json"><code>{
  &quot;CategoryId&quot;: &quot;default&quot;,
  &quot;LeaseId&quot;: &quot;d92bd94fa9b54326a2547415e100c9e2.1742195250069&quot;,
  &quot;Parser&quot;: &quot;DASHSCOPE_DOCMIND&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-2"></a><section><p>响应示例</p><div><a id="code-block-9"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;&quot;,
  &quot;RequestId&quot;: &quot;5832A1F4-AF91-5242-8B75-35BDC9XXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;FileId&quot;: &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;,
    &quot;Parser&quot;: &quot;DASHSCOPE_DOCMIND&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td><a id="42b2686d1d0jz"></a><h4>2.4. 查询文件的解析状态</h4><p>未解析完成的文件无法用于知识库，在请求高峰时段，该过程可能需要数小时。您可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-describefile">DescribeFile接口</a>查询文件的解析状态。</p><ul><li><strong>file_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">添加文件到类目中</a>时接口返回的<code>FileId</code>。</li></ul><p>当本接口返回的<code>Data.Status</code>字段值为<code>PARSE_SUCCESS</code>时，表示文件已解析完成，可以将其导入知识库。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess或AliyunBailianDataReadOnlyAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-11"></a><div><a id="fig-code-group-11-python-tab"></a>Python<div><a id="code-code-group-11-python"></a><pre class="language-python"><code>def describe_file(client, workspace_id, file_id):
    &quot;&quot;&quot;
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)
</code></pre></div><a id="fig-code-group-11-java-tab"></a>Java<div><a id="code-code-group-11-java"></a><pre class="language-java"><code>/**
 * 查询文件的基本信息。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param fileId      文件ID
 * @return 阿里云百炼服务的响应对象
 */
public DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
}
</code></pre></div><a id="fig-code-group-11-php-tab"></a>PHP<div><a id="code-code-group-11-php"></a><pre class="language-php"><code>/**
 * 查询文件的基本信息。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $fileId 文件ID。
 * @return DescribeFileResponse 阿里云百炼服务的响应。
 */
public function describeFile($client, $workspaceId, $fileId) {
    $headers = [];
    $runtime = new RuntimeOptions([]);
    return $client-&gt;describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-11-node-js-tab"></a>Node.js<div><a id="code-code-group-11-node-js"></a><pre class="language-javascript"><code>/**
 * 查询文件的解析状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} fileId - 文件ID
 * @returns {Promise&lt;bailian20231229.DescribeFileResponse&gt;} - 阿里云百炼服务的响应
 */
async function describeFile(client, workspaceId, fileId) {
 const headers = {};
 const runtime = new Util.RuntimeOptions({});
 return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
}
</code></pre></div><a id="fig-code-group-11-c-tab"></a>C#<div><a id="code-code-group-11-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 查询文件的基本信息。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;fileId&quot;&gt;文件ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string fileId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
}
</code></pre></div><a id="fig-code-group-11-go-tab"></a>Go<div><a id="code-code-group-11-go"></a><pre class="language-go"><code>// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - any: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &amp;util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-3"></a><section><p>请求示例</p><div><a id="code-block-10"></a><pre class="language-json"><code>{
  &quot;FileId&quot;: &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-3"></a><section><p>响应示例</p><div><a id="code-block-11"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;&quot;,
  &quot;RequestId&quot;: &quot;B9246251-987A-5628-8E1E-17BB39XXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;CategoryId&quot;: &quot;cate_206ea350f0014ea4a324adff1ca13011_10xxxxxx&quot;,
    &quot;Status&quot;: &quot;PARSE_SUCCESS&quot;,
    &quot;FileType&quot;: &quot;docx&quot;,
    &quot;CreateTime&quot;: &quot;2025-03-17 15:47:13&quot;,
    &quot;FileName&quot;: &quot;阿里云百炼系列手机产品介绍.docx&quot;,
    &quot;FileId&quot;: &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;,
    &quot;SizeInBytes&quot;: &quot;14015&quot;,
    &quot;Parser&quot;: &quot;DASHSCOPE_DOCMIND&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td colspan="2"><a id="64381d8463c79"></a><h3>3. 创建知识库</h3></td></tr><tr><td><a id="8b13d5395ftzn"></a><h4>3.1. 初始化知识库</h4><p>文件解析完成后，您即可将其导入同一业务空间下的知识库。初始化（非最终提交）一个文档搜索类知识库，可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex">CreateIndex接口</a>。</p><ul><li><p><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></p></li><li><p><strong>file_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">添加文件到类目中</a>时接口返回的<code>FileId</code>。</p><blockquote><p>若source_type为<code>DATA_CENTER_FILE</code>，则该参数为必传，否则接口将报错。</p></blockquote></li><li><p><strong>structure_type：</strong>本示例中，请传入<code>unstructured</code>。</p></li><li><p><strong>source_type：</strong>本示例中，请传入<code>DATA_CENTER_FILE</code>。</p></li><li><p><strong>sink_type：</strong>本示例中，请传入<code>BUILT_IN</code>。</p></li></ul><p>本接口返回的<code>Data.Id</code>字段值即为知识库ID，用于后续的索引构建。</p><blockquote><p>请您妥善保管知识库ID，后续该知识库所有相关API操作都将用到它。</p></blockquote></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-12"></a><div><a id="fig-code-group-12-python-tab"></a>Python<div><a id="code-code-group-12-python"></a><pre class="language-python"><code>def create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type):
    &quot;&quot;&quot;
    在阿里云百炼服务中创建知识库（初始化）。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。
        name (str): 知识库名称。
        structure_type (str): 知识库的数据类型。
        source_type (str): 应用数据的数据类型，支持类目类型和文件类型。
        sink_type (str): 知识库的向量存储类型。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        name=name,
        source_type=source_type,
        sink_type=sink_type,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.create_index_with_options(workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-12-java-tab"></a>Java<div><a id="code-code-group-12-java"></a><pre class="language-java"><code>/**
 * 在阿里云百炼服务中创建知识库（初始化）。
 *
 * @param client        客户端对象
 * @param workspaceId   业务空间ID
 * @param fileId        文件ID
 * @param name          知识库名称
 * @param structureType 知识库的数据类型
 * @param sourceType    应用数据的数据类型，支持类目类型和文件类型
 * @param sinkType      知识库的向量存储类型
 * @return 阿里云百炼服务的响应对象
 */
public CreateIndexResponse createIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId, String name, String structureType, String sourceType, String sinkType) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.CreateIndexRequest createIndexRequest = new com.aliyun.bailian20231229.models.CreateIndexRequest();
    createIndexRequest.setStructureType(structureType);
    createIndexRequest.setName(name);
    createIndexRequest.setSourceType(sourceType);
    createIndexRequest.setSinkType(sinkType);
    createIndexRequest.setDocumentIds(Collections.singletonList(fileId));
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.createIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-12-php-tab"></a>PHP<div><a id="code-code-group-12-php"></a><pre class="language-php"><code>/**
 * 在阿里云百炼服务中创建知识库（初始化）。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $fileId 文件ID。
 * @param string $name 知识库名称。
 * @param string $structureType 知识库的数据类型。
 * @param string $sourceType 应用数据的数据类型，支持类目类型和文件类型。
 * @param string $sinkType 知识库的向量存储类型。
 * @return CreateIndexResponse 阿里云百炼服务的响应。
 */
public function createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType) {
    $headers = [];
    $createIndexRequest = new CreateIndexRequest([
        &quot;structureType&quot; =&gt; $structureType,
        &quot;name&quot; =&gt; $name,
        &quot;sourceType&quot; =&gt; $sourceType,
        &quot;documentIds&quot; =&gt; [
            $fileId
        ],
        &quot;sinkType&quot; =&gt; $sinkType
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;createIndexWithOptions($workspaceId, $createIndexRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-12-node-js-tab"></a>Node.js<div><a id="code-code-group-12-node-js"></a><pre class="language-javascript"><code>/**
 * 初始化知识库（索引）
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} fileId - 文件ID
 * @param {string} name - 知识库名称
 * @param {string} structureType - 知识库的数据类型
 * @param {string} sourceType - 应用数据的数据类型，支持类目类型和文件类型
 * @param {string} sinkType - 知识库的向量存储类型
 * @returns {Promise&lt;bailian20231229.CreateIndexResponse&gt;} - 阿里云百炼服务的响应
 */
async function createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType) {
 const headers = {};
 const req = new bailian20231229.CreateIndexRequest({
   name,
   structureType,
   documentIds: [fileId],
   sourceType,
   sinkType
 });
 const runtime = new Util.RuntimeOptions({});
 return await client.createIndexWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-12-c-tab"></a>C#<div><a id="code-code-group-12-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 在阿里云百炼服务中创建知识库（初始化）。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;fileId&quot;&gt;文件ID&lt;/param&gt;
/// &lt;param name=&quot;name&quot;&gt;知识库名称&lt;/param&gt;
/// &lt;param name=&quot;structureType&quot;&gt;知识库的数据类型&lt;/param&gt;
/// &lt;param name=&quot;sourceType&quot;&gt;应用数据的数据类型，支持类目类型和文件类型&lt;/param&gt;
/// &lt;param name=&quot;sinkType&quot;&gt;知识库的向量存储类型&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexResponse CreateIndex(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string fileId,
    string name,
    string structureType,
    string sourceType,
    string sinkType)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var createIndexRequest = new AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexRequest
    {
        StructureType = structureType,
        Name = name,
        SourceType = sourceType,
        SinkType = sinkType,
        DocumentIds = new List&lt;string&gt; { fileId }
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.CreateIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-12-go-tab"></a>Go<div><a id="code-code-group-12-go"></a><pre class="language-go"><code>// CreateIndex 在阿里云百炼服务中创建知识库（初始化）。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//   - name (string): 知识库名称。
//   - structureType (string): 知识库的数据类型。
//   - sourceType (string): 应用数据的数据类型，支持类目类型和文件类型。
//   - sinkType (string): 知识库的向量存储类型。
//
// 返回:
//   - *bailian20231229.CreateIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func CreateIndex(client *bailian20231229.Client, workspaceId, fileId, name, structureType, sourceType, sinkType string) (_result *bailian20231229.CreateIndexResponse, _err error) {
	headers := make(map[string]*string)
	createIndexRequest := &amp;bailian20231229.CreateIndexRequest{
		StructureType: tea.String(structureType),
		Name:          tea.String(name),
		SourceType:    tea.String(sourceType),
		SinkType:      tea.String(sinkType),
		DocumentIds:   []*string{tea.String(fileId)},
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.CreateIndexWithOptions(tea.String(workspaceId), createIndexRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-4"></a><section><p>请求示例</p><div><a id="code-block-12"></a><pre class="language-json"><code>{
  &quot;Name&quot;: &quot;阿里云百炼手机知识库&quot;,
  &quot;SinkType&quot;: &quot;BUILT_IN&quot;,
  &quot;SourceType&quot;: &quot;DATA_CENTER_FILE&quot;,
  &quot;StructureType&quot;: &quot;unstructured&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;,
  &quot;DocumentIds&quot;: [
    &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;
  ]
}
</code></pre></div></section><a id="accordion-响应示例-4"></a><section><p>响应示例</p><div><a id="code-block-13"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;RequestId&quot;: &quot;87CB0999-F1BB-5290-8C79-A875B2XXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;Id&quot;: &quot;mymxbdxxxx&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td><a id="80bd94fddaky3"></a><h4>3.2. 提交索引任务</h4><p>初始化知识库后，您需要调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexjob">SubmitIndexJob接口</a>提交索引任务，以启动知识库的索引构建。</p><ul><li><strong>index_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">初始化知识库</a>时接口返回的<code>Data.Id</code>。</li></ul><p>完成提交后，阿里云百炼随即以异步任务方式开始构建索引。本接口返回的<code>Data.Id</code>为对应的任务ID。下一步中，您将用到此ID查询任务的最新状态。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-13"></a><div><a id="fig-code-group-13-python-tab"></a>Python<div><a id="code-code-group-13-python"></a><pre class="language-python"><code>def submit_index(client, workspace_id, index_id):
    &quot;&quot;&quot;
    向阿里云百炼服务提交索引任务。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)
</code></pre></div><a id="fig-code-group-13-java-tab"></a>Java<div><a id="code-code-group-13-java"></a><pre class="language-java"><code>/**
 * 向阿里云百炼服务提交索引任务。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public SubmitIndexJobResponse submitIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.SubmitIndexJobRequest submitIndexJobRequest = new com.aliyun.bailian20231229.models.SubmitIndexJobRequest();
    submitIndexJobRequest.setIndexId(indexId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.submitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-13-php-tab"></a>PHP<div><a id="code-code-group-13-php"></a><pre class="language-php"><code>/**
 * 向阿里云百炼服务提交索引任务。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @return SubmitIndexJobResponse 阿里云百炼服务的响应。
 */
public static function submitIndex($client, $workspaceId, $indexId) {
    $headers = [];
    $submitIndexJobRequest = new SubmitIndexJobRequest([
        'indexId' =&gt; $indexId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;submitIndexJobWithOptions($workspaceId, $submitIndexJobRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-13-node-js-tab"></a>Node.js<div><a id="code-code-group-13-node-js"></a><pre class="language-javascript"><code>/**
 * 提交索引任务
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise&lt;bailian20231229.SubmitIndexJobResponse&gt;} - 阿里云百炼服务的响应
 */
async function submitIndex(client, workspaceId, indexId) {
  const headers = {};
  const req = new bailian20231229.SubmitIndexJobRequest({ indexId });
  const runtime = new Util.RuntimeOptions({});
  return await client.submitIndexJobWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-13-c-tab"></a>C#<div><a id="code-code-group-13-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 向阿里云百炼服务提交索引任务。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobResponse SubmitIndex(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var submitIndexJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobRequest
    {
           IndexId = indexId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.SubmitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-13-go-tab"></a>Go<div><a id="code-code-group-13-go"></a><pre class="language-go"><code>// SubmitIndex 提交索引任务。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.SubmitIndexJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.SubmitIndexJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexJobRequest := &amp;bailian20231229.SubmitIndexJobRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.SubmitIndexJobWithOptions(tea.String(workspaceId), submitIndexJobRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-5"></a><section><p>请求示例</p><div><a id="code-block-14"></a><pre class="language-json"><code>{
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-5"></a><section><p>响应示例</p><div><a id="code-block-15"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;RequestId&quot;: &quot;7774575F-571D-5854-82C2-634AB8XXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
    &quot;Id&quot;: &quot;3cd6fb57aaf44cd0b4dd2ca584xxxxxx&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td><a id="d10e2d1ab03wa"></a><h4>3.3. 等待索引任务完成</h4><p>索引任务的执行需要一定时间，在请求高峰时段，该过程可能需要数小时。查询其执行状态可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus">GetIndexJobStatus接口</a>。</p><ul><li><strong>job_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">提交索引任务</a>时接口返回的<code>Data.Id</code>。</li></ul><p>当本接口返回的<code>Data.Status</code>字段值为<code>COMPLETED</code>时，表示知识库已创建完成。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-14"></a><div><a id="fig-code-group-14-python-tab"></a>Python<div><a id="code-code-group-14-python"></a><pre class="language-python"><code>def get_index_job_status(client, workspace_id, index_id, job_id):
    &quot;&quot;&quot;
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)
</code></pre></div><a id="fig-code-group-14-java-tab"></a>Java<div><a id="code-code-group-14-java"></a><pre class="language-java"><code>/**
 * 查询索引任务状态。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param jobId       任务ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
    getIndexJobStatusRequest.setIndexId(indexId);
    getIndexJobStatusRequest.setJobId(jobId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    GetIndexJobStatusResponse getIndexJobStatusResponse = null;
    getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
    return getIndexJobStatusResponse;
}
</code></pre></div><a id="fig-code-group-14-php-tab"></a>PHP<div><a id="code-code-group-14-php"></a><pre class="language-php"><code>/**
 * 查询索引任务状态。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @param string $jobId 任务ID。
 * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
 */
public function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
    $headers = [];
    $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
        'indexId' =&gt; $indexId,
        'jobId' =&gt; $jobId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-14-node-js-tab"></a>Node.js<div><a id="code-code-group-14-node-js"></a><pre class="language-javascript"><code>/**
 * 查询索引任务状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} jobId - 任务ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise&lt;bailian20231229.GetIndexJobStatusResponse&gt;} - 阿里云百炼服务的响应
 */
async function getIndexJobStatus(client, workspaceId, jobId, indexId) {
  const headers = {};
  const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
  const runtime = new Util.RuntimeOptions({});
  return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-14-c-tab"></a>C#<div><a id="code-code-group-14-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 查询索引任务状态。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;jobId&quot;&gt;任务ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string jobId,
    string indexId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
    {
        IndexId = indexId,
        JobId = jobId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-14-go-tab"></a>Go<div><a id="code-code-group-14-go"></a><pre class="language-go"><code>// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &amp;bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-6"></a><section><p>请求示例</p><div><a id="code-block-16"></a><pre class="language-json"><code>{
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;JobId&quot;: &quot;3cd6fb57aaf44cd0b4dd2ca584xxxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-6"></a><section><p>响应示例</p><div><a id="code-block-17"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;RequestId&quot;: &quot;E83423B9-7D6D-5283-836B-CF7EAEXXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;Status&quot;: &quot;COMPLETED&quot;,
    &quot;Documents&quot;: [
      {
        &quot;Status&quot;: &quot;FINISH&quot;,
        &quot;DocId&quot;: &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;,
        &quot;Message&quot;: &quot;导入成功&quot;,
        &quot;DocName&quot;: &quot;阿里云百炼系列手机产品介绍&quot;,
        &quot;Code&quot;: &quot;FINISH&quot;
      }
    ],
    &quot;JobId&quot;: &quot;3cd6fb57aaf44cd0b4dd2ca584xxxxxx&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr></tbody></table>

通过以上步骤，您已成功创建了一个知识库，并包含了需要上传的文件。

<a id="检索知识库-2"></a>

<a id="fa1aa9ede9zck"></a>

## 检索知识库

目前，检索知识库支持以下方式：

-   **使用阿里云百炼应用：**[调用应用](https://help.aliyun.com/zh/model-studio/application-calling-guide)时，通过`rag_options`传入知识库ID`index_id`，为您的大模型应用补充私有知识和提供最新信息。
-   **使用阿里云API：**调用[Retrieve接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)在指定的知识库中检索信息并返回原始文本切片。
-   **使用知识检索服务（推荐）：**调用[Search接口](../../application-api-reference/rag-api/knowledge/knowledgesearch.md)跨多个知识库执行联合语义检索，返回按相关性排序的文本切片。检索策略预先在控制台配置并发布，调用方只需传入检索意图（`query`/`images`）与`agent_id`。

三者的区别在于：第一种方式先将检索到的相关文本切片传给您配置的大模型，模型再结合这些切片与用户的原始查询生成最终回答并返回；后两种方式则是直接返回文本切片。其中**知识检索服务（Search接口）**为推荐方式，支持跨多库联合检索与多模态检索，且检索策略在控制台统一配置管理，无需在请求中维护。

接下来为您介绍**使用知识检索服务（Search接口）**的方式。

<table><tbody><tr><td><p>跨多个知识库执行联合语义检索，返回按相关性排序的文本切片，可以通过调用<a href="../../application-api-reference/rag-api/knowledge/knowledgesearch.md">Search接口</a>。</p><ul><li><p><strong>agent_id：</strong>知识检索服务（agent）实例 ID。在控制台<a href="https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list">知识检索服务页面</a>创建并发布后获取。</p></li><li><p><strong>API Key：</strong>阿里云百炼 API Key。在控制台<a href="https://bailian.console.aliyun.com/?tab=model#/api-key">API Key 页面</a>获取。</p></li><li><p><strong>workspace_id：</strong>知识库所在的业务空间，用于拼接 Base URL（<code>https://{workspaceId}.cn-beijing.maas.aliyuncs.com</code>）。在控制台<a href="https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management">业务空间管理</a>获取。</p><blockquote><p>子账号只能检索自己<a href="https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users">已加入的业务空间</a>中的知识库。</p></blockquote></li></ul><p>检索策略（多库权重、知识路由、混排模型等）预先在控制台配置进服务实例并发布，调用方只需传入检索意图（<code>query</code>/<code>images</code>）与<code>agent_id</code>，无需在请求中维护检索策略参数。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>调用前须在百炼控制台<a href="https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list">知识检索服务页面</a>创建并发布知识检索服务（agent），获取服务 ID（<code>agent_id</code>）。未发布时返回 Agent 未发布错误。</li><li>默认用户维度 25 QPS。如遇限流，请稍后重试。</li></ul></div></div><a id="fig-code-group-15"></a><div><a id="fig-code-group-15-curl-tab"></a>cURL<div><a id="code-code-group-15-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;agent_id&quot;: &quot;aid-xxxxxxxxxxxxxxxx&quot;,
    &quot;query&quot;: &quot;请介绍一下阿里云百炼手机X1。&quot;,
    &quot;images&quot;: []
  }'
</code></pre></div><a id="fig-code-group-15-python-tab"></a>Python<div><a id="code-code-group-15-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    &quot;https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search&quot;,
    headers={
        &quot;Authorization&quot;: f&quot;Bearer {os.getenv('DASHSCOPE_API_KEY')}&quot;,
        &quot;Content-Type&quot;: &quot;application/json&quot;,
    },
    json={
        &quot;agent_id&quot;: &quot;aid-xxxxxxxxxxxxxxxx&quot;,
        &quot;query&quot;: &quot;请介绍一下阿里云百炼手机X1。&quot;,
        &quot;images&quot;: [],
    },
)
print(resp.json())
</code></pre></div></div><a id="accordion-请求示例-7"></a><section><p>请求示例</p><div><a id="code-block-18"></a><pre class="language-json"><code>{
  &quot;agent_id&quot;: &quot;aid-xxxxxxxxxxxxxxxx&quot;,
  &quot;query&quot;: &quot;请介绍一下阿里云百炼手机X1。&quot;,
  &quot;images&quot;: []
}
</code></pre></div></section><a id="accordion-响应示例-7"></a><section><p>响应示例</p><div><a id="code-block-19"></a><pre class="language-json"><code>{
  &quot;code&quot;: &quot;Success&quot;,
  &quot;status_code&quot;: 200,
  &quot;status&quot;: &quot;SUCCESS&quot;,
  &quot;success&quot;: true,
  &quot;message&quot;: &quot;success&quot;,
  &quot;request_id&quot;: &quot;xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&quot;,
  &quot;data&quot;: {
    &quot;total&quot;: 3,
    &quot;nodes&quot;: [
      {
        &quot;score&quot;: 0.9201,
        &quot;text&quot;: &quot;阿里云百炼手机产品介绍阿里云百炼 X1 ——畅享极致视界：搭载 6.7英寸 1440 x 3200像素超清屏幕，搭配 120Hz刷新率，流畅视觉体验跃然眼前。256GB海量存储空间与 12GB RAM强强联合，无论是大型游戏还是多任务处理，都能轻松应对。5000mAh电池长续航，加上超感光四摄系统，记录生活每一刻精彩。参考售价：4599- 4999&quot;,
        &quot;metadata&quot;: {
          &quot;doc_id&quot;: &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;,
          &quot;doc_name&quot;: &quot;阿里云百炼系列手机产品介绍&quot;,
          &quot;title&quot;: &quot;阿里云百炼手机产品介绍&quot;,
          &quot;content&quot;: &quot;阿里云百炼手机产品介绍阿里云百炼 X1 ——畅享极致视界：搭载 6.7英寸 1440 x 3200像素超清屏幕，搭配 120Hz刷新率，流畅视觉体验跃然眼前。256GB海量存储空间与 12GB RAM强强联合，无论是大型游戏还是多任务处理，都能轻松应对。5000mAh电池长续航，加上超感光四摄系统，记录生活每一刻精彩。参考售价：4599- 4999&quot;,
          &quot;pipeline_id&quot;: &quot;mymxbdxxxx&quot;,
          &quot;workspace_id&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;,
          &quot;_id&quot;: &quot;llm-4u5xpd1xdjqpxxxx_mymxbd6172_file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx_0_0&quot;,
          &quot;_knowledge_type&quot;: &quot;document&quot;,
          &quot;_knowledge_scene&quot;: &quot;basic_document_qa&quot;
        }
      }
    ],
    &quot;cost_time&quot;: 2629
  }
}
</code></pre></div></section></td></tr></tbody></table>

<a id="结构化输出"></a>

<a id="h2-structured-output"></a>

## 结构化输出

知识库检索 API 不支持 `response_format` 参数。如需 JSON 格式输出，需在**模型调用层**设置 `response_format`。

以 Python SDK `alibabacloud_bailian20231229` 2.14.3 为例，`RetrieveRequest` 共 15 个字段：`index_id`、`query`、`dense_similarity_top_k`、`enable_reranking`、`enable_rewrite`、`extra`、`images`、`query_history`、`rerank`、`rerank_min_score`、`rerank_top_n`、`rewrite`、`save_retriever_history`、`search_filters`、`sparse_similarity_top_k`，其中不含 `response_format`。

Agent API 的 `instructions` 字段可通过提示词指定 JSON 输出格式，即创建应用时将“请以 JSON 格式输出”写入 `instructions`。

阿里云百炼不直接生成 JSON 文件，返回的 JSON 内容需由调用方自行写入文件。

<a id="知识库检索-json-输出"></a>

<a id="h3-structured-output-example"></a>

### 知识库检索 + JSON 输出

先调用检索接口获取知识库文本切片，再将切片作为上下文调用 DashScope 模型接口，并设置 `response_format={"type": "json_object"}`，即可得到结构化输出。

<a id="code-block-20"></a>

```python
import os
import dashscope
from alibabacloud_bailian20231229.client import Client
from alibabacloud_bailian20231229 import models
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions

# 0. 初始化客户端
client = Client(Config(
    access_key_id=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    endpoint="bailian.cn-beijing.aliyuncs.com"
))
dashscope_client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
workspace_id = "llm-xxx"  # 业务空间 ID
runtime = RuntimeOptions()

# 1. 检索知识库
retrieve_req = models.RetrieveRequest(index_id="xxx", query="产品信息")
retrieve_resp = client.retrieve_with_options(workspace_id, retrieve_req, {}, runtime)
context = "\n".join([n.text for n in retrieve_resp.body.data.nodes])

# 2. 调用模型设置 JSON 输出
resp = dashscope_client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": f"根据以下知识库内容回答，输出JSON格式：\n{context}"},
        {"role": "user", "content": "列出所有产品型号及价格"}
    ],
    response_format={"type": "json_object"}
)
print(resp.output_text)
```

模型调用接口的更多参数说明，参见[DashScope API 参考](../../model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

<a id="更新知识库-2"></a>

<a id="f75fa46eb7r1i"></a>

## 更新知识库

接下来通过示例，引导您更新文档搜索类知识库。所有引用该知识库的应用会实时生效您本次的更新（新增内容可用于检索和召回，而已删除内容将不再可用）。

> 数据查询、图片问答类知识库同样支持通过 RAG API 创建与管理，参见[RAG API 参考](../../application-api-reference/rag-api.md)。

-   **如何增量更新知识库：**请您按照以下三步（先上传更新后的文件，再追加文件至知识库，最后删除旧文件）操作。此外暂无其他实现方式。
-   **如何全量更新知识库：**对知识库中的所有文件，请您逐一执行以下三步完成更新。
-   **如何实现知识库的自动更新/同步：**请详见[如何实现知识库的自动更新/同步](rag-knowledge-base-api-guide.md)。
-   **单次更新对文件数量是否有限制：**建议不超过10万个，否则可能导致知识库无法正常更新。

<table><tbody><tr><td><a id="8e00a8be1860o"></a><h3>1. 上传更新后的文件</h3><p>按照<a href="rag-knowledge-base-api-guide.md#4b4a1236aalno">创建知识库：第二步</a>操作，将更新后的文件上传至该知识库所在的业务空间。</p><blockquote><p>您需要重新申请文件上传租约，为更新后的文件生成一组新的上传参数。</p></blockquote></td><td></td></tr><tr><td colspan="2"><a id="f78d5993d3uig"></a><h3>2. 追加文件至知识库</h3></td></tr><tr><td><a id="ca254fff3dtxo"></a><h4>2.1. 提交追加文件任务</h4><p>上传文件解析完成后，请调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexadddocumentsjob">SubmitIndexAddDocumentsJob接口</a>将新文件追加至知识库，并重新构建知识库索引。</p><ul><li><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></li><li><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></li><li><strong>file_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">添加文件到类目中</a>时接口返回的<code>FileId</code>。</li><li><strong>source_type：</strong>在本示例中，请传入<code>DATA_CENTER_FILE</code>。</li></ul><p>完成提交后，阿里云百炼将以异步任务方式开始重新构建知识库。本接口返回的<code>Data.Id</code>为对应的任务ID（job_id）。下一步中，您将用到此ID查询任务的最新状态。</p><div><div><p><strong>重要</strong></p><ul><li>SubmitIndexAddDocumentsJob接口调用成功后，将执行一段时间，您可通过<code>job_id</code>查询任务的最新状态。<strong>在任务完成前，请勿重复提交。</strong></li></ul></div></div></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-16"></a><div><a id="fig-code-group-16-python-tab"></a>Python<div><a id="code-code-group-16-python"></a><pre class="language-python"><code>def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type):
    &quot;&quot;&quot;
    向一个文档搜索类知识库追加导入已解析的文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。
        source_type(str): 数据类型。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request, headers, runtime)
</code></pre></div><a id="fig-code-group-16-java-tab"></a>Java<div><a id="code-code-group-16-java"></a><pre class="language-java"><code>/**
 * 向一个文档搜索类知识库追加导入已解析的文件
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @param fileId      文件ID
 * @param sourceType  数据类型
 * @return 阿里云百炼服务的响应
 */
public SubmitIndexAddDocumentsJobResponse submitIndexAddDocumentsJob(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId, String sourceType) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    SubmitIndexAddDocumentsJobRequest submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest();
    submitIndexAddDocumentsJobRequest.setIndexId(indexId);
    submitIndexAddDocumentsJobRequest.setDocumentIds(Collections.singletonList(fileId));
    submitIndexAddDocumentsJobRequest.setSourceType(sourceType);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.submitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-16-php-tab"></a>PHP<div><a id="code-code-group-16-php"></a><pre class="language-php"><code>/**
 * 向一个文档搜索类知识库追加导入已解析的文件
 *
 * @param Bailian $client 客户端对象
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @param string $fileId 文件ID
 * @param string $sourceType 数据类型
 * @return SubmitIndexAddDocumentsJobResponse 阿里云百炼服务的响应
 * @throws Exception
 */
public function submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType) {
    $headers = [];
    $submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest([
        &quot;indexId&quot; =&gt;$indexId,
        &quot;sourceType&quot; =&gt; $sourceType,
        &quot;documentIds&quot; =&gt; [
            $fileId
        ]
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;submitIndexAddDocumentsJobWithOptions($workspaceId, $submitIndexAddDocumentsJobRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-16-node-js-tab"></a>Node.js<div><a id="code-code-group-16-node-js"></a><pre class="language-javascript"><code>/**
 * 提交追加文件任务
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @param {string} fileId - 文件ID
 * @param {string} sourceType - 数据类型
 * @returns {Promise&lt;bailian20231229.SubmitIndexAddDocumentsJobResponse&gt;} - 阿里云百炼服务的响应
 */
async function submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType) {
    const headers = {};
    const req = new bailian20231229.SubmitIndexAddDocumentsJobRequest({
        indexId,
        documentIds: [fileId],
        sourceType,
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.submitIndexAddDocumentsJobWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-16-c-tab"></a>C#<div><a id="code-code-group-16-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 向一个文档搜索类知识库追加导入已解析的文件
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端（Client）&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;param name=&quot;fileId&quot;&gt;文件ID&lt;/param&gt;
/// &lt;param name=&quot;sourceType&quot;&gt;数据类型&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应&lt;/returns&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse SubmitIndexAddDocumentsJob(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId,
    string fileId,
    string sourceType)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var submitIndexAddDocumentsJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobRequest
    {
        IndexId = indexId,
        DocumentIds = new List&lt;string&gt; { fileId },
        SourceType = sourceType
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.SubmitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-16-go-tab"></a>Go<div><a id="code-code-group-16-go"></a><pre class="language-go"><code>// SubmitIndexAddDocumentsJob 向一个文档搜索类知识库追加导入已解析的文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - fileId(string): 文件ID。
//   - sourceType(string): 数据类型。
//
// 返回:
//   - *bailian20231229.SubmitIndexAddDocumentsJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndexAddDocumentsJob(client *bailian20231229.Client, workspaceId, indexId, fileId, sourceType string) (_result *bailian20231229.SubmitIndexAddDocumentsJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexAddDocumentsJobRequest := &amp;bailian20231229.SubmitIndexAddDocumentsJobRequest{
		IndexId:     tea.String(indexId),
		SourceType:  tea.String(sourceType),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.SubmitIndexAddDocumentsJobWithOptions(tea.String(workspaceId), submitIndexAddDocumentsJobRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-8"></a><section><p>请求示例</p><div><a id="code-block-21"></a><pre class="language-json"><code>{
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;SourceType&quot;: &quot;DATA_CENTER_FILE&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;,
  &quot;DocumentIds&quot;: [
    &quot;file_247a2fd456a349ee87d071404840109b_10xxxxxx&quot;
  ]
}
</code></pre></div></section><a id="accordion-响应示例-8"></a><section><p>响应示例</p><div><a id="code-block-22"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;RequestId&quot;: &quot;F693EB60-FEFC-559A-BF56-A41F52XXXXXX&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;Data&quot;: {
    &quot;Id&quot;: &quot;d8d189a36a3248438dca23c078xxxxxx&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td><a id="92c470208d1dy"></a><h4>2.2. 等待追加任务完成</h4><p>索引任务的执行需要一定时间，在请求高峰时段，该过程可能需要数小时。查询其执行状态可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus">GetIndexJobStatus接口</a>。</p><ul><li><strong>job_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">提交追加文件任务</a>时接口返回的<code>Data.Id</code>。</li></ul><p>当本接口返回的<code>Data.Status</code>字段值为<code>COMPLETED</code>，表示本次更新的文件已全部成功追加至知识库。</p><blockquote><p>本接口返回的文件列表<code>Documents</code>为本次追加（由您提供的<code>job_id</code>唯一确定）的所有文件。</p></blockquote></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-17"></a><div><a id="fig-code-group-17-python-tab"></a>Python<div><a id="code-code-group-17-python"></a><pre class="language-python"><code>def get_index_job_status(client, workspace_id, index_id, job_id):
    &quot;&quot;&quot;
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)
</code></pre></div><a id="fig-code-group-17-java-tab"></a>Java<div><a id="code-code-group-17-java"></a><pre class="language-java"><code>/**
 * 查询索引任务状态。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param jobId       任务ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
    getIndexJobStatusRequest.setIndexId(indexId);
    getIndexJobStatusRequest.setJobId(jobId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    GetIndexJobStatusResponse getIndexJobStatusResponse = null;
    getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
    return getIndexJobStatusResponse;
}
</code></pre></div><a id="fig-code-group-17-php-tab"></a>PHP<div><a id="code-code-group-17-php"></a><pre class="language-php"><code>/**
 * 查询索引任务状态。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @param string $jobId 任务ID。
 * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
 */
public function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
    $headers = [];
    $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
        'indexId' =&gt; $indexId,
        'jobId' =&gt; $jobId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-17-node-js-tab"></a>Node.js<div><a id="code-code-group-17-node-js"></a><pre class="language-javascript"><code>/**
 * 查询索引任务状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} jobId - 任务ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise&lt;bailian20231229.GetIndexJobStatusResponse&gt;} - 阿里云百炼服务的响应
 */
static getIndexJobStatus(client, workspaceId, jobId, indexId) {
    const headers = {};
    const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-17-c-tab"></a>C#<div><a id="code-code-group-17-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 查询索引任务状态。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端对象&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;jobId&quot;&gt;任务ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应对象&lt;/returns&gt;
/// &lt;exception cref=&quot;Exception&quot;&gt;调用过程中发生错误时抛出异常&lt;/exception&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string jobId,
    string indexId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
    {
        IndexId = indexId,
        JobId = jobId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-17-go-tab"></a>Go<div><a id="code-code-group-17-go"></a><pre class="language-go"><code>// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &amp;bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-9"></a><section><p>请求示例</p><div><a id="code-block-23"></a><pre class="language-json"><code>{
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;JobId&quot;: &quot;76f243b9ee534d59a61f156ff0xxxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-9"></a><section><p>响应示例</p><div><a id="code-block-24"></a><pre class="language-json"><code>{
  &quot;Status&quot;: 200,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;RequestId&quot;: &quot;7F727D58-D90E-51E7-B56E-985A42XXXXXX&quot;,
  &quot;Data&quot;: {
    &quot;Status&quot;: &quot;COMPLETED&quot;,
    &quot;Documents&quot;: [
      {
        &quot;Status&quot;: &quot;FINISH&quot;,
        &quot;DocId&quot;: &quot;file_247a2fd456a349ee87d071404840109b_10xxxxxx&quot;,
        &quot;Message&quot;: &quot;导入成功&quot;,
        &quot;DocName&quot;: &quot;阿里云百炼系列手机产品介绍&quot;,
        &quot;Code&quot;: &quot;FINISH&quot;
      }
    ],
    &quot;JobId&quot;: &quot;76f243b9ee534d59a61f156ff0xxxxxx&quot;
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: true
}
</code></pre></div></section></td></tr><tr><td><a id="ac0f070aafg2y"></a><h3>3. 删除旧文件</h3><p>最后，从指定知识库中永久删除旧版本的文件（避免旧的知识被错误检索），可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindexdocument">DeleteIndexDocument接口</a>。</p><ul><li><strong>file_id：</strong>请传入旧版本文件的<code>FileId</code>。</li></ul><div><div><p><strong>说明</strong>仅能删除知识库中状态为导入失败（INSERT_ERROR）或导入成功（FINISH）的文件。如需查询知识库中的文件状态，可调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindexdocuments">ListIndexDocuments接口</a>。</p></div></div></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndexDocument">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndexDocument?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-18"></a><div><a id="fig-code-group-18-python-tab"></a>Python<div><a id="code-code-group-18-python"></a><pre class="language-python"><code>def delete_index_document(client, workspace_id, index_id, file_id):
    &quot;&quot;&quot;
    从指定的文档搜索类知识库中永久删除一个或多个文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    delete_index_document_request = bailian_20231229_models.DeleteIndexDocumentRequest(
        index_id=index_id,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_document_with_options(workspace_id, delete_index_document_request, headers, runtime)
</code></pre></div><a id="fig-code-group-18-java-tab"></a>Java<div><a id="code-code-group-18-java"></a><pre class="language-java"><code>/**
 * 从指定的文档搜索类知识库中永久删除一个或多个文件
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @param fileId      文件ID
 * @return 阿里云百炼服务的响应
 */
public DeleteIndexDocumentResponse deleteIndexDocument(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    DeleteIndexDocumentRequest deleteIndexDocumentRequest = new DeleteIndexDocumentRequest();
    deleteIndexDocumentRequest.setIndexId(indexId);
    deleteIndexDocumentRequest.setDocumentIds(Collections.singletonList(fileId));
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.deleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-18-php-tab"></a>PHP<div><a id="code-code-group-18-php"></a><pre class="language-php"><code>/**
 * 从指定的文档搜索类知识库中永久删除文件
 *
 * @param Bailian $client 客户端对象
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @param string $fileId 文件ID
 * @return mixed 阿里云百炼服务的响应
 * @throws Exception
 */
public function deleteIndexDocument($client, $workspaceId, $indexId, $fileId) {
    $headers = [];
    $deleteIndexDocumentRequest = new DeleteIndexDocumentRequest([
        &quot;indexId&quot; =&gt; $indexId,
        &quot;documentIds&quot; =&gt; [
            $fileId
        ]
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;deleteIndexDocumentWithOptions($workspaceId, $deleteIndexDocumentRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-18-node-js-tab"></a>Node.js<div><a id="code-code-group-18-node-js"></a><pre class="language-javascript"><code>/**
 * 删除旧文件
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @param {string} fileId - 文件ID
 * @returns {Promise&lt;bailian20231229.DeleteIndexDocumentResponse&gt;} - 阿里云百炼服务的响应
 */
async function deleteIndexDocument(client, workspaceId, indexId, fileId) {
    const headers = {};
    const req = new bailian20231229.DeleteIndexDocumentRequest({
        indexId,
        documentIds: [fileId],
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.deleteIndexDocumentWithOptions(workspaceId, req, headers, runtime);
}
</code></pre></div><a id="fig-code-group-18-c-tab"></a>C#<div><a id="code-code-group-18-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 从指定的文档搜索类知识库中永久删除一个或多个文件
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端（Client）&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;param name=&quot;fileId&quot;&gt;文件ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应&lt;/returns&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentResponse DeleteIndexDocument(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId,
    string fileId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var deleteIndexDocumentRequest = new AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentRequest
    {
        IndexId = indexId,
        DocumentIds = new List&lt;string&gt; { fileId }
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DeleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-18-go-tab"></a>Go<div><a id="code-code-group-18-go"></a><pre class="language-go"><code>// DeleteIndexDocument 从指定的文档搜索类知识库中永久删除一个或多个文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexDocumentResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DeleteIndexDocument(client *bailian20231229.Client, workspaceId, indexId, fileId string) (*bailian20231229.DeleteIndexDocumentResponse, error) {
	headers := make(map[string]*string)
	deleteIndexDocumentRequest := &amp;bailian20231229.DeleteIndexDocumentRequest{
		IndexId:     tea.String(indexId),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.DeleteIndexDocumentWithOptions(tea.String(workspaceId), deleteIndexDocumentRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-10"></a><section><p>请求示例</p><div><a id="code-block-25"></a><pre class="language-json"><code>{
  &quot;DocumentIds&quot;: [
    &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;
  ],
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-10"></a><section><p>响应示例</p><div><a id="code-block-26"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;RequestId&quot;: &quot;2D8505EC-C667-5102-9154-00B6FEXXXXXX&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;Data&quot;: {
    &quot;DeletedDocument&quot;: [
      &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;
    ]
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr></tbody></table>

<a id="管理知识库-2"></a>

<a id="52dedfee39zza"></a>

## 管理知识库

<table><tbody><tr><td><a id="33ab40c8b7zdy"></a><h3>查看知识库</h3><p>要查看给定业务空间下的一个或多个知识库的信息，可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindices">ListIndices接口</a>。</p><ul><li><p><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></p></li><li><p><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></p><blockquote><p>子账号只能查看自己<a href="https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users">已加入的业务空间</a>中的知识库。</p></blockquote></li></ul></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/ListIndices">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/ListIndices?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-19"></a><div><a id="fig-code-group-19-python-tab"></a>Python<div><a id="code-code-group-19-python"></a><pre class="language-python"><code>def list_indices(client, workspace_id):
    &quot;&quot;&quot;
    获取指定业务空间下一个或多个知识库的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    runtime = util_models.RuntimeOptions()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)
</code></pre></div><a id="fig-code-group-19-java-tab"></a>Java<div><a id="code-code-group-19-java"></a><pre class="language-java"><code>/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应
 */
public ListIndicesResponse listIndices(com.aliyun.bailian20231229.Client client, String workspaceId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.ListIndicesRequest listIndicesRequest = new com.aliyun.bailian20231229.models.ListIndicesRequest();
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-19-php-tab"></a>PHP<div><a id="code-code-group-19-php"></a><pre class="language-php"><code>/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 *
 * @param Bailian $client 客户端对象（Client）
 * @param string $workspaceId 业务空间ID
 * @return ListIndicesResponse 阿里云百炼服务的响应
 * @throws Exception
 */
public function listIndices($client, $workspaceId) {
    $headers = [];
    $listIndicesRequest = new ListIndicesRequest([]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;listIndicesWithOptions($workspaceId, $listIndicesRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-19-node-js-tab"></a>Node.js<div><a id="code-code-group-19-node-js"></a><pre class="language-javascript"><code>/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 * @param {bailian20231229.Client} client 客户端（Client）
 * @param {string} workspaceId 业务空间ID
 * @returns {Promise&lt;bailian20231229.ListIndicesResponse&gt;} 阿里云百炼服务的响应
 */
async function listIndices(client, workspaceId) {
    const headers = {};
    const listIndicesRequest = new bailian20231229.ListIndicesRequest();
    const runtime = new Util.RuntimeOptions({});
    return await client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-19-c-tab"></a>C#<div><a id="code-code-group-19-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 获取指定业务空间下一个或多个知识库的详细信息。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端（Client）&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应&lt;/returns&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.ListIndicesResponse ListIndices(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var listIndicesRequest = new Bailian20231229.Models.ListIndicesRequest();
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.ListIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-19-go-tab"></a>Go<div><a id="code-code-group-19-go"></a><pre class="language-go"><code>// listIndices 获取指定业务空间下一个或多个知识库的详细信息。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//
// 返回:
//   - *bailian20231229.ListIndicesResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func listIndices(client *bailian20231229.Client, workspaceId string) (_result *bailian20231229.ListIndicesResponse, _err error) {
	headers := make(map[string]*string)
	listIndicesRequest := &amp;bailian20231229.ListIndicesRequest{}
	runtime := &amp;util.RuntimeOptions{}
	return client.ListIndicesWithOptions(tea.String(workspaceId), listIndicesRequest, headers, runtime)
}
</code></pre></div></div><a id="accordion-请求示例-11"></a><section><p>请求示例</p><div><a id="code-block-27"></a><pre class="language-json"><code>{
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-11"></a><section><p>响应示例</p><div><a id="code-block-28"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;RequestId&quot;: &quot;5ACB2EB3-6C9A-5B0F-8E60-3FBE7EXXXXXX&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;Data&quot;: {
    &quot;TotalCount&quot;: &quot;1&quot;,
    &quot;PageSize&quot;: &quot;10&quot;,
    &quot;PageNumber&quot;: &quot;1&quot;,
    &quot;Indices&quot;: [
      {
        &quot;DocumentIds&quot;: [
          &quot;file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx&quot;
        ],
        &quot;Description&quot;: &quot;&quot;,
        &quot;OverlapSize&quot;: 100,
        &quot;SinkInstanceId&quot;: &quot;gp-2zegk3i6ca4xxxxxx&quot;,
        &quot;SourceType&quot;: &quot;DATA_CENTER_FILE&quot;,
        &quot;RerankModelName&quot;: &quot;gte-rerank-hybrid&quot;,
        &quot;SinkRegion&quot;: &quot;cn-beijing&quot;,
        &quot;Name&quot;: &quot;百炼手机知识库&quot;,
        &quot;ChunkSize&quot;: 500,
        &quot;EmbeddingModelName&quot;: &quot;text-embedding-v2&quot;,
        &quot;RerankMinScore&quot;: 0.01,
        &quot;Id&quot;: &quot;mymxbdxxxx&quot;,
        &quot;SinkType&quot;: &quot;BUILT_IN&quot;,
        &quot;Separator&quot;: &quot; |,|，|。|？|！|\n|\\?|\\!&quot;
      }
    ]
  },
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr><tr><td><a id="3fb0970bd7enw"></a><h3>删除知识库</h3><p>要永久性删除某个知识库，可以调用<a href="https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindex">DeleteIndex接口</a>。删除前，请<a href="rag-knowledge-base.md">解除该知识库关联的所有阿里云百炼应用</a>（仅可通过阿里云百炼控制台操作），否则会删除失败。</p><ul><li><p><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></p></li><li><p><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></p><blockquote><p>子账号只能删除自己<a href="https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users">已加入的业务空间</a>中的知识库。</p></blockquote></li><li><p><strong>index_id：</strong>请传入<a href="rag-knowledge-base-api-guide.md">初始化知识库</a>时接口返回的<code>Data.Id</code>。</p></li></ul><p>请注意：本操作不会删除您已<a href="rag-knowledge-base-api-guide.md">添加至类目中</a>的文件。</p></td><td><div><div><p><strong>重要</strong></p><ul><li>子账号调用本示例前需获取<a href="https://help.aliyun.com/zh/model-studio/member-management">API权限</a>（AliyunBailianDataFullAccess策略）。</li><li>本示例支持<a href="https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex">在线调试</a>及多语言<a href="https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex?lang=JAVA&amp;tab=DEMO">代码示例生成</a>。</li></ul></div></div><a id="fig-code-group-20"></a><div><a id="fig-code-group-20-python-tab"></a>Python<div><a id="code-code-group-20-python"></a><pre class="language-python"><code>def delete_index(client, workspace_id, index_id):
    &quot;&quot;&quot;
    永久性删除指定的知识库。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    &quot;&quot;&quot;
    headers = {}
    delete_index_request = bailian_20231229_models.DeleteIndexRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_with_options(workspace_id, delete_index_request, headers, runtime)
</code></pre></div><a id="fig-code-group-20-java-tab"></a>Java<div><a id="code-code-group-20-java"></a><pre class="language-java"><code>/**
 * 永久性删除指定的知识库
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应
 */
public DeleteIndexResponse deleteIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    com.aliyun.bailian20231229.models.DeleteIndexRequest deleteIndexRequest = new com.aliyun.bailian20231229.models.DeleteIndexRequest();
    deleteIndexRequest.setIndexId(indexId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-20-php-tab"></a>PHP<div><a id="code-code-group-20-php"></a><pre class="language-php"><code>/**
 * 永久性删除指定的知识库
 *
 * @param Bailian $client 客户端对象（Client）
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @return mixed 阿里云百炼服务的响应
 * @throws Exception
 */
public function deleteIndex($client, $workspaceId, $indexId) {
    $headers = [];
    $deleteIndexRequest = new DeleteIndexRequest([
        &quot;indexId&quot; =&gt; $indexId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;deleteIndexWithOptions($workspaceId, $deleteIndexRequest, $headers, $runtime);
}
</code></pre></div><a id="fig-code-group-20-node-js-tab"></a>Node.js<div><a id="code-code-group-20-node-js"></a><pre class="language-javascript"><code>/**
 * 永久性删除指定的知识库
 * @param {bailian20231229.Client} client 客户端（Client）
 * @param {string} workspaceId 业务空间ID
 * @param {string} indexId 知识库ID
 * @returns {Promise&lt;bailian20231229.DeleteIndexResponse&gt;} 阿里云百炼服务的响应
 */
async function deleteIndex(client, workspaceId, indexId) {
    const headers = {};
    const deleteIndexRequest = new bailian20231229.DeleteIndexRequest({
        indexId
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-20-c-tab"></a>C#<div><a id="code-code-group-20-c"></a><pre class="language-csharp"><code>/// &lt;summary&gt;
/// 永久性删除指定的知识库。
/// &lt;/summary&gt;
/// &lt;param name=&quot;client&quot;&gt;客户端（Client）&lt;/param&gt;
/// &lt;param name=&quot;workspaceId&quot;&gt;业务空间ID&lt;/param&gt;
/// &lt;param name=&quot;indexId&quot;&gt;知识库ID&lt;/param&gt;
/// &lt;returns&gt;阿里云百炼服务的响应&lt;/returns&gt;
public AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexResponse DeleteIndex(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId, string indexId)
{
    var headers = new Dictionary&lt;string, string&gt;() { };
    var deleteIndexRequest = new Bailian20231229.Models.DeleteIndexRequest
    {
        IndexId = indexId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DeleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
</code></pre></div><a id="fig-code-group-20-go-tab"></a>Go<div><a id="code-code-group-20-go"></a><pre class="language-go"><code>// deleteIndex 永久性删除指定的知识库。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//   - indexId     string: 知识库ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func deleteIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.DeleteIndexResponse, _err error) {
	headers := make(map[string]*string)
	deleteIndexRequest := &amp;bailian20231229.DeleteIndexRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.DeleteIndexWithOptions(tea.String(workspaceId), deleteIndexRequest, headers, runtime)

}
</code></pre></div></div><a id="accordion-请求示例-12"></a><section><p>请求示例</p><div><a id="code-block-29"></a><pre class="language-json"><code>{
  &quot;IndexId&quot;: &quot;mymxbdxxxx&quot;,
  &quot;WorkspaceId&quot;: &quot;llm-4u5xpd1xdjqpxxxx&quot;
}
</code></pre></div></section><a id="accordion-响应示例-12"></a><section><p>响应示例</p><div><a id="code-block-30"></a><pre class="language-json"><code>{
  &quot;Status&quot;: &quot;200&quot;,
  &quot;Message&quot;: &quot;success&quot;,
  &quot;RequestId&quot;: &quot;118CB681-75AA-583B-8D84-25440CXXXXXX&quot;,
  &quot;Code&quot;: &quot;Success&quot;,
  &quot;Success&quot;: &quot;true&quot;
}
</code></pre></div></section></td></tr></tbody></table>

<a id="管理切片"></a>

<a id="b8d3f0g52n9rl"></a>

## 管理切片

对知识库中的切片进行查询、编辑和删除操作。编辑切片所有类型知识库均支持；新增和删除方面，文档搜索类、数据查询类、图片问答类知识库均支持，音视频搜索类知识库仅支持删除。

<table><tbody><tr><td><a id="i5k0m7n29u6ys"></a><h3>查询切片列表</h3><p>调用ListChunks接口查询知识库的切片列表。</p><ul><li><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></li><li><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></li><li><strong>index_id：</strong>知识库ID，即创建知识库时返回的<code>Data.Id</code>。</li><li><strong>page_num：</strong>页码，从1开始（可选，默认1）。</li><li><strong>page_size：</strong>每页数量（可选，默认10）。</li><li><strong>file_id：</strong>文档ID（可选，不传时返回整个知识库的切片）。</li></ul></td><td><a id="fig-code-group-21"></a><div><a id="fig-code-group-21-python-tab"></a>Python<div><a id="code-code-group-21-python"></a><pre class="language-python"><code>def list_chunks(client, workspace_id, index_id, page_num=1, page_size=10, file_id=None):
    &quot;&quot;&quot;查询切片列表&quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.ListChunksRequest(
        index_id=index_id,
        page_num=page_num,
        page_size=page_size,
        file_id=file_id
    )
    runtime = util_models.RuntimeOptions()
    return client.list_chunks_with_options(workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-21-java-tab"></a>Java<div><a id="code-code-group-21-java"></a><pre class="language-java"><code>public static ListChunksResponse listChunks(Client client, String workspaceId, String indexId, Integer pageNum, Integer pageSize) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    ListChunksRequest request = new ListChunksRequest()
        .setIndexId(indexId)
        .setPageNum(pageNum)
        .setPageSize(pageSize);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.listChunksWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-21-php-tab"></a>PHP<div><a id="code-code-group-21-php"></a><pre class="language-php"><code>function listChunks($client, $workspaceId, $indexId, $pageNum = 1, $pageSize = 10) {
    $request = new ListChunksRequest([
        &quot;indexId&quot; =&gt; $indexId,
        &quot;pageNum&quot; =&gt; $pageNum,
        &quot;pageSize&quot; =&gt; $pageSize
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;listChunksWithOptions($workspaceId, $request, [], $runtime);
}
</code></pre></div><a id="fig-code-group-21-node-js-tab"></a>Node.js<div><a id="code-code-group-21-node-js"></a><pre class="language-javascript"><code>async function listChunks(client, workspaceId, indexId, pageNum = 1, pageSize = 10) {
    const request = new bailian20231229.ListChunksRequest({ indexId, pageNum, pageSize });
    const runtime = new Util.RuntimeOptions({});
    return await client.listChunksWithOptions(workspaceId, request, {}, runtime);
}
</code></pre></div><a id="fig-code-group-21-c-tab"></a>C#<div><a id="code-code-group-21-c"></a><pre class="language-csharp"><code>public static ListChunksResponse ListChunks(Client client, string workspaceId, string indexId, int pageNum = 1, int pageSize = 10)
{
    var headers = new Dictionary&lt;string, string&gt;();
    var request = new ListChunksRequest
    {
        IndexId = indexId,
        PageNum = pageNum,
        PageSize = pageSize
    };
    var runtime = new RuntimeOptions();
    return client.ListChunksWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-21-go-tab"></a>Go<div><a id="code-code-group-21-go"></a><pre class="language-go"><code>func listChunks(client *bailian20231229.Client, workspaceId, indexId string, pageNum, pageSize int32) (*bailian20231229.ListChunksResponse, error) {
	headers := make(map[string]*string)
	request := &amp;bailian20231229.ListChunksRequest{
		IndexId:  tea.String(indexId),
		PageNum:  tea.Int32(pageNum),
		PageSize: tea.Int32(pageSize),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.ListChunksWithOptions(tea.String(workspaceId), request, headers, runtime)
}
</code></pre></div></div></td></tr><tr><td><a id="u3w8y5z07g4ke"></a><h3>编辑切片</h3><p>调用UpdateChunk接口修改指定切片的内容。所有类型的知识库均支持此操作。</p><ul><li><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></li><li><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></li><li><strong>pipeline_id：</strong>知识库ID，即创建知识库时返回的<code>Data.Id</code>。</li><li><strong>data_id：</strong>文档ID（切片所属文档，可从ListChunks响应的<code>metadata.doc_id</code>获取）。</li><li><strong>chunk_id：</strong>切片的完整_id值（可从ListChunks响应的<code>metadata._id</code>获取）。</li><li><strong>content：</strong>新的切片内容（10-6000字符）。</li><li><strong>is_displayed_chunk_content：</strong>是否展示切片内容（设为true）。</li></ul></td><td><a id="fig-code-group-22"></a><div><a id="fig-code-group-22-python-tab"></a>Python<div><a id="code-code-group-22-python"></a><pre class="language-python"><code>def update_chunk(client, workspace_id, pipeline_id, data_id, chunk_id, content):
    &quot;&quot;&quot;编辑切片&quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.UpdateChunkRequest(
        pipeline_id=pipeline_id,
        data_id=data_id,
        chunk_id=chunk_id,
        is_displayed_chunk_content=True,
        content=content
    )
    runtime = util_models.RuntimeOptions()
    return client.update_chunk_with_options(workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-22-java-tab"></a>Java<div><a id="code-code-group-22-java"></a><pre class="language-java"><code>public static UpdateChunkResponse updateChunk(Client client, String workspaceId, String pipelineId, String dataId, String chunkId, String content) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    UpdateChunkRequest request = new UpdateChunkRequest()
        .setPipelineId(pipelineId)
        .setDataId(dataId)
        .setChunkId(chunkId)
        .setIsDisplayedChunkContent(true)
        .setContent(content);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.updateChunkWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-22-php-tab"></a>PHP<div><a id="code-code-group-22-php"></a><pre class="language-php"><code>function updateChunk($client, $workspaceId, $pipelineId, $dataId, $chunkId, $content) {
    $request = new UpdateChunkRequest([
        &quot;pipelineId&quot; =&gt; $pipelineId,
        &quot;dataId&quot; =&gt; $dataId,
        &quot;chunkId&quot; =&gt; $chunkId,
        &quot;isDisplayedChunkContent&quot; =&gt; true,
        &quot;content&quot; =&gt; $content
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;updateChunkWithOptions($workspaceId, $request, [], $runtime);
}
</code></pre></div><a id="fig-code-group-22-node-js-tab"></a>Node.js<div><a id="code-code-group-22-node-js"></a><pre class="language-javascript"><code>async function updateChunk(client, workspaceId, pipelineId, dataId, chunkId, content) {
    const request = new bailian20231229.UpdateChunkRequest({ pipelineId, dataId, chunkId, isDisplayedChunkContent: true, content });
    const runtime = new Util.RuntimeOptions({});
    return await client.updateChunkWithOptions(workspaceId, request, {}, runtime);
}
</code></pre></div><a id="fig-code-group-22-c-tab"></a>C#<div><a id="code-code-group-22-c"></a><pre class="language-csharp"><code>public static UpdateChunkResponse UpdateChunk(Client client, string workspaceId, string pipelineId, string dataId, string chunkId, string content)
{
    var headers = new Dictionary&lt;string, string&gt;();
    var request = new UpdateChunkRequest
    {
        PipelineId = pipelineId,
        DataId = dataId,
        ChunkId = chunkId,
        IsDisplayedChunkContent = true,
        Content = content
    };
    var runtime = new RuntimeOptions();
    return client.UpdateChunkWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-22-go-tab"></a>Go<div><a id="code-code-group-22-go"></a><pre class="language-go"><code>func updateChunk(client *bailian20231229.Client, workspaceId, pipelineId, dataId, chunkId, content string) (*bailian20231229.UpdateChunkResponse, error) {
	headers := make(map[string]*string)
	request := &amp;bailian20231229.UpdateChunkRequest{
		PipelineId:              tea.String(pipelineId),
		DataId:                  tea.String(dataId),
		ChunkId:                 tea.String(chunkId),
		IsDisplayedChunkContent: tea.Bool(true),
		Content:                 tea.String(content),
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.UpdateChunkWithOptions(tea.String(workspaceId), request, headers, runtime)
}
</code></pre></div></div></td></tr><tr><td><a id="i3k8m5n07u4ys"></a><h3>删除切片</h3><p>调用DeleteChunk接口删除一个或多个切片。单次最多删除10个。</p><ul><li><strong>client：</strong><a href="rag-knowledge-base-api-guide.md#a8ce8e7788gmh">如何获取client</a></li><li><strong>workspace_id：</strong><a href="https://help.aliyun.com/zh/model-studio/use-workspace">如何获取业务空间ID</a></li><li><strong>pipeline_id：</strong>知识库ID，即创建知识库时返回的<code>Data.Id</code>。</li><li><strong>chunk_ids：</strong>要删除的切片_id列表（从ListChunks响应的<code>metadata._id</code>获取）。</li></ul></td><td><a id="fig-code-group-23"></a><div><a id="fig-code-group-23-python-tab"></a>Python<div><a id="code-code-group-23-python"></a><pre class="language-python"><code>def delete_chunk(client, workspace_id, pipeline_id, chunk_ids):
    &quot;&quot;&quot;删除切片&quot;&quot;&quot;
    headers = {}
    request = bailian_20231229_models.DeleteChunkRequest(
        pipeline_id=pipeline_id,
        chunk_ids=chunk_ids
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_chunk_with_options(workspace_id, request, headers, runtime)
</code></pre></div><a id="fig-code-group-23-java-tab"></a>Java<div><a id="code-code-group-23-java"></a><pre class="language-java"><code>public static DeleteChunkResponse deleteChunk(Client client, String workspaceId, String pipelineId, java.util.List&lt;String&gt; chunkIds) throws Exception {
    Map&lt;String, String&gt; headers = new HashMap&lt;&gt;();
    DeleteChunkRequest request = new DeleteChunkRequest()
        .setPipelineId(pipelineId)
        .setChunkIds(chunkIds);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.deleteChunkWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-23-php-tab"></a>PHP<div><a id="code-code-group-23-php"></a><pre class="language-php"><code>function deleteChunk($client, $workspaceId, $pipelineId, $chunkIds) {
    $request = new DeleteChunkRequest([
        &quot;pipelineId&quot; =&gt; $pipelineId,
        &quot;chunkIds&quot; =&gt; $chunkIds
    ]);
    $runtime = new RuntimeOptions([]);
    return $client-&gt;deleteChunkWithOptions($workspaceId, $request, [], $runtime);
}
</code></pre></div><a id="fig-code-group-23-node-js-tab"></a>Node.js<div><a id="code-code-group-23-node-js"></a><pre class="language-javascript"><code>async function deleteChunk(client, workspaceId, pipelineId, chunkIds) {
    const request = new bailian20231229.DeleteChunkRequest({ pipelineId, chunkIds });
    const runtime = new Util.RuntimeOptions({});
    return await client.deleteChunkWithOptions(workspaceId, request, {}, runtime);
}
</code></pre></div><a id="fig-code-group-23-c-tab"></a>C#<div><a id="code-code-group-23-c"></a><pre class="language-csharp"><code>public static DeleteChunkResponse DeleteChunk(Client client, string workspaceId, string pipelineId, List&lt;string&gt; chunkIds)
{
    var headers = new Dictionary&lt;string, string&gt;();
    var request = new DeleteChunkRequest
    {
        PipelineId = pipelineId,
        ChunkIds = chunkIds
    };
    var runtime = new RuntimeOptions();
    return client.DeleteChunkWithOptions(workspaceId, request, headers, runtime);
}
</code></pre></div><a id="fig-code-group-23-go-tab"></a>Go<div><a id="code-code-group-23-go"></a><pre class="language-go"><code>func deleteChunk(client *bailian20231229.Client, workspaceId, pipelineId string, chunkIds []*string) (*bailian20231229.DeleteChunkResponse, error) {
	headers := make(map[string]*string)
	request := &amp;bailian20231229.DeleteChunkRequest{
		PipelineId: tea.String(pipelineId),
		ChunkIds:   chunkIds,
	}
	runtime := &amp;util.RuntimeOptions{}
	return client.DeleteChunkWithOptions(tea.String(workspaceId), request, headers, runtime)
}
</code></pre></div></div></td></tr></tbody></table>

<a id="api参考"></a>

<a id="edab6f57121zt"></a>

## API参考

请参阅[API目录（知识库）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir-knowledge-base)获取最新完整的知识库API列表及输入输出参数。

<a id="常见问题"></a>

<a id="cc11fcfa1479f"></a>

## 常见问题

1.  **如何实现知识库的自动更新/同步？**
    
    <a id="sec-tabs-3"></a>
    
    <a id="文档搜索类知识库"></a>
    
    <a id="文档搜索类知识库-h4"></a>
    
    #### 文档搜索类知识库
    
    使用对象存储OSS管理文件，通过函数计算FC监听文件变更事件，自动同步更新至知识库，实现知识的实时更新。详见[告别手动操作，让AI知识库自动更新](https://www.aliyun.com/solution/tech-solution/auto-updated-knowledge-base)。
    
    <a id="数据查询-图片问答类知识库"></a>
    
    <a id="数据查询-图片问答类知识库-h4"></a>
    
    #### 数据查询/图片问答类知识库
    
    若要实现数据查询/图片问答类知识库的自动更新，可基于RDS数据表构建知识库。具体操作请参见[创建知识库](rag-knowledge-base.md)。
    
    <a id="音视频搜索类知识库"></a>
    
    <a id="音视频搜索类知识库-h4"></a>
    
    #### 音视频搜索类知识库
    
    不支持。
    
2.  **为什么我新建的知识库里没有内容？**
    
    一般是由于没有执行或未能成功执行[提交索引任务](rag-knowledge-base-api-guide.md)这一步导致。若调用[CreateIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)接口后未成功调用[SubmitIndexJob](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexjob)接口，您将得到一个空知识库。此时，您只需重新执行[提交索引任务](rag-knowledge-base-api-guide.md)并[等待索引任务完成](rag-knowledge-base-api-guide.md)即可。
    
3.  **遇到报错Access your uploaded file failed. Please check if your upload action was successful，应该如何处理？**
    
    一般是由于没有执行或未能成功执行[上传文件到临时存储](rag-knowledge-base-api-guide.md)这一步导致。请在确认该步骤成功执行后，再调用[AddFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile)接口。
    
4.  **遇到报错Access denied: Either you are not authorized to access this workspace, or the workspace does not exist，应该如何处理？**
    
    一般是由于：
    
    -   **您请求的服务地址（**[服务接入点](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-endpoint)**）有误：**以公网接入为例，如果您是中国站用户，应访问北京（公有云用户）地域的接入地址；如果您是国际站用户，应访问新加坡地域的接入地址。如果您正在使用[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex)功能，请确认服务地址下拉框选择正确（中国站选择**华北2（北京）**）。
        
    -   **您传入的WorkspaceId值不正确，或者您还不是该业务空间的成员导致：**请确认`WorkspaceId`值无误且您是该业务空间的成员后，再调用接口。[如何被添加为指定业务空间的成员](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)
        
5.  **遇到报错Specified access key is not found or invalid，应该如何处理？**
    
    一般是由于您传入的`access_key_id`或`access_key_secret`值不正确，或者该`access_key_id`已被[禁用](https://help.aliyun.com/zh/ram/user-guide/disable-an-accesskey-pair-of-a-ram-user)导致。请确认`access_key_id`值无误且未被禁用后，再调用接口。
    
6.  **遇到报错Category is mismatched，应该如何处理？**
    
    一般是由于在调用`ApplyFileUploadLease`接口申请文件上传租约时使用的`CategoryId`，与后续调用`AddFile`接口时传入的`CategoryId`不一致导致。
    
    请确保在整个文件上传流程中（从`ApplyFileUploadLease`到`AddFile`），使用同一个`CategoryId`。您可以通过`ListCategory`接口获取当前业务空间下的类目列表，确认所使用的`CategoryId`正确无误。
    
7.  **调用知识库应用时，为什么 API 返回结果与控制台调试窗口不一致？**
    
    按以下维度排查：
    
    -   **多轮对话上下文**：**控制台调试窗口**默认保留多轮对话历史；API 调用若不传`session_id`，每次都是无上下文的单次调用，依赖上文指代的追问会丢失指代对象，可能返回与调试窗口完全不同的答案。需要多轮对话能力时，从首次调用的响应中取回`session_id`，并在后续调用中传入同一个`session_id`，以保持会话连续性。
    -   **应用发布状态**：应用配置修改后需单击**发布**才会生效，API 调用的始终是**已发布**版本。若调试窗口中验证的是尚未发布的改动，API 返回不会体现这些改动。请先确认应用状态为**已发布**。
    -   **参数对齐**：通过应用调用（App API）时使用应用中配置的默认参数（如`temperature`、`top_p`等），与调试窗口一致；若直接调用模型服务 DashScope 的 API，这些参数需自行显式指定，取值可能与调试环境不同，从而导致回答风格与内容差异。
    -   **知识库关联方式**：通过应用调用（App API）时会自动关联应用中已配置的知识库，无需手动指定；若直接调用知识库检索 API，则必须显式传入`knowledgebase_id`，遗漏或传错会导致检索不到预期知识。

<a id="计费说明"></a>

<a id="7ea6dace3ej4u"></a>

## 计费说明

知识库采用**按量付费（后付费）**模式，按**小时**统计各计费项用量并自动扣费。请保持阿里云账户余额充足（可前往[费用与成本](https://usercenter2.aliyun.com/home)充值），避免因[欠费](../agent-billing/billing-for-knowledge-base.md#ece89cd5852lm)导致服务中断。

| 计费项 | 说明 |
| --- | --- |
| **规格费用** | `标准版` 或 `旗舰版` 知识库的实际运行时长费用，价格详见[知识库计费说明](../agent-billing/billing-for-knowledge-base.md)。变更配置时，按变更时间点[分段计费](../agent-billing/billing-for-knowledge-base.md#d90304901atdb)。 |
| **向量、排序模型调用费用** | 创建、更新或检索知识库时会调用向量（embedding）和排序（rerank）模型，按输入 Token 用量计费，价格以[模型调用计费](../../model-user-guide/test-1/model-pricing.md)页为准。 |

**账单查询：**[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)

<a id="错误码"></a>

<a id="890d73dcdfn92"></a>

## 错误码

如果调用本文中的API失败并收到错误信息，请参见[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)进行解决。
