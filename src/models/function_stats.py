from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from datetime import datetime
from os import environ


class FunctionStatsModel(Model):
    """
    Function stats
    """
    class Meta:
        table_name = "function_stats"
        region = environ.get('AWS_REGION')
    created_at = UnicodeAttribute(
        hash_key=True,
        default=datetime.now().strftime("% Y-%m-%d % H: %")
    )

    message = UnicodeAttribute(
        default=''
    )
