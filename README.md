# Banxico-SIE-client
Python client for Banxico's SIE API.

It makes requests to the server way simpler.

    To instantiate it, you are going to require a token from Banxico's SIE website
        -> SIE website: https://www.banxico.org.mx/SieAPIRest/service/v1/
    The standard format of response is JSON but XML and HTML can also be returned*
    Also consider that you can only request up to 20 series per token and there's a daily query limit.
    For further information about the API visit the SIE website
    -----
    *At the time of writing this client, I was not able to get any response in HTML so JSON or XML are
     strongly advised

Example given:

    token = "c245dd5ed742818adc290e7605f27bda9f4af208cfd5ca668e8ea4c99527462d"
    client = ClienteSIE("SF61745","SF43718","SF43783", token = token)

    #Calling the next method returns the response in JSON and in Spanish by default (both can be changed after instantiation)

    client.getSeriesMetadata()

      {
        "bmx": {
          "series": [
            {
              "idSerie": "SF43783",
              "titulo": "TIIE a 28 días Tasa de interés en por ciento anual",
              "fechaInicio": "23/03/1995",
              "fechaFin": "16/01/2020",
              "periodicidad": "Diaria",
              "cifra": "Porcentajes",
              "unidad": "Sin Unidad"
            },
            {
              "idSerie": "SF43718",
              "titulo": "Tipo de cambio                                          Pesos por dólar E.U.A. Tipo de cambio para solventar obligaciones denominadas en moneda extranjera Fecha de determinación (FIX)",
              "fechaInicio": "12/11/1991",
              "fechaFin": "15/01/2020",
              "periodicidad": "Diaria",
              "cifra": "Tipo de Cambio",
              "unidad": "Pesos por Dólar"
            },
            {
              "idSerie": "SF61745",
              "titulo": "Tasa objetivo",
              "fechaInicio": "21/01/2008",
              "fechaFin": "15/01/2020",
              "periodicidad": "Diaria",
              "cifra": "Porcentajes",
              "unidad": "Sin Unidad"
            }
          ]
        }
      }

    #We can add more series if needed

    client.addMoreSeries("SF43878","SF111916")

    #And see which series are in the instance 

    client.series
      ['SF61745', 'SF43718', 'SF43783', 'SF43878', 'SF111916']
  

    There are 4 types of requests:
      ->Series metadata --> .getSeriesMetadata()
      ->Entire time series --> .getSeriesWhole()
      ->Latest series' observation --> .getSeriesLast()
      ->A starting and ending date lapse --> .getSeriesInterval()
