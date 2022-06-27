from re import A
import memory
from instructions import firmware

MPC = 0
MIR = 0

MAR = 0
MDR = 0
PC = 0
MBR = 0

X = 0
Y = 0
H = 0

A = 0
B = 0


N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0


def read_regs(reg_num):
	global MDR, PC, MBR, X, Y, H, A, B, BUS_A, BUS_B
	
	BUS_A = H

	if reg_num == 0:
		BUS_A = MDR
		BUS_B = H
	elif reg_num == 1:
		BUS_B = PC
	elif reg_num == 2:
		BUS_B = MBR
	elif reg_num == 3:
		BUS_B = X
	elif reg_num == 4:
		BUS_B = Y
	elif reg_num == 5:
		BUS_A = MDR
		BUS_B = X
	elif reg_num == 6:
		BUS_A = MDR
		BUS_B = Y	
	elif reg_num == 7:
		BUS_A = X
		BUS_B = Y
	elif reg_num == 8:
		BUS_B = A
	elif reg_num == 9:
		BUS_B = B
	elif reg_num == 10:
		BUS_A = X
		BUS_B = A
	elif reg_num == 11:
		BUS_A = X
		BUS_B = B
	elif reg_num == 12:
		BUS_A = Y
		BUS_B = A
	elif reg_num == 13:
		BUS_A = Y
		BUS_B = B
	elif reg_num == 14:
		BUS_A = MDR
		BUS_B = A
	elif reg_num == 15:
		BUS_A = MDR
		BUS_B = B
	else:
		BUS_B = 0
		
		
def write_regs(reg_bits):
	global MAR, MDR, PC, X, Y, H, A, B, BUS_C
	if reg_bits & 0b10000000:
		A = BUS_C
	if reg_bits & 0b01000000:
		B = BUS_C
	if reg_bits & 0b00100000:
		MAR = BUS_C
	if reg_bits & 0b00010000:
		MDR = BUS_C
	if reg_bits & 0b00001000:
		PC = BUS_C
	if reg_bits & 0b00000100:
		X = BUS_C
	if reg_bits & 0b00000010:
		Y = BUS_C
	if reg_bits & 0b00000001:
		H = BUS_C

def alu(control_bits):
	global N, Z, BUS_A, BUS_B, BUS_C
	
	a = BUS_A
	b = BUS_B
	o = 0
	
	shift_bits = control_bits & 0b110000000
	shift_bits = shift_bits >> 7
	
	control_bits = control_bits & 0b001111111
	
	if control_bits == 	 0b0101000:
		o = a
	elif control_bits == 0b0100100:
		o = b
	elif control_bits == 0b0101010:
		o = ~a
	elif control_bits == 0b1001100:
		o = ~b
	elif control_bits == 0b1101100:
		o = a + b
	elif control_bits == 0b1101101:
		o = a + b + 1
	elif control_bits == 0b1101001:
		o = a + 1
	elif control_bits == 0b1100101:
		o = b + 1
	elif control_bits == 0b1101111:
		o = b - a
	elif control_bits == 0b1100110:
		o = b - 1
	elif control_bits == 0b1101011:
		o = -a
	elif control_bits == 0b0001100:
		o = a & b
	elif control_bits == 0b0101100:
		o = a | b
	elif control_bits == 0b0100000:
		o = 0
	elif control_bits == 0b1100001:
		o = 1
	elif control_bits == 0b1100010:
		o = -1
	elif control_bits == 0b0011100:
		o = int(a>b) 
	elif control_bits == 0b0111000:
		o = a%2
	elif control_bits == 0b0110100:
		o = b%2
	elif control_bits == 0b1111100:
		o = int(a == b)
	
	if o == 0:
		N = 0
		Z = 1
	else:
		N = 1
		Z = 0
	
	if shift_bits == 0b01:
		o = o << 1
	elif shift_bits == 0b10:
		o = o >> 1
	elif shift_bits == 0b11:
		o = o << 8
		
	BUS_C = o
	
def next_instruction(next, jam):
	global MPC, MBR, N, Z
	
	if jam == 0b000:
		MPC = next 
		return
		
	if jam & 0b001:
		next = next | (Z << 8)
	
	if jam & 0b010:
		next = next | (N << 8)
		
	if jam & 0b100:
		next = next | MBR

	MPC = next
	
def memory_io(mem_bits):
	global PC, MBR, MDR, MAR
	
	if mem_bits & 0b001:
		MBR = memory.read_byte(PC)

	if mem_bits & 0b010:
		MDR = memory.read_word(MAR)
		
	if mem_bits & 0b100:
		memory.write_word(MAR, MDR)
		
def step():
	global MIR, MPC

	MIR = firmware[MPC]
	if MIR == 0:
		return False
		
	read_regs       ( MIR & 0b000000000000000000000000000000001111)
	alu             ((MIR & 0b000000000000111111111000000000000000) >> 15)
	write_regs      ((MIR & 0b000000000000000000000111111110000000) >> 7)
	memory_io       ((MIR & 0b000000000000000000000000000001110000) >> 4)
	next_instruction((MIR & 0b111111111000000000000000000000000000) >> 27, (MIR & 0b000000000111000000000000000000000000) >> 24)
	
	return True