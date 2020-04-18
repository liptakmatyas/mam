import mam
from mam_testlib.file_utils import same_file_content

import os


def test_command_line(tmpdir):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.Reverse(lib)
    assert plugin.name == 'video.reverse'
    assert plugin.suffix == '.rev'
    assert plugin.ext == '.mp4'

    xr_cmd = 'ffmpeg -i input_file -vf reverse output_file'
    cmd_as_list = plugin.cmd('input_file', 'output_file')
    assert ' '.join(cmd_as_list) == xr_cmd

#   TODO    This test should be tagged as 'slow' and 'external', since it
#           actually runs `ffmpeg`
def test_output(tmpdir, test_input):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.Reverse(lib)

    src = test_input('test-video.mp4')
    xr_dst_fn = 'test-video.mp4.rev.mp4'
    xr_dst = '{}/{}'.format(tmpdir, xr_dst_fn)

    plugin._op(src, xr_dst)
    assert os.path.isfile(xr_dst)
    assert same_file_content(xr_dst, test_input(xr_dst_fn))

