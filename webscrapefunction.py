def runAlgorithm():
    from re import findall
    from math import ceil
    from time import sleep
    from random import uniform
    import csv


    def get_search_urls():
        """ returns the craigslist (state, urls) to search each city in Georgia and California for our target make/model and year
        """
        city_state_to_search = {'Georgia': {'Atlanta': 'https://atlanta.craigslist.org/search/',
                                             'Albany': 'https://albanyga.craigslist.org/search/',
                                            'Athens': 'https://athensga.craigslist.org/search/',
                                             'Augusta': 'https://augusta.craigslist.org/search/',
                                           'Brunswick':'https://brunswick.craigslist.org/search/',
                                           'Columbus': 'https://columbusga.craigslist.org/search/',
                                           'Macon': 'https://macon.craigslist.org/search/',
                                           'North West GA': 'http://nwga.craigslist.org/search/',
                                           'Savannah': 'https://savannah.craigslist.org/search/',
                                           'Statesboro': 'https://statesboro.craigslist.org/search/',
                                          'Valdosta': 'https://valdosta.craigslist.org/search/'},
                            'California': {'bakersfield':	'https://bakersfield.craigslist.org/search/',
                                             'chico':	'https://chico.craigslist.org/search/',
                                            'fresno/madera':	'https://fresno.craigslist.org/search/',
                                            'gold country':	'https://goldcountry.craigslist.org/search/',
                                            'hanford-corcoran':	'https://hanford.craigslist.org/search/',
                                            'humboldt county':	'https://humboldt.craigslist.org/search/',
                                            'imperial county':	'https://imperial.craigslist.org/search/',
                                            'inland empire':	'https://inlandempire.craigslist.org/search/',
                                            'los angeles':	'https://losangeles.craigslist.org/search/',
                                            'mendocino county':	'https://mendocino.craigslist.org/search/',
                                            'merced':	'https://merced.craigslist.org/search/',
                                            'modesto':	'https://modesto.craigslist.org/search/',
                                            'monterey bay':	'https://monterey.craigslist.org/search/',
                                            'orange county':	'https://orangecounty.craigslist.org/search/',
                                            'palm springs':	'https://palmsprings.craigslist.org/search/',
                                            'redding':	'https://redding.craigslist.org/search/',
                                            'sacramento':	'https://sacramento.craigslist.org/search/',
                                            'san diego':	'https://sandiego.craigslist.org/search/',
                                            'san luis obispo':	'https://slo.craigslist.org/search/',
                                            'santa barbara':	'https://santabarbara.craigslist.org/search/',
                                            'santa maria':	'https://santamaria.craigslist.org/search/',
                                            'san francisco bay area':	'https://sfbay.craigslist.org/search/',
                                            'siskiyou county':	'https://siskiyou.craigslist.org/search/',
                                            'stockton':	'https://stockton.craigslist.org/search/',
                                            'susanville':	'https://susanville.craigslist.org/search/',
                                            'ventura county':	'https://ventura.craigslist.org/search/',
                                            'visalia-tulare':	'https://visalia.craigslist.org/search/',
                                            'yuba-sutter':	'https://yubasutter.craigslist.org/search/'}
                                }
        city_state_to_search = {'Georgia': {'Atlanta': 'https://atlanta.craigslist.org/search/',
                                            'Albany': 'https://albanyga.craigslist.org/search/',
                                            }
                                }

        urls = []

        for state in city_state_to_search.keys():
            for city in city_state_to_search[state].keys():
                for model in ["Camry", "Corolla"]:
                    url = city_state_to_search[state][city]
                    url += 'cta?srchType=T&'                                   # search both private and dealer
                    url += 'auto_make_model=' + "Toyota" + "+"                 # set the make to Toyota
                    url += model                                               # set the model to either Camry or Corolla
                    url += '&min_auto_year=' + "2010"                          # set min year to 2010
                    url += '&max_auto_year=' + "2015"                          # set max year to 2015
                    urls.append((state, url))
                    print(urls)# save the url that we will search

        print('{0} Search urls constructed'.format(str(len(urls))))
        for (index,url) in enumerate(urls):
            print("{0}. {1}".format(index +1, url))

        return urls

    def get_site_text(aList_of_urls):

        """
         returns a list of tuples containing the (aURL, correspondingHTML)
        """
        import urllib.request
        theText = []
        for state, url in aList_of_urls:

            request = urllib.request.Request(url)
            try:
                response = urllib.request.urlopen(request)
                the_page = response.read()
                response.close()
                theText.append((state, url, the_page.decode()))
            except:
                print("! Connection Closed ! " + url)

        return theText

    def get_ad_urls(aList_of_search_state_url_html_pairs):
        """ Returns a list of tuples containting (year, make, model, price, state, ad_url)"""
        ad_urls = [] # this will be a list of tuples containing (ad_title, state, price, ad_url)
        for (state, url, html) in aList_of_search_state_url_html_pairs:

            print(url)
            # if the search html contains 0 ads, skip the ad searching algorithm
            display_count = findall("""<span class="displaycountShow">((.|\n)*?)</span>""", html)

            if display_count[0][0]=='0':
                print("   0 Results Found | {}".format(url))
            else:
                # get the base url, we need it it build the ad urls
                base_url = findall('((.|\n)*?)search/', url)
                base_url = base_url[0][0]


                # get the number of ads in total

                number_of_ads = findall("""<span class="totalcount">(\d*)</span>""", html)
                #print(number_of_ads)
                number_of_ads = number_of_ads[0]
                #print(number_of_ads)
                #print(" " * (4 - len(number_of_ads)) + number_of_ads + " Results Found | {}".format(url))


                # get the number of pages on the craigslist search url
                number_of_pages = ceil(int(number_of_ads)/100)
                #print("number of pages {}".format(number_of_pages))

                # build a search url for each page
                page_urls = [url]
                if number_of_pages>1:
                    for i in range(1,number_of_pages):
                        new_url = url+"&s=" + str(i*100)
                        page_urls.append(new_url)


                # for each page of ads, get the ad titles and urls
                for i,u in enumerate(page_urls):
                    #sleep(1 * uniform(0, 1))
                    # print("      page {} | {}".format(i+1,u))
                    # print([u])
                    page_text = get_site_text([(state,u)])
                    page_text = page_text[0][2]
                    # print("page_text")
                    # print(page_text)
                    html_ad_pattern = """<p class="result-info">((.|\n)*?)<\/p>"""
                    ads = findall(html_ad_pattern, page_text)
                    for ad in ads:

                        ad = ad[0]
                        ad_url = findall("""<a href="(.*)" data-id="\d*" class="result-title hdrlnk">""", ad)[0]


                        # if the ad url is longer than 20 it is a search result from another city
                        if len(ad_url)<21:
                            #sleep(1*uniform(0,1))

                            title = findall("""class="result-title hdrlnk">(.*)<\/a>""", ad)[0]
                            title = title.upper()



                            if "TOYOTA" in title:
                                make = "Toyota"
                            else:
                                make = "unk"

                            if "CAMRY" in title:
                                model = "Camry"
                            else:
                                model = "unk"

                            if "COROLLA" in title:
                                model = "Corolla"



                            year = findall("(\d\d\d\d)", title)
                            if year == []:
                                year = "unk"
                            else:
                                year = year[0]

                            price = findall("""<span class="result-price">(.*)</span>""", ad)
                            if price == []:
                                price = "unk"
                            else:
                                price = price[0]

                            ad_url = base_url+ad_url

                            if "unk" not in [year, make, model, price]:
                                #print("{} | {} | {} | {} | {} | {}".format(year, make, model, price, state, ad_url))
                                observation = [year, make, model, price, state, ad_url]
                                ad_urls.append(observation)

        return ad_urls

    def get_regression_predictors(aStringOFHTML):
        """returns an ordered list of predictors from a single page of text"""
        predictors = ["odometer: ", "transmission: ", "fuel: ", "paint color: ", "cylinders: ", "condition: ",
                      "title status: "]
        predictor_values = []
        for predictor in predictors:
            aPattern = "<span>" + predictor + "<b>(.*)<\/b><\/span>"
            data = findall(aPattern, aStringOFHTML)
            if len(data) == 0:
                data = "unk"
            else:
                data = data[0]
            predictor_values.append(data)
        return predictor_values

    a = get_search_urls()

    b = get_site_text(a)

    c = get_ad_urls(b)

    end_result = [["URL", "YEAR", "MAKE", "MODEL", "PRICE", "STATE",
                   "ODOMETER", "TRANSMISSION", "FUEL", "COLOR", "CYLINDERS", "CONDITION"]]
    for (year, make, model, price, state, ad_url) in c:
        observation = [ad_url, year, make, model, price, state]
        try:
            text = get_site_text([(state,ad_url)])[0][2]
            predictors = get_regression_predictors(text)
            observation.extend(predictors)
            end_result.append(observation)
        except:
            pass

    outputfile = "data.csv"

    import csv
    with open(outputfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for result in end_result:
            writer.writerow(result)

runAlgorithm()