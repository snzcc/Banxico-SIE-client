from requests import Request, Session


class ClienteSIE():
    """
    Banxico SIE's API client
    To instantiate it, you are going to require a token from Banxico's SIE website
        -> SIE website: https://www.banxico.org.mx/SieAPIRest/service/v1/
    The standard format of response is JSON but XML and HTML can also be returned*

    token -> A valid token from Banxico's SIE website -- must be string
    response format -> Either JSON or XML; HTML is also possible in theory but to the day of publishing, I 
                                     could not get any HTML response -- must be string
    language -> Responses fields can be returned in Spanish ('SPA') or English ('ENG'); Spanish is the default 
                        -- must be string
    series -> Series can be in 2 styles: range (e.g.: 'SF12-SF20') or one by one (e.g.: 'SF1', 'SF2', ...)**
                   -- must be string

    *At the time of writing this client, I was not able to get any response in HTML so JSON or XML are 
      advised
    **Notice that they must be a string or series of strings as well
    """
    def __init__(self, *series, token = None, response_format = "JSON", language = "SPA"):
        self.token = token
        self.headers = self.headerz()
        self.format = response_format.upper()
        self.lang = language.upper()
        self.series = self.unpack(series)
        self.params = {}
        self.dates = None
        self.settn()
        self.b_url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/"
        self.session = Session()
        
    def addDates(self, yyyy_1, mm_1, dd_1, yyyy_0, mm_0,dd_0):
        """
        Adds starting and ending dates to the client 
        Note: In order to get request to the API an 'interval'-ed series, this method must be run

        End date (most recent) is given in yyyy_1, mm_1, dd_1
        Start date (oldest) is given in yyyy_0, mm_0, dd_0
        Parameters are expected to be integers
        """
        date1 = str(yyyy_1) + '-' + str(mm_1) + '-' + str(dd_1)
        date0 = str(yyyy_0) + '-' + str(mm_0) + '-' + str(dd_0) + '/'
        result = date0 + date1
        self.dates = result

    def addMoreSeries(self, *series):
        """
        Adds more series to the client 
        Series must be given as strings
        """
        for item in series:
            self.series.append(arg)

    def removeSeries(self, *series):
        """
        Removes series from the client
        Series must be given as strings
        """
        for item in series:
            self.series.remove(item)

    def changeResponseFormat(self, new_format):
        """
        Changes response format of requests
        Must be 'XML', 'JSON' or 'HTML'
        """
        self.format = new_format
        self.resp_form()

    def changeResponseLanguage(self, new_language):
        """
        Changes response language
        Can only be Spanish ('SPA') or English ('ENG')
        """
        self.lang = new_language
        self.langs()

    def change_token(self, token):
        """
        Changes client's token
        Token must be given as a string
        """
        self.token = token
        self.headerz()

    def series2string(self):
        """
        Makes the list of series a string to be sent in requests
        Just for requests building, do not call this method
        """
        string = ''
        for item in self.series:
            if string == '':
                string = string + item
            else:
                string = string + ',' + item 
        return string

    def seriesMetadata(self):
        """
        Builds the appropriate URL for metadata requests
        """
        addition = self.series2string()
        url = self.b_url + '/' + addition 
        return url

    def seriesWhole(self):
        """
        Builds the appropriate URL for whole series requests
        """
        url = self.seriesMetadata() + '/' + 'datos'
        return url

    def seriesLast(self):
        """
        Builds the appropriate URL for last observation requests
        """
        url = self.seriesWhole() + '/' + 'oportuno'
        return url

    def seriesInterval(self):
        """
        Builds the appropriate URL for interval requests
        """
        url = self.seriesWhole() + self.dates
        return url


    def getSeriesMetadata(self):
        """
        Requests series metadata and returns response in the set language and format
        """
        req = self.set_request(self.seriesMetadata())
        res = self.session.send(req)
        return res.text

    def getSeriesWhole(self):
        """
        Requests whole series (all available observations) and returns response in the set language and 
        format
        """
        req = self.set_request(self.seriesWhole())
        res = self.session.send(req)
        return res.text

    def getSeriesLast(self):
        """
        Requests series last observation and returns response in the set language and format
        """
        req = self.set_request(self.seriesLast())
        res = self.session.send(req)
        return res.text

    def getSeriesInterval(self):
        """
        Requests series from a starting and ending date and returns response in the set language and format
        """
        req = self.set_request(self.seriesInterval())
        res = self.session.send(req)
        return res.text


    def set_request(self, url):
        """
        Builds and prepares the request to be sent
        """
        r = Request(method='GET', url = url, headers = self.headers, params = self.params)
        return r.prepare()

    def resp_form(self):
        """
        Returns the format in which response is to be requested: JSON, XML or HTML
        Note: to the day of publishing this code, HTML is not working so JSON or XML are advised
        """
        res = "mediaType"
        if self.format == "JSON":
            self.params[res] = "json"
        if self.format == "XML":
            self.params[res] = "xml"
        if self.format == "HMTL":
            self.params[res] = "html"
        
    def langs(self):
        """
        Returns the language in which response is requested
        Do not call it
        """
        lan = "locale"
        if self.lang == "SPA":
            self.params[lan] = "es"
        if self.lang == "ENG":
            self.params[lan] = "en"

    def headerz(self):
        """
        Sets appropriate headers
        """
        return {"Bmx-Token": self.token}

    def settn(self):
        """
        Sets client's headers and parameters
        Do not call it
        """
        self.resp_form()
        self.langs()
        self.headerz()

    def unpack(self, series):
        """
        Unpacks *series tuple
        """
        res = []
        for item in series:
            res.append(item)
        return res