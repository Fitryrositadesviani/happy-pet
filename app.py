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
    .sub-category-title {{
        font-weight: bold;
        font-size: 1.2em; /* Sekitar 2 tingkat lebih besar dari teks biasa (1em) */
        margin-bottom: 0;
        padding-bottom: 0;
        display: inline-block; /* Agar tombol bisa di samping */
        margin-right: 10px; /* Jarak antara judul dan tombol */
    }}

    .sub-category-item {{
        margin-left: 20px;
        margin-top: 0;
        margin-bottom: 0;
        display: flex; /* Menggunakan flexbox untuk item dan tombol */
        align-items: center; /* Pusatkan secara vertikal */
        justify-content: space-between; /* Dorong item dan tombol ke ujung */
    }}

    .sub-category-item-text {{
        flex-grow: 1; /* Biarkan teks mengambil ruang yang tersedia */
    }}

    .note-buttons {{
        display: flex;
        gap: 5px; /* Jarak antar tombol edit/hapus */
    }}

    /* Styling untuk Background Kategori */
    .category-card {{
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
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
def display_section_content(content_dict, level, is_user_notes=False, category_name=None):
    """Fungsi pembantu untuk menampilkan konten dictionary secara rekursif, dengan tombol edit/hapus untuk catatan pengguna."""
    for key, value in content_dict.items():
        if is_user_notes:
            st.markdown(f"<div class='sub-category-item'>", unsafe_allow_html=True)
            st.markdown(f"<p class='sub-category-title sub-category-item-text'>{key}:</p>", unsafe_allow_html=True)
            
            # Tombol Edit dan Hapus untuk sub-kategori
            with st.container():
                cols = st.columns([0.1, 0.1])
                with cols[0]:
                    if st.button("Edit", key=f"edit_sub_btn_{category_name}_{key}", help=f"Edit sub-kategori '{key}'"):
                        st.session_state.edit_item = {'category': category_name, 'sub_category': key, 'type': 'sub_category'}
                        st.session_state.current_page = "Catatan Anda" # Pastikan tetap di halaman yang sama
                        st.experimental_rerun()
                with cols[1]:
                    if st.button("Hapus", key=f"delete_sub_btn_{category_name}_{key}", help=f"Hapus sub-kategori '{key}'"):
                        st.session_state.delete_item = {'category': category_name, 'sub_category': key, 'type': 'sub_category'}
                        st.session_state.current_page = "Catatan Anda"
                        st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True) # Tutup sub-category-item untuk judul sub-kategori
        else:
            st.markdown(f"<p class='sub-category-title'>{key}:</p>", unsafe_allow_html=True)

        if isinstance(value, list):
            for idx, item in enumerate(value):
                if is_user_notes:
                    st.markdown(f"<div class='sub-category-item'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='sub-category-item-text'>- {item}</p>", unsafe_allow_html=True)
                    with st.container():
                        cols = st.columns([0.1, 0.1])
                        with cols[0]:
                            if st.button("Edit", key=f"edit_list_item_btn_{category_name}_{key}_{idx}", help=f"Edit item '{item}'"):
                                st.session_state.edit_item = {'category': category_name, 'sub_category': key, 'index': idx, 'value': item, 'type': 'list_item'}
                                st.session_state.current_page = "Catatan Anda"
                                st.experimental_rerun()
                        with cols[1]:
                            if st.button("Hapus", key=f"delete_list_item_btn_{category_name}_{key}_{idx}", help=f"Hapus item '{item}'"):
                                st.session_state.delete_item = {'category': category_name, 'sub_category': key, 'index': idx, 'type': 'list_item'}
                                st.session_state.current_page = "Catatan Anda"
                                st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='sub-category-item'>- {item}</p>", unsafe_allow_html=True)
            st.markdown("")
        elif isinstance(value, dict):
            st.markdown(f"<div style='margin-left: 20px;'>", unsafe_allow_html=True)
            display_section_content(value, level + 1, is_user_notes, category_name=category_name)
            st.markdown(f"</div>", unsafe_allow_html=True)
        else: # Untuk nilai string tunggal
            if is_user_notes:
                st.markdown(f"<div class='sub-category-item'>", unsafe_allow_html=True)
                st.markdown(f"<p class='sub-category-item-text'>{value}</p>", unsafe_allow_html=True)
                with st.container():
                    cols = st.columns([0.1, 0.1])
                    with cols[0]:
                        if st.button("Edit", key=f"edit_single_item_btn_{category_name}_{key}", help=f"Edit catatan '{key}'"):
                            st.session_state.edit_item = {'category': category_name, 'sub_category': key, 'value': value, 'type': 'single_string'}
                            st.session_state.current_page = "Catatan Anda"
                            st.experimental_rerun()
                    with cols[1]:
                        if st.button("Hapus", key=f"delete_single_item_btn_{category_name}_{key}", help=f"Hapus catatan '{key}'"):
                            st.session_state.delete_item = {'category': category_name, 'sub_category': key, 'type': 'single_string'}
                            st.session_state.current_page = "Catatan Anda"
                            st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='sub-category-item'>{value}</p>", unsafe_allow_html=True)
        st.markdown("")

def display_notes_data(notes_data_to_display, selected_category_to_show=None):
    """Menampilkan data catatan yang sudah ada dalam format rapi."""
    st.subheader("Daftar Kategori:")
    col_idx = 0
    cols = st.columns(4)
    
    if 'scroll_to_category' not in st.session_state:
        st.session_state.scroll_to_category = None

    for category_name in notes_data_to_display.keys():
        with cols[col_idx]:
            if st.button(category_name, key=f"nav_btn_{category_name}"):
                st.session_state.selected_category_nav = category_name
                st.session_state.scroll_to_category = category_name
                st.experimental_rerun()

        col_idx = (col_idx + 1) % 4
    
    st.markdown("---")

    if st.session_state.get('selected_category_nav'):
        target_category = st.session_state.selected_category_nav
        if target_category in notes_data_to_display:
            content = notes_data_to_display[target_category]
            bg_color = CATEGORY_COLORS.get(target_category, SECONDARY_BACKGROUND_COLOR)

            st.markdown(f"<a id='{target_category.replace(' ', '_')}'></a>", unsafe_allow_html=True)

            st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
            st.header(f"🌷 Kategori: {target_category}")
            if isinstance(content, dict):
                display_section_content(content, level=1)
            elif isinstance(content, list):
                for item in content:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"- {content}")
            st.markdown(f"</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Kategori Lainnya:")
            
            for category, content in notes_data_to_display.items():
                if category != target_category:
                    bg_color = CATEGORY_COLORS.get(category, SECONDARY_BACKGROUND_COLOR)
                    st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
                    st.header(f"🌷 Kategori: {category}")
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
        for category, content in notes_data_to_display.items():
            bg_color = CATEGORY_COLORS.get(category, SECONDARY_BACKGROUND_COLOR)

            st.markdown(f"<a id='{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)

            st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
            st.header(f"🌷 {category}")

            if isinstance(content, dict):
                display_section_content(content, level=1)
            elif isinstance(content, list):
                for item in content:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"- {content}")
            st.markdown(f"</div>", unsafe_allow_html=True)

    if st.session_state.scroll_to_category:
        category_id = st.session_state.scroll_to_category.replace(' ', '_')
        st.markdown(f"""
            <script>
                document.getElementById('{category_id}').scrollIntoView({{behavior: 'smooth'}});
            </script>
        """, unsafe_allow_html=True)
        st.session_state.scroll_to_category = None

