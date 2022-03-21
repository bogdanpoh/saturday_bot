
class BaseModel(object):
    def __str__(self):
        properties = vars(self)
        return ", ".join("%s: %s" % item for item in properties.items())
