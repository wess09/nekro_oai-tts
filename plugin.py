from pydantic import Field

from nekro_agent.api.plugin import ConfigBase, NekroPlugin

plugin = NekroPlugin(
    name="MiMo 语音合成",
    module_name="mimo_tts",
    description="调用 MiMo TTS 接口合成语音，并发送到当前会话。",
    version="0.1.0",
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
        default="mimo-v2-tts",
        title="模型",
        description="当前默认支持 mimo-v2-tts。",
    )
    DEFAULT_VOICE: str = Field(
        default="mimo_default",
        title="默认音色",
        description="默认音色，可选 mimo_default/default_zh/default_en。",
    )
    VOICE_OPTIONS_HINT: str = Field(
        default=(
            "mimo_default: 通用默认音色\n"
            "default_zh: 中文女声\n"
            "default_en: 英文女声"
        ),
        title="音色说明",
        description="提示 AI 和管理员可用音色及适用场景。",
    )
    DEFAULT_STYLE: str = Field(
        default="",
        title="默认风格",
        description="可选。会拼接为 <style>风格</style> 放在待合成文本前。",
    )
    STYLE_HINT: str = Field(
        default="可选整体风格示例：开心、悲伤、生气、悄悄话、夹子音、东北话、粤语、唱歌。",
        title="风格说明",
        description="用于提示 AI 如何填写 style 参数。",
    )
    AUDIO_TAG_EXAMPLES: str = Field(
        default=(
            "可直接把细粒度音频标签写进 content 正文中，例如：\n"
            "（紧张，深呼吸）呼……冷静，冷静。不就是一个面试吗……（语速加快，碎碎念）自我介绍已经背了五十遍了，应该没问题的。加油，你可以的……（小声）哎呀，领带歪没歪？\n"
            "（极其疲惫，有气无力）师傅……到地方了叫我一声……（长叹一口气）我先眯一会儿，这班加得我魂儿都要散了。\n"
            "如果我当时……（沉默片刻）哪怕再坚持一秒钟，结果是不是就不一样了？（苦笑）呵，没如果了。\n"
            "（寒冷导致的急促呼吸）呼——呼——这、这大兴安岭的雪……（咳嗽）简直能把人骨头冻透了……别、别停下，走，快走。\n"
            "（提高音量喊话）大姐！这鱼新鲜着呢！早上刚捞上来的！哎！那个谁，别乱翻，压坏了你赔啊？！"
        ),
        title="音频标签示例",
        description="注入给 AI 的细粒度音频标签示例。",
    )
    DEFAULT_USER_MESSAGE: str = Field(
        default="",
        title="默认用户提示",
        description="可选。会作为 user 角色消息发送，帮助调整语气与风格。",
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
