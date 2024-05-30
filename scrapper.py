import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from flask import Flask, request, render_template, redirect
app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
@app.route('/')
def main(keyword="python programming"):
    try:
        driver.get(f'https://www.youtube.com/results?search_query={keyword}')
        ActionChains(driver).scroll_by_amount(0,100000).perform()
        time.sleep(2)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content,'html.parser')
        anchor_elements = soup.find_all('a')
        channels_list = []
        videos_list = []
        playlists_list = []

        for element in anchor_elements:
            href = element.get('href')
            if href:
                full_href = "https://www.youtube.com" + href.split('&')[0]
                if '/@' in full_href and full_href not in channels_list:
                    channels_list.append(full_href)
                elif 'watch' in href:
                    embedUrl = "https://www.youtube.com/embed/"+href.split('&')[0].replace('/watch?v=','')
                    if embedUrl not in videos_list:
                        videos_list.append(embedUrl)
                    else:
                        continue
                elif 'playlist' in full_href and full_href not in playlists_list:
                    playlists_list.append(full_href)
                else:    
                    continue
        return render_template('index.html', channels_list=channels_list, videos_list=videos_list, playlists_list=playlists_list)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/search', methods=['POST'])
def searchFor():
    value = request.form['search']
    return redirect(f'/search/{value}')

@app.route('/search/<value>')
def searchedForValue(value):
    return main(keyword=value)


if __name__ == '__main__':
    app.run(debug=True)
    main()