# --- Fungsi untuk Mengelola Catatan Default (Admin Page) ---
def edit_default_notes_page():
    st.title("⚙️ Edit Catatan Utama")
    st.warning("Halaman ini ditujukan untuk mengedit catatan utama. Perubahan di sini akan mempengaruhi semua pengguna.")

    if 'edit_default_message' in st.session_state and st.session_state.edit_default_message:
        if st.session_state.edit_default_message_type == 'success':
            st.success(st.session_state.edit_default_message)
        elif st.session_state.edit_default_message_type == 'warning':
            st.warning(st.session_state.edit_default_message)
        elif st.session_state.edit_default_message_type == 'info':
            st.info(st.session_state.edit_default_message)
        st.session_state.edit_default_message = ""
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
        new_category_content = {}

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
                else:
                    default_notes[new_category_name] = {}

                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.session_state.edit_default_message = f"Kategori '{new_category_name}' berhasil ditambahkan!"
                st.session_state.edit_default_message_type = 'success'
            st.rerun()
        else:
            st.session_state.edit_default_message = "Nama kategori tidak boleh kosong."
            st.session_state.edit_default_message_type = 'warning'
            st.rerun()

    # --- Edit Konten yang Ada ---
    st.markdown("---")
    st.subheader("Edit Konten yang Ada")
    categories = list(default_notes.keys())
    selected_category = st.selectbox("Pilih Kategori:", [""] + categories, key="edit_default_category_select")

    if selected_category:
        current_category_content = default_notes[selected_category]

        st.markdown(f"**Mengedit Kategori: {selected_category}**")

        if isinstance(current_category_content, dict):
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
                        st.experimental_rerun()

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
                    st.rerun()

            st.markdown("---")
            st.subheader("Hapus Sub-Kategori")
            sub_categories_to_delete = list(current_category_content.keys())
            sub_category_to_delete = st.selectbox("Pilih Sub-Kategori yang akan dihapus:", [""] + sub_categories_to_delete, key="delete_default_sub_category_select")
            
            if sub_category_to_delete:
                confirm_sub = st.checkbox(f"Saya yakin ingin menghapus sub-kategori '{sub_category_to_delete}'", key="confirm_delete_default_sub_category")
                if st.button(f"Hapus Sub-Kategori '{sub_category_to_delete}'", key="delete_default_sub_category_button"):
                    if confirm_sub:
                        del default_notes[selected_category][sub_category_to_delete]
                        save_json_data(default_notes, DEFAULT_NOTES_FILE)
                        st.session_state.edit_default_message = f"Sub-kategori '{sub_category_to_delete}' berhasil dihapus."
                        st.session_state.edit_default_message_type = 'success'
                        st.rerun()
                    else:
                        st.session_state.edit_default_message = "Centang kotak konfirmasi untuk menghapus."
                        st.session_state.edit_default_message_type = 'info'
                        st.experimental_rerun()


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
    categories_to_delete_default = list(default_notes.keys())
    category_to_delete = st.selectbox("Pilih Kategori yang akan dihapus:", [""] + categories_to_delete_default, key="delete_default_main_category_select")
    
    if category_to_delete:
        confirm = st.checkbox(f"Saya yakin ingin menghapus kategori '{category_to_delete}'", key="confirm_delete_default_main_category")
        if st.button(f"Hapus Kategori '{category_to_delete}'", key="delete_default_main_category_button"):
            if confirm:
                del default_notes[category_to_delete]
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.session_state.edit_default_message = f"Kategori '{category_to_delete}' berhasil dihapus."
                st.session_state.edit_default_message_type = 'success'
                st.rerun()
            else:
                st.session_state.edit_default_message = "Centang kotak konfirmasi untuk menghapus."
                st.session_state.edit_default_message_type = 'info'
                st.experimental_rerun()

