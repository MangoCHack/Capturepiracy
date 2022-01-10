import requests
import bs4
import re

def get_ga(url: str):
    url_with_scheme = "https://" + url if "//" not in url else url
    try:
        response = requests.get(url_with_scheme, stream=True)
        print(response.headers)
        soup = bs4.BeautifulSoup(response.content, "html5lib")
    except:
        return 'None'
    else:
        google_analytics_pattern = re.compile(r"UA-[0-9]+-[0-9]+")
        google_analytics_pattern_ver4 = re.compile(r'G-\w+')

        google_analytics_codes = google_analytics_pattern.findall(
            " ".join(
                [
                    str(script_tag)
                    for script_tag in soup.find_all("script", {"src": True})
                ]
            )
        )

        google_analytics_codes_ver4 = google_analytics_pattern_ver4.findall(
            " ".join(
                [
                    str(script_tag)
                    for script_tag in soup.find_all("script", {"src": True})
                ]
            )
        )

    if len(google_analytics_codes) == 0 and len(google_analytics_codes_ver4) != 0:
        google_analytics_codes = google_analytics_codes_ver4
    elif len(google_analytics_codes) == 0 and len(google_analytics_codes_ver4) == 0:
        google_analytics_codes = ['None']
    return ' '.join(google_analytics_codes)

if __name__ == '__main__':
    fp = open('ga.csv','r', encoding='cp949')
    lines = fp.readlines()
    fp.close()
    del lines[0]

    fp2 = open('GA_result.csv','w')
    fp2.write('Site URL, GA\n')
    for l in lines:
        site_url = l.strip()
        main_ga = get_ga(site_url)
        l = l + ',' + main_ga + '\n'
        print(l)
        fp2.write(l)
    fp2.close()