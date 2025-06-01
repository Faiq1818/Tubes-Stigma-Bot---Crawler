## i. Penjelasan algoritma greedy yang digunakan
Bot "Crawler" mengimplementasikan serangkaian strategi berbasis algoritma greedy untuk mencapai tujuannya dalam permainan. Algoritma greedy yang digunakan berfokus pada pengambilan keputusan yang optimal secara lokal pada setiap langkah dengan harapan mencapai hasil yang baik secara global. Implementasi spesifiknya meliputi:

1.  Pemilihan Target Berlian Berbasis Kepadatan: Bot menghitung "kepadatan" untuk setiap berlian yang dapat dijangkau. Kepadatan didefinisikan sebagai poin berlian dibagi dengan jarak (langkah yang dibutuhkan) untuk mencapainya. Bot akan secara greedy memilih berlian dengan kepadatan tertinggi sebagai target utamanya. Perhitungan ini juga mempertimbangkan rute melalui teleporter jika itu menawarkan kepadatan yang lebih baik.
2.  Prioritas Kembali ke Markas: Bot akan secara greedy memutuskan untuk kembali ke markas jika:
    1.  Jumlah berlian yang dibawa mencapai ambang batas tertentu (misalnya, 3 berlian).
    2.  Sisa waktu permainan menipis dan jarak ke markas (baik langsung maupun via teleporter) menjadi kritis.
3.  Pengejaran Bot Lawan (Opportunistik): Jika bot lawan yang membawa sejumlah berlian signifikan berada dalam jarak dekat, bot "Crawler" akan secara greedy mencoba mengejarnya. Untuk menghindari pengejaran yang sia-sia, terdapat mekanisme blacklist dan batas langkah pengejaran.
4.  Pengambilan Keputusan Lainnya:
    1.  Jika jumlah berlian di papan sedikit, bot dapat secara greedy menargetkan tombol berlian jika lebih dekat.
    2.  Jika dalam perjalanan kembali ke markas dan ada berlian yang sangat dekat, bot akan secara greedy mengambilnya terlebih dahulu jika kapasitas memungkinkan.

Secara keseluruhan, bot membuat keputusan langkah demi langkah dengan memilih opsi yang memberikan keuntungan paling langsung berdasarkan kondisi permainan saat ini.

## Library, Frameworks & Tools yang digunakan

- Python 3.13

<i>Pastikan version Python 3.13 di Komputer anda (Versi lain mungkin tidak berkerja)</i>

## ii. Requirement program dan instalasi

1. Copy repository ini
```
git clone https://github.com/Faiq1818/Tubes-Stigma-Bot---Crawler.git
```
2. Masuk ke root foldernya
3. Masukan bot di main.py
4. Jalankan botnya menggunakan sintaks yang sudah diberikan

## iii. Kontributor
| Nama | NIM | Github |
| -- | -- | -- | 
| Faiq Ghozy Erlangga  | 123140139 | [Faiq1818](https://github.com/Faiq1818)
| Rifka Priseilla Br Silitonga | 123140024 | [rifkasltg](https://github.com/rifkasltg)
| Prima Agusta Sembiring | 123140119 | [PrimaSembiring](https://github.com/PrimaSembiring)