# --- Fungsi untuk Mengelola Catatan Pengguna ---
def add_new_user_category(user_notes):
    st.markdown("---")
    st.subheader("Tambah Kategori Baru Anda")
    new_category_name = st.text_input("Nama Kategori Baru:", key="new_user_category_name_input")
    new_category_type = st.radio("Tipe Konten Kategori Baru:", ["Teks Tunggal", "Daftar Item", "Sub-Kategori (Nested Dictionary)"], key="new_user_category_type_radio")

    new_category_content_input = None
    if new_category_type == "Daftar Item":
        new_category_content_input = st.text_area("Isi Daftar Item (satu item per baris):", height=100, key="new_user_category_list_content")
    elif new_category_type == "Teks Tunggal":
        new_category_content_input = st.text_input("Isi Teks Tunggal:", key="new_user_category_text_content")
    else: # Sub-Kategori (Nested Dictionary)
        st.info("Untuk menambah sub-kategori kosong, masukkan nama kategori. Anda dapat menambahkan sub-item nanti dengan mengedit kategori.")
        new_category_content_input = {}

    if st.button("Tambah Kategori Baru", key="add_new_user_category_button_final"):
        if new_category_name:
            if new_category_name in user_notes:
                st.session_state.user_notes_message = f"Kategori '{new_category_name}' sudah ada. Silakan pilih nama lain atau edit yang sudah ada."
                st.session_state.user_notes_message_type = 'warning'
            else:
                if new_category_type == "Daftar Item":
                    items = [item.strip() for item in (new_category_content_input or "").split('\n') if item.strip()]
                    user_notes[new_category_name] = items
                elif new_category_type == "Teks Tunggal":
                    user_notes[new_category_name] = (new_category_content_input or "").strip()
                else:
                    user_notes[new_category_name] = {}
                
                save_json_data({"user_notes": user_notes}, USER_NOTES_FILE)
                st.session_state.user_notes_message = f"Kategori '{new_category_name}' berhasil ditambahkan!"
                st.session_state.user_notes_message_type = 'success'
                st.experimental_rerun()
        else:
            st.session_state.user_notes_message = "Nama kategori tidak boleh kosong."
            st.session_state.user_notes_message_type = 'warning'
            st.experimental_rerun()


