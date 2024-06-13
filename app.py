import streamlit as st
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('mode.chained_assignment', None)
import numpy as np
import matplotlib.pyplot as plt

st.title('Sistem Pendukung Keputusan - Metode Weighted Product')
st.write('Perhitungan Pendukung Keputusan dengan Metode WP untuk Mengurutkan Fasilitas Fakultas Terburuk di Perguruan Tinggi (Unsoed).')

def table_of_contents():
    st.sidebar.title('Daftar Isi')
    st.sidebar.write('[Identifikasi Masalah](#identifikasi-masalah)')
    st.sidebar.write('[Normalisasi Data Kualifikasi](#normalisasi-data-kualifikasi)')
    st.sidebar.write('[Pemberian Bobot Kriteria - BEM UNSOED 2024](#pemberian-bobot-kriteria-bem-unsoed-2024)')
    st.sidebar.write('1. [Menghitung Normalisasi Bobot](#menghitung-normalisasi-bobot)')
    st.sidebar.write('2. [Data Alternatif Hasil Survei](#data-alternatif-hasil-survei)')

table_of_contents()

alt = pd.DataFrame({'Alternatif': ['Fakultas Biologi', 'Fakultas Ekonomi dan Bisnis', 'Fakultas Hukum', 'Fakultas Ilmu Budaya', 'Fakultas Ilmu Sosial Politik', 'Fakultas Ilmu-Ilmu Kesehatan', 'Fakultas Kedokteran', 'Fakultas Matematika dan Ilmu Pengetahuan Alam', 'Fakultas Perikanan dan Ilmu Kelautan', 'Fakultas Pertanian', 'Fakultas Peternakan', 'Fakultas Teknik'],
                    'Kode': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']}).set_index('Kode')
sc_gedung = pd.DataFrame({'Kualifikasi': ['Gedung mengalami kerusakan dan tidak ada perbaikan', 'Alih fungsi gedung yang tidak sesuai', 'Gedung kotor dan berlumut', 'Tidak ada keluhan'],
                          'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
sc_jalan = pd.DataFrame({'Kualifikasi': ['Jalanan rusak dan berlubang', 'Jalanan trotoar berlumut', 'Resapan air di jalanan yang kurang', 'Tidak ada keluhan'],
                         'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
sc_keamanan = pd.DataFrame({'Kualifikasi': ['Adanya pelecehan seksual', 'Kehilangan barang/motor/dompet/helm', 'Satpam kurang tegas', 'Sudah merasa aman'],
                            'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
sc_lahanparkir = pd.DataFrame({'Kualifikasi': ['Sangat Sempit', 'Sempit', 'Luas', 'Sangat Luas'],
                              'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
sc_toilet = pd.DataFrame({'Kualifikasi': ['Sangat Kotor', 'Kotor', 'Bersih', 'Sangat Bersih'],
                         'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
sc_perpus = pd.DataFrame({'Kualifikasi': ['Singkatnya jam operasional', 'Kurangnya buku dan sumber bacaan', 'Akses repositori perpus', 'Kurangnya ruang membaca'],
                          'Skala': [4, 3, 2, 1]}).set_index('Kualifikasi')
kriteria = pd.DataFrame({'Kriteria': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', ''],
                         'Keterangan': ['Keluhan Gedung', 'Keluhan Jalan', 'Keluhan Keamanan', 'Keluhan Lahan Parkir', 'Keluhan Toilet', 'Keluhan Perpustakaan', ''],
                         'Kategori': ['Benefit', 'Benefit', 'Benefit', 'Benefit', 'Benefit', 'Benefit', 'Jumlah'],
                         'Bobot': [4, 4, 3, 4, 3, 2, 20]}).set_index('Kriteria')
bobot = pd.DataFrame([{'Kriteria': 'Bobot Keluhan', 'C1': 0.20, 'C2': 0.20, 'C3': 0.15, 'C4': 0.20, 'C5': 0.15, 'C6': 0.10}]).set_index('Kriteria')
responden = pd.DataFrame({'Alternatif': ['Fakultas Biologi', 'Fakultas Ekonomi dan Bisnis', 'Fakultas Hukum', 'Fakultas Ilmu Budaya', 'Fakultas Ilmu Sosial Politik', 'Fakultas Ilmu-Ilmu Kesehatan', 'Fakultas Kedokteran', 'Fakultas Matematika dan Ilmu Pengetahuan Alam', 'Fakultas Perikanan dan Ilmu Kelautan', 'Fakultas Pertanian', 'Fakultas Peternakan', 'Fakultas Teknik'],
                          'Keluhan Gedung': ['Gedung mengalami kerusakan dan tidak ada perbaikan', 'Gedung kotor dan berlumut', 'Tidak ada keluhan', 'Tidak ada keluhan', 'Gedung mengalami kerusakan dan tidak ada perbaikan', 'Gedung mengalami kerusakan dan tidak ada perbaikan', 'Tidak ada keluhan', 'Tidak ada keluhan', 'Tidak ada keluhan', 'Gedung mengalami kerusakan dan tidak ada perbaikan', 'Gedung kotor dan berlumut', 'Gedung mengalami kerusakan dan tidak ada perbaikan'],
                          'Keluhan Jalan': ['Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang', 'Jalanan rusak dan berlubang'],
                          'Keluhan Keamanan': ['Adanya pelecehan seksual', 'Sudah merasa aman', 'Sudah merasa aman', 'Sudah merasa aman', 'Sudah merasa aman', 'Kehilangan barang/motor/dompet/helm', 'Sudah merasa aman', 'Kehilangan barang/motor/dompet/helm', 'Kehilangan barang/motor/dompet/helm', 'Kehilangan barang/motor/dompet/helm', 'Kehilangan barang/motor/dompet/helm', 'Kehilangan barang/motor/dompet/helm'],
                          'Keluhan Lahan Parkir': ['Sempit', 'Sempit', 'Sangat Sempit', 'Sempit', 'Luas', 'Luas', 'Sempit', 'Sangat Sempit', 'Sangat Sempit', 'Luas', 'Luas', 'Sempit'],
                          'Keluhan Toilet': ['Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor', 'Sangat kotor'],
                          'Keluhan Perpustakaan': ['Kurangnya buku dan sumber bacaan', 'Kurangnya buku dan sumber bacaan', 'Kurangnya buku dan sumber bacaan', 'Jam operasional perpustakaan', 'Kurangnya buku dan sumber bacaan','Akses repositori perpus', 'Kurangnya buku dan sumber bacaan', 'Kurangnya buku dan sumber bacaan', 'Akses repositori perpus', 'Jam operasional perpustakaan', 'Kurangnya buku dan sumber bacaan', 'Kurangnya buku dan sumber bacaan']}).set_index('Alternatif')



st.subheader('Identifikasi Masalah')
st.write('Tabel Alternatif :')
st.write(alt)

st.subheader('Normalisasi Data Kualifikasi')
st.write('Tabel Skala Kriteria Keluhan Gedung :')
st.write(sc_gedung)
st.write('Tabel Skala Kriteria Keluhan Jalan :')
st.write(sc_jalan)
st.write('Tabel Skala Kriteria Keluhan Keamanan :')
st.write(sc_keamanan)
st.write('Tabel Skala Kriteria Keluhan Lahan Parkir :')
st.write(sc_lahanparkir)
st.write('Tabel Skala Kriteria Keluhan Toilet :')
st.write(sc_toilet)
st.write('Tabel Skala Kriteria Keluhan Perpustakaan :')
st.write(sc_perpus)

st.subheader('Pemberian Bobot Kriteria - BEM UNSOED 2024')
st.write('Tabel Bobot Kriteria :')
st.write(kriteria)

st.subheader('1. Menghitung Normalisasi Bobot')
st.write('Rumus Normalisasi Bobot :')
st.latex(r'W_{j} = \frac{W_{j}}{\sum{W_{j}}}')
st.write('Hasil Normalisasi Bobot :')
st.write(bobot)

st.subheader('2. Data Alternatif Hasil Survei')
st.write('Tabel Jawaban Responden :')
st.write(responden)



# # Fungsi untuk menghitung Weighted Product
# def weighted_product(row, bobot):
#     S = 1
#     for i, nilai in enumerate(row[:-1]):
#         if isinstance(nilai, str):
#             continue
#         pangkat = bobot[i]
#         S *= float(nilai) ** pangkat
#     return S

# # Perhitungan Weighted Product
# S = df.apply(lambda row: weighted_product(row, df.iloc[0, -len(row):]), axis=1)
# df['Weighted Product'] = S

# # Normalisasi Weighted Product
# df['Normalisasi'] = df['Weighted Product'] / df['Weighted Product'].sum()

# # Tampilkan hasil perhitungan
# st.subheader('Hasil Perhitungan Weighted Product')
# st.write(df)

# # Plot Normalisasi Weighted Product
# fig, ax = plt.subplots()
# ax.bar(df['Alternatif'], df['Normalisasi'])
# ax.set_xlabel('Alternatif')
# ax.set_ylabel('Nilai Normalisasi')
# ax.set_title('Normalisasi Weighted Product')
# st.pyplot(fig)

# # Penjelasan metode Weighted Product
# # ... (bagian ini sama dengan sebelumnya)

# # Penjelasan metode Weighted Product
# st.subheader('Penjelasan Metode Weighted Product')
# st.write('Metode Weighted Product (WP) adalah salah satu metode dalam Sistem Pendukung Keputusan (SPK) yang digunakan untuk menyelesaikan masalah Multi-Attribute Decision Making (MADM). Metode ini menggunakan perkalian untuk menghubungkan rating atribut, di mana rating setiap atribut harus dipangkatkan terlebih dahulu dengan bobot atribut yang bersangkutan.')
# st.write('Langkah-langkah dalam metode Weighted Product adalah sebagai berikut:')
# st.write('1. Menentukan kriteria dan bobot untuk setiap kriteria.')
# st.write('2. Menghitung nilai Weighted Product (S) untuk setiap alternatif dengan rumus:')
# st.write('$$S = \\prod_{j=1}^{n} (x_{ij})^{w_j}$$')
# st.write('di mana $x_{ij}$ adalah nilai alternatif ke-i pada kriteria ke-j, dan $w_j$ adalah bobot dari kriteria ke-j.')
# st.write('3. Melakukan normalisasi nilai Weighted Product (S) dengan membagi setiap nilai S dengan jumlah total dari semua nilai S.')
# st.write('4. Memilih alternatif dengan nilai normalisasi tertinggi sebagai solusi terbaik.')