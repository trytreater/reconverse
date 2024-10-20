import abc


class LLM(abc.ABC):
    def generate(
        self,
        instructions: str,
        prompt: str,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> str:
        raise NotImplementedError
