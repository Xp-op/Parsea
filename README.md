# Parsea
Simple Scannerless Parser library for Python

## Usage
```py
from Parsea import Parsea

class Parser(Parsea):
    
    def parseInt(self, string: str):
        self.init(string)
        num = self.while_strings("0123456789")
        return int(num) if num else None
    
    def parseAlpha(self, string: str):
        self.init(string)
        alpha = self.while_strings(self.in_range("a","z")+self.in_range("A","Z"))
        return alpha if alpha else None

p = Parser()

print(p.parseInt('1203')) # 1203
print(p.parseInt('heLLo')) # None

print(p.parseAlpha('heLLo')) # heLLo
print(p.parseAlpha('1203')) # None
```
