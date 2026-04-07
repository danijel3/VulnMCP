from fastmcp import FastMCP

from vulnmcp.models.classifier import SeverityClassifier


def register(mcp: FastMCP) -> None:
    """Register severity classification tools on the MCP server."""

    classifier = SeverityClassifier()

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    def classify_severity(
        description: str, language: str | None = None
    ) -> dict:
        """Classify the severity of a vulnerability based on its description.

        Uses CIRCL's fine-tuned transformer models:
        - English descriptions: RoBERTa-base model (low/medium/high/critical)
        - Chinese descriptions: MacBERT-base model (low/medium/high)
        - Russian descriptions: ruRoBERTa-large model (low/medium/high/critical)

        Language is auto-detected from the text unless explicitly specified.

        Args:
            description: The vulnerability description text (English, Chinese, or Russian).
            language: Optional language hint — "en" for English, "zh" for Chinese,
                      "ru" for Russian. Auto-detected if omitted.

        Returns:
            A dict with: label (severity), score (confidence), model, language.
        """
        return classifier.classify(description, language=language)
