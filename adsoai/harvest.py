from sickle import Sickle


class ZenodoHarvester(object):

    def __init__(self):
        self.url = "https://zenodo.org/oai2d"
        self.prefix = "oai_datacite"
        self.records = None
        self.count = 0

    def get_records(self, setname=None, last_logtime=None):
        if not setname:
            return
        else:
            harvester = Sickle(self.url)
            query = {"metadataPrefix": self.prefix,
                     "set": setname,
                     "from": last_logtime}
            self.records = harvester.ListRecords(**query)
