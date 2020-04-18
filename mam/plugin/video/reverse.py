from mam.core.assetlibrary import ShellPluginBase


class Reverse(ShellPluginBase):
    name = 'video.reverse'
    suffix = '.rev'
    ext = '.mp4'

    def cmd(self, src, dst):
        return [
            "ffmpeg",
            "-i", src,
            "-vf", "reverse",
            dst,
        ]

