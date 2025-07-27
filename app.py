import streamlit as st
import json
import os

# Nama file untuk menyimpan catatan
DATA_FILE = 'notes.json'

def load_notes():
    """Memuat catatan dari file JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_notes(notes):
    """Menyimpan catatan ke file JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)

def display_section(title, items):
    """Fungsi pembantu untuk menampilkan bagian dengan bullet points."""
    st.subheader(title)
    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, dict):
        for key, value in items.items():
            if isinstance(value, list):
                st.markdown(f"- **{key}**:")
                for sub_item in value:
                    st.markdown(f"  - {sub_item}")
            else:
                st.markdown(f"- **{key}**: {value}")
    else:
        st.write(items) # Untuk kasus single line seperti "Planet: 8"

def display_notes_data():
    """Menampilkan data catatan yang sudah ada dalam format rapi."""
    st.title("🗒️ Catatan Happy Pet & Pengetahuan Umum")

    # Menggunakan kamus untuk menyimpan kategori dan itemnya
    # Ini akan membuat struktur data lebih mudah dikelola
    notes_data = {
        "Kategori Hewan": {
            "Karnivora": ["Pinguicula", "Aldrovandra", "Panda", "Capung", "Musang", "Drosera", "Kalajengking", "Tukan"],
            "Bukan Karnivora": ["Semut", "Kuda Nil", "Marmut"],
            "Herbivora": ["Iguana", "Kolibri", "Lembu Laut", "Kuda Nil", "Dugong", "Ngengat", "Gazel", "Badak"],
            "Omnivora": ["Gorila", "Bajing Tanah", "Beruang", "Billfish", "Burung Unta"],
            "Anonim (Tidak Dikategorikan)": ["Rafflesia"],
            "Reptil": ["Penyu", "Iguana", "Komodo", "Kura-Kura", "Alligator", "Gavial", "Ular Laut"],
            "Mamalia": ["Lembu Laut (Herbivora)", "Narwhal", "Porpoise", "Armadillo", "Panda", "Kerbau"],
            "Yang Tidak Bisa Terbang": ["Kasuari", "Takahe", "Kiwi", "Rhea"],
            "Bernapas Menggunakan Kulit": ["Cacing Tanah", "Tembakul", "Kodok"],
            "Serangga": ["Ulat", "Kumbang", "Belalang", "Kutu", "Jangkrik"],
            "Yang Bisa Melompat (Daftar ini sepertinya salah, perlu dikoreksi)": ["Siput", "Kura-kura"],
        },
        "Shio Cina": {
            "Daftar Shio": ["Tikus", "Kerbau", "Harimau", "Kelinci", "Naga", "Ular", "Kuda", "Kambing/Domba", "Monyet", "Ayam Jago", "Anjing", "Babi"],
            "Kelompok Elemen": {
                "Kayu": ["Harimau", "Kelinci"],
                "Air": ["Tikus", "Babi"],
                "Api": ["Ular", "Kuda"],
                "Logam": ["Monyet", "Ayam Jago"],
                "Tanah": ["Kerbau", "Naga", "Kambing/Domba", "Anjing"],
            },
            "Kelompok Kompatibilitas": {
                "Grup 1": ["Tikus", "Naga", "Monyet"],
                "Grup 2": ["Kerbau", "Ular", "Ayam Jago"],
                "Grup 3": ["Harimau", "Kuda", "Anjing"],
                "Grup 4": ["Kelinci", "Kambing/Domba", "Babi"],
            }
        },
        "Lokasi Geografis & Kehidupan": {
            "Yang Ditemukan di Kutub Selatan": ["Anjing Laut Antartika", "Penguin", "Cormorant Antartika"],
            "Yang Ditemukan di Kutub Utara": ["Anjing Laut"],
            "Yang Tidak Ditemukan di Kutub Selatan": ["(Tidak ada item spesifik yang diberikan)"],
        },
        "Fitur Fisik & Karakteristik": {
            "Yang Tidak Melompat": ["Gajah"],
            "Organ Terbesar Manusia": "Kulit",
            "Jumlah Gigi Saat Dewasa": 32,
            "Grup Otot Terlebar dalam Tubuh Manusia": "Bukan Rhomboid",
            "Kuku Terbentuk dari Zat": "Keratin",
            "Zat Pembentuk Kulit dan Rambut": "(Tidak ada item spesifik yang diberikan)",
            "Terumbu Karang Terbesar Sedunia di Laut Coral": "Terumbu Penghalang Besar",
            "Bertahan Paling Lama Tanpa Air": "Bukan Jerapah",
        },
        "Astronomi & Geografi": {
            "Planet Berputar Searah Jarum Jam": "Venus",
            "Jumlah Planet": 8,
            "Suhu di Inti Bumi": "6000°C",
            "Benua Terkecil": "Australia",
            "Benua Terbesar": "Asia",
            "Samudra Terbesar": "Samudra Pasifik",
            "Samudra Terkecil": "Samudra Arktik", # Diperbaiki menjadi Arktik
            "Persen Air Tawar di Bumi": "2.5%",
            "Yang Dapat Diakses (Air Tawar)": "0.007%",
        },
        "Warna & Ilmu Pengetahuan": {
            "Sinar Biru + Sinar Merah": "Magenta",
            "Sinar Merah + Sinar Hijau": "Bukan Krem",
            "Ametis": "Ungu",
            "Yang Bisa Membuat Mutiara Meleleh": ["Jus Lemon", "Cuka"],
            "Yang Tidak Bisa Membuat Mutiara Meleleh": "Bukan Cokelat Panas",
            "Gas ke-6 yang Paling Banyak di Atmosfer": "Bukan Helium",
            "Gas ke-62 yang Banyak Terdapat di Atmosfer": "Bukan Karbon Monoksida",
        },
        "Waktu & Kalender": {
            "1 Abad": "36500 hari",
            "Songkran": "13 April",
            "Musim Gugur (Belahan Bumi Utara)": "23 September - 21 Desember",
            "Musim Gugur (Belahan Bumi Selatan)": "21 Maret - 21 Juni",
            "Hari Pertama Musim Semi (Astronomis)": "20 Maret - 21 Juni",
        },
        "Zodiak & Elemen (Barat)": { # Diperjelas sebagai Zodiak Barat
            "Zodiak Elemen Air": ["Pisces", "Scorpio", "Cancer"],
            "Zodiak Elemen Tanah": ["Capri", "Virgo", "Taurus"],
            "Urutan Zodiak": ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagitarius"],
        },
        "Hari Kebangsaan": {
            "Jepang": "11 Februari",
            "Singapura": "9 Agustus",
            "Brazil": "7 September",
            "Vietnam": "2 September 1945",
            "Italia": "2 Juni",
            "Cina": "1 Oktober",
            "Amerika": "4 Juli",
            "Spanyol": "12 Oktober",
            "Jerman": "3 Oktober",
            "Thailand": "5 Desember",
            "Filipina": "12 Juni",
            "Malaysia": "31 Agustus",
        },
        "Musik": {
            "Senar Biola": 4,
            "Tangga Musik dalam Satu Oktaf": 8,
            "Alat Musik": {
                "Piano": "Perkusi",
                "Basun": "Tiup",
                "Celesta": "(Tidak ada deskripsi)",
                "Bandoneon": "Aerofon, ada yang mengatakan alat musik tiup, keyboard",
                "Pikolo": "Seruling Tiup",
                "Marimba": "Dipukul menggunakan stik seperti keyboard tapi dipukul",
                "Zurma": "Tiup",
                "Tamborin": "Pukul",
                "Okarina": "Tiup",
                "Obo": "Tiup",
                "Clavinet": "Bukan Tiup",
                "Akordeon": "Bukan Keyboard",
            },
        },
        "Lain-lain": {
            "Yang Tidak Bisa Ditemukan Saat Memancing": "Ranjang Laut",
            "Yang Tidak Bisa Ditemukan di Rumah Mojo": "Rak Buku",
            "Yang Mudah Rusak": ["Anggur", "Beras Merah"],
            "Yang Tidak Mudah Rusak": "Madu",
            "Yang Tidak Beracun": "Pari Torpedo",
            "Makanan yang Tidak Ampuh Membangunkan": ["Cookie", "Kue Lapis Stroberi", "Cuka Putih Suling"],
            "Makanan yang Ampuh Membangunkan": ["Apel Merah", "Pisang", "Cokelat Panas"],
            "Maksimum Kertas Dilipat": "(Tidak ada item spesifik yang diberikan)",
            "Batas Maks Kertas Dilipat": "(Tidak ada item spesifik yang diberikan)",
            "Pencipta David Tembaga, di Bargello": "Bukan Michelangelo, Bukan Donarte Levidi, Bukan Salvador Doli",
            "Pencipta The Scream": "Edward Munch",
            "Pencipta Pieta": "Michelangelo",
            "Pelukis The Persistence of Memory": "Salvador Doli",
            "Pencipta The Sistine Madonna": "(Tidak ada item spesifik yang diberikan)",
        },
        "Ikan Bulan Juni": {
            "Muncul di Bulan Juni": ["Ikan Nyamuk", "Neon Tetra", "Cupang Ekor Mahkota", "Ikan Ceri Barb", "Banded Leporinus", "Ikan Pari", "Hiu Paus", "Arwana Mata Belo", "Biru Polka", "Gararufa", "Bintik Hati"],
            "Tidak Muncul di Bulan Juni": ["Tuna Sirip Biru Atlantik", "Tuna Biru Selatan"],
        },
        "Ikan Siang & Malam": {
            "Ikan Siang": ["Ikan Mata Merah", "Banded Leporinus", "Ikan Buntal", "Ikan Biji Labu", "Ikan Mungil", "Tompel Pink"],
            "Ikan Malam": ["Denison Duri", "Cumi Colosal", "Pelangi Boesemani"],
        }
    }

    # Menampilkan setiap bagian
    for category, content in notes_data.items():
        st.header(f"✨ {category}")
        if isinstance(content, dict):
            for sub_category, items in content.items():
                display_section(f"**{sub_category}**", items)
        elif isinstance(content, list):
            for item in content:
                st.markdown(f"- {item}")
        else:
            st.write(content) # Untuk kategori yang langsung berupa string


