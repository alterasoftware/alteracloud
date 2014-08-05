"""
.. moduleauthor:: Altera Corporation <rromano@altera.com>
"""

from __future__ import absolute_import

from . import alteracloud
from .alteracloud import AlteraApiConnection

__version__ = '0.1.0'

# do not set __package__ = "alteracloud", else we will end up with
# alteracloud.<*allofthethings*>
__all__ = ['AlteraApiConnection']

# avoid the "from alteracloud import alteracloud" idiom
del alteracloud




