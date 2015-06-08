from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZTUtils import  make_query

BatchTemplate = ViewPageTemplateFile("batchnavigation.pt")


class BatchMacrosView(BrowserView):
    @property
    def macros(self):
        return self.template.macros


class BatchView(BrowserView):
    """ View class for browser navigation  (classic) """

    template = BatchTemplate
    batch = None
    batchformkeys = None

    def __call__(self, batch, batchformkeys=None):
        self.batch = batch
        self.batchformkeys = batchformkeys
        return self.template()

    def make_link(self, pagenumber):
        raise NotImplementedError


class PloneBatchView(BatchView):
    def make_link(self, pagenumber=None):
        form = self.request.form
        if self.batchformkeys:
            batchlinkparams = dict([(key, form[key])
                                    for key in self.batchformkeys
                                    if key in form])
        else:
            batchlinkparams = form.copy()

        start = max(pagenumber - 1, 0) * self.batch.pagesize
        return '%s?%s' % (self.context.absolute_url(), make_query(batchlinkparams,
                         {self.batch.b_start_str: start}))
