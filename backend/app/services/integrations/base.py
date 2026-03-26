class BaseIntegration:
    def fetch_data(self):
        raise NotImplementedError

    def transform(self, raw_data):
        raise NotImplementedError