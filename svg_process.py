import json
import xml.etree.ElementTree as ET

icons = [
    "skc_d",
    "skc_n",
    "fg_d",
    "fg_n",
    "bkn_d",
    "bkn_n",
    "bkn_-ra_d",
    "bkn_-ra_n",
    "bkn_-sn_d",
    "bkn_-sn_n",
    "bkn_ra_d",
    "bkn_ra_n",
    "bkn_sn_d",
    "bkn_sn_n",
    "bkn_+ra_d",
    "bkn_+ra_n",
    "bkn_+sn_d",
    "bkn_+sn_n",
    "ovc_ts",
    "ovc_ts_ra",
    "ovc_ts_ha",
    "ovc",
    "ovc_-ra",
    "ovc_-sn",
    "ovc_ra",
    "ovc_sn",
    "ovc_+ra",
    "ovc_+sn",
    "ovc_ra_sn",
    "ovc_ha",
    "-bl",
    "bl",
    "dst",
    "du_st",
    "smog",
    "strm",
    "vlka"
]

ids = dict()

for icon in icons:
    ids[icon.replace("+","p").replace("-","m")] = icon

visibility = []

tree = ET.parse('weather.svg')
root = tree.getroot()
for elem in root.findall(".//*[@id]"):
    for id in ids.keys():
        if elem.attrib["id"].endswith(id):
            visibility.append({
    "write": {
      "enable": False,
      "channel": None,
      "value": {
        "off": "0",
        "on": "1"
      },
      "check": False
    },
    "click": {
      "enable": False,
      "dashboard": None
    },
    "style": {
      "enable": False,
      "channel": None,
      "value": ""
    },
    "visible": {
      "enable": True,
      "channel": "weather/"+ elem.attrib["id"].replace(id, "") +"icon",
      "condition": "==",
      "value": "\"" + ids[id] + "\""
    },
    "long-press": {
      "enable": False,
      "dashboard": None
    },
    "long-press-write": {
      "enable": False,
      "channel": None,
      "value": {
        "off": "0",
        "on": "1"
      },
      "check": False
    },
    "id": elem.attrib["id"]
  }
)

print(json.dumps(visibility))