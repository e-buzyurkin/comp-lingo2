from db.models import Text, Corpus


class TextRepository:
    def __init__(self):
        pass

    def collect_text(self, text: Text):
        return {
            "id": text.id,
            "title": text.title,
            "description": text.description,
            "content": text.content,
            "corpus_id": text.corpus_id,
            "has_translation": text.has_translation_id,
        }

    def getText(self, id: int):
        text = Text.objects.get(pk=id)
        return self.collect_text(text)

    def create_text(self, data: dict) -> dict:
        corpus = Corpus.objects.get(pk=data["corpus"]) if "corpus" in data else None
        has_translation = Text.objects.get(pk=data["has_translation"]) if "has_translation" in data else None

        text = Text.objects.create(
            title=data.get("title", ""),
            description=data.get("description", ""),
            content=data.get("content", ""),
            corpus=corpus,
            has_translation=has_translation,
        )
        return self.collect_text(text)

    def update_text(self, id: int, data: dict) -> dict:
        text = Text.objects.get(pk=id)

        text.title = data.get("title", text.title)
        text.description = data.get("description", text.description)
        text.content = data.get("content", text.content)

        if "corpus" in data:
            text.corpus = Corpus.objects.get(pk=data["corpus"])
        if "has_translation" in data:
            text.has_translation = Text.objects.get(pk=data["has_translation"])

        text.save()
        return self.collect_text(text)

    def deleteText(self, id: int):
        text = Text.objects.get(pk=id)
        text.delete()
        return id
