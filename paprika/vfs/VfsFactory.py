from paprika.vfs.ProtocolBuilder import ProtocolBuilder


class VfsFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_client(url):
        protocol_json = ProtocolBuilder.build(url)
        protocol = protocol_json['protocol']
        if protocol == "sftp":
            from paprika.vfs.SftpUrlBuilder import SftpUrlBuilder
            from paprika.vfs.SftpClient import SftpClient
            json_url = SftpUrlBuilder.build(url)
            return SftpClient(json_url)
        if protocol == "smb":
            from paprika.vfs.SmbUrlBuilder import SmbUrlBuilder
            from paprika.vfs.SmbClient import SmbClient
            json_url = SmbUrlBuilder.build(url)
            return SmbClient(json_url)
        if protocol == "file":
            from paprika.vfs.FileUrlBuilder import FileUrlBuilder
            from paprika.vfs.FileClient import FileClient
            json_url = FileUrlBuilder.build(url)
            return FileClient(json_url)
        if protocol == "zip":
            from paprika.vfs.ZipUrlBuilder import ZipUrlBuilder
            from paprika.vfs.ZipClient import ZipClient
            json_url = ZipUrlBuilder.build(url)
            return ZipClient(json_url)

