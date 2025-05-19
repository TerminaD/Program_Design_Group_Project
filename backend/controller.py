class Controller:
    def __init__(self, db, crawler):
        self.db = db
        self.crawler = crawler

    def load_assignments(self):
        # Load from local database
        return self.db.get_assignments()

    def refresh_assignments(self):
        # Fetch new data and save
        items = self.crawler.fetch_assignments()
        self.db.save_assignments(items)
        return items