def edit_user_note_modal(user_notes):
    if 'edit_item' in st.session_state and st.session_state.edit_item:
        item_to_edit = st.session_state.edit_item
        category = item_to_edit['category']
        sub_category = item_to_edit.get('sub_category')
        item_type = item_to_edit['type']
        
        st.subheader(f"Edit Catatan Anda: {category} > {sub_category or ''}")

        if item_type == 'sub_category':
            current_content = user_notes[category][sub_category]
            if isinstance(current_content, list):
                edited_value = st.text_area("Edit isi (satu item per baris):", value="\n".join(current_content), height=150, key="edit_modal_textarea")
                updated_content = [item.strip() for item in edited_value.split('\n') if item.strip()]
            elif isinstance(current_content, str):
                edited_value = st.text_input("Edit isi:", value=current_content, key="edit_modal_textinput")
                updated_content = edited_value.strip()
            elif isinstance(current_content, dict):
                st.info("Untuk mengedit sub-kategori bersarang, gunakan editor JSON di bawah.")
                edited_value = st.text_area("Edit JSON:", value=json.dumps(current_content, indent=4, ensure_ascii=False), height=200, key="edit_modal_jsonarea")
                try:
                    updated_content = json.loads(edited_value)
                except json.JSONDecodeError:
                    st.error("Format JSON tidak valid.")
                    updated_content = None # Menandakan error
        
        elif item_type == 'list_item':
            current_value = item_to_edit['value']
            edited_value = st.text_input("Edit item daftar:", value=current_value, key="edit_list_item_modal_textinput")
            updated_content = edited_value.strip()

        elif item_type == 'single_string':
            current_value = item_to_edit['value']
            edited_value = st.text_input("Edit catatan:", value=current_value, key="edit_single_string_modal_textinput")
            updated_content = edited_value.strip()
        
        else:
            updated_content = None

        if updated_content is not None:
            if st.button("Simpan Perubahan", key="save_edit_modal_button"):
                if item_type == 'sub_category':
                    if isinstance(user_notes[category], dict): # Pastikan ini adalah dictionary
                        user_notes[category][sub_category] = updated_content
                    else:
                        st.error("Struktur data tidak sesuai untuk pengeditan sub-kategori ini.")
                        return
                elif item_type == 'list_item':
                    if isinstance(user_notes[category][sub_category], list): # Pastikan ini adalah list
                        user_notes[category][sub_category][item_to_edit['index']] = updated_content
                    else:
                        st.error("Struktur data tidak sesuai untuk pengeditan item daftar ini.")
                        return
                elif item_type == 'single_string':
                    if isinstance(user_notes[category], dict): # Ini adalah sub-kategori (nested)
                        user_notes[category][sub_category] = updated_content
                    else: # Ini adalah kategori langsung
                        user_notes[category] = updated_content

                save_json_data({"user_notes": user_notes}, USER_NOTES_FILE)
                st.session_state.user_notes_message = "Catatan berhasil diperbarui!"
                st.session_state.user_notes_message_type = 'success'
                st.session_state.edit_item = None # Hapus data edit
                st.experimental_rerun()
        
        if st.button("Batal", key="cancel_edit_modal_button"):
            st.session_state.edit_item = None
            st.experimental_rerun()


