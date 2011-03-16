from pyutils.decorators import logprint

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

if __name__ == "__main__":
    test_logprint()
