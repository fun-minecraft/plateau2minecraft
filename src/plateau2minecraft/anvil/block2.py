from frozendict import frozendict
from nbt import nbt

from .legacy import LEGACY_ID_MAP

class Block:
    """
    Minecraftのブロックを表します。

    Attributes
    ----------
    namespace: :class:`str`
        ブロックの名前空間、通常は``minecraft``
    id: :class:`str`
        ブロックのID、例: stone, diamond_blockなど
    properties: :class:`dict`
        ブロックのプロパティを辞書として表します
    """

    __slots__ = ("namespace", "id", "properties")

    def __init__(self, namespace: str, block_id: str = None, properties: dict = None):
        """
        Parameters
        ----------
        namespace
            ブロックの名前空間。block_idが指定されない場合、これをブロックIDと仮定し、名前空間を``"minecraft"``に設定します
        block_id
            ブロックのID
        properties
            ブロックのプロパティ
        """
        if block_id is None:
            self.namespace = "minecraft"
            self.id = namespace
        else:
            self.namespace = namespace
            self.id = block_id
        self.properties = properties or {}

    def name(self) -> str:
        """
        ブロックを``minecraft:block_id``形式で返します
        """
        return self.namespace + ":" + self.id

    def __repr__(self):
        return f"Block({self.name()})"

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.namespace == other.namespace and self.id == other.id and self.properties == other.properties

    def __hash__(self):
        return hash(self.name()) ^ hash(frozendict(self.properties))

    @classmethod
    def from_name(cls, name: str, *args, **kwargs):
        """
        ``namespace:block_id``形式から新しいBlockを作成します

        Parameters
        ----------
        name
            上記形式のブロック名
        args, kwargs
            メインコンストラクタに渡される引数
        """
        namespace, block_id = name.split(":")
        return cls(namespace, block_id, *args, **kwargs)

    @classmethod
    def from_palette(cls, tag: nbt.TAG_Compound):
        """
        Section.Paletteのタグ形式から新しいBlockを作成します

        Parameters
        ----------
        tag
            セクションのパレットからの生のタグ
        """
        name = tag["Name"].value
        properties = dict(tag.get("Properties", {}))
        return cls.from_name(name, properties=properties)

    @classmethod
    def from_numeric_id(cls, block_id: int, data: int = 0):
        """
        フラッテン化前のblock_id:data形式から新しいBlockを作成します（バージョン1.13以前）

        Parameters
        ----------
        block_id
            ブロックの数値ID
        data
            バリアントを表す数値データ
        """
        key = f"{block_id}:{data}"
        if key not in LEGACY_ID_MAP:
            raise KeyError(f"Block {key} not found")
        name, properties = LEGACY_ID_MAP[key]
        return cls("minecraft", name, properties=properties)


class OldBlock:
    """
    1.13以前の数値IDを持つMinecraftのブロックを表します。

    Attributes
    ----------
    id: :class:`int`
        ブロックの数値ID
    data: :class:`int`
        ブロックデータ、バリアントを表します
    """

    __slots__ = ("id", "data")

    def __init__(self, block_id: int, data: int = 0):
        """
        Parameters
        ----------
        block_id
            ブロックのID
        data
            ブロックデータ
        """
        self.id = block_id
        self.data = data

    def convert(self) -> Block:
        return Block.from_numeric_id(self.id, self.data)

    def __repr__(self):
        return f"OldBlock(id={self.id}, data={self.data})"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        elif not isinstance(other, Block):
            return False
        else:
            return self.id == other.id and self.data == other.data

    def __hash__(self):
        return hash(self.id) ^ hash(self.data)
