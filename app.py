import streamlit as st
import json
import os

# --- Konfigurasi Aplikasi (Lambang, Judul, Tema) ---
st.set_page_config(
    page_title="Catatan Happy Pet",
    page_icon="🐾", # Lambang baru
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com/search?q=streamlit+documentation',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# Ini adalah aplikasi catatan ceria untuk Happy Pet!"
    }
)

# Menentukan warna kustom untuk tema yang lebih ceria
PRIMARY_COLOR = "#FFD1DC" # Pink Pastel
BACKGROUND_COLOR = "#F0F2F6" # Abu-abu sangat terang
SECONDARY_BACKGROUND_COLOR = "#FFFFFF" # Putih
TEXT_COLOR = "#333333" # Abu-abu gelap untuk keterbacaan
FONT = "sans-serif"

# --- Definisi Warna Latar Belakang untuk Setiap Kategori ---
CATEGORY_COLORS = {
    "Kategori Hewan": "#FFE0F0",
    "Shio Cina": "#E0FFFF",
    "Lokasi Geografis & Kehidupan": "#E6F2FF",
    "Fitur Fisik & Karakteristik": "#FFF2E6",
    "Astronomi & Geografi": "#F0E6FF",
    "Warna & Ilmu Pengetahuan": "#E6FFEA",
    "Waktu & Kalender": "#FFE6E6",
    "Zodiak & Elemen": "#FFFFE0",
    "Hari Kebangsaan": "#F5E6FF",
    "Musik": "#E0FFE0",
    "Lain-lain": "#FDFDBD",
    "Ikan Bulan Juni": "#BFEFFF",
    "Ikan Siang & Malam": "#ADD8E6"
}

