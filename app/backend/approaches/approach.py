class Document:
    id: Optional[str]  # The ID of the document.
    content: Optional[str]  # The content of the document.
    embedding: Optional[List[float]]  # The vector embedding of the document.
    image_embedding: Optional[List[float]]  # The vector embedding of the document's image.
    category: Optional[str]  # The category of the document.
    sourcepage: Optional[str]  # The source page of the document.
    sourcefile: Optional[str]  # The source file of the document.
    oids: Optional[List[str]]  # The list of object IDs associated with the document.
    groups: Optional[List[str]]  # The list of groups the document belongs to.
    captions: List[QueryCaptionResult]  # The list of captions associated with the document.
    score: Optional[float] = None  # The search score of the document.
    reranker_score: Optional[float] = None  # The reranker score of the document.

    def serialize_for_results(self) -> dict[str, Any]:
        """
        Serializes the document object into a dictionary format suitable for displaying search results.

        Returns:
            A dictionary containing the serialized document information.
        """
        return {
            "id": self.id,
            "content": self.content,
            "embedding": Document.trim_embedding(self.embedding),
            "imageEmbedding": Document.trim_embedding(self.image_embedding),
            "category": self.category,
            "sourcepage": self.sourcepage,
            "sourcefile": self.sourcefile,
            "oids": self.oids,
            "groups": self.groups,
            "captions": (
                [
                    {
                        "additional_properties": caption.additional_properties,
                        "text": caption.text,
                        "highlights": caption.highlights,
                    }
                    for caption in self.captions
                ]
                if self.captions
                else []
            ),
            "score": self.score,
            "reranker_score": self.reranker_score,
        }

    @classmethod
    def trim_embedding(cls, embedding: Optional[List[float]]) -> Optional[str]:
        """
        Trims the vector embedding of the document to a more concise format.

        Args:
            embedding: The vector embedding of the document.

        Returns:
            The trimmed embedding as a string, or None if the embedding is empty.

        """
        if embedding:
            if len(embedding) > 2:
                # Format the embedding list to show the first 2 items followed by the count of the remaining items.
                return f"[{embedding[0]}, {embedding[1]} ...+{len(embedding) - 2} more]"
            else:
                return str(embedding)

        return None