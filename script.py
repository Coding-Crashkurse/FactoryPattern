"""Simple Factory Pattern Example - DataStore Implementations"""

import json
from abc import ABC, abstractmethod
from pathlib import Path


class DataStore(ABC):
    """Abstract base class for all DataStore implementations."""

    @abstractmethod
    def save(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> dict[str, str]:
        pass


class InMemoryStore(DataStore):
    """In-memory storage using Python dictionary."""

    def __init__(self):
        self._data: dict[str, str] = {}
        print("[OK] InMemoryStore initialized")

    def save(self, key: str, value: str) -> None:
        self._data[key] = value
        print(f"  > Saved to memory: {key} = {value}")

    def get(self, key: str) -> str | None:
        value = self._data.get(key)
        print(f"  > Read from memory: {key} = {value}")
        return value

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            print(f"  > Deleted from memory: {key}")
            return True
        return False

    def list_all(self) -> dict[str, str]:
        return self._data.copy()


class FileStore(DataStore):
    """Persistent storage using JSON file."""

    def __init__(self, filename: str = "data.json"):
        self.filename = Path(filename)
        self._data: dict[str, str] = {}
        self._load()
        print(f"[OK] FileStore initialized (file: {filename})")

    def _load(self) -> None:
        if self.filename.exists():
            with open(self.filename, encoding="utf-8") as f:
                self._data = json.load(f)

    def _save_to_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def save(self, key: str, value: str) -> None:
        self._data[key] = value
        self._save_to_file()
        print(f"  > Saved to file: {key} = {value}")

    def get(self, key: str) -> str | None:
        value = self._data.get(key)
        print(f"  > Read from file: {key} = {value}")
        return value

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._save_to_file()
            print(f"  > Deleted from file: {key}")
            return True
        return False

    def list_all(self) -> dict[str, str]:
        return self._data.copy()


def create_data_store(store_type: str) -> DataStore:
    """Factory function to create the appropriate DataStore implementation."""
    if store_type == "memory":
        return InMemoryStore()
    elif store_type == "file":
        return FileStore()
    else:
        raise ValueError(f"Unknown store type: {store_type}")


def demo_store(store: DataStore, store_name: str) -> None:
    """Demonstrate DataStore usage."""
    print(f"\n{'=' * 60}")
    print(f"Demo: {store_name}")
    print(f"{'=' * 60}")

    store.save("name", "John Doe")
    store.save("email", "john@example.com")
    store.save("age", "30")

    store.get("name")
    store.get("email")

    store.delete("age")

    print("\n  All stored data:")
    for key, value in store.list_all().items():
        print(f"    {key}: {value}")


def main():
    print("\n" + "=" * 60)
    print("FACTORY PATTERN TUTORIAL")
    print("=" * 60)
    print("\nTwo DataStore implementations:")
    print("1. InMemoryStore - Fast, volatile")
    print("2. FileStore     - Slower, persistent")
    print("\nBoth implement the same ABC interface!")

    memory_store = create_data_store("memory")
    demo_store(memory_store, "InMemoryStore")

    file_store = create_data_store("file")
    demo_store(file_store, "FileStore")

    print("\n" + "=" * 60)
    print("DONE! Check out the data.json file.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
