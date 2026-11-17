"""Write a tiny air-only structure for the opt-in, port-free GameTest server."""
from pathlib import Path
import gzip, struct
root=Path(__file__).resolve().parents[1]
def string(value):
    data=value.encode();return struct.pack('>H',len(data))+data
def tag(kind,name,payload):return bytes([kind])+string(name)+payload
data=bytes([10])+string('')
data+=tag(3,'DataVersion',struct.pack('>i',3465))
data+=tag(9,'size',bytes([3])+struct.pack('>i',3)+struct.pack('>iii',3,3,3))
data+=tag(9,'palette',bytes([10])+struct.pack('>i',1)+tag(8,'Name',string('minecraft:air'))+bytes([0]))
data+=tag(9,'blocks',bytes([10])+struct.pack('>i',0))
data+=tag(9,'entities',bytes([10])+struct.pack('>i',0))+bytes([0])
path=root/'audit/dev-validation-resources/data/wans_minego_expansion/structures/empty.nbt'
path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(data,mtime=0))
print(path)
