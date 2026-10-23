# 接入实时语音对话模型

让 Agent 工具自动创建并运行语音客户端，接入 Token Plan 的实时语音对话模型。

## 支持的模型

模型

能力

`qwen-audio-3.0-realtime-plus`

实时语音对话

更多模型以 [Token Plan 支持的实时语音对话模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 为准。

## 前提

-   已订阅 Token Plan。个人版在 [我的订阅（个人版）](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 获取以 `sk-sp-` 开头的 API Key；团队版在 [成员管理](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list) 分配席位后获取 API Key。
-   本地已安装 Python 3.9 及以上版本，并有可用的麦克风和扬声器。

## 步骤一：把接入指令发给 Agent 工具

展开下面的接入指令，复制后发给当前使用的 Agent 工具。它会读取已配置的 Token Plan Key、安装依赖、创建 `qwen_realtime_voice.py` 并运行，不需要手动配置 Key 或编写 Python。

接入指令（含语音客户端脚本）

```
请在当前项目接入 Token Plan 实时语音对话模型 qwen-audio-3.0-realtime-plus：

1. 使用当前 Agent 工具已配置的 Token Plan API Key（优先读取 TOKEN_PLAN_API_KEY，其次读取 ANTHROPIC_AUTH_TOKEN）。如果两者都没有，提示我先在 Agent 工具中配置 Token Plan Key。不要向我展示 Key，也不要写入文件或日志。
2. 安装依赖：pip install "websockets>=15" sounddevice certifi
3. 创建 qwen_realtime_voice.py，内容如下：

```python
#!/usr/bin/env python3
import asyncio
import base64
import json
import os
import queue
import ssl
import threading

import certifi
import sounddevice as sd
import websockets

API_KEY = os.environ.get("TOKEN_PLAN_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
if not API_KEY:
    raise SystemExit("Token Plan API Key not found. Configure it in the Agent tool first.")
WS_URL = "wss://token-plan.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.0-realtime-plus"

play_queue = queue.Queue()

def play_audio():
    with sd.RawOutputStream(samplerate=24000, channels=1, dtype="int16") as stream:
        while True:
            chunk = play_queue.get()
            if chunk is None:
                break
            stream.write(chunk)

async def receive(ws):
    transcript = []
    async for message in ws:
        event = json.loads(message)
        event_type = event["type"]
        if event_type == "conversation.item.input_audio_transcription.completed":
            print(f"\n[你说] {event.get('transcript', '')}", flush=True)
        elif event_type == "response.audio.delta":
            play_queue.put(base64.b64decode(event["delta"]))
        elif event_type == "response.audio_transcript.delta":
            transcript.append(event.get("delta", ""))
        elif event_type == "response.audio_transcript.done":
            print(f"[AI] {''.join(transcript)}", flush=True)
            transcript.clear()
        elif event_type == "error":
            print(f"[错误] {event}", flush=True)

async def send_mic(ws):
    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue()

    def callback(indata, frames, time_info, status):
        loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        blocksize=1600,
        callback=callback,
    ):
        print("开始说话，按 Ctrl+C 结束。", flush=True)
        while True:
            chunk = await audio_queue.get()
            await ws.send(
                json.dumps(
                    {
                        "type": "input_audio_buffer.append",
                        "audio": base64.b64encode(chunk).decode(),
                    }
                )
            )

async def main():
    context = ssl.create_default_context(cafile=certifi.where())
    async with websockets.connect(
        WS_URL,
        ssl=context,
        additional_headers={"Authorization": f"Bearer {API_KEY}"},
        max_size=None,
    ) as ws:
        await ws.recv()
        await ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "modalities": ["audio", "text"],
                        "voice": "longanqian",
                        "instructions": "你是语音助手，回答简洁自然。",
                        "input_audio_format": "pcm",
                        "output_audio_format": "pcm",
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.5,
                            "silence_duration_ms": 600,
                        },
                    },
                }
            )
        )
        threading.Thread(target=play_audio, daemon=True).start()
        await asyncio.gather(receive(ws), send_mic(ws))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        play_queue.put(None)
```

4. 使用 Bash 工具运行 python3 qwen_realtime_voice.py，timeout 设为 600000 毫秒。
5. 启动后提示“开始说话，按 Ctrl+C 结束”。
```

**说明**首次运行时，需要在系统设置中允许运行 Agent 工具的应用（如 Cursor、Terminal）访问麦克风，否则脚本收不到声音。建议使用耳机，避免扬声器播放的语音被麦克风采集，触发模型打断。

## 步骤二：开始语音对话

Agent 工具运行脚本后，看到“开始说话”提示即可说话。终端显示识别结果和模型回复，扬声器播放模型语音。按 Ctrl+C 结束会话。

**说明**Agent 工具负责安装依赖、创建脚本和启动会话。语音数据在本地客户端和 Token Plan 之间传输，不经过 Agent 工具的文本模型。

## 保存为工具扩展

需要再次使用时，让 Agent 工具把上面的指令保存为当前工具的 Skill、Slash Command 或 Agent 配置，之后通过该工具的触发方式启动。常见工具的扩展机制和路径如下：

工具

扩展机制

配置文件路径

Claude Code

Slash Command

`.claude/commands/voice-chat.md`

Codex

Skill

`~/.codex/skills/token-plan-voice/SKILL.md`

Qwen Code

Skill

`~/.qwen/skills/voice-chat/SKILL.md`

OpenCode

Agent

`.opencode/agents/voice-chat.md`

OpenClaw

Skill

`~/.openclaw/workspace/skills/token-plan-voice/SKILL.md`

Hermes Agent

Skill

`~/.hermes/skills/media/voice-chat/SKILL.md`

Qoder

Skill

`~/.qoder/skills/voice-chat/SKILL.md`

Skill 和 Agent 的 front matter 格式见 [接入多模态生成模型](https://help.aliyun.com/zh/model-studio/token-plan-multimodal-gen#tp-mm-other-tools-h)。

## 限制

-   外放时，模型语音可能被麦克风再次采集并打断，建议使用耳机。
-   Agent 工具的 Bash 调用有超时限制。长时间对话建议将脚本作为独立进程运行，或封装为 MCP server。
-   当前方案只处理语音输入和输出。
