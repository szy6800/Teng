import undetected_chromedriver as uc
driver = uc.Chrome(version_main=104, use_subprocess=True)
# driver.set_window_size(80, 80)
driver.set_window_position(0, 0)
driver.get("https://www.itjuzi.com/login")
print(driver.page_source)