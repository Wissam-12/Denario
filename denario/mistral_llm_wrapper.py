from litellm import completion

class MistralLLMWrapper:
    def __init__(
        self,
        name="mistral-small-2503",
        temperature=0.7,
        max_output_tokens=8192,
    ):
        self.name = name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.model = f"mistral/{name}"

    def stream(self, prompt: str):
        """
        Stream tokens in a LangGraph-compatible way.
        """
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
            stream=True,
        )

        for chunk in response:
            if "choices" in chunk and chunk["choices"]:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield type(
                        "Chunk",
                        (),
                        {
                            "content": content,
                            "usage_metadata": None,
                        },
                    )
