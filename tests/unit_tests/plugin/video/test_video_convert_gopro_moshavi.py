import mam
from mam_testlib.file_utils import same_file_content

import os


def test_command_line(tmpdir):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.convert.GoproMoshavi(lib)
    assert plugin.name == 'video.convert.gopro.moshavi'
    assert plugin.suffix == '.mosh'
    assert plugin.ext == '.avi'

    xr_cmd = ' '.join([
        'ffmpeg',
        '-i input_file',
        '-vcodec libx264',
        '-x264-params keyint=9999999:scenecut=0',
        '-qscale:v 0',
        '-an',
        '-b:v 20000k',
        '-maxrate 20000k',
        '-bufsize 10000k',
        '-bf 0',
        'output_file'
    ])
    cmd_as_list = plugin.cmd('input_file', 'output_file')
    assert ' '.join(cmd_as_list) == xr_cmd

#   TODO    This test should be tagged as 'slow' and 'external', since it
#           actually runs `ffmpeg`
#   NOTE:   The file content is shaky, we cannot check for exact match.
def test_output(tmpdir, test_input):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.convert.GoproMoshavi(lib)

    src = test_input('test-video.mp4')
    xr_dst_fn = 'test-video.mp4.mosh.avi'
    xr_dst = '{}/{}'.format(tmpdir, xr_dst_fn)

    plugin._op(src, xr_dst)
    assert os.path.isfile(xr_dst)

