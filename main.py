import bs4 as bs
import requests
import xlsxwriter
import argparse
import os

parser = argparse.ArgumentParser(description="Create SEO report template.")
parser.add_argument("url", action="store")
args = parser.parse_args()
url = args.url

page = requests.get(url)

soup = bs.BeautifulSoup(page.text, "html.parser")

tags = soup.find_all(["h1","h2","h3","p","title"])

meta_descs = soup.find_all("meta", attrs={"name": "description"})
meta_titles = soup.find_all("meta", attrs={"name": "title"})

j = 1
while os.path.exists(f"./report-{str(j).zfill(2)}.xlsx"):
  j += 1
filename = f"report-{str(j).zfill(2)}.xlsx"

workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()

bold = workbook.add_format({"bold": True})
text_wrap = workbook.add_format({"text_wrap": True})
worksheet.set_column(first_col=1, last_col=2, width=80, cell_format=text_wrap)


row = 0  
worksheet.write(row, 0, "url", bold)
worksheet.write(row, 1, url)
row += 2

worksheet.write(row, 0, "tag", bold)
worksheet.write(row, 1, "current", bold)
worksheet.write(row, 2, "revised", bold)
row += 1

for tag in meta_titles:
  worksheet.write(row, 0, "meta title")
  worksheet.write(row, 1, tag["content"].strip())
  row += 1

for tag in meta_descs:
  worksheet.write(row, 0, "meta desc")
  worksheet.write(row, 1, tag["content"].strip())
  row += 1


for tag in tags:
  worksheet.write(row, 0, tag.name)
  worksheet.write(row, 1, tag.text.strip())
  row += 1

workbook.close()

print(f"{filename} generated")