from db.models import Corpus


class CorpusRepository:
    def __init__(self):
        pass

    def collect_corpus(self, corpus: Corpus):
        return {
            "id": corpus.id,
            "title": corpus.title,
            "description": corpus.description,
            "genre": corpus.genre,
            "texts": [
                {
                    "id": text.id,
                    "title": text.title,
                    "description": text.description,
                    "content": text.content,
                    "has_translation": text.has_translation_id,
                }
                for text in corpus.texts.all()
            ],
        }

    def getCorpus(self, id: int):
        corpus = Corpus.objects.get(pk=id)
        return self.collect_corpus(corpus)

    def create_corpus(self, data: dict) -> dict:
        corpus = Corpus.objects.create(
            title=data.get("title", ""),
            description=data.get("description", ""),
            genre=data.get("genre", "")
        )
        return self.collect_corpus(corpus)

    def update_corpus(self, id: int, data: dict) -> dict:
        corpus = Corpus.objects.get(pk=id)
        corpus.title = data.get("title", corpus.title)
        corpus.description = data.get("description", corpus.description)
        corpus.genre = data.get("genre", corpus.genre)
        corpus.save()
        return self.collect_corpus(corpus)

    def deleteCorpus(self, id: int):
        corpus = Corpus.objects.get(pk=id)
        corpus.delete()
        return id
