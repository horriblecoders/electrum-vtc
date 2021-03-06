import gettext

class _(unicode):

    observers = set()
    lang = None

    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            _.switch_lang('en')
        t = _.translate(s, *args, **kwargs)
        o = super(_, cls).__new__(cls, t)
        o.source_text = s
        return o

    @staticmethod
    def translate(s, *args, **kwargs):
        tr = _.lang(s).format(args, kwargs)
        tr = tr.decode('utf8')
        return tr

    @staticmethod
    def bind(label):
        try:
            _.observers.add(label)
        except:
            pass
        # garbage collection
        new = set()
        for label in _.observers:
            try:
                new.add(label)
            except:
                pass
        _.observers = new

    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        from electrum_vtc.i18n import LOCALE_DIR
        locales = gettext.translation('electrum', LOCALE_DIR, languages=[lang], fallback=True)
        _.lang = locales.gettext
        for label in _.observers:
            try:
                label.text = _(label.text.source_text)
            except:
                pass
