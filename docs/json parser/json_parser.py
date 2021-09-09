from Parsea import Parsea

class JsonParser(Parsea):
    
    def parseString(self, string: str):
        self.init(string)
        return self.expr()
    
    def expr(self):
        if self.maybe_str("{"): # if current character is '{'
            return self.dict() # its a dict
        
        if self.maybe_str("["): # if current character is '['
            return self.list() # its a list
        
        return self.value() # value instead

    def dict(self):
        obj = {} # create empty dict object
        
        # while current character is not EOF and current character is not '}'
        while self.char is not None and self.char != "}":
            key = self.string() # try string
            if key is False: # if fail
                raise SyntaxError("Expected string literal") # SyntaxError
            
            if not self.maybe_str(":"):
                raise SyntaxError("Expected colon")
            
            obj[key] = self.expr() # get expression and put it in dict object
            
            self.check_ignore() # ignore whitespace
            if self.char != "}": # if current character is not '}'
                if not self.maybe_str(","): # if not comma
                    raise SyntaxError("Expected comma after key value") # SyntaxError
        
        if not self.maybe_str("}"): # check if current character is not '}'
            raise SyntaxError("Expected closing curly bracket") # SyntaxError
        
        return obj # return the result

    def list(self):
        obj = [] # create empty list object
        
        while self.char is not None and self.char != ']':
            obj.append(self.expr()) # get expression and put it in list object
            
            self.check_ignore() # ignore whitespace
            if self.char != "]": # if current character is not ']'
                if not self.maybe_str(","): # if not comma
                    raise SyntaxError("Expected comma after element") # SyntaxError

        # check if current character is not ']'
        if not self.maybe_str("]"):
            raise SyntaxError("Expected closing square bracket") # SyntaxError
        
        return obj # return the result

    def value(self):
        v = self.number() # try number
        if v: # if success
            return v # return
        
        v = self.string() # try string
        if v: # if success
            return v # return
        
        # check other literal: true, false and null
        i, m = self.optional(
            self.maybe_str,
            "true", # 0
            "false", # 1
            "null" # 2
        ) # i is the match index and m is the string
        
        if m is None: # if m is None, SyntaxError
            raise SyntaxError("Expected a value: number, string, bool or null literal")
        
        if i == 0: # true
            return True
        elif i == 1: # false
            return False
        return None # null

    def string(self):
        # check if current character is quote("|')
        _, quote = self.optional(self.maybe_str, "'", '"')
        
        if quote is None: # check if the quote is none or not
            return False # current character is not quote
        
        text = ""
        
        # while current character is not EOF and character is not quote
        while self.char is not None and self.char != quote:
            text += self.advance()
        
        if not self.maybe_str(quote): # if the character is not quote(character is eof)
            raise SyntaxError(f"Expected closing quote") # SyntaxError
        
        # match_str will actually eat the character so we don't need advance
        return text
    
    def number(self):
        num = self.while_strings("0123456789") # eat characters until current character is not digit
        if not num: # if the current character is not digit
            return False
        
        if self.char == ".": # check if current character is dot (float number)
            num += self.advance() # eat current character and move to the next character
            n = self.while_strings("0123456789") # digit
            if not n: # if the current character is not digit
                raise SyntaxError("Expected number after dot") # SyntaxError
            return float(num) # return result in float type
        
        return int(num) # if current character is not dot, return integer


def get_line_and_col_by_index(s: str, pos: int):
    if not s:
        return (1,1)
    s = s[:pos+1].splitlines(keepends=True)
    return len(s), len(s[-1])

if __name__ == "__main__":
    parser = JsonParser()
    
    json = open("test.json").read()
    
    try:
        print(parser.parseString(json))
    except SyntaxError as e:
        print(f"{e} {get_line_and_col_by_index(json,parser.pos)}")