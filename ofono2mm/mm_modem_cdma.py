from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next.constants import PropertyAccess
from dbus_next import Variant

class MMModemCDMAInterface(ServiceInterface):
    def __init__(self, mm_modem):
        super().__init__('org.freedesktop.ModemManager1.Modem.ModemCdma')
        self.mm_modem = mm_modem
        self.props = {
            'ActivationState': Variant('u', 0),
            'Meid': Variant('s', ''),
            'Esn': Variant('s', ''),
            'Sid': Variant('u', 0),
            'Nid': Variant('u', 0),
            'Cdma1xRegistrationState': Variant('u', 0),
            'EvdoRegistrationState': Variant('u', 0)
        }

    @method()
    def Activate(self, carrier_code: 's'):
        pass

    @method()
    def ActivateManuel(self, properties: 'a{sv}') -> 'o':
        pass

    @dbus_property(access=PropertyAccess.READ)
    def ActivationState(self) -> 'u':
        return self.props['ActivationState'].value

    @dbus_property(access=PropertyAccess.READ)
    def Meid(self) -> 's':
        return self.props['Meid'].value

    @dbus_property(access=PropertyAccess.READ)
    def Esn(self) -> 's':
        return self.props['Esn'].value

    @dbus_property(access=PropertyAccess.READ)
    def Sid(self) -> 'u':
        return self.props['Sid'].value

    @dbus_property(access=PropertyAccess.READ)
    def Nid(self) -> 'u':
        return self.props['Nid'].value

    @dbus_property(access=PropertyAccess.READ)
    def Cdma1xRegistrationState(self) -> 'u':
        return self.props['Cdma1xRegistrationState'].value

    @dbus_property(access=PropertyAccess.READ)
    def EvdoRegistrationState(self) -> 'u':
        return self.props['Cdma1xRegistrationState'].value
