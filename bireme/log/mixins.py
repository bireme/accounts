#-*- coding: utf-8 -*-
from django.forms.models import model_to_dict


class AuditLog(object):
    '''
    Class used to mark wich models audit log of changes will be recorded
    '''
    def __init__(self, *args, **kwargs):
        super(AuditLog, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])

    def save(self, *args, **kwargs):
        super(AuditLog, self).save(*args, **kwargs)
        self.__initial = self._dict
