import sys

fsrc = open(str(sys.argv[1]), 'r')

lines = []
lines_bin = []
names = []

instructions = [
                'addtox', 
                'addtoy', 
                'movy',
                'xmem',
                'ymem',
                'hmem',
                'subfromy',
                'subfromx',
                'goto',
                'xgety',
                'xincy',
                'xmodtwo',
                'ymodtwo',
                'xgetzero',
                'ygetzero',
                'xgetone',
                'ygetone',
                'xinv',
                'ygetx',
                'hincone',
                'movh',
                'hdecone',
                'xprodmem',
                'jzy',
                'jzh',
                'jzxmodtwo',
                'jzxgthany',
                'jzymodtwo',
                'hgetx' ,
                'hgety',
                'hgetzero',
                'jnxisnegative',
                'jnyisnegative',
                'yprodmem',
                'ydivmem',
                'xdivmem',
                'xdivtwo',
                'xmodmem',
                'ymodmem',
                'movx',
                'xincone',
                'yincone',
                'xdecone',
                'ydecone',
                'jzx', 
                'xprody',
                'halt', 
                'wb', 
                'ww',
                'hgetone',
                'jzxequalsy',
                'xplush',
                'jzhgthany'
               ]

instruction_set = {
                   'addtox'        : 0x02, # x = x + mem
                   'addtoy'        : 0x1B, # y = y + mem
                   'movy'          : 0x32, # mem = y 
                   'xmem'          : 0x11, # x = mem
                   'ymem'          : 0x14, # y = mem 
                   'hmem'          : 0x40, # h = mem
                   'subfromy'      : 0x17, # y = y - mem
                   'subfromx'      : 0x0D, # x = x - mem
                   'goto'          : 0x09, # goto address
                   'xgety'         : 0x1A, # X = Y; 
                   'xincy'         : 0x1E, # X = X + Y 
                   'xmodtwo'       : 0x1F, # X = X%2; 
                   'ymodtwo'       : 0x20, # Y = Y%2; 
                   'xgetzero'      : 0x22, # X = 0
                   'ygetzero'      : 0x23, # Y = 0
                   'xgetone'       : 0x7C, # X = 1 
                   'ygetone'       : 0x7D, # Y = 1
                   'xinv'          : 0x24, # X = -X
                   'ygetx'         : 0x25, # Y = X; 
                   'hincone'       : 0x26, # H = H + 1; 
                   'hdecone'       : 0x27, # H = H - 1;
                   'xincone'       : 0x71, # X = X + 1; goto 0
                   'yincone'       : 0x73, # Y = Y + 1; goto 0
                   'xdecone'       : 0x72, # X = X - 1; goto 0
                   'ydecone'       : 0x74, # Y = Y - 1; goto 0
                   'xprodmem'      : 0x28, # X = X * mem[address]
                   'jzy'           : 0x30, # if Y = 0 then goto address
                   'jzxmodtwo'     : 0x37, # if X%2 = 0 then goto address
                   'jzxgthany'     : 0x39, # if X > Y = 0 then goto address
                   'jzymodtwo'     : 0x3B, # if Y%2 = 0 then goto address
                   'hgetx'         : 0x3D, # H = X
                   'hgety'         : 0x3E, # H = Y
                   'hgetzero'      : 0x3F, # H = 0
                   'jnxisnegative' : 0x43, # if 0 > x = 1 go to address (x positivo ou negativo)
                   'jnyisnegative' : 0x46, # if 0 > y = 1 go to address (y positivo ou negativo)
                   'yprodmem'      : 0x49, # Y = Y * mem[address]
                   'ydivmem'       : 0x51, # Y = Y / mem[address]
                   'xdivmem'       : 0x59, # X = X / mem[address]
                   'xdivtwo'       : 0x7E, # X = X/2
                   'xmodmem'       : 0x61, # X = X % mem[address]
                   'ymodmem'       : 0x69, # Y = Y % mem[address]
                   'movx'          : 0x06, # mem = x 
                   'jzx'           : 0x0B, # if x = 0 goto address
                   'jzh'           : 0x7F, # if H = 0 then goto address
                   'hgetone'       : 0x81, # h = 1
                   'xprody'        : 0x75, # X = X*Y
                   'jzxequalsy'    : 0x82, # if x == y goto address
                   'jzhgthany'     : 0x84, # if h>y goto address
                   'xplush'        : 0x86, # X = X + H + 1]
                   'movh'          : 0x87, # mem = h 
                   'halt'          : 0xFF  # halt
                  }

def is_instruction(str):
   global instructions
   inst = False
   for i in instructions:
      if i == str:
         inst = True
         break
   return inst
   
def is_name(str):
   global names
   name = False
   for n in names:
      if n[0] == str:
         name = True
         break
   return name
   
def encode_2ops(inst, ops):
   line_bin = []
   if len(ops) > 1:
      if ops[0] == 'x' or ops[0] == 'y' or ops[0] == 'h':
         if is_name(ops[1]):
            line_bin.append(instruction_set[inst])
            line_bin.append(ops[1])
   return line_bin

def encode_0ops(inst):
   line_bin = []
   line_bin.append(instruction_set[inst])
   return line_bin

def encode_goto(ops):
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['goto'])
         line_bin.append(ops[0])
   return line_bin
   