def delete_user_note_confirmation(user_notes):
    if 'delete_item' in st.session_state and st.session_state.delete_item:
        item_to_delete = st.session_state.delete_item
        category = item_to_delete['category']
        sub_category = item_to_delete.get('sub_category')
        item_type = item_to_delete['type']
        index = item_to_delete.get('index')

        st.warning(f"Apakah Anda yakin ingin menghapus {'item' if item_type == 'list_item' else 'sub-kategori' if item_type == 'sub_category' else 'catatan'} ini?")
        st.markdown(f"**Kategori:** {category}")
        if sub_category:
            st.markdown(f"**Sub-Kategori:** {sub_category}")
        if item_type == 'list_item' and index is not None:
            st.markdown(f"**Item yang akan dihapus:** {user_notes[category][sub_category][index]}")
        elif item_type == 'single_string' and sub_category:
            st.markdown(f"**Catatan yang akan dihapus:** {user_notes[category][sub_category]}")
        elif item_type == 'sub_category':
            st.markdown(f"**Sub-Kategori yang akan dihapus:** {sub_category}")


        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ya, Hapus", key="confirm_delete_user_note_button"):
                if item_type == 'list_item':
                    if isinstance(user_notes[category][sub_category], list):
                        del user_notes[category][sub_category][index]
                        # Hapus sub-kategori jika kosong setelah penghapusan item terakhir
                        if not user_notes[category][sub_category]:
                            del user_notes[category][sub_category]
                            st.session_state.user_notes_message = f"Item berhasil dihapus dan sub-kategori '{sub_category}' dihapus karena kosong."
                    else:
                        st.error("Struktur data tidak sesuai untuk penghapusan item daftar ini.")
                        st.session_state.user_notes_message = "Gagal menghapus item: Struktur data tidak sesuai."

                elif item_type == 'single_string' or item_type == 'sub_category':
                    if isinstance(user_notes[category], dict):
                        del user_notes[category][sub_category]
                    else:
                        del user_notes[category] # Jika kategori langsung berisi string
                    st.session_state.user_notes_message = f"Catatan '{sub_category or category}' berhasil dihapus."

                save_json_data({"user_notes": user_notes}, USER_NOTES_FILE)
                st.session_state.user_notes_message_type = 'success'
                st.session_state.delete_item = None # Hapus data penghapusan
                st.experimental_rerun()
        with col2:
            if st.button("Batal", key="cancel_delete_user_note_button"):
                st.session_state.delete_item = None
                st.experimental_rerun()


