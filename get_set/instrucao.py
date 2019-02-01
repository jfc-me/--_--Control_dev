class Instrucoes():
    _ip = ""
    _result = ""

    @property
    def end_ip(self):
        return self._ip

    @end_ip.setter
    def end_ip(self, myIp):
        self._ip = myIp

    def _get_result(self):
        return self._result

    def _set_result(self,all_result):
        self._result = all_result

    resultado = property(fset=_set_result, fget=_get_result)