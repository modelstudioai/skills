# 移动端iOS SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互移动端iOS SDK，包括SDK下载安装、关键接口及代码示例。

MultiModalDialog SDK是阿里云通义团队提供的支持音视频端到端多模实时交互的SDK。通过SDK对接千问大模型以及后端多种Agent，能够支持用户接入语音对话、天气、音乐、新闻等多种能力，并支持视频和图像的大模型对话能力。

## **多模态实时交互服务架构**

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

## **前提条件**

开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **交互数据链路说明**

SDK支持WebSocket和RTC 两个链路与服务端交互，多模交互支持AudioOnly和AudioAndVideo 两种模式：

-   音频交互：推荐使用WebSocket 连接，连接速度较快，性能要求较低。
    
    -   WS 链路音频格式说明：
        
        -   上行：支持 pcm 和 opus 格式音频进行语音识别。
            
        -   下行：支持 pcm 和 mp3 音频流。
            
-   视频交互：推荐使用Websocket链路，参考[通过 Websocket 链路请求LiveAI](#65b15ddaeeg4s)。
    

## **交互模式说明**

SDK支持 **Push2Talk**、 **Tap2Talk**和**Duplex**（全双工）三种交互模式。

-   Push2Talk: 长按说话，抬起结束（或者点击开始，点击结束 ）的收音方式。
    
-   Tap2Talk: 点击开始说话，自动判断用户说话结束的收音方式。
    
-   Duplex: 全双工交互，连接开始后支持任意时刻开始说话，支持语音打断。视频交互建议使用duplex模式。
    

## **环境和依赖**

-   导入SDK ([multimodal-dialog-ios-1.0.5.1.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260304/gqwdjp/multimodal-dialog-ios-1.0.5.1.zip)）
    
    -   multimodal\_dialog.framework 百炼多模对话SDK。
        
    -   MultimodalDialogTongyiMetathings.framework License模式使用的SDK
        
-   百炼环境接入
    
    -   多模对话服务基于阿里云大模型服务平台百炼，接入鉴权使用百炼[API\_KEY](https://help.aliyun.com/zh/model-studio/get-api-key)，请您在百炼平台创建API\_KEY，移动端为了安全考虑，您也可以在服务端接入[短时Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，并下发给客户端使用。
        

## **接口说明**

### MultimodalDialog

服务入口类

#### 1 MultiModalDialog

初始化服务对象，设置对话参数和回调。

```
/// 初始化多模态对话管理器
    /// - Parameters:
    ///   - url: 服务URL
    ///   - chainMode: 链接模式 （RTC/WebSocket）
    ///   - workSpaceId: 工作空间ID,在百炼管控台获取
    ///   - appId: 应用ID, 多模对话管控台配置
    ///   - mode: 对话模式 (tap2talk/push2talk/duplex)
public init(url: String?, chainMode: ChainMode, workSpaceId: String, appId:String ,mode: DialogMode)
```

#### **2 start**

启动对话服务. 返回on\_started回调。注意on\_started会回调dialog\_id。

```
/// 发起对话请求,连接到对话服务
    /// - Parameters:
    ///   - apiKey: API密钥
    ///   - params: 多模态请求参数
    ///   - completion: 完成回调，返回连接是否成功及错误信息
    public func start(apiKey: String, params: MultiModalRequestParam, completion: @escaping (Bool, TYError?) -> Void )
```

#### **3** startSpeech

通知服务端开始上传音频，注意需要在Listening状态才可以调用。只需要在push2talk/tap2talk模式下调用。

```
/// 开始说话（按下说话模式）
    public func startSpeech()
```

#### **4** sendAudioData

通知服务端上传音频。

```
/// 发送音频数据
    /// - Parameters:
    ///   - data: 音频数据指针
    ///   - length: 数据长度
    /// - Returns: 状态码
    public func sendAudioData(data: UnsafeMutablePointer<UInt8>, length: Int32) -> Int32?
```

#### **5** stopSpeech

通知服务端结束上传音频。只需要在push2talk模式下调用。

```
/// 停止说话（按下说话模式）
    public func stopSpeech()
```

#### **6 interrupt**

通知服务端，客户端需要打断当前交互，开始说话。会返回RequestAccepted。

```
// 中断当前对话
    /// - Parameter completion: 完成回调，返回中断是否成功
    public func interrupt(completion: ((Bool) -> Void)? = nil)
```

#### **7** sendLocalRespondingStarted

通知服务端，客户端开始播放tts音频。

```
/// 发送响应开始信号
    public func sendLocalRespondingStarted()
```

#### **8** sendLocalRespondingEnded

通知服务端，客户端结束播放tts音频。

```
/// 发送响应结束信号
    public func sendLocalRespondingEnded()
```

#### **9 stop**

结束当前轮次对话。断开服务端连接。

```
/// 断开连接
    public func stop()
```

#### **10** requestToRespond

端侧主动通过文本发起tts语音合成，或者向服务端发起图片等其他请求。

```
/// 请求响应
    /// - Parameters:
    ///   - type: 请求类型
    ///   - text: 请求文本
    ///   - params: 附加参数
    public func requestToRespond(type:String, text:String, params:[String : Any])
```

#### **11** updateInfo

更新参数信息等操作。

```
/// 更新信息
    /// - Parameter params: 更新参数
    public func updateInfo(params:[String : Any])
```

### Callback

提供给用户层的回调函数。

```
/// 服务端建联成功回调
    public var onConnected: (() -> Void)?
    
    /// 对话服务协议完成，可以开始说话的回调
    public var onConversationStarted: (() -> Void)?
    
    /// 音频事件回调。SpeechStarted/SpeechEnded/RespondingStarted/RespondingEnded
    public var onConversationEvent: ((DialogEvent) -> Void)?
    
    /// Idle/Listening/Thinking/Responding状态转换回调
    public var onConversationStatechanged: ((DialogState) -> Void)?
    
    /// 收到对话文本回调,包含用户识别内容和大模型回复内容
    public var onMessageReceived: (([String: Any]?, ResponsetMessageType) -> Void)?
    
    /// 错误回调
    public var onErrorReceived: ((TYError) -> Void)?
    
    /// 音量变化回调,RTC 链路支持
    public var onVolumeChanged: ((Float, TYVolumeSourceType) -> Void)?
    
    /// 发送第一帧视频，视频模式回调，RTC 链路支持
    public var onFirstVideoPacketSent: (() -> Void)?
    
    /// 性能数据回调
    public var onPerformaceDataReceived: ((TYChatPerformace) -> Void)?
    
    /// 连接状态变化回调，RTC链路支持
    public var onConnectionStatusChanged: ((RTCConnectionStatus) -> Void)?
    
    /// 录音数据回调，RTC链路支持
    public var onRecorderData:  ((UnsafeMutablePointer<UInt8>, Int32) -> Void)?
    
    /// 合成音频数据回调
    public var onSynthesizedData:  ((UnsafeMutablePointer<UInt8>, Int32) -> Void)?
```

### MultiModalRequestParam

请求参数类

请求参数均支持builder模式设置参数，参数的值和说明参考如下。以下是客户端需要/可选配置的参数。

#### **Start建联请求参数**

一级参数

二级参数

三级参数

四级参数

类型

是否必选

说明

input

workspace\_id

string

是

用户业务空间id

app\_id

string

是

客户在管控台创建的应用id，可以根据值规律确定使用哪个对话系统

dialog\_id

string

否

对话id，如果传入表示接着聊

parameters

upstream

type

string

是

上行类型：

AudioOnly 仅语音通话

AudioAndVideo 上传视频

mode

string

否

客户端使用的模式，可选项：

-   push2talk
    
-   tap2talk
    
-   duplex
    

默认tap2talk

audio\_format

string

否

音频格式，支持pcm，opus，默认为pcm

downstream

voice

string

否

合成语音的音色

sample\_rate

int

否

合成语音的采样率，默认采样率24000Hz

intermediate\_text

string

否

控制返回给用户那些中间文本：

transcript 返回用户语音识别结果

dialog 返回对话系统回答中间结果

可以设置多种，以逗号分割，默认为transcript

audio\_format

string

否

音频格式，支持pcm，mp3，默认为pcm

client\_info

user\_id

string

是

终端用户id，用来做用户相关的处理

device

uuid

string

否

客户端全局唯一的id，需要用户自己生成，传入SDK

network

ip

string

否

调用方公网ip

location

latitude

string

否

调用方维度信息

longitude

string

否

调用方经度信息

city\_name

string

否

调用方所在城市

biz\_params

user\_defined\_params

object

否

其他需要透传给agent的参数

user\_defined\_tokens

object

否

透传agent所需鉴权信息

tool\_prompts

object

否

透传agent所需prompt

#### **RequestToRespond 请求参数**

一级参数

二级参数

三级参数

类型

是否必选

说明

input

type

string

是

服务应该采取的交互类型：

transcript 表示直接把文本转语音

prompt 表示把文本送大模型回答

text

string

是

要处理的文本，可以是""空字符串，非null即可

parameters

images

list\[\]

否

需要分析的图片信息

biz\_params

object

否

与Start消息中biz\_params相同，传递对话系统自定义参数。RequestToRespond的biz\_params参数只在本次请求中生效。

#### **UpdateInfo 请求参数**

一级参数

二级参数

三级参数

类型

是否必选

说明

parameters

images

list\[\]

否

图片数据

client\_info

status

object

否

客户端当前状态

biz\_params

object

否

与Start消息中biz\_params相同，传递对话系统自定义参数

### **对话状态说明（**DialogState**）**

voicechat服务有LISTENING、THINKING、RESPONDING三个状态，分别代表：

```
IDLE("Idle"), 系统尚未建立连接
LISTENING("Listening"), 表示机器人正在监听用户输入。用户可以发送音频。
THINKING("Thinking"),表示机器人正在思考。
RESPONDING("Responding")表示机器人正在生成语音或语音回复中。
```

### **对话LLM输出结果**

对话结果通过`onMessageReceived` 回调，格式如下。

一级参数

二级参数

三级参数

类型

是否必选

说明

output

event

string

是

事件名称如：RequestAccepted

dialog\_id

string

是

对话id

round\_id

string

是

本轮交互的id

llm\_request\_id

string

是

调用llm的request\_id

text

string

是

系统对外输出的文本，流式**全量**输出

spoken

string

是

合成语音时使用的文本，流式全量输出

finished

bool

是

输出是否结束

extra\_info

object

否

其他扩展信息，目前支持：

commands: 命令字符串

agent\_info: 智能体信息

tool\_calls: 插件返回的信息

dialog\_debug: 对话debug信息

timestamps: 链路中各节点时间戳

## **调用交互时序图**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8131377471/p957947.png)

## **调用示例**

### **初始化对话参数**

调用MultiModalRequestParam类中的各子类的builder方法构建参数。

```
var params = MultiModalRequestParam{ multiBuilder in
            multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                upstreamBuilder.mode = DialogMode.duplex.rawValue
                upstreamBuilder.type = "AudioOnly"
            })
            multiBuilder.clientInfo = MultiModalRequestParam.ClientInfo(builder: {
                clientInfoBuilder in
                clientInfoBuilder.userId = "test-ios-user"
                clientInfoBuilder.device = MultiModalRequestParam.ClientInfo.Device(uuid: "12345")
            })
            multiBuilder.downStream = MultiModalRequestParam.DownStream(builder: {
                downStreamBuilder in
                downStreamBuilder.sampleRate = 48000
            })
        }
```

### **创建**MultiModalDialog对象

```
self.conversation = MultiModalDialog(url: self.HOST, chainMode: self.chain,  workSpaceId:self.WORKSPACE_ID ,
appId: self.APP_ID, mode: DialogMode.duplex)
```

### **完整调用示例**

```
//
//  ChatViewController.swift
//  ChatViewController
//
//  Created by songsong.sss on 2025/3/24.
//

import UIKit
import multimodal_dialog
import SnapKit
import AVFoundation

class ChatViewController: UIViewController {
    let videoView = UIView() //视频预览流窗口
    var HOST = ""
    var API_KEY = ""
    var WORKSPACE_ID = ""
    var APP_ID = ""
    var chain = ChainMode.WebSocket
    var isconnected : Bool
    var conversation:MultiModalDialog?
    var isInDialog = false
    var audioRecorder: TYAudioRecorder?
    var audioPlayer: AudioPlayer?
    var image_url: String?
    
    
    
    lazy var titleLabel1: UILabel = createLabel(text: "用户说:")
    lazy var titleLabel2: UILabel = createLabel(text: "AI 说:")
    lazy var titleLabel3: UILabel = createLabel(text: "")
    
    lazy var textView1: UITextView = createTextField()
    lazy var textView2: UITextView = createTextField()
    lazy var textView3: UITextView = createTextField()
    
    private let buttonStack: UIStackView = {
            let stack = UIStackView()
            stack.axis = .horizontal
            stack.spacing = 20
            stack.distribution = .fillEqually
            return stack
        }()
        
    private let refreshButton: UIButton = {
            let btn = UIButton(type: .system)
            btn.setTitle("刷新内容", for: .normal)
            btn.backgroundColor = .systemBlue
            btn.tintColor = .white
            btn.layer.cornerRadius = 8
            return btn
        }()
        
    private let submitButton: UIButton = {
            let btn = UIButton(type: .system)
            btn.setTitle("提交内容", for: .normal)
            btn.backgroundColor = .systemGreen
            btn.tintColor = .white
            btn.layer.cornerRadius = 8
            return btn
        }()

    
    init(){
        self.isconnected = false
        super.init(nibName: nil, bundle: nil)
    }
    
    public func updateParam(url: String, apiKey: String , workSpaceId: String, appId: String, chain: String ,image_url:String){
        self.HOST = url
        self.API_KEY = apiKey
        self.image_url = image_url
        self.WORKSPACE_ID = workSpaceId
        self.APP_ID = appId
        if chain.lowercased() == "websocket" {
            self.chain = ChainMode.WebSocket
            self.audioRecorder = TYAudioRecorder()
            self.audioRecorder?.setup(sampleRate: 16000, numOfChannels: 1, bitsPerChannel: 16)
            self.audioRecorder?.delegate = self
            
            self.audioPlayer = AudioPlayer()
            self.audioPlayer?.delegate = self
        }else{
            self.chain = ChainMode.RTC
        }
        self.conversation = MultiModalDialog(url: self.HOST, chainMode: self.chain,  workSpaceId:self.WORKSPACE_ID ,
                                             appId: self.APP_ID, mode: DialogMode.duplex)
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        print("==================viewDidLoad")
        setupDialogCallbacks()
        
        //视频模式页面配置
        if self.chain == ChainMode.RTC {
            view.addSubview(videoView)
            videoView.backgroundColor = .white
            
            videoView.snp.makeConstraints { make in
                make.edges.equalToSuperview()
            }
            
            videoView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(videoViewTapped)))
        }else {
        //音频模式页面配置
            setupUI()
        }
        //启动连接
        connect()
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        TYLogger.shared.debug("==========viewWillDisappear")
        self.isInDialog = false
        self.audioPlayer?.stop()
        self.audioRecorder?.stopRecorder(shouldNotify: false)
        self.conversation?.stop()
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        TYLogger.shared.debug("==========viewDidDisappear")
    }
    
    func connect(){
        self.conversation?.stop()
        isInDialog = false
        
        var params = MultiModalRequestParam{ multiBuilder in
            multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                upstreamBuilder.mode = DialogMode.duplex.rawValue
                upstreamBuilder.type = "AudioAndVideo"
            })
            multiBuilder.clientInfo = MultiModalRequestParam.ClientInfo(builder: {
                clientInfoBuilder in
                clientInfoBuilder.userId = "test-ios-user"
                clientInfoBuilder.device = MultiModalRequestParam.ClientInfo.Device(uuid: "12345")
            })
            multiBuilder.downStream = MultiModalRequestParam.DownStream(builder: {
                downStreamBuilder in
                downStreamBuilder.sampleRate = 48000
            })
        }
        
        self.conversation?.start(apiKey:self.API_KEY, params: params, completion: { success, error in
            if success {
                print("success")
                self.isconnected = true
            }else {
                self.isconnected = false
                if let e = error {
                    print("连接失败，错误：\(String(describing: error))")
                } else {
                    print("连接失败，无错误信息")
                }
            }})
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    
    // 必须使用 @objc 标记，因为这个方法需要暴露给 Objective-C 运行时
    @objc func videoViewTapped() {
        TYLogger.shared.debug("videoViewTapped")
    }
    
    deinit{
        self.conversation?.stop()
    }
    
    
    private func setupDialogCallbacks() {
        self.conversation?.onConnected = {
            print("callback: onConnectionReady ")
        }
        
        self.conversation?.onVolumeChanged = { volume , type in
        }
        
        self.conversation?.onConversationStarted = {
            TYLogger.shared.debug("callback: onConversationStarted")
            //RTC 进入视频模式
            if self.chain == ChainMode.RTC {
                self.conversation?.requestToRespond(type: "prompt", text: "", params: self.createVideoChatParams())
            }
        }
        
        self.conversation?.onConversationEvent = { event in
            switch event{
            case .RespondingStarted:
                self.conversation?.sendLocalRespondingStarted()
                break
            case .RespondingEnded:
                //结束发送tts数据
                self.audioPlayer?.finishFeed(true)
                break
            case .SpeechStarted:
                break
            case .SpeechEnded:
                if self.chain != ChainMode.RTC {
                    self.audioRecorder?.stopRecorder(shouldNotify: false)
                }
                break
            default:
                break
            }
            print("callback: onConversationEvent ",event)
        }
        
        self.conversation?.onMessageReceived = { message, type in
            let payload = message?["payload"] as? [String: Any]
            let output = payload?["output"] as? [String: Any]
            
            
            let dialogId = output?["dialog_id"] as? String
            var debug_info = ("dialog_id:").appending(dialogId ?? "")
            if type == ResponsetMessageType.speaking {
                let text = output?["text"] as? String
                DispatchQueue.main.async {
                    self.textView1.text = text
                }
                
            }else{
                let spoken = output?["spoken"] as? String
                let llm_request_id = output?["llm_request_id"] as? String
                let round_id = output?["round_id"] as? String
                
                DispatchQueue.main.async {
                    self.textView2.text = spoken
                }
                self.handleCommand(output: output)
                debug_info = debug_info.appending("\n llm_request_id:").appending(llm_request_id ?? "")
                debug_info = debug_info.appending("\n round_id:").appending(round_id ?? "")
            }
            DispatchQueue.main.async {
                self.textView3.text = debug_info
            }
        }
        
        self.conversation?.onConversationStatechanged = {state in
            DispatchQueue.main.async {
                self.titleLabel3.text = state.rawValue
            }
            
            switch state {
            case .idle:
                break
            case .listening:
                print("camera::::", self.conversation?.getCurrentCameraDirection())
                if self.chain != ChainMode.RTC {
                    self.audioRecorder?.startRecorder()
                }
                break
            case .responding:
                break
            case .thinking:
                break
            }
            print("callback: onConversationStatechanged ",state)
        }
        self.conversation?.onErrorReceived = { err in
            print("callback: onErrorReceived: ",err.key, err.message )
            if(err.key.hasPrefix("RTCException.")) {
            }
        }
        
        self.conversation?.onFirstVideoPacketSent = {
            print("callback: onFirstVideoPacketSent")
        }
        
        self.conversation?.onConnectionStatusChanged = {
            state in
            print("onConnectionStatusChanged ::::::" ,state)
            switch state{
            case .failed :
                self.conversation?.stop()
                break
            case .inited:
                break
            case .disconnected:
                break
            case .connected:
                print("==================connected")
                self.isInDialog = true
                //设置视频显示
                if self.chain == ChainMode.RTC {
                    DispatchQueue.main.async {
                        self.conversation?.setupLocalView(self.videoView, config: TYVideoConfig(fps: 24, width: 480, height: 640, bitrate: 0))
                        self.conversation?.publishLocalVideo()
                    }
                }
                
                break
            case .connecting:
                break
            case .reconnecting:
                break
            @unknown default:
                break
            }
            
        }
        
        self.conversation?.onSynthesizedData = { data, len in
            let audio = Data(bytes: UnsafeRawPointer(data), count: Int(len))
            TYLogger.shared.info("process \(len)")
            self.audioPlayer?.process(audioByte:data, length:Int(len))
        }
            
    }
    
    //RTC only
    private func createVideoChatParams() -> [String: Any]{
        var video:[String: Any] = [
            "action":"connect",
            "type" : "voicechat_video_channel"
        ]
        var videos = [video]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                bizBuilder in
                bizBuilder.videos = videos
            })
        }
        return updateParam.parameters
        
    }
    
    //for VQA
    private func createImageParams() -> [String: Any]{
        var imageObject:[String: Any] = [
            "type":"url",
            "value":self.image_url ?? ""
        ]
        var images = [imageObject]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.clientInfo = MultiModalRequestParam.ClientInfo(builder: {
                clientInfoBuilder in
                clientInfoBuilder.userId = "test-ios-user"
                clientInfoBuilder.device = MultiModalRequestParam.ClientInfo.Device(uuid: "12345")
            })
            multiBuilder.images = images
        }
        return updateParam.parameters
        
    }
    
    //handle command
    private func handleCommand(output: [String: Any]?)-> Void {
        
    }
    
    
    // 创建标签的辅助方法
    private func createLabel(text: String) -> UILabel {
        let label = UILabel()
        label.text = text
        label.font = UIFont.systemFont(ofSize: 16, weight: .medium)
        label.textAlignment = .right
        label.setContentHuggingPriority(.defaultHigh, for: .horizontal)
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }
    
    // 创建文本框的辅助方法
    private func createTextField() -> UITextView {
        let tv = UITextView()
        tv.layer.cornerRadius = 8
        tv.layer.borderColor = UIColor.systemGray4.cgColor
        tv.layer.borderWidth = 1
        tv.font = UIFont.systemFont(ofSize: 14)
        tv.isScrollEnabled = false
        tv.autocorrectionType = .no
        return tv
    }
    
    private func setupUI() {
            view.backgroundColor = .white
            view.addSubview(titleLabel1)
            view.addSubview(textView1)
            view.addSubview(titleLabel2)
            view.addSubview(textView2)
            view.addSubview(textView3)
            view.addSubview(titleLabel3)
            view.addSubview(buttonStack)
            
            buttonStack.addArrangedSubview(refreshButton)
            buttonStack.addArrangedSubview(submitButton)
            
            // AutoLayout 约束
            let safeArea = view.safeAreaLayoutGuide
            let padding: CGFloat = 20
            
            titleLabel1.translatesAutoresizingMaskIntoConstraints = false
            textView1.translatesAutoresizingMaskIntoConstraints = false
            titleLabel2.translatesAutoresizingMaskIntoConstraints = false
            textView2.translatesAutoresizingMaskIntoConstraints = false
            textView3.translatesAutoresizingMaskIntoConstraints = false
            titleLabel3.translatesAutoresizingMaskIntoConstraints = false
            buttonStack.translatesAutoresizingMaskIntoConstraints = false
            
            NSLayoutConstraint.activate([
                titleLabel1.topAnchor.constraint(equalTo: safeArea.topAnchor, constant: padding),
                titleLabel1.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                titleLabel1.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                
                textView1.topAnchor.constraint(equalTo: titleLabel1.bottomAnchor, constant: 8),
                textView1.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                textView1.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                textView1.heightAnchor.constraint(greaterThanOrEqualToConstant: 100),
                
                titleLabel2.topAnchor.constraint(equalTo: textView1.bottomAnchor, constant: padding),
                titleLabel2.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                titleLabel2.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                
                textView2.topAnchor.constraint(equalTo: titleLabel2.bottomAnchor, constant: 8),
                textView2.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                textView2.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                textView2.heightAnchor.constraint(greaterThanOrEqualToConstant: 100),
                
                textView3.topAnchor.constraint(equalTo: textView2.bottomAnchor, constant: 8),
                textView3.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                textView3.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                textView3.heightAnchor.constraint(greaterThanOrEqualToConstant: 100),
                
                titleLabel3.topAnchor.constraint(equalTo: textView3.bottomAnchor, constant: padding),
                titleLabel3.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                titleLabel3.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                
                
                buttonStack.bottomAnchor.constraint(equalTo: safeArea.bottomAnchor, constant: -padding),
                buttonStack.leadingAnchor.constraint(equalTo: safeArea.leadingAnchor, constant: padding),
                buttonStack.trailingAnchor.constraint(equalTo: safeArea.trailingAnchor, constant: -padding),
                buttonStack.heightAnchor.constraint(equalToConstant: 50)
            ])
        }
    
}

extension [String: Any] {
    func toUTF8String() -> String? {
        do {
            let data = try JSONSerialization.data(withJSONObject: self, options: .prettyPrinted)
            return String(data: data, encoding: .utf8)
        } catch {
            return nil
        }
    }
}

extension ChatViewController: TYAudioRecorderDelegate {
    /// Recorder启动回调，在主线程中调用
    func recorderDidStart(){
        TYLogger.shared.info("recorderDidStart")
    }
    
    /// Recorder停止回调，在主线程中调用
    func recorderDidStop(){
        TYLogger.shared.info("recorderDidStop")
    }
    
    /// Recorder收录到数据，通常涉及VAD及压缩等操作，为了避免阻塞主线，
    /// 因此将在AudioQueue的线程中调用，注意线程安全！！！
    func voiceRecorded(_ buffer: UnsafeMutablePointer<UInt8>, length: Int32){
//        TYLogger.shared.debug("voiceRecorded \(length)")
        self.conversation?.sendAudioData(data: buffer, length: length)
        
    }
    
    /// 录音机无法打开或其他错误的时候会回调
    func recorderDidFail(_ error: Error?){
        TYLogger.shared.error("recorderDidFail")
    }
}

//播放器回调
extension ChatViewController:AudioPlayerDelegate {
    func playDone() {
        self.conversation?.sendLocalRespondingEnded()
        
    }
}
```

#### **异常处理**

-   服务端错误
    

错误码为string类型，前缀为`"VoiceChat."`， 如`"VoiceChat.40000000"`。

**错误码-服务端错误**

**错误名称**

**说明**

40000000

ClientError

客户端错误

40000001

InvalidParameter

参数不合规，如参数缺失

40000002

DirectiveNotSupported

指令不支持，如指令名称错误

40000003

MessageInvalid

指令不合规，如指令格式错误

40000004

ConnectError

连接错误，如客户端或数字人RTC退出

40010000

AccessDenied

拒绝访问

40010001

UNAUTHORIZED

未授权

40020000

DataInspectionFailed

输入或输出触发绿网

50000000

InternalError

服务端内部错误，联系服务端排查

50000001

UnknownError

服务端内部未知错误，联系服务端排查

50010000

InternalAsrError

asr内部错误

50020000

InternalLLMError

大模型内部错误

50030000

InternalSynthesizerError

tts内部错误

-   客户端错误
    

**错误码-客户端错误**

**说明**

PremissionFailed

获取录音录像权限失败

RTC.AuthFailed

RTC链路鉴权错误

RTC.JoinChannelFailed

加入RTCChannel失败

VoiceChat.ConversationFailed

对话服务请求失败

## **更多SDK接口使用说明**

### **双工交互**

移动端iOS SDK支持Duplex 双工交互模式。 在双工交互模式下，SDK支持在播放语音合成回复的同时，输入录音数据。当用户在此时说话时，服务会自动打断当前播报数据返回 (客户端播放器缓存需要应用层处理)，并开始新的回复。

双工交互需要实现回声消除（AEC，Acoustic Echo Cancellation），iOS SDK内置了回声消除算法。当您需要使用双工交互时，仍需要您进行必要的配置。

-   输入麦克风录音音频
    

请将实时录音获取的音频数据通过如下接口传入SDK。

```
self.conversation?.sendAudioData(data: data, length: length)
```

-   输入参考通道音频
    

请将实时播放的音频数据通过如下接口传入SDK。注意传入数据需要保证与当前播放数据一致。

```
self.conversation?.sendRefData(data: data, length: length)
```

### **通过 RTC 链路请求LiveAI**

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过iOS 全功能版本SDK， 您可以在应用中实现视频通话的功能。 本 SDK 内置了 RTC 协议，实现音视频双工的实时交互。

-   LiveAI调用时序
    

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例
    

完整代码请参考 "环境和依赖" 章节下载的 iOS Demo。

选择 RTC 链路启动后，会默认开启 RTC 内部的视频录制， 与服务端建立视频通话。

```
//1. 设置交互类型为AudioAndVideo
multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                upstreamBuilder.mode = mode.rawValue
                upstreamBuilder.type = "AudioAndVideo"
            })
//2. 初始化 MultiModalDialog 实例，选择 RTC 链路 chainMode: ChainMode.RTC
self.conversation = MultiModalDialog(url: self.HOST, chainMode: self.chain,  workSpaceId:self.WORKSPACE_ID ,
                                             appId: self.APP_ID, mode: mode)

//3. 在建联后发送voicechat_video_channel 请求
private func createVideoChatParams() -> [String: Any]{
        var video:[String: Any] = [
            "action":"connect",
            "type" : "voicechat_video_channel"
        ]
        var videos = [video]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                bizBuilder in
                bizBuilder.videos = videos
            })
        }
        return updateParam.parameters
}

//4. 开始音视频交互。处理交互流程。注意 demo 中有关ChainMode.RTC 类型的特殊处理。
//完整代码请参考示例代码。
```

### **通过 Websocket 链路请求LiveAI**

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过iOS 全功能版本SDK， 您也可以在Websocket链路中通过自行录制视频帧的方式来调用视频通话功能。

注意：通过 Websocket 调用 LiveAI发送图片只支持base64编码，每张图片的大小在180K以下。

-   LiveAI调用时序
    

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例
    

请注意参照如下的调用流程实现 通过Websocket 协议调用 LiveAI。

```
//1. 设置交互类型为AudioAndVideo
multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                upstreamBuilder.mode = mode.rawValue
                upstreamBuilder.type = "AudioAndVideo"
            })
//2. 初始化 MultiModalDialog 实例。选择WebSocket 链路 chainMode: ChainMode.WebSocket
self.conversation = MultiModalDialog(url: self.HOST, chainMode: self.chain,  workSpaceId:self.WORKSPACE_ID ,
                                             appId: self.APP_ID, mode: mode)

//3. 在建联后主动发起voicechat_video_channel 请求. 
//或者通过语音指令”打开视频通话“返回的”open_videochat“指令触发createVideoChatParams
private func createVideoChatParams() -> [String: Any]{
        var video:[String: Any] = [
            "action":"connect",
            "type" : "voicechat_video_channel"
        ]
        var videos = [video]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                bizBuilder in
                bizBuilder.videos = videos
            })
        }
        return updateParam.parameters
}

//4. 每 500ms 提交一张视频帧照片数据，注意图片尺寸小于 180KB。
/**
 * DEMO 中通过调用本地图片演示在 websocket 链路中实现 liveAI
 * 您集成在应用中需要自行采集视频或者图片，实现每500ms发送一帧数据。
 */
//开始后台执行发送图片的操作
func startPeriodicExecution() {
    timer = DispatchSource.makeTimerSource(queue: queue)
    timer?.schedule(deadline: .now(), repeating: .milliseconds(500))
    timer?.setEventHandler { [weak self] in
        self?.sendLocalImageBase64()
    }
    timer?.resume()
}

//update image base64
private func sendLocalImageBase64() {
    print("send_local_image_base64() called : \(Thread.current)")
    var imageObjectBase64:[String: Any] = [
                "type":"base64",
                "value":getImageAsBase64FromAssets(imageName:"bridge") //请实现图片 base64 编码
    ]
    var images = [imageObjectBase64]
    
    var updateParam = MultiModalRequestParam{ multiBuilder in
        multiBuilder.images = images
    }
    
    self.conversation?.updateInfo(params: updateParam.parameters)
    
}
```

### **VQA交互**

VQA 是对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本请求拍照意图触发**"visual\_qa"**拍照指令。

当收到拍照指令后， 发送图片链接或者base64数据（支持小于180KB的图片）。

建联后发起拍照请求。

```
//创建图片请求参数
    private func createImageParams() -> [String: Any]{
        var imageObject:[String: Any] = [
            "type":"url",
            "value":self.image_url ?? ""
        ]
        //或者使用图片base 64编码直接上传。注意只支持180KB 以下大小图片
        var imageObjectBase64:[String: Any] = [
                    "type":"base64",
                    "value":"imagebase64"
        ]
        var images = [imageObject]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.images = images
        }
        return updateParam.parameters
    }
//发起请求
self.conversation?.requestToRespond(type: "prompt", text: "", params: self.createImageParams())
```

### **文本合成TTS**

```
self.conversation?.requestToRespond(type: "prompt", text: "幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。", params:[:])
```

### **自定义提示词变量和传值**

-   在管控台项目【提示词】配置自定义变量。
    

如下图示例，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975545.png)

-   在代码中设置变量。
    

如下示例，设置`"user_name" = "大米"`。

```
//在请求参数构建中传入biz_params.user_prompt_params
var promptParam = ["user_name" : "大米"]
var params = MultiModalRequestParam{ multiBuilder in
            multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                bizBuilder in
                bizBuilder.userPromptParams = promptParam
            })
}
```

-   请求回复
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975544.png)
