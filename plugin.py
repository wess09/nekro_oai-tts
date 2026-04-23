from pydantic import Field

from nekro_agent.api.plugin import ConfigBase, NekroPlugin

plugin = NekroPlugin(
    name="MiMo 语音合成",
    module_name="mimo_tts",
    description="调用 MiMo TTS 接口合成语音，并发送到当前会话。",
    version="0.1.1",
    author="AzurLane",
    url="https://api.xiaomimimo.com/",
    support_adapter=["onebot_v11"],
    allow_sleep=True,
    sleep_brief="用于将文本合成为语音并发送成语音消息，仅在需要语音回复时激活。",
)


@plugin.mount_config()
class MiMoTTSConfig(ConfigBase):
    MIMO_API_KEY: str = Field(
        default="",
        title="MiMo API Key",
        description="小米 MiMo 平台的 API Key。",
    )
    BASE_URL: str = Field(
        default="https://api.xiaomimimo.com/v1",
        title="API Base URL",
        description="MiMo OpenAI 兼容接口基础地址，默认带 /v1。",
    )
    MODEL: str = Field(
        default="mimo-v2.5-tts",
        title="模型",
        description="支持 mimo-v2.5-tts, mimo-v2.5-tts-voicedesign, mimo-v2.5-tts-voiceclone。",
    )
    DEFAULT_VOICE: str = Field(
        default="冰糖",
        title="默认音色",
        description="mimo-v2.5-tts 模型可用。 voiceclone 和 voicedesign 模型无需填写。",
    )
    VOICE_CLONE_SOURCE: str = Field(
        default="",
        title="音色克隆源 (Data URI)",
        description="使用 mimo-v2.5-tts-voiceclone 模型时，在此处填写音频的 Base64 Data URI。格式: data:audio/mpeg;base64,UklGRi...",
    )
    VOICE_OPTIONS_HINT: str = Field(
        default=(
            "冰糖: 中文女声\n"
            "茉莉: 中文女声\n"
            "苏打: 中文男声\n"
            "白桦: 中文男声\n"
            "Mia: 英文女声\n"
            "Chloe: 英文女声\n"
            "Milo: 英文男声\n"
            "Dean: 英文男声"
        ),
        title="音色说明",
        description="提示 AI 和管理员可用音色及适用场景。",
    )
    DEFAULT_USER_MESSAGE: str = Field(
        default="",
        title="默认 User Message",
        description="调用 mimo-v2.5-tts 模型时，用于控制风格的默认 user 角色消息。",
    )
    AUDIO_TAG_EXAMPLES: str = Field(
        default=(
            "利用 [音频标签] 对文本进行精细化声音控制。必须严格遵守以下标签规范，严禁使用列表以外的任何词汇作为标签内容，确保标签简单、纯粹。"
            "一、 标签词汇表（严禁超出此范围）："
            "语气： 平淡、严肃、轻快、低沉、高昂、温柔、沙哑、小声。"
            "情绪： 开心、难过、焦急、冷静、疲惫、无奈、惊喜、失落。"
            "生理声音： 深呼吸、喘息、咳嗽、清嗓子、笑声、哭腔、叹气。"
            "节奏控制： 语速加快、语速放慢、沉默片刻。"
            "二、 执行准则（必须严格遵守）："
            "封闭式选词： 标签内仅能包含上述列表中的词汇。"
            "纯声音控制： 严禁出现动作描述。"
            "高频覆盖： 每段话或每个逻辑停顿点，必须使用 1 个 [标签]。"
            "格式规范： 所有标签必须使用半角方括号 []，放在句首。"
            "三、 标签使用示例（参考此格式）："
            "[平淡,清嗓子]明天早上的会议取消了。"
            "[焦急,语速加快]还有五分钟就要迟到了，快点出发吧。"
            "[深呼吸,冷静]事情已经发生了，我们先看看补救措施。"
            "[无奈,叹气]算了，就这样吧，反正也改不了了。"
            "[温柔,语速放慢]辛苦了，早点回去休息吧。"
        ),
        title="音频标签示例",
        description="注入给 AI 的细粒度音频标签示例。",
    )
    AUDIO_FORMAT: str = Field(
        default="wav",
        title="输出格式",
        description="建议使用 wav，便于直接发送为语音消息。",
    )
    REQUEST_TIMEOUT: int = Field(
        default=90,
        title="超时秒数",
        description="合成请求超时时间。",
    )
    ENABLE_PROXY_ACCESS: bool = Field(
        default=False,
        title="启用代理访问",
        description="启用后通过系统默认代理访问 MiMo API。",
    )


config = plugin.get_config(MiMoTTSConfig)