def main():
    st.set_page_config(layout="wide")

    st.sidebar.title("Navigasi")
    page_selection = st.sidebar.radio("Pilih Halaman", ["Lihat Catatan Tersimpan", "Tambah Catatan Baru", "Catatan Default Happy Pet"])

    if page_selection == "Catatan Default Happy Pet":
        display_notes_data()

    elif page_selection == "Tambah Catatan Baru":
        st.title("➕ Tambah Catatan Baru")
        note_title = st.text_input("Judul Catatan")
        note_content = st.text_area("Isi Catatan Anda", height=200)

        if st.button("Simpan Catatan"):
            if note_title and note_content:
                notes = load_notes()
                if "user_notes" not in notes:
                    notes["user_notes"] = {}
                notes["user_notes"][note_title] = note_content
                save_notes(notes)
                st.success("Catatan berhasil disimpan!")
                st.write(f"**Judul:** {note_title}")
                st.write(f"**Isi:** {note_content}")
            else:
                st.warning("Judul dan isi catatan tidak boleh kosong.")

    elif page_selection == "Lihat Catatan Tersimpan":
        st.title("📚 Catatan Anda")
        notes = load_notes()

        if "user_notes" in notes and notes["user_notes"]:
            st.write("Berikut adalah catatan yang Anda simpan:")
            # Tampilan catatan dengan opsi hapus
            for title, content in notes["user_notes"].items():
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.subheader(title)
                    st.write(content)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True) # Jarak agar tombol tidak terlalu dekat
                    if st.button(f"Hapus '{title}'", key=f"delete_{title}"):
                        del notes["user_notes"][title]
                        save_notes(notes)
                        st.experimental_rerun() # Refresh halaman setelah menghapus

            # Bagian untuk mengedit catatan
            st.markdown("---")
            st.subheader("Edit Catatan (Pilih salah satu)")
            selected_note_to_edit = st.selectbox(
                "Pilih catatan untuk diedit:",
                [""] + list(notes["user_notes"].keys()),
                key="select_edit_note"
            )

            if selected_note_to_edit:
                # Inisialisasi session_state jika belum ada
                if 'edited_title' not in st.session_state or st.session_state.edited_title != selected_note_to_edit:
                    st.session_state.edited_title = selected_note_to_edit
                    st.session_state.edited_content = notes["user_notes"][selected_note_to_edit]

                new_title = st.text_input("Judul Baru:", value=st.session_state.edited_title, key="edit_title_input")
                new_content = st.text_area("Isi Baru:", value=st.session_state.edited_content, height=200, key="edit_content_area")

                if st.button("Update Catatan", key="update_note_button"):
                    if new_title and new_content:
                        # Hapus catatan lama jika judul berubah
                        if new_title != st.session_state.edited_title:
                            del notes["user_notes"][st.session_state.edited_title]
                        notes["user_notes"][new_title] = new_content
                        save_notes(notes)
                        st.success("Catatan berhasil diperbarui!")
                        # Clear session state for editing after update
                        if 'edited_title' in st.session_state:
                            del st.session_state.edited_title
                        if 'edited_content' in st.session_state:
                            del st.session_state.edited_content
                        st.experimental_rerun() # Refresh halaman setelah memperbarui
                    else:
                        st.warning("Judul dan isi catatan tidak boleh kosong.")
        else:
            st.info("Anda belum memiliki catatan yang disimpan.")

if __name__ == "__main__":
    main()