def display_user_notes_page():
    st.title("🍯 Catatan Anda")

    # Inisialisasi user_notes_message di session_state
    if 'user_notes_message' not in st.session_state:
        st.session_state.user_notes_message = ""
        st.session_state.user_notes_message_type = ""

    # Menampilkan pesan konfirmasi
    if st.session_state.user_notes_message:
        if st.session_state.user_notes_message_type == 'success':
            st.success(st.session_state.user_notes_message)
        elif st.session_state.user_notes_message_type == 'warning':
            st.warning(st.session_state.user_notes_message)
        elif st.session_state.user_notes_message_type == 'info':
            st.info(st.session_state.user_notes_message)
        st.session_state.user_notes_message = "" # Reset pesan setelah ditampilkan
        st.session_state.user_notes_message_type = ""

    user_notes_data_container = load_json_data(USER_NOTES_FILE)
    user_notes = user_notes_data_container.get("user_notes", {})

    if not user_notes:
        st.info("Anda belum memiliki catatan. Silakan tambahkan satu di bawah!")

    # Tampilkan catatan pengguna dengan tombol edit dan hapus
    st.subheader("Berikut adalah catatan yang Anda simpan:")
    
    # Check if we are in edit or delete confirmation mode
    if 'edit_item' in st.session_state and st.session_state.edit_item:
        edit_user_note_modal(user_notes)
    elif 'delete_item' in st.session_state and st.session_state.delete_item:
        delete_user_note_confirmation(user_notes)
    else:
        for category, content in user_notes.items():
            bg_color = CATEGORY_COLORS.get(category, SECONDARY_BACKGROUND_COLOR)
            st.markdown(f"<div class='category-card' style='background-color: {bg_color};'>", unsafe_allow_html=True)
            
            # Judul kategori dan tombol "Hapus Kategori"
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.header(f"🗂️ {category}")
            with col2:
                if st.button("Hapus Kategori", key=f"delete_category_{category}"):
                    st.session_state.delete_item = {'category': category, 'type': 'category'}
                    st.experimental_rerun()

            if isinstance(content, dict):
                display_section_content(content, level=1, is_user_notes=True, category_name=category)
            elif isinstance(content, list):
                for idx, item in enumerate(content):
                    st.markdown(f"<div class='sub-category-item'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='sub-category-item-text'>- {item}</p>", unsafe_allow_html=True)
                    with st.container():
                        cols = st.columns([0.1, 0.1])
                        with cols[0]:
                            if st.button("Edit", key=f"edit_top_list_item_btn_{category}_{idx}", help=f"Edit item '{item}'"):
                                st.session_state.edit_item = {'category': category, 'index': idx, 'value': item, 'type': 'list_item_top_level'}
                                st.experimental_rerun()
                        with cols[1]:
                            if st.button("Hapus", key=f"delete_top_list_item_btn_{category}_{idx}", help=f"Hapus item '{item}'"):
                                st.session_state.delete_item = {'category': category, 'index': idx, 'type': 'list_item_top_level'}
                                st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            else: # String tunggal sebagai isi kategori
                st.markdown(f"<div class='sub-category-item'>", unsafe_allow_html=True)
                st.markdown(f"<p class='sub-category-item-text'>{content}</p>", unsafe_allow_html=True)
                with st.container():
                    cols = st.columns([0.1, 0.1])
                    with cols[0]:
                        if st.button("Edit", key=f"edit_top_string_item_btn_{category}", help=f"Edit catatan '{category}'"):
                            st.session_state.edit_item = {'category': category, 'value': content, 'type': 'single_string_top_level'}
                            st.experimental_rerun()
                    with cols[1]:
                        if st.button("Hapus", key=f"delete_top_string_item_btn_{category}", help=f"Hapus catatan '{category}'"):
                            st.session_state.delete_item = {'category': category, 'type': 'single_string_top_level'}
                            st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # Tombol "Tambah" di akhir setiap kategori
            st.markdown("<br>", unsafe_allow_html=True) # Tambahkan sedikit ruang
            if isinstance(content, dict): # Hanya tambahkan sub-kategori jika kategorinya adalah dict
                if st.button(f"Tambah Catatan di '{category}'", key=f"add_note_to_category_{category}"):
                    st.session_state.add_note_to_category = category
                    st.experimental_rerun()
            st.markdown(f"</div>", unsafe_allow_html=True)
            
            if st.session_state.get('add_note_to_category') == category:
                with st.expander(f"Tambahkan Catatan Baru ke '{category}'"):
                    new_sub_category_name = st.text_input("Nama Catatan/Sub-Kategori Baru:", key=f"new_sub_name_{category}")
                    new_sub_category_type = st.radio("Tipe Konten:", ["Teks Tunggal", "Daftar Item"], key=f"new_sub_type_{category}")
                    new_sub_category_content_input = st.text_area("Isi Catatan Baru (pisahkan dengan baris baru jika daftar):", height=100, key=f"new_sub_content_{category}")

                    if st.button("Simpan Catatan Baru", key=f"save_new_sub_note_{category}"):
                        if new_sub_category_name:
                            if new_sub_category_name in user_notes[category]:
                                st.session_state.user_notes_message = f"Catatan/Sub-Kategori '{new_sub_category_name}' sudah ada di '{category}'."
                                st.session_state.user_notes_message_type = 'warning'
                            else:
                                if new_sub_category_type == "Daftar Item":
                                    items = [item.strip() for item in (new_sub_category_content_input or "").split('\n') if item.strip()]
                                    user_notes[category][new_sub_category_name] = items
                                else:
                                    user_notes[category][new_sub_category_name] = (new_sub_category_content_input or "").strip()

                                save_json_data({"user_notes": user_notes}, USER_NOTES_FILE)
                                st.session_state.user_notes_message = f"Catatan '{new_sub_category_name}' berhasil ditambahkan ke '{category}'!"
                                st.session_state.user_notes_message_type = 'success'
                                st.session_state.add_note_to_category = None # Reset
                                st.experimental_rerun()
                        else:
                            st.session_state.user_notes_message = "Nama catatan tidak boleh kosong."
                            st.session_state.user_notes_message_type = 'warning'
                        st.experimental_rerun()
                    if st.button("Batal", key=f"cancel_new_sub_note_{category}"):
                        st.session_state.add_note_to_category = None
                        st.experimental_rerun()
        
        # Tambahkan tombol "Tambah Kategori Baru Anda" di paling bawah
        st.markdown("---")
        add_new_user_category(user_notes)


