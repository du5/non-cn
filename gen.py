from rich.progress import track
import ipaddress
import geoip2.database
import math

ASNReader = geoip2.database.Reader('geoip/GeoLite2-ASN.mmdb')
CountryReader = geoip2.database.Reader('geoip/GeoLite2-Country.mmdb')
nw = []
donext = 0

for s in track(range(int(math.pow(256, 4))), refresh_per_second=1):
    if donext > s:
        continue
    nip = ipaddress.ip_address(s)
    try:
        w = ASNReader.asn(nip).network
        donext = s + int(w.hostmask)
        if CountryReader.country(nip).country.iso_code != "CN":
            nw.append(w)
    except:
        pass


for s in track(range(len(nw))):
    nw[s] = str(nw[s])


fo = open("ip.txt", "w")
fo.write('\n'.join(nw))
fo.close()
