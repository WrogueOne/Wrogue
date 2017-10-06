class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None,
                 is_blessed=False, is_cursed=False,
                 **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message

        self.is_blessed = is_blessed
        self.is_cursed = is_cursed
        
        self.function_kwargs = kwargs
