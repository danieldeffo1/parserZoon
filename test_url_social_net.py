from urllib.parse import unquote

url = "https://zoon.ru/redirect/?to=https%3A%2F%2Fvk.com%2Fmeddynasty&hash=fdf6e88a9c5fd8539a1d6ed8f8fbb03e&from=5b97a01451e59327c8330737.558c&ext_site=ext_vk&backurl=https%3A%2F%2Fzoon.ru%2Fspb%2Fmedical%2Fmeditsinskij_tsentr_dinastiya_na_ulitse_lenina%2F"
url = unquote(url.split("?to=")[1].split("&")[0])
print(url)
