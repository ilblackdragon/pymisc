from pymisc.decorators import logprint, memoized

@logprint
def test_logprint():

    @logprint
    def test(q):
        x = [a + 10 for a in q]
        print('123')
        print('321')
        return x

    r = test([1,23])
    print(r)

count = 0
def test_memoized():
    @memoized
    def fibonacci(x):
        global count
        count += 1
        return fibonacci(x - 1) + fibonacci(x - 2) if x > 2 else 1
        
    assert(fibonacci(10) == 55)
    assert(count == 10)

if __name__ == "__main__":
    test_logprint()
    test_memoized()
