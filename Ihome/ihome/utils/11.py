def outter1(func1):  # 传入wrapper2()
	print('加载了outter1')

	def wrapperl(*args, **kwargs):
		print('执行了wrapperl')
		res1 = func1(*args, **kwargs)
		return res1

	return wrapperl  # 这里返回的是函数调用wrapper1()


def outter2(func2):  # 传入wrapper3()
	print('加载了outter2')

	def wrapper2(*args, **kwargs):
		print('执行了wrapper2')
		res2 = func2()
		return res2

	return wrapper2  # 这里返回的是函数调用wrapper2()


def outter3(func3):  # 传入index()
	print('加载了outter3')

	def wrapper3(*args, **kwargs):
		print('执行了wrapper3')
		res3 = func3(*args, **kwargs)
		return res3

	return wrapper3  # 这里返回的是函数调用wrapper3()


@outter1
@outter2
@outter3
def index():
	print('from index')


index()