def encode_wb(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         if int(ops[0]) < 256:
            line_bin.append(int(ops[0]))
   return line_bin   

def encode_ww(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         val = int(ops[0])
         if val < pow(2,32):
            line_bin.append(val & 0xFF)
            line_bin.append((val & 0xFF00) >> 8)
            line_bin.append((val & 0xFF0000) >> 16)
            line_bin.append((val & 0xFF000000) >> 24)
   return line_bin
      
def encode_instruction(inst, ops):
   if (inst == 'addtox' or 
       inst == 'addtoy' or 
       inst == 'movx' or
       inst == 'movy' or
       inst == 'xmem' or
       inst == 'ymem' or
       inst == 'hmem' or
       inst == 'subfromy' or
       inst == 'subfromx' or
       inst == 'xprodmem' or
       inst == 'yprodmem' or
       inst == 'ydivmem' or
       inst == 'xdivmem' or
       inst == 'xmodmem' or
       inst == 'ymodmem' or 
       inst == 'jnxisnegative' or
       inst == 'jnyisnegative' or
       inst == 'jzy' or
       inst == 'jzxmodtwo' or
       inst == 'jzxgthany'or
       inst == 'jzymodtwo'or
       inst == 'jzh' or
       inst == 'jzx' or 
       inst == 'movh' or
       inst == 'jzxequalsy' or
       inst == 'jzhgthany'):
       return encode_2ops(inst, ops)
   elif (inst == 'xgety' or
         inst == 'ygetx' or
         inst == 'xincy' or
         inst == 'xmodtwo' or 
         inst == 'ymodtwo' or
         inst == 'xgetzero' or
         inst == 'ygetzero' or
         inst == 'xinv' or
         inst == 'hincone' or
         inst == 'hdecone' or
         inst == 'hgetx' or
         inst == 'hgety' or
         inst == 'hgetzero' or
         inst == 'ydecone' or 
         inst == 'xdecone' or
         inst == 'yincone' or
         inst == 'xincone' or
         inst == 'xprody' or
         inst == 'xgetone' or
         inst == 'ygetone' or
         inst == 'xdivtwo' or 
         inst == 'hgetone' or
         inst == 'xplush'):
         return encode_0ops(inst) 
   elif inst == 'goto':
      return encode_goto(ops)
   elif inst == 'halt':
      return encode_0ops('halt') 
   elif inst == 'wb':
      return encode_wb(ops)
   elif inst == 'ww':
      return encode_ww(ops)
   else:
      return []
   
   
def line_to_bin_step1(line):
   line_bin = []
   if is_instruction(line[0]):
      line_bin = encode_instruction(line[0], line[1:])
   else:
      line_bin = encode_instruction(line[1], line[2:])
   
   return line_bin
   
def lines_to_bin_step1():
   global lines
   for line in lines:
      line_bin = line_to_bin_step1(line)
      if line_bin == []:
         print("Erro de sintaxe na linha ", lines.index(line))
         return False
      lines_bin.append(line_bin)
   return True

def find_names():
   global lines
   for k in range(0, len(lines)):
      is_label = True
      for i in instructions:
          if lines[k][0] == i:
             is_label = False
             break
      if is_label:
         names.append((lines[k][0], k))
         
def count_bytes(line_number):
   line = 0
   byte = 1
   while line < line_number:
      byte += len(lines_bin[line])
      line += 1
   return byte

def get_name_byte(str):
   for name in names:
      if name[0] == str:
         return name[1]
         
def resolve_names():
   for i in range(0, len(names)):
      names[i] = (names[i][0], count_bytes(names[i][1]))
   for line in lines_bin:
      for i in range(0, len(line)):
         if is_name(line[i]):
            if (line[i-1] == instruction_set['addtox'] or 
                line[i-1] == instruction_set['addtoy'] or 
                line[i-1] == instruction_set['movx'] or
                line[i-1] == instruction_set['movy'] or
                line[i-1] == instruction_set['xmem'] or
                line[i-1] == instruction_set['ymem'] or
                line[i-1] == instruction_set['hmem'] or
                line[i-1] == instruction_set['movh'] or
                line[i-1] == instruction_set['subfromx'] or
                line[i-1] == instruction_set['subfromy'] or
                line[i-1] == instruction_set['xprodmem'] or
                line[i-1] == instruction_set['yprodmem'] or
                line[i-1] == instruction_set['ydivmem'] or
                line[i-1] == instruction_set['xdivmem'] or
                line[i-1] == instruction_set['xmodmem'] or
                line[i-1] == instruction_set['ymodmem'] or
                line[i-1] == instruction_set['xprody']):
               line[i] = get_name_byte(line[i])//4
            else:
               line[i] = get_name_byte(line[i])

for line in fsrc:
   tokens = line.replace('\n','').replace(',','').lower().split(" ")
   i = 0
   while i < len(tokens):
      if tokens[i] == '':
         tokens.pop(i)
         i -= 1
      i += 1
   if len(tokens) > 0:
      lines.append(tokens)
   
find_names()
if lines_to_bin_step1():
   resolve_names()
   byte_arr = [0]
   for line in lines_bin:
      for byte in line:
         byte_arr.append(byte)
   fdst = open(str(sys.argv[2]), 'wb')
   fdst.write(bytearray(byte_arr))
   fdst.close()

fsrc.close()