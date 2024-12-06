import feedparser as fp
import json
import Warnings as wn


class RSSFeedHandler:
    def __init__(self):
        self.feeds = []
        self.items = []

    def add_feed(self, url):
        self.feeds.append(url)

    def load_feed_urls(self, file):
        try:
            with open(file, "r") as f:
                self.feeds = [line.strip() for line in f if line.strip()]
        except FileNotFoundError as e:
            wn.warn("No file found", category=UserWarning)

    def save_feed_urls(self, file):
        with open(file, "w") as f:
            for url in self.feeds:
                file.write(url + "\n")

    def fetch_feeds(self):
        self.items = []
        for feed_url in self.feeds:
            feed = fp.parse(feed_url)
            for entry in feed.entries:
                self.items.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary
                        if "summary" in entry
                        else "",
                        "authors": entry.authors
                        if "authors" in entry
                        else "",
                        "tags": [],
                    }
                )

    def add_tag_to_item(self, item_index, tag):
        if 0 <= item_index <= len(self.items):
            self.itmes[item_index]["tags"].append(tag)
        else:
            raise IndexError("Index invalid")

    def add_tag_to_feed(self, url, tag):
        for item in self.items:
            if item.get("feed_url") == url:
                item["tags"].append(tag)

    def list_items(self):
        for i, item in enumerate(self.items):
            for k, v in item.items():
                print(f"{k}: {v}")
            print("\n")

    def save_items(self, file_path):
        with open(file_path, "w"):
            json.dump(self.items, file, indent=4)

    def load_items(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            wn.warn("File to load not found", category=UserWarning)
            return []

    def get_new_items(self, file_path):
        saved_items = self.load_items(file_path)
        saved_titles = {item["title"] for item in saved_items}
        return [
            item for item in self.items if item["title"] not in saved_titles
        ]


if __name__ == "__main__":
    handler = RSSFeedHandler()
    handler.add_feed("http://www.nature.com/nmat/current_issue/rss/")
    handler.fetch_feeds()
    handler.list_items()
