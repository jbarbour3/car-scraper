

def build_CL_search_url_strings():

    cars_to_search = create_2dList_from_csv('cars_to_search.csv')

    cities_to_query = create_2dList_from_csv('cities_to_query.csv')

    with open('search_url_strings.csv','w') as f:
        for (make, model, from_year, to_year) in cars_to_search:
            for (city, state, craigslist_base_url) in cities_to_query:
                url = build_search_url( craigslist_base_url, city, state, make, model, from_year, to_year)
                f.write(url)
                print(url)
                f.write('\n')

    return None


def create_2dList_from_csv(a_csv_file, first_line_is_header=True):
        a2dList = []
        with open(a_csv_file) as f:
            for line in f:
                if first_line_is_header:
                    first_line_is_header=False
                else:
                    data = line.strip('\n')
                    data = data.split(',')
                    a2dList.append(data)
        return a2dList


def build_search_url(a_base_url, a_city, a_state, a_make, a_model, a_from_year, a_to_year):
        """ writes the craigslist search url for a city for a specified make/model and year range
        """
        url = a_base_url
        url += 'cta?srchType=T&'                    # search both private and dealer
        url += 'auto_make_model=' + a_make + "+"    # set the make
        url += a_model                              # set the model
        url += '&min_auto_year=' + a_from_year      # set the from year
        url += '&max_auto_year=' + a_to_year        # set the to year
        return url


if __name__ == '__main__':
    build_CL_search_url_strings()