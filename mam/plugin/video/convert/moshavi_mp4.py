from mam.core.assetlibrary import ShellPluginBase


class MoshaviMp4(ShellPluginBase):
    name = 'video.convert.moshavi.mp4'
    suffix = ''
    ext = '.mp4'

    def cmd(self, src, dst):
        return [
            "ffmpeg",
            "-i", src,
            "-strict", "-2",
            dst,
        ]
