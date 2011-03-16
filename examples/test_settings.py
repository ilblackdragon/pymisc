from pymisc.settings import settings

def test_settings():
    settings = Settings('test.cfg')
    settings.wow = 'cool'
    settings.default('foo', 'bar')  # Just set default for this value
    print(settings.foo)
    # It all'll saved on app exit

if __name__ == "__main__":
   test_settings() 
