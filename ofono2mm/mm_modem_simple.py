from dbus_next.service import (ServiceInterface, method, dbus_property, signal)
from dbus_next.constants import PropertyAccess
from dbus_next import Variant

class MMModemSimpleInterface(ServiceInterface):
    def __init__(self, mm_modem, ofono_interfaces, ofono_interface_props):
        super().__init__('org.freedesktop.ModemManager1.Modem.Simple')
        self.mm_modem = mm_modem
        self.ofono_interfaces = ofono_interfaces
        self.ofono_interface_props = ofono_interface_props
        self.props = {
             'state': Variant('u', 6),
             'signal-quality': Variant('(ub)', [0, True]),
             'current-bands': Variant('au', []),
             'access-technologies': Variant('u', 19),
             'm3gpp-registration-state': Variant('u', 4),
             'm3gpp-operator-code': Variant('s', ''),
             'm3gpp-operator-name': Variant('s', ''),
             'cdma-cdma1x-registration-state': Variant('u', 0),
             'cdma-evdo-registration-state': Variant('u', 0),
             'cdma-sid': Variant('u', 0),
             'cdma-nid': Variant('u', 0)
        }

    async def set_props(self):
        old_props = self.props.copy()
        if 'org.ofono.NetworkRegistration' in self.ofono_interface_props:
            self.props['m3gpp-operator-name'] = Variant('s', self.ofono_interface_props['org.ofono.NetworkRegistration']['Name'].value if "Name" in self.ofono_interface_props['org.ofono.NetworkRegistration'] else '')

            if 'MobileCountryCode' in self.ofono_interface_props['org.ofono.NetworkRegistration']:
                MCC = self.ofono_interface_props['org.ofono.NetworkRegistration']['MobileCountryCode'].value
            else:
                MCC = ''

            if 'MobileNetworkCode' in self.ofono_interface_props['org.ofono.NetworkRegistration']:
                MNC = self.ofono_interface_props['org.ofono.NetworkRegistration']['MobileNetworkCode'].value
            else:
                MNC = ''

            self.props['m3gpp-operator-code'] = Variant('s', f'{MCC}-{MNC}')

            if 'Strength' in self.ofono_interface_props['org.ofono.NetworkRegistration']:
                self.props['signal-quality'] = Variant('(ub)', [self.ofono_interface_props['org.ofono.NetworkRegistration']['Strength'].value, True])

            if 'Status' in self.ofono_interface_props['org.ofono.NetworkRegistration']:
                if self.ofono_interface_props['org.ofono.NetworkRegistration']['Status'].value == 'registered' or self.ofono_interface_props['org.ofono.NetworkRegistration']['Status'].value == 'roaming':
                    self.props['state'] = Variant('u', 8)
                elif self.ofono_interface_props['org.ofono.NetworkRegistration']['Status'].value == 'searching':
                    self.props['state'] = Variant('u', 7)
        else:
            self.props['m3gpp-operator-name'] = Variant('s', '')
            self.props['m3gpp-operator-code'] = Variant('s', '')
            self.props['signal-quality'] = Variant('(ub)', [0, True])
            self.props['state'] = Variant('u', 6)

    @method()
    async def Connect(self, properties: 'a{sv}') -> 'o':
        for b in self.mm_modem.bearers:
            if self.mm_modem.bearers[b].props['Properties'].value['apn'] == properties['apn']:
                await self.mm_modem.bearers[b].add_auth_ofono(properties['username'].value if 'username' in properties else '',
                                                                properties['password'].value if 'password' in properties else '')
                self.mm_modem.bearers[b].props['Properties'] = Variant('a{sv}', properties)
                await self.mm_modem.bearers[b].doConnect()
                return b

        bearer = await self.mm_modem.doCreateBearer(properties)

        try:
            await self.mm_modem.bearers[bearer].doConnect()
        except Exception as e:
            pass

        return bearer

    @method()
    async def Disconnect(self, path: 'o'):
        if path == '/':
            for b in self.mm_modem.bearers:
                try:
                    await self.mm_modem.bearers[b].doDisconnect()
                except Exception as e:
                    pass
        if path in self.mm_modem.bearers:
            try:
                await self.mm_modem.bearers[path].doDisconnect()
            except Exception as e:
                pass

    @method()
    async def GetStatus(self) -> 'a{sv}':
        await self.set_props()
        return self.props
