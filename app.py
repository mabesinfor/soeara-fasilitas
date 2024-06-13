import streamlit as st
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('mode.chained_assignment', None)
import matplotlib.pyplot as plt
import base64
import requests

response = requests.get("https://optus-asia.com/wp-content/uploads/2024/01/dss.jpg")
image_data = base64.b64encode(response.content).decode('utf-8')

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_data}" style="height: 200px;width: 100%;object-fit: cover;">
    </div>
    """,
    unsafe_allow_html=True
)
st.title('Sistem Pendukung Keputusan - Metode Weighted Product')
st.write('Perhitungan Pendukung Keputusan dengan Metode WP untuk Mengurutkan Fasilitas Fakultas Terburuk di Perguruan Tinggi (Unsoed).')

def table_of_contents():
    st.sidebar.title('Daftar Isi')
    st.sidebar.write('[Identifikasi Masalah](#identifikasi-masalah)')
    st.sidebar.write('[Normalisasi Data Kualifikasi](#normalisasi-data-kualifikasi)')
    st.sidebar.write('[Pemberian Bobot Kriteria - BEM UNSOED 2024](#pemberian-bobot-kriteria-bem-unsoed-2024)')
    st.sidebar.write('1. [Menghitung Normalisasi Bobot](#menghitung-normalisasi-bobot)')
    st.sidebar.write('2. [Data Alternatif Hasil Survei](#data-alternatif-hasil-survei)')
    st.sidebar.write('3. [Perubahan Nilai Skala Kriteria](#perubahan-nilai-skala-kriteria)')
    st.sidebar.write('4. [Menghitung Vektor S](#menghitung-vektor-s)')
    st.sidebar.write('5. [Menghitung Vektor V](#menghitung-vektor-v)')
    st.sidebar.write('6. [Memberikan Peringkat Alternatif](#memberikan-peringkat-alternatif)')

table_of_contents()

def highlight_top_rank(row):
    if row['Ranking'] == 1:
        return ['background-color: #edbe3b'] * len(row)
    elif row['Ranking'] == 2:
        return ['background-color: #e8e8e6'] * len(row)
    elif row['Ranking'] == 3:
        return ['background-color: #ccb491'] * len(row)

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
nilai_sk = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
                         'C1': [4,2,1,1,4,4,1,1,1,4,2,4],
                         'C2': [4,4,4,4,4,4,4,4,4,4,4,4],
                         'C3': [4,1,1,1,1,3,1,3,3,3,3,3],
                         'C4': [3,3,4,3,2,2,3,4,4,2,2,3],
                         'C5': [4,4,4,4,4,4,3,4,4,4,4,4],
                         'C6': [3,3,3,4,3,2,1,3,2,4,3,3]}).set_index('Alternatif')
vektor_s = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'Jumlah'],
                        'Vektor S': [3.669259019,2.594557934,2.392462398,2.32461613,2.748217621,3.111789293,1.9382261,2.821066404,2.708969922,3.335133185,2.821066404,3.514289702,33.97965411]}).set_index('Alternatif')
chart_vektor_s = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
                        'Vektor S': [3.669259019,2.594557934,2.392462398,2.32461613,2.748217621,3.111789293,1.9382261,2.821066404,2.708969922,3.335133185,2.821066404,3.514289702]})
vektor_v = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'Jumlah'],
                        'Vektor V': [0.1079840014,0.07635621968,0.07040867426,0.06841200099,0.0808783283,0.09157801556,0.05704078369,0.08302222249,0.07972329303,0.09815088683,0.08302222249,0.1034233512,1,]}).set_index('Alternatif')
chart_vektor_v = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
                        'Vektor V': [0.1079840014,0.07635621968,0.07040867426,0.06841200099,0.0808783283,0.09157801556,0.05704078369,0.08302222249,0.07972329303,0.09815088683,0.08302222249,0.1034233512]})
rank = pd.DataFrame({'Alternatif': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
                     'Vektor V': [0.1079840014,0.07635621968,0.07040867426,0.06841200099,0.0808783283,0.09157801556,0.05704078369,0.08302222249,0.07972329303,0.09815088683,0.08302222249,0.1034233512],
                     'Ranking': [1,9,10,11,7,4,12,6,8,3,5,2]}).set_index('Alternatif')
rank = rank.style.apply(highlight_top_rank, axis=1)
                            
st.subheader('Identifikasi Masalah')
st.write('Tabel Alternatif :')
st.write(alt)
st.divider()
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
st.divider()
st.subheader('Pemberian Bobot Kriteria - BEM UNSOED 2024')
st.write('Tabel Bobot Kriteria :')
st.write(kriteria)
st.divider()
st.subheader('1. Menghitung Normalisasi Bobot')
st.write('Rumus Normalisasi Bobot :')
st.latex(r'W_{j} = \frac{W_{j}}{\sum{W_{j}}}')
st.write('Hasil Normalisasi Bobot :')
st.write(bobot)
st.divider()
st.subheader('2. Data Alternatif Hasil Survei')
st.write('Tabel Jawaban Responden :')
st.write(responden)
st.divider()
st.subheader('3. Perubahan Nilai Skala Kriteria')
st.write('Tabel Nilai Skala Kriteria :')
st.write(nilai_sk)
st.divider()
st.subheader('4. Menghitung Vektor S')
st.write('Rumus Vektor S :')
st.latex(r'S_{i} = \prod_{j=1}^{n} (x_{ij})^{w_{j}}')
st.write('Contoh Hitung Vektor S dengan A1 :')
st.latex(r'S_{A1} = (4)^{0.20} \times (4)^{0.20} \times (4)^{0.15} \times (3)^{0.20} \times (4)^{0.15} \times (3)^{0.10} = 3.669259019')
st.write('Tabel Hasil Perhitungan Vektor S :')
st.write(vektor_s)
chart_vektor_s = chart_vektor_s.set_index('Alternatif')
fig_s, ax_s = plt.subplots(figsize=(10, 6))
chart_vektor_s.plot(kind='bar', ax=ax_s, color='skyblue')
ax_s.set_title('Vektor S')
ax_s.set_ylabel('Nilai Vektor S')
ax_s.set_xlabel('Alternatif')
plt.tight_layout()
st.pyplot(fig_s)
st.divider()
st.subheader('5. Menghitung Vektor V')
st.write('Rumus Vektor V :')
st.latex(r'V_{i} = \frac{S_{i}}{\prod_{j=1}^{n} (x_{ij})^{w_{j}}}')
st.write('Contoh Hitung Vektor V dengan A1 :')
st.latex(r'V_{A1} = \frac{3.669259019}{33.97965411} = 0.1079840014')
st.write('Tabel Hasil Perhitungan Vektor V :')
st.write(vektor_v)
chart_vektor_v = chart_vektor_v.set_index('Alternatif')
fig_v, ax_v = plt.subplots(figsize=(10, 6))
chart_vektor_v.plot(kind='bar', ax=ax_v, color='lightgreen')
ax_v.set_title('Vektor V')
ax_v.set_ylabel('Nilai Vektor V')
ax_v.set_xlabel('Alternatif')
plt.tight_layout()
st.pyplot(fig_v)
st.divider()
st.subheader('6. Memberikan Peringkat Alternatif')
st.write('Tabel Ranking Alternatif :')
st.write(rank)
st.divider()
st.metric(label="🥇 A1", value="Fakultas Biologi", delta="10.8%", delta_color="normal")
st.metric(label="🥈 A12", value="Fakultas Teknik", delta="10.3%", delta_color="off")
st.metric(label="🥉 A10", value="Fakultas Pertanian", delta="9.8%", delta_color="inverse")
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