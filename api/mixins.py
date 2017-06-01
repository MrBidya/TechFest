class UsageMixin:
    usage_type = ''
    usage_example = ''
    @classmethod
    def get_usage(cls):
        if cls.usage_type:
            string = "Send a request to this url with the following data: {{'equation': '{}'}}".format(cls.usage_type)
        else:
            string = ''
        return string

    @classmethod
    def get_example(cls):
        if cls.usage_example:
            string = "{{'equation': {}}}".format(cls.usage_example)
        else:
            string = ''
        return string
