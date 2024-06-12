import json
from typing import List, Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class GoogleApiRequest:
    def __init__(self, topics: List[str] = ["rugby", "football", "tennis"]) -> None:
        self.base_url = "https://trends.google.com/"
        self.topics = topics

    def _make_request(self) -> str:
        """
        This is the main scraper. It uses selenium in the backend to hit 2 consecutive pages to
        trigger the page's requests to the backend API. The first page, to stash the cookies,
        the second to render the page that hits the target API. The tokens cannot be generated
        client side so this is a temporary workaround until google releases an official API.

        The logging is boosted so that the Network requests can be scraped, which in turn will
        give the API request used to get the Share of Search data displayed on Google's trend
        data page.
        """

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)

        driver.get(self.base_url)
        WebDriverWait(driver, 2).until(lambda d: d.get_cookie("NID")["value"])

        driver.get(
            self.base_url
            + f"trends/explore?date=today%203-m&geo=GB&q={','.join(self.topics)}&hl=en"
        )
        WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "defs"))
        )

        logs = driver.get_log("performance")
        driver.quit()

        return logs

    def _parse_logs(self, logs: str) -> str:
        """
        The target_url is the endpoint used to generate the widget data.
        The target api request is already formed within the logs using the query_url as a base.
        All that needs to be done here is to scan the logs for the target url. This includes the
        token that is generated server side.
        """

        target_url = ""
        query_url = self.base_url + "trends/api/widgetdata/multiline?"

        for log in logs:
            entry = json.loads(log["message"])["message"]
            if (
                entry["method"] == "Network.responseReceived"
                and query_url in entry["params"]["response"]["url"]
            ):
                target_url = entry["params"]["response"]["url"]

        return target_url

    def request_data(self) -> Optional[str]:
        """
        Here we re-call the target endpoint to directly access the Share of Search data that
        sits behind Google's Widget.
        """

        logs = self._make_request()
        target_url = self._parse_logs(logs)

        if target_url:
            response = requests.get(target_url)
            if response.ok:
                data = response.text
                data = data.lstrip(")]}',")

                return data

        return
