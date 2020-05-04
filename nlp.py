import uuid

from snownlp import SnowNLP
from webthing import (
    Action,
    Event,
    Property,
    SingleThing,
    Thing,
    Value,
    WebThingServer,
    background_thread_loop,
)


class SentimentAnalysisAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(
            self, uuid.uuid4().hex, thing, "sentiment_analysis", input_=input_
        )

    async def perform_action(self):
        print(self.input)
        s = SnowNLP(self.input["text"])
        await self.thing.set_property("sentiments", s.sentiments)


class WordTokenizeAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "word_tokenize", input_=input_)

    async def perform_action(self):
        print(self.input)
        s = SnowNLP(self.input["text"])
        await self.thing.set_property("words", s.words)


class KeywordExtractionAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(
            self, uuid.uuid4().hex, thing, "keyword_extraction", input_=input_
        )

    async def perform_action(self):
        print(self.input)
        s = SnowNLP(self.input["text"])
        await self.thing.set_property("keywords", s.keywords(self.input["limit"]))


class SummarizationExtractionAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(
            self, uuid.uuid4().hex, thing, "summarization_extraction", input_=input_
        )

    async def perform_action(self):
        print(self.input)
        s = SnowNLP(self.input["text"])
        await self.thing.set_property("summarization", s.summary(self.input["limit"]))


class NLP(Thing):
    def __init__(self, id_, title):
        Thing.__init__(
            self, id_, title, ["NLP"], "A web connected nlp thing",
        )

    async def create(self):
        await self.add_property(
            Property(
                self,
                "sentiments",
                Value(1),
                metadata={
                    "@type": "SentimentsProperty",
                    "title": "Sentiments",
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Latest sentiments response from NLP",
                },
            )
        )

        await self.add_property(
            Property(
                self,
                "words",
                Value([]),
                metadata={
                    "@type": "WordsProperty",
                    "title": "Words",
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Latest words response from NLP",
                },
            )
        )

        await self.add_property(
            Property(
                self,
                "keywords",
                Value([]),
                metadata={
                    "@type": "KeyWordsProperty",
                    "title": "KeyWords",
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Latest keywords response from NLP",
                },
            )
        )

        await self.add_property(
            Property(
                self,
                "summary",
                Value([]),
                metadata={
                    "@type": "SummaryProperty",
                    "title": "Summary",
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Latest summary response from NLP",
                },
            )
        )

        await self.add_available_action(
            "sentiment_analysis",
            {
                "title": "情绪分析",
                "description": "向 NLP Thing 发送文本并判断文本的情绪",
                "input": {
                    "type": "object",
                    "required": ["text"],
                    "properties": {"text": {"type": "string"}},
                },
            },
            SentimentAnalysisAction,
        )

        await self.add_available_action(
            "word_tokenize",
            {
                "title": "分词",
                "description": "向 NLP Thing 发送文本并返回词组",
                "input": {
                    "type": "object",
                    "required": ["text"],
                    "properties": {"text": {"type": "string"}},
                },
            },
            WordTokenizeAction,
        )

        await self.add_available_action(
            "keywords_extraction",
            {
                "title": "关键词提取",
                "description": "向 NLP Thing 发送文本并提取关键词",
                "input": {
                    "type": "object",
                    "required": ["text", "limit"],
                    "properties": {
                        "text": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
            KeywordExtractionAction,
        )

        await self.add_available_action(
            "summary_extraction",
            {
                "title": "摘要提取",
                "description": "向 NLP Thing 发送文本并提取摘要",
                "input": {
                    "type": "object",
                    "required": ["text", "limit"],
                    "properties": {
                        "text": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
            SummarizationExtractionAction,
        )

        return SingleThing(self)  # MultipleThings({self.id: self}, "nlp thing")


with background_thread_loop() as loop:
    app = WebThingServer(loop, NLP("thing:nlp:1", "nlp thing").create,).create()
