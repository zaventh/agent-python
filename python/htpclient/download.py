import requests

import sys

from htpclient.initialize import Initialize


class Download:
    @staticmethod
    def download(url, output):
        if Initialize.get_os() == 1:
            output = output.replace("/", '\\')

        # Check header
        head = requests.head(url)
        # not sure if we only should allow 200, but then it's present for sure
        if head.status_code != 200:
            return False

        with open(output, "wb") as file:
            response = requests.get(url, stream=True)
            total_length = response.headers.get('Content-Length')

            if total_length is None:  # no content length header
                file.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\rDownloading: [%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write("\n")
        return True