from pathlib import Path

import yaml

from bayegani.descriptor_loader.descriptor_loader import DescriptorLoader, Descriptor


class FileDescriptorLoader(DescriptorLoader):
    def __init__(self, file_path: Path):
        with open(file_path, 'r', encoding='utf-8') as fp:
            descriptor = Descriptor.parse_obj(yaml.safe_load(fp))

        super().__init__(descriptor=descriptor)
