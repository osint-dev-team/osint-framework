from src.scripts.osint.social_networks.sn_src.vk.vk_checker import VKChecker

if __name__ == '__main__':
    # demo
    vkc = VKChecker('+7', '1234567890', 'D://chromedriver.exe')
    print(vkc.run())
