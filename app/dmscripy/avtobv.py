from scipy import io as sio

class AvBv:
	def __init__(self):
		self.AvBv()
	def AvBv(self):
		self.table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
		self.tr = {}
		for i in range(58):
			self.tr[self.table[i]] = i
		self.s = [11, 10, 3, 8, 4, 6]
		self.xor = 177451812
		self.add = 8728348608

	def dec(self,x):
		r=0
		for i in range(6):
			r+=self.tr[x[self.s[i]]]*58**i
		return (r-self.add)^self.xor

	def enc(self,x):
		x=(x^self.xor)+self.add
		r=list('BV1  4 1 7  ')
		for i in range(6):
			r[self.s[i]]=self.table[x//58**i%58]
		return ''.join(r)

# 作者：mcfx
# 链接：https://www.zhihu.com/question/381784377/answer/1099438784
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。