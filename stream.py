from io import RawIOBase

class BotoStreamingIO(RawIOBase):
    def __init__(self, body, content_length):
        self.body = body
        self.remaining = content_length

    def read(self, size=-1):
        if size == -1:
            return self.readall()
        return self.body.read(size)

    def readable(self, _):
        return True

    def readinto(self, buff):
        if not self.remaining:
            return 0
        sz0 = min(len(buff), self.remaining)
        data = self.body.read(sz0)
        sz = len(data)
        self.remaining -= sz
        #if not data:
        if sz < sz0 and self.remaining:
            raise EOFError(
                'The client disconnected while sending the POST/PUT body ' \
                '({} more bytes were expected)'.format(self.remaining)
            )
        buff[:sz] = data
        return sz
