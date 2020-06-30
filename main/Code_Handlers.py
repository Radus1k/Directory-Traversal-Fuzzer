class Code_Handlers:
    def __init__(self):
        self.OK = 200
        self.CREATED = 201
        self.NO_CONTENT = 204
        self.BAD_REQ = 400
        self.FORBIDDEN = 403
        self.UNATHORIZED = 401
        self.NOT_FOUND = 404
        self.CONFLICT = 409
        self.INTERNAL_ERROR = 500
        self.NOT_IMPLEMENTED = 501
        self.SERVICE_UNAV = 503

    def get_status(self, text, title):
        title = title.lower()
        text = text.lower()
        if title.find("201 created") > 0 or text.find("201 created") > 0:
            return self.CREATED
        if title.find("no content") > 0 or text.find("no content") > 0:# pretty risky..
            return self.NO_CONTENT
        if title.find("404 not found") > 0 or text.find('404')>0 or text.find("not found")>0 or text.find("no such file")>0:
            return self.NOT_FOUND
        if title.find("forbidden") > 0 or title.find("403") > 0 or text.find("forbidden") > 0:
            return self.FORBIDDEN
        if title.find("unauthorized") > 0 or title.find("401") > 0 or text.find("unauthorized") > 0 or text.find('permission denied')>0:
            return self.UNATHORIZED
        if title.find("conflict") > 0 or title.find("409") > 0: #or text.find("bad request") > 0:# too often
            return self.CONFLICT
        if title.find("internal error") > 0 or title.find("503") > 0 or text.find("internal error") > 0:
            return self.INTERNAL_ERROR
        if title.find("internal error") > 0 or title.find("503") > 0 or text.find("internal error") > 0:
            return self.INTERNAL_ERROR
        if title.find("not implemented") > 0 or title.find("500") > 0 or text.find("not implemented") > 0:
            return self.NOT_IMPLEMENTED
        if title.find("service unavailable") > 0 or title.find("503") > 0 or text.find("service unavailable") > 0:
            return self.SERVICE_UNAV
        return 200
