import os


def get_hierarchy_path(str_id, file_ext, root, auto_mkdir=True, prefix_path_length=3):
    """
    Generate path name for large amount of files in next form:
    1234567890.txt -> 123/456/789/
    Attached filenames consists of extra_path, that build from id, and id plus filetype.
    """
    str_id_len = len(str_id)
    if str_id_len >= prefix_path_length:
        extra_path = os.path.join(*[
            str_id[i * prefix_path_length : (i + 1) * prefix_path_length]
                for i in xrange(str_id_len / prefix_path_length)
        ])
        if auto_mkdir:
            try:
                os.makedirs(os.path.join(root, extra_path))
            except OSError:
                pass
    else:
        extra_path = ''
    return os.path.join(root, extra_path, str_id + file_ext)

