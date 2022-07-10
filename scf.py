import requests
import hashlib
import base64
import re


def main():
    numbers = {
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAdCAIAAAAl5NuSAAACy0lEQVQ4EZ1UTWgTQRSeJNtsNyXbxmZF3BWkgpocRC9NDyYn8RD04A9YKKRUiCAV8VAPimg9VEE8KaV6Cg1YgxRyEAoePGgvaS+tCLYg7Sk5yBooW9Nk003i7My83c2mFnVZeN977/vem3m7M54jR4+j/324DqHcGrtVHTn3SxF13kx6kc6rmz3zs8KzvIvsaessD9dy98sK33SxiOtXP/ePprk1O+e1oZzaWXisOpS8ruPXB4y6lPiRyxoy+Oai2CMbLyfKInMCK2/l5ImDJ0/h9/DwVLio00RTjG09T4HEEo893TpDtoiQUJjqvzzptZa3lBXij8Iqk1SHRmsxhmlnuX41VqURfbVvImvVBpAXZpYE5iiVm5coJGI5rUdZJlDIcSWQOG0m1wPNd6JJOlEivn66wnia8Mn9PaDCgn9DY1ga2CVjM8WNqLzLwiUuA+QO6/tW6mJBsXHeREQswZRVtfOnsYtsaJAVDbJNLE42QIu0n2QbNr8NzZX84NeVYQwxOdxi3wgJqvV9gPVHa9bZr1OHcI2DkdEUFkcMa9kd9P0D/9TZXQqL3YtxU2xfsUdLgm2ddSliM/dAwRYEfdo6hli87oUxNHmYO5Da7IWwAb5PW6biZUuMRDsNNIeNiiDWuBUzbi67q1hkFFE24LixiMM0ozI71vqmf85MmGJPoWQdt9rIoIPvhIP1YxL1uza+0P+UDCyTD8Bx2x5K73mBoSvpikK1evD9E4qIGOWFQpEiJCW0F3FnR4LjtTuJHYK86pLwiuWZxHN7NgQz3744vfU61bIuuliqujhdZm210Mwk0+D92lfvWLb8MEbLk8r46jStwfMN1knvnR8X7y4yDyFfb18/c1bxziOtswN1dmq5Bme+8GNooTcPgvc+WkoMHGLsfV3ozm/2KIeQFGryHJ2cX1ODKx8O3LjW/e67U4mxY9muzF+4vwHPdM7J2FS8qwAAAABJRU5ErkJggg==': '0',
        'iVBORw0KGgoAAAANSUhEUgAAABUAAAAcCAIAAAABemMJAAAAyElEQVQ4EWOUVVBjoAAw4dWr8Xfm3lf3b75ZHodLGQsuCYaovs/l3h/4QPKcOBUxYOqX/p+Y8y3J+6MM+1/c2uAySPrNA38nRXyxMPjGx/APLk+IAdcf921W9VuwayFamF8/4eST+cJOwACs4fdJYHO9lNlC9p8ENAOl4faDlDL/fM13cD1XUy/TUyAPZ5iDlMIAXP9eztwbXIdOwcSJpeH6nzIeAllKKsDqfxIMGdVPQmBhUToaflgChQSh0fAjIbCwKB3o8AMADiotC5QUM1oAAAAASUVORK5CYII=': '1',
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAdCAIAAAAl5NuSAAACO0lEQVQ4EWOUVVBjIBewoGqU/p+Y8z3a9puM6E92hn9gObafn9iuXeBe08u27AaqYgZGhM12Vd9aI97LsEP0oKkDcjnubhWOL2J6ipCBaU6c+q7c5Ss7QoL9508g5z87+y+EGAPTp5PiXnEsMP1MUCktJYhO5k/3RKZXyCqqi2noAZG4opNM01aBT1BV//jM308uhpsG0wwS+MS/uV5K35Ozaz1cmoHhKeP8Il6vVmGY/h+GLj+lofIwzT+fCDcF8OWtQNKGxHy6iGv6BQ6ogNKvJDTNNalc82FeQdKFYM64CNPM8EfGDCIOsxmhChfrCTPM5X/5lEjVrPmHD2ou2xOo74i2OUMJFHUg8InlGoTBQKRm6V++mj+gWp6yzCdJc8vU91rQBMR5Yh0bVC8xNicuehOtCU1nP6/zlSyC6WVAyxhwcQhD+l/L1LfRcAd/Eu7MZkOKUNyapb1+T656bSj6F2rga+GmcLS0gEOzT8OX1sj3sLhhAqW/OI5lSJaCTcTUjOZULDkR7jc0zba/17UjO1VoXht38za4ajQGsmbbX1v7XmvxQQoD5tcXREvCWQ+hqUfhwjVL/1mO0Ml1fqFQUBsjikosHJjmxPYPFlA7OU+0CkciIhOLJpgQJHma/Ugy/w4WYn2ylUidQOVgzebx32Ugpv3k3VxE0LUwiyGa3aRhOeY180G4FGEG2M+ivL+hKmVer7hJWBMDA/8adb5SsM1/RWFJiRh9SGogAYYkQAoTVuiTogeuFgCpiqrSY0PgFgAAAABJRU5ErkJggg==': '2',
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAdCAIAAAAl5NuSAAACpElEQVQ4EWOUVVBjIBewoGiUNvtbkPPNXvM7H99PdojMT/ZPr7lPbONs6mV6iqIWyGGE2/y/dtGHaPMvUD3o6ph+PhGckM014wayBDO/gDCY3/55oetnmDvYfv5k+fuX5S/LfxaG/2Dp/yx83228WT9tY73wGa6fCc4CMz4J7Jol7aUurqEnBkLq0hGtonc/MUMV8b0t7/uDpAGhmfH1SUkvU970XqbrSPInF3G4BIid/wkVYjf4XouQhTv7Bvu2RUz3EBJIrM9MX43+esn/Bgsx/vzEtfYiRBZu81MGjMBE6N9ygx1mN0KQgQGuGVkQk/2akXzN0ga/+KAmsj1ZBDebKJv/1+l/heq4zjEBrpcYZ2cseusm8w+shWdXLxtS0MCSBcI4GMvc+a+990832w/KfH/BYlwnegTTD8OkQTSq5u7tj0OUkKUhbJZP9wQ7CzmWoaRNoBRhPzP9fM355DUjOyzEkMxG1fzzJzsSgqTKf+yin7XMX9UtfnZx+88oaSS9SLkKWRTGlv4fHPEjKfCzligsml8LN4VzzYcGGiJLwjRgoxNnvyu3+wrOrUyvD0mapUIcjOpsbBpBYvNTBQ8+gSj9J2r+vQyqjjjNwEKj6SI3VAv7d8MICJNYzQxPfyIpZSNRszQ7JJEBtTH9fIOsWZoBJQogUijk/3J48v7JfmIbsuacz+tX/vbBbYBP32dY8mb4dIFjBtRcqEf+ixq8mLz9/br2P3YaKDZqBv6euf3NZO+PsJJYaGklrEhDSdvsXwyDviwMYmL4yQpNE+y/2RngXmVg+Mm/Jpu7C5GtIDafYkcUkUDV7D/ZIQihk/nTPdHqML5SlFyFlMKCi3+EuHzTkv7Nx/4L5nT2n59Y717nWjOFff4pmBiCRtKMECSWBQDfGNuYxLjW9gAAAABJRU5ErkJggg==': '3',
        'iVBORw0KGgoAAAANSUhEUgAAABUAAAAbCAIAAAAcf1OxAAABhElEQVQ4EWOUVVBjIAhqN7xM0vwFVsZ5olUkchFcBxOchZsR+M0XqhlTDWH9/7vTPoliaoSKENIvXfzNV+k3Tu0MBPT/7Yn4wI5bNwN+/XZTP1nw/QNq//ma+xN2U/DYb/uz1eULWBfPwW0c2LXjtv9/d9UHGZAmpteH+NOf4NCOS795+2dfJXCEfxKc3oDHkVilzH61en8EBxvH+RVc85/ishzkOky5/92N75XBun9e58/txVSALIKh3w7u8p/8m9vY8NkNMgdNv+2P1iCIy9nubuUtPYVsFVY2sn7pP8v73oLDnOHndcH4SkasOlAFkfQntn+ApBaGT8Kd2QRdDjEHpt+u/VO5+XewGOeJyfjDHNkFYP3Scd8mQ73N+mSrMFL2RlaKlQ3Ub/tzYclbPrDsz3uC1UXEeBthlmzjCc7//xnIQpzHW2D+RxhIGouF4edP5p8/8eZxkIl/2dn/gE1mYvjJ+hNqB/PPX4xElZ8Mcd8uVkPCiIzyE2obVopS/w91/QDSPZdPKmG8AQAAAABJRU5ErkJggg==': '4',
        'iVBORw0KGgoAAAANSUhEUgAAABUAAAAcCAIAAAABemMJAAAB+ElEQVQ4EWOUVVBjoACwIOv9uefmK2VkAWzsTyel9OOYYTJMMAaQ9vrHh8QjjomsX+Q/O3GakFShuB8m/km4yZRrPoyHl0a2X/MPZe6HW/SJeRecTYCBZH+U9C+o4l8MTwlog0sj6UcE3k9GuDwhBpJ+UfZ/ENWfPsGjl5B2BmT9fD8JKsdQgKQfLvfpDfH2I+L/r4wI1AQZ76f3vaF+YWBg//mJ9e51rjVT2OefglsBZ2Czn4EBrhmo7ic73xct81d1i59d3P4zShquE8JA6P/LB009LD9/soMQmkqGv3xKr1o3fEtEMYKRQP61S/2VFPTJXuk73LSf98TjPdlOQvnM/ALCcCksjIfnmDcs5dr1k9XN+Ds3OLBYBP+LPuXacAOiGOF+LJrhQtdnc+Vu5YdxvxkG/oWxidMPVH2ykus8LEj4RP+QrJ+BgeXJa5guBE20/QwMWEsXEvT/lpGB2vsTkUGI1m/X900Lqh2YHOHJljj90nHfe1w+w2zn3dwAZTIg8p/Gfx9buCiCIW32t3vl+73Vb0ShxQPbtRXcMxDy8PTX/ul+0EeQOErK/cPODo9qoBzb3a2i8UVMSKUT3CNwI9l/IgoiuCDIXJ6DkwUTZiMLAdlw/ac4Tmj+1VL6zc6AbCfzz59sn55yndjDMb2X6TqaXhAXAA8XiW6ahRdHAAAAAElFTkSuQmCC': '5',
        'iVBORw0KGgoAAAANSUhEUgAAABUAAAAdCAIAAADKJrCsAAADAklEQVQ4EaWVX0hTURzHz7brzt30bqLcfNgN0kFtPZR7mgQqhASlPkx6MB98iBZICWL0IESISKZoSCBRSeKg7CHsQfNB7KF82faQ9aK9GBR3D3XFP9fadrY2u3fn/nZv2wyhy4V7fr/f9/M7v3POb2em4ydOov94mH+xXYPxy42J0zzBOJPTWYlsXY9yz+4xizEKmkrP7w3Gn/TuCDhbOv2XmtqL1lyo1PxdU7t3W/axjjKEWFQLpzGiGQ8gWMQ3jcg6TCrC887Jp+aIVi3yBtJ91/cuAI1QQf2BRPT+Fp8LE5Ef6mZfAKkjCHk9aOMzdZiN/oPHN7cpjOTq0UNgBQBYGRr5YLxZoMtj117aZ0rNbJwtNzbww62wZyI3OlGkLO3I866Uz5umKTejbKS0utib5zvTbi1q33xdrDvMA+fX5iHagcs4HFXVbbcSPYFfbj6R85sRYcUN+8KsbWzJmAt4H5/S3LJl2ZV9OL3VXkcMwizCcaE+3lOP2wNVnUEGNhfq5zm6eIRSB33TEsBWQrDyGhIRoen7Uui3S3NpfIZ3gMa1316XQqQ8POe6dKrGc+aY8taeF4beOGVNknX4d8e7qQHzA600eRIT56sbVVcGzRt5b8w00+/onXfCkhINHalcCcU8Mosr3O3VPKoP3g9wyyIA3mSfGgFTVyEuPGEymMahafRTOdgpQV2CxlskWBySmXXYXJDq39hHKwgJ79V5JO2X6aojjegvBepfjsEhOTLCkXibpG4v8JEIhsKSvuChCfx+AgdtkdUrAHgUYtckiiV9rfRsirNke87+1LwSu6C2eZ5H5kdRTot5d2ZH8jecnqVtaq9Zu17KNlfZRTWi8yjSz4VlaqfcHVsrDzJ+6FLkyQ6HtsdbYHKxcmiAnnHB/ddIVqZ+uGErEVL6X9VhDI2nGHLl837ujtZgFmdltVqH9nxj3n61NZxL8pjWn2EY9YWwmYhVE9cqxj6Ao/D+BX/XSPxqY1xQ/nnohU9sUsz+bs42GTL93VwF9QN/5O8fGRn4ilT2qk0AAAAASUVORK5CYII=': '6',
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAIAAACjcKk8AAABuklEQVQ4EWOUVVBjIBcwkasRpI8FrDnu28Xqt3ykmcO/Rp0im8nWfI99DQMjKQEW+P1UxxtRkO+4D1YIJawnweb/3WkfwToZfl7gq14PNIJozdLF33yVfoPDlH9zL8tTEItYzf/rvD6wg7W+PsRTegrMIlKzdNUXe5l/YB0CuxrgFsIZELOwk/9aEdZy14BdDFZIhGbphq/2kIBiQLYWqJ2w5n+tLh8gDnp9CNlaIjRLV321gFrLe2I2mlVoXIgVCPJ/ufMnSCD/vMCTBw1kuDR+zXHfYYHMdWIFJA/BdQIZeDW3BH2CZrUn3NNBSQoN4NFs9sNeE5KkWK8d5jiJphHExa3ZPOKHDFQD9/nZWLTi0fwv0+wzRMfPC5xICQPZFFw2B/7QgsYQ+7VTmEEFMQKH5sTAb1C9P7lP9CLbhszGrvmvm+Z3iKqf19m7kNWjsLFq9vqlDI0i1rsXcbkZaAw2zebeP6BuZuC4uxDFLlQONs0hSt+gil6z70JkQFSNIB4WzX+UpSH5nuHnU9YtmFoQIpiavX7LQLICA8PrN8wIlVhYmJoN/sA8zP76HiMWLQghkspthDYICwBClnHZDNYAMQAAAABJRU5ErkJggg==': '7',
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAdCAIAAAAl5NuSAAADUElEQVQ4EZ1UX0hTURi/u7vbmV29ztwiuwvSQOYegj2kIqXlg5DkgxQlaInCVIiepKQgMss9ZEFQUlkPIZgz+gfiopDA5cMUApMYvejTBuVVi93m3dH96d57zrl3ExVpG7vf953f7/u+c7/fOYaDh0qp//0wWxBPd0vt9WsuOwQgqSxDEBXYoD+n7z4dyYIbsis7Ey8GV2scMAuDHRqGC0Z699z+oi0a862FxOETo69+HbMniM9AaEomGeWrhNIMJ7lPmKJ+05yIIDRBUtSNwZVKLqX6ZiFQ1FRb5DyyT/nVOvom83Az3ErP4DqPSVrleulei8gqUTo8ub+qyxjB6SlKNMz5LfO8ob4Myi0wdto+a/mg7F6rfHzDjvJB6/glAzIz/wPXcoMCCsRcjcgg5DZ+HUMjzN1Mkm7TAu4FbU1eIOSQaMQwc7pCJ+xsEfLMDIgipCPeXL4Vh193laA4G8bTImRqOCcYRo5YdwtWb6anB57/dqHgIvvYjyyNTBk6e20L6kBAydLQdGzAky5TMdUe+HZ66WyJ+lJg/msvmMGpsxXGN8V911ccQHslGIUfMO+T19rp04LanNWI+J0JJZiaKkkduAZCBjv1wHpz2KCNn6IyK/Opp8PLdbqwaQqaIJUEQBOsLO/CvouWl/h8aHuWhT32kzBzFiYONNXyxYo8i4pleU5Y1VmkgEPoH1trw/okbbcNrjaXklfSVXDhGZ0lz49gfNFSczK2V9YnK7md7Pg7WsQiKY+3V0jqzswhH3dFP3T6tiN+0OqzouPBVfztUbSgtl3RKjkQDOZOeXXCJivizQnhwyVWeuSJqOQ6HseobYWN8jAL5CqxO+S3qJI5sLGpyC7cNCYLUYDRtmTbTrykw4aXYVQ+SGrlkUULjnGxBs/2bE/czaFVWogQcuSRJYQpcXeHNsbsLM7EaMcf0mFe0CdfGGjOojFclmpE0gdSTaPhMDTPf9OVeKZ7bah/2cUizdNCoPDcE5msyzN95/1yc1k8o5wZQvU+ApAUlBdpuGjrOAUCCo4oTE7z2ccKJfTR0jiBJhn50sX3LsppCQdsLefNX5GXURkHKGfq6mWpoTxm5zYAhfoEMGoKzeaOPDS9+UFgylNvOzO6S/sfNQgekSrMrRAAAAAASUVORK5CYII=': '8',
        'iVBORw0KGgoAAAANSUhEUgAAABQAAAAcCAIAAADuuAg3AAAC9klEQVQ4EZVUTUwTQRSeblvG1rYW6KKwJVZMEDgYPFB6kaMHwEQSDyZGkChejAlKRY1eROJBrDFBYjAEYhNCPGCIP3DQi3CBJoYQEspBenE5yJ9hwZah7dbZnZl1t9QE2snOe99837w3f89U6isHWb/KpmT7pe1A5a4L7qpDFiQdWog4B59aPi3ruSajWJC7+zYuVyb0lH82cnx7nn81rAHmI+5C5gipkXe/6o+TaBjkAMpDaYvyJxTLrq8uGZDso3PE55gSZHoG1gN8WvU5KcZ3XRFOnC6qwO1UaXCkYJUSE4Fb8VaBOFrabX8WgxtQBVH0WNMFa5SyaSc0x8cfrrsUj1udLPa34bAscnfDFlEC5B6+ma3EiuWw/eWMTZ1J5qt3WtVZVBekqsqSxEJR2xPDlhJY+Q69cojEc8XPNWOLRPaneBoXiDG6O4Rm+EasokSAhLc2w8QVsroYAzOXYxbXKMx78NayNWtUyFLQkJwGdGnisJmdBOCFVE62Cqa9HjbolBtZZKvI1LA63uNnDGMvdOyc0ZYHMzwTc68jTsbcPP8YNdJrwDDcn0VvW+hFYChb80zIMS1RB5at9I5t9Xek6yoUmuCXO/u25gZWTirbYaVKZMK54ofB2rWiHzsgk/l/2yz8MG2jhKUiXzmLrMw3BVvuH12QzHTurE7KH75jn9VAZMo+quXxvIaakuAbz2zssIQgUpsk5k+/L6mvcTyaAlU8fa2SEiPXdRoN2XDTYugM7ais4iIW69PWsXKb/qSXHhUUv2LKQcS1LQkvmVW0DUYOJk63+7dVLSfOwRnF2nfk1vDvAMkZuT+G8FYbxcLeW6VS8KfxhXSvluxz3tJn+zP64HWR2wdWImOJziamUHtchvsn1nobNsljQzF31wMSFg9rNQyAnomfF8uIEp+wasAkBDKB8ApRzBO8DnWlO9c5A4D2vGooThbcaLMYq6Kubn/57oS8tdgjQ8gKNYBIss1PFYRuu+4OcayKsFT0aWvYvo2/Mt8Dn3GoSZ0AAAAASUVORK5CYII=': '9'
    }
    sums = 0
    for page in range(1, 6):
        url = 'http://match.yuanrenxue.com/api/match/4?page=' + str(page)
        response = requests.get(url)
        response = response.json()
        j_key = hashlib.md5(
            base64.b64encode((response['key'] + response['value']).encode()).replace(b'=', b'')).hexdigest()
        tds = re.findall('(?<=<td>).+?(?=</td>)', response['info'])
        for td in tds:
            imgs = re.findall('(?<=<img).+?(?=>)', td)
            outnumber = ['', '', '', '', '']
            i = 0
            for img in imgs:
                number = re.findall('(?<=data:image/png;base64,).+?(?=")', img)[0]
                imgclass = re.findall('(?<=img_number ).+?(?=")', img)[0]
                imgstyle = int(int(re.findall('(?<=style="left:).+?(?=px")', img)[0]) / 11)
                if imgclass != j_key:
                    outnumber[i + imgstyle] = numbers[number]
                    i += 1
            outnumber = int(''.join(list(filter(lambda n: n, outnumber))))
            sums += outnumber
    print(sums)
    # 总数：243701


if __name__ == '__main__':
    main()