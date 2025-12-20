import main

class ConcreteRepository(main.Repository):
    def save(self, data: dict) -> None:
        print(f"Saving data: {data}")


def test_repository_save():

    repo = ConcreteRepository()
    repo.save({"key": "value"})