# --- CSS Kustom untuk Styling Aplikasi Secara Keseluruhan dan Kategori ---
st.markdown(f"""
    <style>
    /* Styling Global */
    .reportview-container {{
        background: {BACKGROUND_COLOR};
    }}
    .sidebar .sidebar-content {{
        background: {SECONDARY_BACKGROUND_COLOR};
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_COLOR};
    }}
    p, li, div, .stTextInput, .stTextArea {{
        color: {TEXT_COLOR};
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: {TEXT_COLOR};
        border-radius: 5px;
        border: 1px solid {PRIMARY_COLOR};
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_COLOR};
        color: {SECONDARY_BACKGROUND_COLOR};
        border: 1px solid {TEXT_COLOR};
    }}

    /* Mengatur ukuran font untuk subkategori */
    /* Menggunakan p atau span untuk subkategori agar tidak terlalu besar */
    .sub-category-title {{
        font-weight: bold;
        font-size: 1.2em; /* Sekitar 2 tingkat lebih besar dari teks biasa (1em) */
        margin-bottom: 0; /* Hapus margin bawah default */
        padding-bottom: 0; /* Hapus padding bawah default */
    }}

    .sub-category-item {{
        margin-left: 20px; /* Indentasi untuk item */
        margin-top: 0; /* Hapus margin atas default */
        margin-bottom: 0; /* Hapus margin bawah default */
    }}

    /* Styling untuk Background Kategori */
    .category-card {{
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); /* Sedikit bayangan */
    }}
    /* Menghilangkan margin atas untuk bullet point pertama setelah judul sub-kategori */
    .stMarkdown ul:first-of-type {{
        margin-top: 0;
    }}
    /* Gaya untuk link navigasi kategori */
    .category-nav-link {{
        text-decoration: none;
        color: {TEXT_COLOR};
        padding: 5px 0;
        display: block;
        transition: color 0.2s;
    }}
    .category-nav-link:hover {{
        color: {PRIMARY_COLOR};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Nama File Data ---
USER_NOTES_FILE = 'user_notes.json'
DEFAULT_NOTES_FILE = 'default_notes.json'

# --- Fungsi Utility untuk JSON ---
def load_json_data(file_path):
    """Memuat data dari file JSON."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error(f"Error: Gagal membaca file JSON '{file_path}'. Pastikan formatnya benar.")
            return {}
    return {}

def save_json_data(data, file_path):
    """Menyimpan data ke file JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Fungsi untuk Menampilkan Catatan ---
def display_section_content(content_dict, level):
    """Fungsi pembantu untuk menampilkan konten dictionary secara rekursif."""
    for key, value in content_dict.items():
        # Menampilkan nama sub-kategori dengan titik dua dan bold
        # Menggunakan div dengan class kustom untuk kontrol font dan margin
        st.markdown(f"<p class='sub-category-title'>{key}:</p>", unsafe_allow_html=True)

        if isinstance(value, list):
            for item in value:
                # Menampilkan item dengan indentasi, tanpa bullet
                st.markdown(f"<p class='sub-category-item'>{item}</p>", unsafe_allow_html=True)
            st.markdown("") # Tambahkan baris kosong setelah daftar item
        elif isinstance(value, dict):
            # Rekursif untuk sub-sub-kategori
            # Tambahkan indentasi untuk sub-sub-kategori
            st.markdown(f"<div style='margin-left: 20px;'>", unsafe_allow_html=True)
            display_section_content(value, level + 1)
            st.markdown(f"</div>", unsafe_allow_html=True)
        else:
            # Untuk nilai string tunggal di bawah sub-kategori
            st.markdown(f"<p class='sub-category-item'>{value}</p>", unsafe_allow_html=True)
        st.markdown("") # Tambahkan baris kosong setelah setiap sub-kategori


def display_notes_data(notes_data_to_display, selected_category_to_show=None):
    """Menampilkan data catatan yang sudah ada dalam format rapi."""
    # st.title("📔 Catatan Happy Pet") # Judul ini akan diatur di main()

    # Tampilkan daftar kategori sebagai link navigasi
    st.subheader("Daftar Kategori:")
    col_idx = 0
    cols = st.columns(4) # Misalnya 4 kolom untuk daftar kategori
    
    # Simpan state untuk scroll
    if 'scroll_to_category' not in st.session_state:
        st.session_state.scroll_to_category = None

    # Buat tombol atau link untuk setiap kategori
    for category_name in notes_data_to_display.keys():
        with cols[col_idx]:
            if st.button(category_name, key=f"nav_btn_{category_name}"):
                st.session_state.selected_category_nav = category_name
                st.session_state.scroll_to_category = category_name # Set category to scroll to
                # st.rerun() # Tidak perlu rerun di sini karena main() akan dipanggil lagi dan state sudah diatur

        col_idx = (col_idx + 1) % 4
    
    st.markdown("---") # Garis pemisah

    # Tampilkan kategori yang dipilih jika ada
    if st.session_state.get('selected_category_nav'):
        target_category = st.session_state.selected_category_nav
        if target_category in notes_data_to_display:
            content = notes_data_to_display[target_category]
            bg_color = CATEGORY_COLORS.get(target_category, SECONDARY_BACKGROUND_COLOR)

            # Marker untuk scroll
            st.markdown(f"<a id='{target_category.replace(' ', '_')}'></a>", unsafe_allow_html=True)

            st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
            st.header(f"🌷 Kategori: {target_category}") # ICON DI SINI
            if isinstance(content, dict):
                display_section_content(content, level=1)
            elif isinstance(content, list):
                for item in content:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"- {content}")
            st.markdown(f"</div>", unsafe_allow_html=True)

            st.markdown("---") # Garis pemisah setelah kategori yang dipilih
            st.subheader("Kategori Lainnya:")
            
            # Tampilkan kategori lainnya di bawahnya
            for category, content in notes_data_to_display.items():
                if category != target_category:
                    bg_color = CATEGORY_COLORS.get(category, SECONDARY_BACKGROUND_COLOR)
                    st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
                    st.header(f"🌷 Kategori: {category}") # ICON DI SINI
                    st.markdown(f"<a id='{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                    if isinstance(content, dict):
                        display_section_content(content, level=1)
                    elif isinstance(content, list):
                        for item in content:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown(f"- {content}")
                    st.markdown(f"</div>", unsafe_allow_html=True)
    else:
        # Jika tidak ada kategori yang dipilih, tampilkan semua seperti biasa
        for category, content in notes_data_to_display.items():
            bg_color = CATEGORY_COLORS.get(category, SECONDARY_BACKGROUND_COLOR)

            # Marker untuk scroll, pastikan ID unik dan valid (tanpa spasi)
            st.markdown(f"<a id='{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)

            st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
            st.header(f"🌷 {category}") # ICON DI SINI

            if isinstance(content, dict):
                display_section_content(content, level=1)
            elif isinstance(content, list):
                for item in content:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"- {content}")
            st.markdown(f"</div>", unsafe_allow_html=True)

    # JavaScript untuk menggulir ke elemen dengan ID tertentu
    if st.session_state.scroll_to_category:
        category_id = st.session_state.scroll_to_category.replace(' ', '_')
        st.markdown(f"""
            <script>
                document.getElementById('{category_id}').scrollIntoView({{behavior: 'smooth'}});
            </script>
        """, unsafe_allow_html=True)
        st.session_state.scroll_to_category = None # Reset scroll state


# --- Fungsi untuk Mengelola Catatan Default ---
def edit_default_notes_page():
    st.title("⚙️ Edit Catatan Utama")
    st.warning("Halaman ini ditujukan untuk mengedit catatan utama. Perubahan di sini akan mempengaruhi semua pengguna.")

    # Menampilkan pesan konfirmasi yang disimpan di session_state
    if 'edit_default_message' in st.session_state and st.session_state.edit_default_message:
        if st.session_state.edit_default_message_type == 'success':
            st.success(st.session_state.edit_default_message)
        elif st.session_state.edit_default_message_type == 'warning':
            st.warning(st.session_state.edit_default_message)
        elif st.session_state.edit_default_message_type == 'info':
            st.info(st.session_state.edit_default_message)
        st.session_state.edit_default_message = "" # Reset pesan setelah ditampilkan
        st.session_state.edit_default_message_type = ""

    default_notes = load_json_data(DEFAULT_NOTES_FILE)

    if not default_notes:
        st.error("Tidak dapat memuat catatan utama untuk diedit. Pastikan file 'default_notes.json' ada dan formatnya benar.")
        return

    # --- Tambah Kategori Baru ---
    st.markdown("---")
    st.subheader("Tambah Kategori Baru")
    new_category_name = st.text_input("Nama Kategori Baru:", key="new_default_category_name")
    new_category_type = st.radio("Tipe Konten Kategori Baru:", ["Teks Tunggal", "Daftar Item", "Sub-Kategori (Nested Dictionary)"], key="new_default_category_type")

    new_category_content = None
    if new_category_type == "Daftar Item":
        new_category_content = st.text_area("Isi Daftar Item (satu item per baris):", height=100, key="new_default_category_list_content")
    elif new_category_type == "Teks Tunggal":
        new_category_content = st.text_input("Isi Teks Tunggal:", key="new_default_category_text_content")
    else: # Sub-Kategori (Nested Dictionary)
        st.info("Untuk menambah sub-kategori, masukkan nama kategori kosong dan kemudian edit di bagian 'Edit Konten yang Ada'.")
        new_category_content = {} # Inisialisasi sebagai dictionary kosong

    if st.button("Tambah Kategori Baru", key="add_new_default_category_button"):
        if new_category_name:
            if new_category_name in default_notes:
                st.session_state.edit_default_message = f"Kategori '{new_category_name}' sudah ada. Silakan pilih nama lain atau edit yang sudah ada."
                st.session_state.edit_default_message_type = 'warning'
            else:
                if new_category_type == "Daftar Item":
                    items = [item.strip() for item in (new_category_content or "").split('\n') if item.strip()]
                    default_notes[new_category_name] = items
                elif new_category_type == "Teks Tunggal":
                    default_notes[new_category_name] = (new_category_content or "").strip()
                else: # Sub-Kategori (Nested Dictionary)
                    default_notes[new_category_name] = {}

                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.session_state.edit_default_message = f"Kategori '{new_category_name}' berhasil ditambahkan!"
                st.session_state.edit_default_message_type = 'success'
            st.rerun()
        else:
            st.session_state.edit_default_message = "Nama kategori tidak boleh kosong."
            st.session_state.edit_default_message_type = 'warning'
            st.rerun() # Rerun juga untuk menampilkan warning

    # --- Edit Konten yang Ada ---
    st.markdown("---")
    st.subheader("Edit Konten yang Ada")
    categories = list(default_notes.keys())
    selected_category = st.selectbox("Pilih Kategori:", [""] + categories, key="edit_default_category_select")

    if selected_category:
        current_category_content = default_notes[selected_category]

        st.markdown(f"**Mengedit Kategori: {selected_category}**")

        if isinstance(current_category_content, dict):
            # Editor untuk sub-kategori
            st.subheader("Edit Sub-Kategori:")
            sub_categories = list(current_category_content.keys())
            selected_sub_category = st.selectbox(
                "Pilih Sub-Kategori untuk diedit:",
                [""] + sub_categories,
                key="edit_default_sub_category_select"
            )

            if selected_sub_category:
                current_sub_content = current_category_content[selected_sub_category]
                st.markdown(f"**Mengedit: {selected_category} > {selected_sub_category}**")

                if isinstance(current_sub_content, list):
                    edited_list_str = st.text_area(
                        "Edit daftar item (satu item per baris):",
                        value="\n".join(current_sub_content),
                        height=150,
                        key="edit_default_sub_list_area"
                    )
                    updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
                    if st.button("Simpan Perubahan Sub-Kategori", key="save_sub_category_list_btn"):
                        default_notes[selected_category][selected_sub_category] = updated_items
                        save_json_data(default_notes, DEFAULT_NOTES_FILE)
                        st.session_state.edit_default_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui!"
                        st.session_state.edit_default_message_type = 'success'
                        st.rerun()
                elif isinstance(current_sub_content, str):
                    edited_str_value = st.text_input(
                        "Edit nilai:",
                        value=current_sub_content,
                        key="edit_default_sub_string_input"
                    )
                    if st.button("Simpan Perubahan Sub-Kategori", key="save_sub_category_string_btn"):
                        default_notes[selected_category][selected_sub_category] = edited_str_value
                        save_json_data(default_notes, DEFAULT_NOTES_FILE)
                        st.session_state.edit_default_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui!"
                        st.session_state.edit_default_message_type = 'success'
                        st.rerun()
                elif isinstance(current_sub_content, dict):
                    st.info("Untuk mengedit lebih dalam (nested dictionary), Anda perlu memanipulasi JSON secara manual atau ini akan menjadi sangat kompleks.")
                    json_str = st.text_area("Edit JSON Sub-Kategori:", value=json.dumps(current_sub_content, indent=4, ensure_ascii=False), height=200, key="edit_nested_dict_area")
                    try:
                        updated_dict = json.loads(json_str)
                        if st.button("Simpan Perubahan JSON Sub-Kategori", key="save_nested_dict_btn"):
                            default_notes[selected_category][selected_sub_category] = updated_dict
                            save_json_data(default_notes, DEFAULT_NOTES_FILE)
                            st.session_state.edit_default_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui dari JSON!"
                            st.session_state.edit_default_message_type = 'success'
                            st.rerun()
                    except json.JSONDecodeError:
                        st.error("Format JSON tidak valid.")
                        st.rerun() # Rerun untuk menampilkan pesan error JSON

            st.markdown("---")
            st.subheader("Tambahkan Sub-Kategori Baru")
            new_sub_category_name = st.text_input("Nama Sub-Kategori Baru:", key="new_sub_category_name")
            new_sub_category_type = st.radio("Tipe Konten Sub-Kategori Baru:", ["Teks Tunggal", "Daftar Item"], key="new_sub_category_type")
            new_sub_category_content_input = st.text_area("Isi Sub-Kategori Baru (pisahkan dengan baris baru jika daftar):", height=100, key="new_sub_category_content_input")

            if st.button("Tambah Sub-Kategori Baru", key="add_new_sub_category_button"):
                if new_sub_category_name and selected_category:
                    if new_sub_category_name in default_notes[selected_category]:
                        st.session_state.edit_default_message = f"Sub-kategori '{new_sub_category_name}' sudah ada di '{selected_category}'. Silakan pilih nama lain atau edit yang sudah ada."
                        st.session_state.edit_default_message_type = 'warning'
                    else:
                        if new_sub_category_type == "Daftar Item":
                            items = [item.strip() for item in (new_sub_category_content_input or "").split('\n') if item.strip()]
                            default_notes[selected_category][new_sub_category_name] = items
                        else: # Teks Tunggal
                            default_notes[selected_category][new_sub_category_name] = (new_sub_category_content_input or "").strip()

                        save_json_data(default_notes, DEFAULT_NOTES_FILE)
                        st.session_state.edit_default_message = f"Sub-kategori '{new_sub_category_name}' berhasil ditambahkan ke '{selected_category}'!"
                        st.session_state.edit_default_message_type = 'success'
                    st.rerun()
                else:
                    st.session_state.edit_default_message = "Nama sub-kategori dan isi tidak boleh kosong."
                    st.session_state.edit_default_message_type = 'warning'
                    st.rerun() # Rerun untuk menampilkan warning

            st.markdown("---")
            st.subheader("Hapus Sub-Kategori")
            sub_category_to_delete = st.selectbox("Pilih Sub-Kategori yang akan dihapus:", [""] + sub_categories, key="delete_default_sub_category_select")
            if sub_category_to_delete and st.button(f"Hapus Sub-Kategori '{sub_category_to_delete}'", key="delete_default_sub_category_button"):
                confirm_sub = st.checkbox(f"Saya yakin ingin menghapus sub-kategori '{sub_category_to_delete}'", key="confirm_delete_default_sub_category")
                if confirm_sub:
                    del default_notes[selected_category][sub_category_to_delete]
                    save_json_data(default_notes, DEFAULT_NOTES_FILE)
                    st.session_state.edit_default_message = f"Sub-kategori '{sub_category_to_delete}' berhasil dihapus."
                    st.session_state.edit_default_message_type = 'success'
                    st.rerun()
                else:
                    st.session_state.edit_default_message = "Centang kotak konfirmasi untuk menghapus."
                    st.session_state.edit_default_message_type = 'info'
                    st.rerun() # Rerun untuk menampilkan info


        elif isinstance(current_category_content, list):
            edited_list_str = st.text_area(
                "Edit daftar item (satu item per baris):",
                value="\n".join(current_category_content),
                height=250,
                key="edit_default_category_list_area"
            )
            updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
            if st.button("Simpan Perubahan Kategori", key="save_category_list_btn"):
                default_notes[selected_category] = updated_items
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.session_state.edit_default_message = f"Kategori '{selected_category}' berhasil diperbarui!"
                st.session_state.edit_default_message_type = 'success'
                st.rerun()

        elif isinstance(current_category_content, str):
            edited_str_value = st.text_input(
                "Edit nilai:",
                value=current_category_content,
                key="edit_default_category_string_input"
            )
            if st.button("Simpan Perubahan Kategori", key="save_category_string_btn"):
                default_notes[selected_category] = edited_str_value
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.session_state.edit_default_message = f"Kategori '{selected_category}' berhasil diperbarui!"
                st.session_state.edit_default_message_type = 'success'
                st.rerun()
        else:
            st.info("Tipe data tidak didukung untuk pengeditan langsung di sini (bukan daftar, teks, atau kamus).")
            st.text_area("Konten JSON mentah (untuk debugging/pengeditan manual):", json.dumps(current_category_content, indent=4, ensure_ascii=False), height=200, disabled=True)


    # --- Hapus Kategori dari Catatan Default ---
    st.markdown("---")
    st.subheader("Hapus Kategori dari Catatan utama")
    category_to_delete = st.selectbox("Pilih Kategori yang akan dihapus:", [""] + categories, key="delete_default_main_category_select")
    if category_to_delete and st.button(f"Hapus Kategori '{category_to_delete}'", key="delete_default_main_category_button"):
        confirm = st.checkbox(f"Saya yakin ingin menghapus kategori '{category_to_delete}'", key="confirm_delete_default_main_category")
        if confirm:
            del default_notes[category_to_delete]
            save_json_data(default_notes, DEFAULT_NOTES_FILE)
            st.session_state.edit_default_message = f"Kategori '{category_to_delete}' berhasil dihapus."
            st.session_state.edit_default_message_type = 'success'
            st.rerun()
        else:
            st.session_state.edit_default_message = "Centang kotak konfirmasi untuk menghapus."
            st.session_state.edit_default_message_type = 'info'
            st.rerun()


# --- Fungsi untuk Mengelola Catatan Pengguna ---
def edit_user_notes_content(notes_data, selected_category):
    """Fungsi pembantu untuk mengedit konten catatan pengguna."""
    if selected_category and selected_category in notes_data["user_notes"]:
        current_content = notes_data["user_notes"][selected_category]

        st.markdown(f"**Mengedit Kategori: {selected_category}**")

        if isinstance(current_content, dict):
            # Editor untuk sub-kategori
            st.subheader("Edit Sub-Kategori Anda:")
            sub_categories = list(current_content.keys())
            selected_sub_category = st.selectbox(
                "Pilih Sub-Kategori untuk diedit:",
                [""] + sub_categories,
                key=f"edit_user_sub_category_select_{selected_category}"
            )

            if selected_sub_category:
                current_sub_content = current_content[selected_sub_category]
                st.markdown(f"**Mengedit: {selected_category} > {selected_sub_category}**")

                if isinstance(current_sub_content, list):
                    edited_list_str = st.text_area(
                        "Edit daftar item (satu item per baris):",
                        value="\n".join(current_sub_content),
                        height=150,
                        key=f"edit_user_sub_list_area_{selected_category}_{selected_sub_category}"
                    )
                    updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
                    if st.button("Simpan Perubahan Sub-Kategori Anda", key=f"save_user_sub_category_list_btn_{selected_category}_{selected_sub_category}"):
                        notes_data["user_notes"][selected_category][selected_sub_category] = updated_items
                        save_json_data(notes_data, USER_NOTES_FILE)
                        st.session_state.user_notes_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui!"
                        st.session_state.user_notes_message_type = 'success'
                        st.rerun()
                elif isinstance(current_sub_content, str):
                    edited_str_value = st.text_input(
                        "Edit nilai:",
                        value=current_sub_content,
                        key=f"edit_user_sub_string_input_{selected_category}_{selected_sub_category}"
                    )
                    if st.button("Simpan Perubahan Sub-Kategori Anda", key=f"save_user_sub_category_string_btn_{selected_category}_{selected_sub_category}"):
                        notes_data["user_notes"][selected_category][selected_sub_category] = edited_str_value
                        save_json_data(notes_data, USER_NOTES_FILE)
                        st.session_state.user_notes_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui!"
                        st.session_state.user_notes_message_type = 'success'
                        st.rerun()
                elif isinstance(current_sub_content, dict):
                    st.info("Untuk mengedit lebih dalam (nested dictionary), Anda perlu memanipulasi JSON secara manual atau ini akan menjadi sangat kompleks.")
                    json_str = st.text_area("Edit JSON Sub-Kategori:", value=json.dumps(current_sub_content, indent=4, ensure_ascii=False), height=200, key=f"edit_user_nested_dict_area_{selected_category}_{selected_sub_category}")
                    try:
                        updated_dict = json.loads(json_str)
                        if st.button("Simpan Perubahan JSON Sub-Kategori Anda", key=f"save_user_nested_dict_btn_{selected_category}_{selected_sub_category}"):
                            notes_data["user_notes"][selected_category][selected_sub_category] = updated_dict
                            save_json_data(notes_data, USER_NOTES_FILE)
                            st.session_state.user_notes_message = f"Sub-kategori '{selected_sub_category}' berhasil diperbarui dari JSON!"
                            st.session_state.user_notes_message_type = 'success'
                            st.rerun()
                    except json.JSONDecodeError:
                        st.error("Format JSON tidak valid.")
                        st.rerun()

            st.markdown("---")
            st.subheader("Tambahkan Sub-Kategori Baru Anda")
            new_sub_category_name = st.text_input("Nama Sub-Kategori Baru:", key=f"new_user_sub_category_name_{selected_category}")
            new_sub_category_type = st.radio("Tipe Konten Sub-Kategori Baru:", ["Teks Tunggal", "Daftar Item"], key=f"new_user_sub_category_type_{selected_category}")
            new_sub_category_content_input = st.text_area("Isi Sub-Kategori Baru (pisahkan dengan baris baru jika daftar):", height=100, key=f"new_user_sub_category_content_input_{selected_category}")

            if st.button("Tambah Sub-Kategori Baru Anda", key=f"add_new_user_sub_category_button_{selected_category}"):
                if new_sub_category_name and selected_category:
                    if new_sub_category_name in notes_data["user_notes"][selected_category]:
                        st.session_state.user_notes_message = f"Sub-kategori '{new_sub_category_name}' sudah ada di '{selected_category}'. Silakan pilih nama lain atau edit yang sudah ada."
                        st.session_state.user_notes_message_type = 'warning'
                    else:
                        if new_sub_category_type == "Daftar Item":
                            items = [item.strip() for item in (new_sub_category_content_input or "").split('\n') if item.strip()]
                            notes_data["user_notes"][selected_category][new_sub_category_name] = items
                        else: # Teks Tunggal
                            notes_data["user_notes"][selected_category][new_sub_category_name] = (new_sub_category_content_input or "").strip()

                        save_json_data(notes_data, USER_NOTES_FILE)
                        st.session_state.user_notes_message = f"Sub-kategori '{new_sub_category_name}' berhasil ditambahkan ke '{selected_category}'!"
                        st.session_state.user_notes_message_type = 'success'
                    st.rerun()
                else:
                    st.session_state.user_notes_message = "Nama sub-kategori dan isi tidak boleh kosong."
                    st.session_state.user_notes_message_type = 'warning'
                    st.rerun()

            st.markdown("---")
            st.subheader("Hapus Sub-Kategori Anda")
            sub_category_to_delete = st.selectbox("Pilih Sub-Kategori yang akan dihapus:", [""] + sub_categories, key=f"delete_user_sub_category_select_{selected_category}")
            if sub_category_to_delete and st.button(f"Hapus Sub-Kategori '{sub_category_to_delete}' Anda", key=f"delete_user_sub_category_button_{selected_category}"):
                confirm_sub = st.checkbox(f"Saya yakin ingin menghapus sub-kategori '{sub_category_to_delete}' Anda", key=f"confirm_delete_user_sub_category_{selected_category}")
                if confirm_sub:
                    del notes_data["user_notes"][selected_category][sub_category_to_delete]
                    save_json_data(notes_data, USER_NOTES_FILE)
                    st.session_state.user_notes_message = f"Sub-kategori '{sub_category_to_delete}' Anda berhasil dihapus."
                    st.session_state.user_notes_message_type = 'success'
                    st.rerun()
                else:
                    st.session_state.user_notes_message = "Centang kotak konfirmasi untuk menghapus."
                    st.session_state.user_notes_message_type = 'info'
                    st.rerun()


        elif isinstance(current_content, list):
            edited_list_str = st.text_area(
                "Edit daftar item (satu item per baris):",
                value="\n".join(current_content),
                height=250,
                key=f"edit_user_category_list_area_{selected_category}"
            )
            updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
            if st.button("Simpan Perubahan Kategori Anda", key=f"save_user_category_list_btn_{selected_category}"):
                notes_data["user_notes"][selected_category] = updated_items
                save_json_data(notes_data, USER_NOTES_FILE)
                st.session_state.user_notes_message = f"Kategori '{selected_category}' Anda berhasil diperbarui!"
                st.session_state.user_notes_message_type = 'success'
                st.rerun()

        elif isinstance(current_content, str):
            edited_str_value = st.text_input(
                "Edit nilai:",
                value=current_content,
                key=f"edit_user_category_string_input_{selected_category}"
            )
            if st.button("Simpan Perubahan Kategori Anda", key=f"save_user_category_string_btn_{selected_category}"):
                notes_data["user_notes"][selected_category] = edited_str_value
                save_json_data(notes_data, USER_NOTES_FILE)
                st.session_state.user_notes_message = f"Kategori '{selected_category}' Anda berhasil diperbarui!"
                st.session_state.user_notes_message_type = 'success'
                st.rerun()
        else:
            st.info("Tipe data tidak didukung untuk pengeditan langsung di sini (bukan daftar, teks, atau kamus).")
            st.text_area("Konten JSON mentah (untuk debugging/pengeditan manual):", json.dumps(current_content, indent=4, ensure_ascii=False), height=200, disabled=True)

    st.markdown("---")
    st.subheader("Hapus Kategori Anda")
    user_categories = list(notes_data["user_notes"].keys())
    category_to_delete = st.selectbox("Pilih Kategori Anda yang akan dihapus:", [""] + user_categories, key="delete_user_main_category_select")
    if category_to_delete and st.button(f"Hapus Kategori '{category_to_delete}' Anda", key="delete_user_main_category_button"):
        confirm = st.checkbox(f"Saya yakin ingin menghapus kategori '{category_to_delete}' Anda", key="confirm_delete_user_main_category")
        if confirm:
            del notes_data["user_notes"][category_to_delete]
            save_json_data(notes_data, USER_NOTES_FILE)
            st.session_state.user_notes_message = f"Kategori '{category_to_delete}' Anda berhasil dihapus."
            st.session_state.user_notes_message_type = 'success'
            st.rerun()
        else:
            st.session_state.user_notes_message = "Centang kotak konfirmasi untuk menghapus."
            st.session_state.user_notes_message_type = 'info'
            st.rerun()


# --- Fungsi Utama Aplikasi ---
def main():
    st.sidebar.title("Navigasi Utama")
    # PERUBAHAN UTAMA DI SINI UNTUK URUTAN DAN NAMA SESUAI PERMINTAAN
    page_selection = st.sidebar.radio(
        "Pilih Halaman",
        [
            "Catatan Default Happy Pet",
            "Edit Catatan Default",
            "Lihat Catatan Tersimpan",
            "Tambah Catatan Baru"
        ]
    )

    # Inisialisasi session state untuk kategori yang dipilih jika belum ada
    if 'selected_category_nav' not in st.session_state:
        st.session_state.selected_category_nav = None
    
    # Inisialisasi session state untuk pesan default edit jika belum ada
    if 'edit_default_message' not in st.session_state:
        st.session_state.edit_default_message = ""
        st.session_state.edit_default_message_type = ""
    
    # Inisialisasi session state untuk pesan user notes edit/add/delete
    if 'user_notes_message' not in st.session_state:
        st.session_state.user_notes_message = ""
        st.session_state.user_notes_message_type = ""


    # Logika pemilihan halaman
    if page_selection == "Catatan Default Happy Pet": # SESUAI DENGAN NAMA DI SIDEBAR
        st.title("📔 Catatan Default Happy Pet") # Judul Halaman Utama
        default_notes = load_json_data(DEFAULT_NOTES_FILE)
        if default_notes:
            display_notes_data(default_notes)
        else:
            st.info("Tidak ada catatan utama yang ditemukan atau ada kesalahan saat memuat.")

    elif page_selection == "Edit Catatan Default": # SESUAI DENGAN NAMA DI SIDEBAR
        edit_default_notes_page()

    elif page_selection == "Lihat Catatan Tersimpan": # SESUAI DENGAN NAMA DI SIDEBAR
        st.title("🍯 Catatan Anda") # IKON YANG DIMINTA
        notes = load_json_data(USER_NOTES_FILE)

        # Menampilkan pesan konfirmasi yang disimpan di session_state
        if 'user_notes_message' in st.session_state and st.session_state.user_notes_message:
            if st.session_state.user_notes_message_type == 'success':
                st.success(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'warning':
                st.warning(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'info':
                st.info(st.session_state.user_notes_message)
            st.session_state.user_notes_message = "" # Reset pesan setelah ditampilkan
            st.session_state.user_notes_message_type = ""

        if "user_notes" in notes and notes["user_notes"]:
            # --- Tampilkan Daftar Kategori sebagai Navigasi ---
            st.subheader("Daftar Kategori Anda:")
            col_idx = 0
            cols = st.columns(4)
            user_categories = list(notes["user_notes"].keys())
            
            if 'user_scroll_to_category' not in st.session_state:
                st.session_state.user_scroll_to_category = None

            for category_name in user_categories:
                with cols[col_idx]:
                    if st.button(category_name, key=f"user_nav_btn_{category_name}"):
                        st.session_state.user_selected_category_nav = category_name
                        st.session_state.user_scroll_to_category = category_name
                col_idx = (col_idx + 1) % 4
            
            st.markdown("---")

            # --- Tampilkan Catatan Berdasarkan Kategori ---
            target_category = st.session_state.get('user_selected_category_nav')

            if target_category and target_category in notes["user_notes"]:
                st.header(f"🌷 Kategori: {target_category}") # IKON YANG DIMINTA
                st.markdown(f"<a id='user_{target_category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                
                category_content = notes["user_notes"][target_category]
                if isinstance(category_content, dict):
                    display_section_content(category_content, level=1)
                elif isinstance(category_content, list):
                    for item in category_content:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(f"- {category_content}")
                
                # --- Tambahkan tombol Edit di bawah kategori yang dipilih ---
                if st.button(f"✏️ Edit Kategori '{target_category}'", key=f"edit_user_category_btn_{target_category}"):
                    st.session_state.editing_user_category = target_category
                    st.session_state.selected_category_nav = target_category # Pastikan tetap di kategori ini
                    st.rerun()

                st.markdown("---")
                st.subheader("Kategori Anda Lainnya:")
                for category, content in notes["user_notes"].items():
                    if category != target_category:
                        st.header(f"🌷 Kategori: {category}") # IKON YANG DIMINTA
                        st.markdown(f"<a id='user_{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                        if isinstance(content, dict):
                            display_section_content(content, level=1)
                        elif isinstance(content, list):
                            for item in content:
                                st.markdown(f"- {item}")
                        else:
                            st.markdown(f"- {content}")
                        # Tombol edit untuk kategori lain jika diinginkan, namun untuk menjaga fokus edit,
                        # kita akan membiarkan edit_user_notes_content menangani pemilihan kategori.
            else:
                # Jika tidak ada kategori yang dipilih, tampilkan semua user notes
                for category, content in notes["user_notes"].items():
                    st.header(f"🌷 Kategori: {category}") # IKON YANG DIMINTA
                    st.markdown(f"<a id='user_{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                    if isinstance(content, dict):
                        display_section_content(content, level=1)
                    elif isinstance(content, list):
                        for item in content:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown(f"- {content}")
                    # Tombol edit untuk kategori ini
                    if st.button(f"✏️ Edit Kategori '{category}'", key=f"edit_user_category_btn_all_{category}"):
                        st.session_state.editing_user_category = category
                        st.session_state.selected_category_nav = category # Set kategori agar tampil di atas
                        st.rerun()

            # --- Bagian Edit Catatan Pengguna ---
            st.markdown("---")
            st.subheader("📝 Edit Catatan Anda")
            
            # Memilih kategori yang akan diedit
            user_categories_for_edit = [""] + list(notes["user_notes"].keys())
            
            # Jika tombol edit ditekan sebelumnya, atur nilai default selectbox
            preselected_category = ""
            if 'editing_user_category' in st.session_state and st.session_state.editing_user_category:
                preselected_category = st.session_state.editing_user_category
            
            selected_category_to_edit = st.selectbox(
                "Pilih Kategori Anda untuk Diedit/Dihapus:", 
                user_categories_for_edit, 
                index=user_categories_for_edit.index(preselected_category) if preselected_category in user_categories_for_edit else 0,
                key="user_edit_category_select"
            )
            
            # Reset editing_user_category setelah digunakan
            if 'editing_user_category' in st.session_state:
                del st.session_state.editing_user_category

            if selected_category_to_edit:
                edit_user_notes_content(notes, selected_category_to_edit)
            else:
                st.info("Pilih kategori di atas untuk mulai mengedit atau menghapus catatannya.")

        else:
            st.info("Anda belum memiliki catatan tersimpan. Tambahkan catatan baru terlebih dahulu!")

    elif page_selection == "Tambah Catatan Baru": # SESUAI DENGAN NAMA DI SIDEBAR
        st.title("➕ Tambah Catatan Baru")

        # Menampilkan pesan konfirmasi yang disimpan di session_state
        if 'user_notes_message' in st.session_state and st.session_state.user_notes_message:
            if st.session_state.user_notes_message_type == 'success':
                st.success(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'warning':
                st.warning(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'info':
                st.info(st.session_state.user_notes_message)
            st.session_state.user_notes_message = "" # Reset pesan setelah ditampilkan
            st.session_state.user_notes_message_type = ""

        user_notes = load_json_data(USER_NOTES_FILE)
        
        # Pastikan struktur dasar ada
        if "user_notes" not in user_notes:
            user_notes["user_notes"] = {}

        existing_categories = list(user_notes["user_notes"].keys())
        
        # Pilihan Kategori
        category_choice = st.radio("Pilih Kategori:", ["Kategori yang Sudah Ada", "Buat Kategori Baru"], key="user_category_choice")

        selected_category = ""
        if category_choice == "Kategori yang Sudah Ada":
            if existing_categories:
                selected_category = st.selectbox("Pilih Kategori:", [""] + existing_categories, key="user_select_category")
            else:
                st.info("Belum ada kategori. Silakan buat kategori baru.")
                category_choice = "Buat Kategori Baru" # Paksa ke buat baru jika tidak ada kategori
        
        if category_choice == "Buat Kategori Baru":
            new_category_name = st.text_input("Nama Kategori Baru:", key="user_new_category_name")
            if new_category_name:
                selected_category = new_category_name

        # Input untuk Judul Catatan/Sub-Kategori
        note_title = st.text_input("Judul Catatan/Sub-Kategori:", key="user_note_title")
        
        # Pilihan tipe konten (List, String, atau Dictionary)
        content_type = st.radio("Tipe Konten Catatan:", ["Daftar Item", "Teks Tunggal", "Sub-Kategori (Nested Dictionary)"], key="user_content_type")

        note_content = None
        if content_type == "Daftar Item":
            note_content = st.text_area("Isi Catatan (satu item per baris):", height=150, key="user_note_list_content")
        elif content_type == "Teks Tunggal":
            note_content = st.text_area("Isi Catatan (teks tunggal):", height=100, key="user_note_text_content")
        else: # Sub-Kategori (Nested Dictionary)
            st.info("Untuk membuat sub-kategori (nested dictionary), Anda hanya perlu memberikan judul. Konten akan dibuat sebagai dictionary kosong dan Anda bisa mengisinya nanti melalui fitur edit.")
            note_content = {} # Inisialisasi sebagai dictionary kosong

        if st.button("Simpan Catatan Baru", key="save_new_user_note"):
            if selected_category and note_title:
                # Inisialisasi kategori jika baru
                if selected_category not in user_notes["user_notes"]:
                    user_notes["user_notes"][selected_category] = {} # Awalnya sebagai dict untuk sub-kategori
                
                # Menambahkan atau memperbarui konten
                if content_type == "Daftar Item":
                    items = [item.strip() for item in (note_content or "").split('\n') if item.strip()]
                    user_notes["user_notes"][selected_category][note_title] = items
                elif content_type == "Teks Tunggal":
                    user_notes["user_notes"][selected_category][note_title] = (note_content or "").strip()
                else: # Sub-Kategori (Nested Dictionary)
                    # Jika judul catatan sudah ada dan itu dictionary, gabungkan. Jika tidak, timpa.
                    if note_title in user_notes["user_notes"][selected_category] and isinstance(user_notes["user_notes"][selected_category][note_title], dict):
                        st.session_state.user_notes_message = f"Judul '{note_title}' sudah ada sebagai sub-kategori di '{selected_category}'. Catatan baru tidak ditambahkan. Silakan edit yang sudah ada."
                        st.session_state.user_notes_message_type = 'warning'
                        st.rerun()
                    else:
                        user_notes["user_notes"][selected_category][note_title] = {} # Buat dictionary kosong
                
                save_json_data(user_notes, USER_NOTES_FILE)
                st.session_state.user_notes_message = f"Catatan '{note_title}' berhasil ditambahkan ke kategori '{selected_category}'!"
                st.session_state.user_notes_message_type = 'success'
                st.rerun() # Rerun untuk membersihkan form dan menampilkan pesan
            else:
                st.session_state.user_notes_message = "Harap isi Nama Kategori dan Judul Catatan."
                st.session_state.user_notes_message_type = 'warning'
                st.rerun() # Rerun untuk menampilkan warning

# Menjalankan aplikasi
if __name__ == "__main__":
    main()
