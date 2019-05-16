import os

from .qnap import Qnap

class FileStation(Qnap):
    """
    Access QNAP FileStation.
    """

    def list_share(self):
        """
        List all shared folders.
        """
        return self.req(self.endpoint(
            func='get_tree',
            params={
                'is_iso': 0,
                'node': 'share_root',
            }
        ))

    def list(self, path, limit=10000):
        """
        List files in a folder.
        """
        return self.req(self.endpoint(
            func='get_list',
            params={
                'is_iso': 0,
                'limit': limit,
                'path': path
            }
        ))

    def get_file_info(self, path):
        """
        Get file information.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='stat',
            params={
                'path': dir_path,
                'file_name': file_name
            }
        ))

    def search(self, path, pattern):
        """
        Search for files/folders.
        """
        return self.req(self.endpoint(
            func='search',
            params={
                'limit': 10000,
                'start': 0,
                'source_path': path,
                'keyword': pattern
            }
        ))

    def delete(self, path):
        """
        Delete file(s)/folder(s)
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='delete',
            params={
                'path': dir_path,
                'file_total': 1,
                'file_name': file_name
            }
        ))

    def download(self, path):
        """
        Download file.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req_binary(self.endpoint(
            func='download',
            params={
                'isfolder': 0,
                'source_total': 1,
                'source_path': dir_path,
                'source_file': file_name
            }
        ))

    def upload(self, path, data, overwrite=True):
        """
        Upload file.
        """
        dir_path = os.path.dirname(path)
        file_path = path.replace('/', '-')
        file_name = os.path.basename(path)
        return self.req_post(self.endpoint(
            func='upload',
            params={
                'type': 'standard',
                'overwrite': 1 if overwrite else 0,
                'dest_path': dir_path,
                'progress': file_path
            }),
            files={
                'file': (
                    file_name,
                    data,
                    'application/octet-stream'
                )
            }
        )
    
    def get_share_link_list(self, dir_='ASC', start=0, limit=10000, sort_type='filename'):
        
        return self.req(self.endpoint(
                func='get_share_list',
                params={
                    'dir': dir_,
                    'start': start,
                    'limit': limit,
                    'sort': sort_type
                }
            )
        )
    
    def create_share_link(self, file_path, hostname=None, ssl=False, access_code=None, expire_time=None):
        
        params = {}
        
        params['path'], params['file_name'] = os.path.split(file_path)
        params['hostname'] = hostname if hostname is not None else self.host
        params['ssl'] = 'true' if ssl else 'false'
        
        if access_code is not None:
            params['access_code'] = access_code
        
        if expire_time is not None:
            params['expire_time'] = int(expire_time.timestamp())
        
        params['file_total'] = 1
        params['c'] = 1
        
        return self.req(self.endpoint(
                func='get_share_link',
                params=params,
            )
        )