# -*- coding: utf-8 -*-
"""Parser for model response."""
import json
from typing import Optional, Sequence, Any, Generator, Union, Tuple

from ..message import ToolUseBlock
from ..utils.common import _is_json_serializable


class ModelResponse:
    """Encapsulation of data returned by the model.

    The main purpose of this class is to align the return formats of different
    models and act as a bridge between models and agents.
    """

    def __init__(
        self,
        text: Optional[str] = None,
        reason_text: Optional[str] = None,
        embedding: Optional[Sequence] = None,
        image_urls: Optional[Sequence[str]] = None,
        raw: Any = None,
        parsed: Optional[Any] = None,
        stream: Union[
            None,
            Generator[str, None, None],
            Generator[tuple[str, str, list[ToolUseBlock]], None, None],
        ] = None,
        tool_calls: Optional[list[ToolUseBlock]] = None,
    ) -> None:
        """Initialize the model response.

        Args:
            text (`str`, optional):
                The text field.
            embedding (`Sequence`, optional):
                The embedding returned by the model.
            image_urls (`Sequence[str]`, optional):
                The image URLs returned by the model.
            raw (`Any`, optional):
                The raw data returned by the model.
            parsed (`Any`, optional):
                The parsed data returned by the model.
            stream (`Generator`, optional):
                The stream data returned by the model.
            tool_calls (`Optional[list[dict]]`, defaults to `None`):
                The tool calls made by the model.
        """
        self._text = text
        self._reason_text = reason_text
        self.embedding = embedding
        self.image_urls = image_urls
        self.raw = raw
        self.parsed = parsed
        self._stream = stream
        self.tool_calls = tool_calls
        self._is_stream_exhausted = False

    @property
    def text(self) -> Union[str, None]:
        """Return the text field. If the stream field is available, the text
        field will be updated accordingly."""
        if self._text is None:
            if self.stream is not None:
                for _, chunk in self.stream:
                    self._text = chunk
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Set the text field."""
        self._text = value

    @property
    def reason_text(self) -> Union[str, None]:
        """Return the text field. If the stream field is available, the text
        field will be updated accordingly."""
        if self._reason_text is None:
            if self.stream is not None:
                for _, chunk in self.stream:
                    self._text = chunk
        return self._text

    @reason_text.setter
    def reason_text(self, value: str) -> None:
        """Set the reason_text field."""
        self._reason_text = value

    @property
    def stream(self) -> Union[None, Generator[Tuple[bool, str], None, None]]:
        """Return the stream generator if it exists."""
        if self._stream is None:
            return self._stream
        else:
            return self._stream_generator_wrapper()

    @property
    def is_stream_exhausted(self) -> bool:
        """Whether the stream has been processed already."""
        return self._is_stream_exhausted

    def _stream_generator_wrapper(
        self,
    ) -> Generator[Tuple[bool, str], None, None]:
        """During processing the stream generator, the text field is updated
        accordingly."""
        if self._is_stream_exhausted:
            raise RuntimeError(
                "The stream has been processed already. Try to obtain the "
                "result from the text field.",
            )

        # These two lines are used to avoid mypy checking error
        if self._stream is None:
            return

        try:
            last_chunk = next(self._stream)

            for chunk in self._stream:
                if isinstance(chunk, tuple):
                    self._reason_text = chunk[0]
                    self._text = chunk[1]
                    self.tool_calls = chunk[2]
                    if (
                        self._reason_text is not None
                        and len(self._reason_text) > 0
                    ):
                        yield False, (
                            f"[Thinking]\n{self._reason_text}\n"
                            f"[Answer]\n{self._text}"
                        )
                    else:
                        yield False, self._text
                    last_chunk = chunk
                elif isinstance(chunk, str):
                    self._text = chunk
                    yield False, chunk
                    last_chunk = chunk
            if isinstance(last_chunk, tuple):
                self._reason_text = last_chunk[0]
                self._text = last_chunk[1]
                self.tool_calls = last_chunk[2]
            else:
                self._text = last_chunk
            if self._reason_text is not None and len(self._reason_text) > 0:
                yield True, (
                    f"[Thinking]\n{self._reason_text}\n"
                    f"[Answer]\n{self._text}"
                )
            else:
                yield True, self._text or ""

            return
        except StopIteration:
            return

    def __str__(self) -> str:
        if _is_json_serializable(self.raw):
            raw = self.raw
        else:
            raw = str(self.raw)

        serialized_fields = {
            "text": self.text,
            "embedding": self.embedding,
            "image_urls": self.image_urls,
            "parsed": self.parsed,
            "raw": raw,
        }
        return json.dumps(serialized_fields, indent=4, ensure_ascii=False)
