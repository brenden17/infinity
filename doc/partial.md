!SLIDE
## Currying에서 온 그대, partial

* 갈라파고스 제도, partial 함수
* 종의 기원
* 진화

!SLIDE
## 갈라파고스 제도, partial 함수
[partial](https://docs.python.org/2.7/library/functools.html#functools.partial)
~~~~{python}
from functools import partial
def add(a, b):
	"""Add a to b"""
	return a + b
add_one = partial(add, 1)
add_one(10)
~~~~

!SLIDE
## 종의 기원
### [Lambda calculus](http://en.wikipedia.org/wiki/Lambda_calculus) 
~~~~{python}
* sqsum(x, y) = x * x + y * y
* (x, y) -> x * x + y * y
* x -> (y -> x * x + y * y) # currying
~~~~

### functional language
* first class function - decorator
* first class citizen

!SLIDE
### 진화
~~~~{python}
add.__name__
add.__doc__
add_one.__name__
add_one.__doc__
add_one
from functools import update_wrapper
update_wapper(add_one, add)
add_one.__name__
add_one.__doc__
~~~~
!SLIDE
~~~~{python}

def my_decorator(f):
    @wraps(f)
	def wrapper(*args, **kwarg):
		return f(*args, **kwarg)
	return wrapper

@my_decorator
def example():
    """doc of example"""
	return 1
	
example.__name__
example.__doc__
~~~~
