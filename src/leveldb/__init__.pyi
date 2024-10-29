from __future__ import annotations

import typing

__all__ = [
    "LevelDB",
    "LevelDBEncrypted",
    "LevelDBException",
    "LevelDBItemsIterator",
    "LevelDBItemsRangeIterator",
    "LevelDBIterator",
    "LevelDBKeysIterator",
    "LevelDBValuesIterator",
]

class LevelDB:
    """
    A LevelDB database
    """

    def __contains__(self, key: bytes) -> bool: ...
    def __delitem__(self, key: bytes) -> None: ...
    def __getitem__(self, key: bytes) -> bytes: ...
    def __init__(self, path: str, create_if_missing: bool = False) -> None:
        """
        Construct a new :class :`LevelDB` instance from the database at the given path.

        A leveldb database is like a dictionary that only contains bytes as the keys and values and exists entirely on the disk.

        :param path: The path to the database directory.
        :param create_if_missing: If True a new database will be created if one does not exist at the given path.
        :raises: LevelDBException if create_if_missing is False and the db does not exist.
        """

    def __iter__(self) -> LevelDBKeysIterator: ...
    def __setitem__(self, key: bytes, value: bytes) -> None: ...
    def close(self, compact: bool = False) -> None:
        """
        Close the leveldb database.

        :param compact: If True will compact the database making it take less memory.
        """

    def compact(self) -> None:
        """
        Remove deleted entries from the database to reduce its size.
        """

    def create_iterator(self) -> LevelDBIterator:
        """
        Create a new leveldb Iterator.
        """

    def delete(self, key: bytes) -> None:
        """
        Delete a key from the database.

        :param key: The key to delete from the database.
        """

    def get(self, key: bytes) -> bytes:
        """
        Get a key from the database.

        :param key: The key to get from the database.
        :return: The data stored behind the given key.
        :raises: KeyError if the requested key is not present.
        :raises: LevelDBException on other error.
        """

    def items(self) -> LevelDBItemsIterator:
        """
        An iterable of all items in the database.
        """

    def iterate(
        self, start: bytes | None = None, end: bytes | None = None
    ) -> LevelDBItemsIterator | LevelDBItemsRangeIterator:
        """
        Iterate through all keys and data that exist between the given keys.

        :param start: The key to start at. Leave as None to start at the beginning.
        :param end: The key to end at. Leave as None to finish at the end.
        """

    def keys(self) -> LevelDBKeysIterator:
        """
        An iterable of all keys in the database.
        """

    def put(self, key: bytes, value: bytes) -> None:
        """
        Set a value in the database.
        """

    def put_batch(self, batch: dict[bytes, bytes | None]) -> None:
        """
        Set a group of values in the database.
        """

    def values(self) -> LevelDBValuesIterator:
        """
        An iterable of all values in the database.
        """

class LevelDBEncrypted(Exception):
    pass

class LevelDBException(Exception):
    pass

class LevelDBItemsIterator:
    def __iter__(self) -> typing.Any: ...
    def __next__(self) -> tuple[bytes, bytes]: ...

class LevelDBItemsRangeIterator:
    def __iter__(self) -> typing.Any: ...
    def __next__(self) -> tuple[bytes, bytes]: ...

class LevelDBIterator:
    def key(self) -> bytes:
        """
        Get the key of the current entry in the database.
        :raises: runtime_error if iterator is not valid.
        """

    def next(self) -> None:
        """
        Seek to the next entry in the database.
        """

    def prev(self) -> None:
        """
        Seek to the previous entry in the database.
        """

    def seek(self, target: bytes) -> None:
        """
        Seek to the given entry in the database.
        If the entry does not exist it will seek to the location after.
        """

    def seek_to_first(self) -> None:
        """
        Seek to the first entry in the database.
        """

    def seek_to_last(self) -> None:
        """
        Seek to the last entry in the database.
        """

    def valid(self) -> bool:
        """
        Is the iterator at a valid entry.
        If False, calls to other methods may error.
        """

    def value(self) -> bytes:
        """
        Get the value of the current entry in the database.
        :raises: runtime_error if iterator is not valid.
        """

class LevelDBKeysIterator:
    def __iter__(self) -> typing.Any: ...
    def __next__(self) -> bytes: ...

class LevelDBValuesIterator:
    def __iter__(self) -> typing.Any: ...
    def __next__(self) -> bytes: ...

__version__: str
