import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from typing import Optional
from enum import Enum
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import os,time
import socket


app = FastAPI()

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)

client = gspread.authorize(creds)

sheet = client.open('stock-product-uneeds').sheet1

data = sheet.get_all_records() 

raw_data = '{' + str(data) + '}'
id_produk = []
nama_produk = []
stok = []
harga_beli = []
harga_jual = []
barang = []




for i in data:
    # a.append(i)
    barang.append(i)
    id_produk.append(i['id_produk'])
    nama_produk.append(i['nama_produk'])
    stok.append(i['stok'])
    harga_beli.append(i['harga_beli'])
    harga_jual.append(i['harga_jual'])
    # print(i['nama_produk'])


@app.get('/')
def index():
    print(nama_produk)
    return {'message':"sukses","data":barang}


class Produk(BaseModel):
    nama_produk: Optional[str] = None
    stok: Optional[str] = None
    harga_beli: Optional[str] = None
    harga_jual : Optional[str] = None
    category : Optional[str] = None


@app.post('/insert/')
async def insert_produk(item : Produk):
    nama = item.nama_produk
    stok = item.stok
    harga_beli = item.harga_beli
    harga_jual = item.harga_jual
    category = item.category

    # print(values)
    # sheet.set_basic_filter('B1')
    list_data = sheet.col_values(1)

    if len(list_data) >= 1:
        id_produk = 'SK10'+str(len(list_data))+ category[0:3]

    length_list = str(len(list_data) + 1)

    # print()
    sheet.update('A%s:F%s' %(length_list,length_list), [[id_produk, nama,stok,harga_beli,harga_jual,category]])
    response_data = {'message' :'sukses','sku' : id_produk}
    return response_data
    

if __name__ == "__main__":
    uvicorn.run(app, host=IPAddr, port=8000)