import os


class FilePart:

    def __init__(self, s3_url: str, local_filename: str, size: str):
        self.s3_url = s3_url
        self.local_filename = local_filename
        self.size = size

    @classmethod
    def from_link(cls, link):
        return cls(
            s3_url=link['key'],
            local_filename=link['Key'],
            size=link['Size']
        )

    def __enter__(self):
        """ Downloads the file from s3"""

    def __exit__(self):
        try:
            os.remove(self.local_filename)
        except OSError:
            pass
        """Deletes file from s3"""