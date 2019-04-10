from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder

class FHJSONEncoder(JSONEncoder):
    """
    Extending the JSONEncoder class to add extra-functionality
    """
    def iterencode(self, o, _one_shot=False):
        """
        Overriding the method to replace the 'NaN' with 'null' values
        """
        iterencode = super(FHJSONEncoder, self).iterencode(o, _one_shot)
        iterencode = [i.replace('NaN', 'null') for i in iterencode]
        return iterencode


class FHJSONRenderer(JSONRenderer):
    """
    Extending the JSONRenderer class to add extra-functionality
    """
    # Set our custom encoder as default one
    encoder_class = FHJSONEncoder