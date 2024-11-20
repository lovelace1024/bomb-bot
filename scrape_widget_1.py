from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# URL of the widget page
hpwidgetlink = "https://www.innovativelanguage.com/widgets/wotd/embed.php?language=Hebrew&type=large&bg=url%28/widgets/wotd/skin/images/large/Mountains.png%29%20no-repeat%200%200&content=%23000&header=%2388A1B6&highlight=%2388A1B6&opacity=.25&scrollbg=%23323E47&sound=%239A958C&text=%23353B1A&quiz=N"

# Set up Selenium with Firefox and Geckodriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser UI)
service = Service("/snap/bin/geckodriver")  # Replace with your Geckodriver path
driver = webdriver.Firefox(service=service, options=options)
def scrape_link(url):
    try:
        # Open the URL in the browser
        driver.get(url)

        # Wait for JavaScript to load the content
        time.sleep(3)

        # Retrieve image source
        try:
            image_div = driver.find_element(By.CLASS_NAME, "wotd-widget-container-images-space")
            image = image_div.find_element(By.TAG_NAME, "img")
            image_src = image.get_attribute("src")
            print("Image Source:", image_src)
        except Exception as e:
            print("Error retrieving image:", e)

        # Retrieve text content
        try:
            text_span = driver.find_element(By.CLASS_NAME, "wotd-widget-sentence-main-space-text")
            text_content = text_span.text
            print("Text Content:", text_content)
        except Exception as e:
            print("Error retrieving text:", e)
        try:
            # Locate the <a> tag with the target class
            audio_link = driver.find_element(By.CLASS_NAME, "wotd-widget-sentence-main-space-sound")
            # Extract the href attribute
            audio_href = audio_link.get_attribute("href")
            print("Audio File Href:", audio_href)
        except Exception as e:
            print("Error retrieving audio file href:", e)
        try:
            # Locate the parent div with the unique class
            parent_div = driver.find_element(By.CLASS_NAME, "wotd-widget-container-up-inner")

            # Locate the target nested div within the parent
            title_r_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.romanization")
            title_v_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.vowelled")
            d_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.english")
            article_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.noun")
            # Retrieve the text content of the target div
            title_r_text = title_r_div.text
            title_v_text = title_v_div.text
            d_text = d_div.text
            article_text = article_div.text
            print("Title romanization Text:", title_r_text)
            print("Title vowelled Text:", title_v_text)
            print("Definition:", d_text)
            print("Article of Speech:", article_text)
        except Exception as e:
            print("Error retrieving something in title div:", e)
        try:
            # Locate the parent div with the class "jspContainer"
            jsp_container = driver.find_element(By.CLASS_NAME, "jspContainer")

            # Find all <span> elements with the target class inside the "jspContainer" div
            heb_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-main-space-text")
            rom_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.romanization")
            eng_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.english")
            vow_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.vowelled")
            # Extract the text content from each <span> and store in a list
            heb_list = [span.get_attribute("innerText") for span in heb_elements]
            rom_list = [span.get_attribute("innerText") for span in rom_elements]
            eng_list = [span.get_attribute("innerText") for span in eng_elements]
            vow_list = [span.get_attribute("innerText") for span in vow_elements]
#            for idx, span in enumerate(span_elements):
#                print(f"Span {idx + 1} - Visible: {span.is_displayed()}, Text: {span.get_attribute('innerText')}")
            print("Examples - Hebrew:", heb_list)
            print("Examples - English:", eng_list)
        except Exception as e:
            print("Error retrieving examples:", e)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()
    return image_src, text_content, title_r_text, title_v_text, d_text, article_text, heb_list, rom_list, eng_list, vow_list
#scrape_link(hpwidgetlink)
