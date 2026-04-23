# MiMo TTS 插件 (v2.5)

基于小米 MiMo V2.5 系列 TTS 接口的 NekroAgent 语音合成插件。

它会把文本请求发到 MiMo TTS 接口，拿到音频后直接以 QQ 语音消息形式发回当前会话。

## 主要功能

- **支持多种合成模型**：
  - `mimo-v2.5-tts`: 使用预置精品音色合成。
  - `mimo-v2.5-tts-voicedesign`: 通过文本描述设计新音色。
  - `mimo-v2.5-tts-voiceclone`: 通过音频样本克隆任意音色。
- **灵活的风格控制**：
  - 支持通过 `user` 角色消息传递自然语言指令来控制整体风格（仅限 `mimo-v2.5-tts` 模型）。
  - 支持在合成文本中直接嵌入 `[音频标签]`（如 `[小声]`、`[深呼吸]`）进行细粒度控制。
- **易于使用的命令**：
  - 提供 `/mimo_tts_speak` 命令，方便用户快速测试。
  - 提供 `/mimo_tts_help` 命令，查看详细用法。
- **完整的 AI 接口**：
  - 暴露 `send_mimo_voice` 方法给 AI，使其可以自主调用语音合成功能。

## 配置项

在 `plugin.py` 的 `MiMoTTSConfig` 类中可以修改以下配置：

- `MIMO_API_KEY`: **(必填)** 小米 MiMo 平台的 API Key。
- `MODEL`: 使用的 TTS 模型。
  - `mimo-v2.5-tts` (默认): 使用预置音色。
  - `mimo-v2.5-tts-voicedesign`: 通过文本描述设计音色。
  - `mimo-v2.5-tts-voiceclone`: 通过音频样本克隆音色。
- `DEFAULT_VOICE`: `mimo-v2.5-tts` 模型的默认音色，默认为 `冰糖`。
- `VOICE_CLONE_SOURCE`: **音色克隆专用**。用于存放音频样本的 Base64 Data URI。
- `VOICE_OPTIONS_HINT`: 可用预置音色列表，会注入给 AI 参考。
- `DEFAULT_USER_MESSAGE`: `mimo-v2.5-tts` 模型的默认风格指令（自然语言控制）。
- `AUDIO_TAG_EXAMPLES`: 音频标签的用法示例，会注入给 AI 参考。
- `AUDIO_FORMAT`: 输出音频格式，建议使用 `wav`。
- `REQUEST_TIMEOUT`: API 请求超时时间（秒）。
- `ENABLE_PROXY_ACCESS`: 是否通过系统代理访问 API。

## 使用方法

### 1. 基础用法 (预置音色)

1. 将 `MODEL` 设置为 `mimo-v2.5-tts`。
2. 使用命令 `/mimo_tts_speak 你好`，即可听到默认音色（`冰糖`）的语音。
3. AI 可以通过调用 `send_mimo_voice(content="你好", voice="茉莉")` 来切换不同音色。
4. AI 也可以通过 `send_mimo_voice(content="你好", user_message="用活泼的少女音说")` 来控制风格。

### 2. 音色设计 (文本描述)

1. 将 `MODEL` 设置为 `mimo-v2.5-tts-voicedesign`。
2. 此时 AI 调用必须提供 `user_message` 来描述音色，例如：`send_mimo_voice(content="这是我设计的声音。", user_message="一个沉稳、富有磁性的大叔音")`。

### 3. 音色克隆 (音频样本)

这是最强大的功能，可以克隆任何人的声音。

**第一步：生成音频 Data URI**

您需要将一个包含目标音色的音频文件（MP3 或 WAV）转换成 Base64 Data URI 字符串。

您可以使用在线工具（搜索 "file to base64 data uri"）或以下 Python 脚本完成转换：

```python
import base64

# 1. 将 "your_audio.mp3" 替换为您的音频文件名
file_path = "your_audio.mp3"  

# 2. 根据文件类型设置 MIME 类型 (mp3 -> "audio/mpeg", wav -> "audio/wav")
mime_type = "audio/mpeg"

try:
    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f"data:{mime_type};base64,{encoded_string}"
    print("--- 转换成功，请复制以下完整内容 ---")
    print(data_uri)
    print("------------------------------------")
except FileNotFoundError:
    print(f"错误：找不到文件 '{file_path}'。")
```

运行后，复制输出的**一整长串**以 `data:audio/...;base64,...` 开头的文本。

**第二步：修改配置**

1. 将 `MODEL` 设置为 `mimo-v2.5-tts-voiceclone`。
2. 将刚刚复制的 Data URI 字符串，完整地粘贴到 `VOICE_CLONE_SOURCE` 的 `default` 值中。

**第三步：使用**

重启应用使配置生效。现在，所有语音合成请求（如 `/mimo_tts_speak 你好`）都会使用您提供的音频样本进行音色克隆。

## 命令参考

- `/mimo_tts_speak [文本]`
  - 使用当前配置的默认模型和音色合成语音。
  - 示例: `/mimo_tts_speak [开心]今天天气真好！`
- `/mimo_tts_help`
  - 显示详细的帮助信息，包括各模型用法和主要配置项。

## AI 方法 (`send_mimo_voice`)

- **`content: str`**: (必填) 要合成的文本，可内嵌 `[音频标签]`。
- **`voice: str`**: (可选) 指定预置音色 ID（如 `冰糖`, `苏打`）。仅在 `mimo-v2.5-tts` 模型下有效。
- **`user_message: str`**: (可选)
  - 在 `mimo-v2.5-tts` 模型下，用于自然语言风格控制。
  - 在 `mimo-v2.5-tts-voicedesign` 模型下，为**必填项**，用于描述音色。
