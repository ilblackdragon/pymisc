import subprocess

from utils import RecursiveDict
from abstract import IBase

class Version(object):
    
    def __init__(self, major, minor, build):
        self.major = int(major)
        self.minor = int(minor)
        self.build = int(build)
        
    def __str__(self):
        return '%s-%s-%s' % (self.major, self.minor, self.build)

class IApplication(IBase):
    """
    Setup interface and reflection for all types of applications
    It could be just execute or some chanel of data transfer (pipe\netword\file\etc)
    """
    pass
    
class Application(IApplication):
    
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.version = Version(0, 0, 0)

    def execute(self, args = None):
        if not args:
            args = []
        retcode = subprocess.call([self.path] + args)
        return retcode

    def get_basename(self):
        return self.name
    
    def get_version(self):
        return self.version

    def __str__(self):
        return ('%s\t%s') % (self.path, str(self.version))

class ApplicationManager(object):
    
    def __init__(self):
        self.apps = []
        self.versions = RecursiveDict(4)
        
    def add_app(self, app):
        self.apps.append(app)
        version = app.get_version()
        name = app.get_basename()
        self.versions[name][version.major][version.minor][version.build] = app
        
    def search_apps(self, mask):
        pass

    def print_available(self):
        for appname in self.versions:
            print(appname)
            for major in self.versions[appname]:
                print("\t%s" % str(major))
                for minor in self.versions[appname][major]:
                    print("\t\t%s" % str(minor))
                    for build in self.versions[appname][major][minor]:
                        print("\t\t\t" % str(build))
                
    def get_by_version(self, basename, version):
        if basename in self.versions and version.major in self.versions[basename] and version.minor in self.versions[basename][version.major] and version.build in self.versions[basename][version.major][version.minor]:
            return self.versions[basename][version.major][version.minor][version.build]
        return None

