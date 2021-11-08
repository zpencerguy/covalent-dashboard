from datetime import datetime, timedelta
from collections import MutableMapping


class CacheManager(MutableMapping):

    def __init__(self,
                update_fun,
                expire_timediff=timedelta(days=1),
                **kwargs):

       self.update_fun = update_fun
       self.expire_timediff = expire_timediff
       self._dict = dict()
       self._update_kwargs = kwargs

    def __getitem__(self, key):

       if not self._is_valid(key) and self.update_fun:
           value = self.update_fun(key, **self._update_kwargs)
           self.__setitem__(key, value)
       return self._dict[key][1]

    def __setitem__(self, key, value):
       self._dict[key] = (datetime.now(), value)

    def __delitem__(self, key):
       del self._dict[key]

    def __iter__(self):
       return iter(self._dict)

    def __len__(self):
       return len(self._dict)

    def _is_valid(self, key):
       if key in self._dict:
           timestamp = self._dict[key][0]
           if datetime.now() - timestamp < self.expire_timediff:
               return True
       return False

    def cleanup_cache(self):
       # Clear out all expired entries from the cache
       expired_keys = list()
       for key, val in self._dict.items():

           if not self._is_valid(key):
               expired_keys.append(key)

       for key in expired_keys:
           del self._dict[key]