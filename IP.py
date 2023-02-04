class IP:
    def __init__(self):
        self.byte_value = bytearray(b'x\00\x00\x00\x00')
        self.str_value = "0.0.0.0"
        
    def __init__(self, str_val:str):
        self.byte_value = bytearray(b'x\00\x00\x00\x00')
        self.str_value = "0.0.0.0"
        self.set_ip_from_str(str_val)
        
    def to_str(self):
        return self.str_value

    def __is_correct_byte_value__(self, b):
        return b >= 0 and b <= 255
    
    def set_ip_from_str(self, str_val:str):
        self.str_value = str_val
        octets = str_val.split('.')
        assert(len(octets) == 4)
        for i, k in zip(octets, range(len(self.byte_value))):
            assert(i.isnumeric())
            num = int(i)
            assert(self.__is_correct_byte_value__(num))
            self.byte_value[k] = int(i)
        
            
    def set_ip_from_bytearray(self, byte_val:bytearray):
        if(len(byte_val) != 4):
            assert()
        self.byte_value = byte_val
        self.str_value = ""
        for i in self.byte_value:
            self.str_value += str(i) + "."
        self.str_value = self.str_value[:-1]