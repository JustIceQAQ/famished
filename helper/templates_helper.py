from jinja2.utils import markupsafe


class MomentJs(object):

    def __init__(self, timestamp):
        self.timestamp = timestamp

    # Wrapper to call moment.js method
    def render(self, method_format):
        return markupsafe.Markup(
            f"<script>\ndocument.write(moment(\"{self.timestamp}\").{method_format});\n</script>"
        )

    # Format time
    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def from_now(self):
        return self.render("fromNow()")
