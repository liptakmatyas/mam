from mam.core.assetlibrary import ShellPluginBase


class GoproMoshavi(ShellPluginBase):
    name = 'video.convert.gopro.moshavi'
    suffix = '.mosh'
    ext = '.avi'

    def cmd(self, src, dst):
        return [
            "ffmpeg",
            "-i", src,

            #   video
            "-vcodec", "libx264",
            "-x264-params", "keyint=9999999:scenecut=0",
            "-qscale:v", "0",

            #   disable audio
            "-an",

            #   bitrate
            "-b:v",     "20000k",
            "-maxrate", "20000k",
            "-bufsize", "10000k",

            #   no B-frames
            "-bf", "0",

            dst,
        ]