# --- Halaman Utama Aplikasi ---
def main():
    st.sidebar.title("Navigasi Utama")
    
    # Inisialisasi 'current_page' di session_state jika belum ada
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Lihat Catatan Utama"
    
    # Navigasi Sidebar
    if st.sidebar.button("Lihat Catatan Utama"):
        st.session_state.current_page = "Lihat Catatan Utama"
        st.session_state.selected_category_nav = None # Reset kategori yang dipilih saat pindah halaman
        st.session_state.scroll_to_category = None
        st.experimental_rerun()

    if st.sidebar.button("Catatan Anda"):
        st.session_state.current_page = "Catatan Anda"
        st.session_state.selected_category_nav = None # Reset kategori yang dipilih saat pindah halaman
        st.session_state.scroll_to_category = None
        st.experimental_rerun()
        
    if st.sidebar.button("Edit Catatan Utama (Admin)"):
        st.session_state.current_page = "Edit Catatan Utama (Admin)"
        st.session_state.selected_category_nav = None # Reset kategori yang dipilih saat pindah halaman
        st.session_state.scroll_to_category = None
        st.experimental_rerun()

    # Tampilkan halaman berdasarkan pilihan di sidebar
    if st.session_state.current_page == "Lihat Catatan Utama":
        st.title("📔 Catatan Happy Pet")
        default_notes = load_json_data(DEFAULT_NOTES_FILE)
        display_notes_data(default_notes)
    elif st.session_state.current_page == "Catatan Anda":
        display_user_notes_page()
    elif st.session_state.current_page == "Edit Catatan Utama (Admin)":
        edit_default_notes_page()

if __name__ == '__main__':
    # Pastikan file JSON ada, jika tidak, buat dengan struktur dasar
    if not os.path.exists(USER_NOTES_FILE):
        with open(USER_NOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"user_notes": {
                "Informasi tambahan": {
                    "yang bisa terbang": ["Rangkong yang tidak bisa terbang", "burung unta", "takahe", "kakapo"],
                    "kandungan air dalam tubuh manusia": "70%",
                    "banyaknya tulang yang ada di tubuh manusia": "206"
                },
                "happy pet": {
                    "yang tidak ada di rumah mojo": "TV"
                }
            }}, f, indent=4, ensure_ascii=False)
            
    if not os.path.exists(DEFAULT_NOTES_FILE):
        with open(DEFAULT_NOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "Kelompok Elemen": {
                    "Kayu": ["Harimau", "Kelinci"],
                    "Air": ["Tikus", "Babi"],
                    "Api": ["Ular"]
                },
                "Elemental Groups": {
                    "Wood": ["Tiger", "Rabbit"],
                    "Water": ["Rat", "Pig"],
                    "Fire": ["Snake", "Horse"],
                    "Metal": ["Monkey", "Rooster"],
                    "Earth": ["Ox", "Dragon", "Goat/Sheep", "Dog"]
                },
                "Compatibility Groups": {
                    "Rat": ["Dragon", "Monkey"],
                    "Ox": ["Snake", "Rooster"],
                    "Tiger": ["Horse", "Dog"],
                    "Rabbit": ["Goat/Sheep", "Pig"]
                }
            }, f, indent=4, ensure_ascii=False)

    main()
