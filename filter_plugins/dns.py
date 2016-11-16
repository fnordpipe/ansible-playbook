# Copyright (c) 2016 crito <crito@fifo.sh>

class FilterModule(object):
    def filters(self):
        return {
            'getDomain': self.getDomain,
            'groupZones': self.groupZones
        }

    def getDomain(self, value):
        return value[value.find('.') + 1:]

    def groupZones(self, hosts, hostvars):
        zones = {}
        for host in hosts:
            if host in hostvars and 'ansible_default_ipv4' in hostvars[host]:
                zones.setdefault(self.getDomain(host), []).append({
                    'name': host.split('.')[0],
                    'type': 'A',
                    'data': hostvars[host]['ansible_default_ipv4']['address']
                })
        return zones
