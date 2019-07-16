import os
from dataclasses import dataclass


@dataclass
class FilePart:
    s3_url: str
    local_filename: str
    size: str

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