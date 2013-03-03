"""Basic functionality to work with plugins/backends/configuring classes by names"""

import os
import sys
import pkgutil
import inspect

def load_all_modules_from_dir(dirname):
    """Import all python modules from dirname and return list of them"""
    module_list = []
    package_name = '.'.join(os.path.split(dirname))
    for importer, module_name, _ in pkgutil.iter_modules([dirname]):
        full_module_name = '%s.%s' % (package_name, module_name)
        if full_module_name in sys.modules:
            module = sys.modules[full_module_name]
        else:
            module = importer.find_module(module_name).load_module(module_name)
        module_list.append((module_name, module))
    return module_list

def load_all_backends(dirname, backend_base_class, backend_name_member='BACKEND_NAME'):
    """Load all python modules from `dirname` folder and enumerate all classes in them.
    Classes that are inherited from `backend_base_class` will be added to returning dict with key
    defined by module name or `backend_name_member` member of class.
    """
    module_list = load_all_modules_from_dir(dirname)
    backend_list = {}
    for module_name, module in module_list:
        for _, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and cls != backend_base_class and \
                issubclass(cls, backend_base_class):
                backend_name = getattr(cls, backend_name_member, module_name)
                backend_list[backend_name] = cls
                print(backend_name, cls)
    return backend_list

def load_all_plugins(dirname, plugin_base_class, plugin_name_member='PLUGIN_NAME'):
    """Load all python modules from `dirname` folder and enumerate all classes in them.
    Classes that are inherited from `plugin_base_class` will be added to returning dict with key
    defined by module name or `plugin_name_member` member of class.
    """
    return load_all_backends(dirname, plugin_base_class, plugin_name_member)

def create_backend(backend_list, name, *args, **kwargs):
    """Create backend from backend_list by name and additional arguments.
    If name is not present in backend_list - None will be returned
    >>> isinstance(create_backend({'test': object}, 'test'), object)
    True
    >>> create_backend({'test': object}, 'other') is None
    True
    """
    if name not in backend_list:
        return None
    return backend_list[name](*args, **kwargs)

def create_plugin(plugin_list, name, *args, **kwargs):
    """Create plugin from plugin_list by name and additional arguments.
    If name is not present in plugin_list - None will be returned
    """
    return create_backend(plugin_list, name, *args, **kwargs)

def get_class_by_name(class_name):
    """Returns a class based on class name
    >>> str(get_class_by_name('pymisc.utils.structs.Struct'))
    'pymisc.utils.structs.Struct'
    """
    mod_str, cls_str = class_name.rsplit('.', 1)
    mod = __import__(mod_str, globals(), locals(), [''])
    cls = getattr(mod, cls_str)
    return cls

def create_object_by_cls_name(class_name, *args, **kwargs):
    """Create object based on class name and pass arguments to constructor
    >>> create_object_by_cls_name('pymisc.utils.structs.Struct', a=1, b=2)
    Struct(a=1, b=2)
    """
    cls = get_class_by_name(class_name)
    if cls is not None:
        return cls(*args, **kwargs)
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()

