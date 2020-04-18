import mam
from mam_testlib.file_utils import same_file_content

import os


def test_command_line(tmpdir):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.convert.MoshaviMp4(lib)
    assert plugin.name == 'video.convert.moshavi.mp4'
    assert plugin.suffix == ''
    assert plugin.ext == '.mp4'

    xr_cmd = ' '.join([
        'ffmpeg',
        '-i input_file',
        '-strict -2',
        'output_file'
    ])
    cmd_as_list = plugin.cmd('input_file', 'output_file')
    assert ' '.join(cmd_as_list) == xr_cmd

#   TODO    This test should be tagged as 'slow' and 'external', since it
#           actually runs `ffmpeg`
#   NOTE:   The file content is shaky, we cannot check for exact match.
def test_output(tmpdir, test_input):
    lib = mam.core.AssetLibrary(tmpdir)
    plugin = mam.plugin.video.convert.MoshaviMp4(lib)

    src = test_input('test-video.mp4')
    xr_dst_fn = 'test-video.mp4.mosh.avi'
    xr_dst = '{}/{}'.format(tmpdir, xr_dst_fn)

    plugin._op(src, xr_dst)
    assert os.path.isfile(xr_dst)

