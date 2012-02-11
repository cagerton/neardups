from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
import re


class XRayHasher():
    """Hacky groundwork of a project that extracts some concept of structure from documents without looking at the coentent"""

    # these tokens are going to be hella fat.
    def gen_token(self, tag, height=1, attrs=True, prefix=""):
        """Generates a token for a given tag."""
        ## strip whitespace.
        if attrs:
          at_string = "".join(sorted(["K:%s;V:%s;" % (k.lower(),v.lower()) for k,v in tag.attrs]))
        else:
          at_string = ""
        tag_string = "T:%s;%s" % (tag.name, at_string)
        if height > 1:
            child_tokens = [self.gen_token(child, height=height-1, attrs=attrs) for child in tag.findAll(recursive=False)]
        else:
            child_tokens = [[""]]
        if len(child_tokens)==0:
            child_tokens = [["LEAF"]]

        # flatten. ugly.
        child_tokens = [item for sublist in child_tokens for item in sublist]

        return ["%s-%s" % (tag_string, child_token) for child_token in [t for t in child_tokens]]

    def gen_tags(self,soup, height=1, attrs=True):
        for tag in soup.findAll():
            for tok in self.gen_token(tag, height=height, attrs=attrs):
                yield tok


if __name__ == "__main__":
    html = "<html><head><title>foo</title></head><body><div><div>one</div><div>two</div></div></body></html>"
    xray = XRayHasher()

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="read FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.filename is not None:
        f = open(options.filename)
        html = f.read()
        f.close

    for t in xray.gen_tags(BeautifulSoup(html), height=2):
        print re.sub("[^\w]","",t)
