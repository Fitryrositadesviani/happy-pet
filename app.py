import streamlit as st
import json
import os

# --- Konfigurasi Aplikasi (Lambang, Judul, Tema) ---
st.set_page_config(
    page_title="Catatan Ceria Happy Pet",
    page_icon="🐾", # Lambang baru
    layout="wide",
    initial_sidebar_state="expanded",
    # Tema warna yang lebih ceria
    # Anda bisa coba warna lain di sini: https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
    menu_items={
        'Get Help': 'https://www.google.com/search?q=streamlit+documentation',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# Ini adalah aplikasi catatan ceria untuk Happy Pet!"
    }
)

# Menentukan warna kustom untuk tema yang lebih ceria
# Warna pastel atau cerah biasanya memberikan kesan ceria
# Pastikan kontras teks cukup jelas
PRIMARY_COLOR = "#FFD1DC" # Pink Pastel
BACKGROUND_COLOR = "#F0F2F6" # Abu-abu sangat terang
SECONDARY_BACKGROUND_COLOR = "#FFFFFF" # Putih
TEXT_COLOR = "#333333" # Abu-abu gelap untuk keterbacaan
FONT = "sans-serif"

st.markdown(f"""
    <style>
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
    h3 {{
        font-size: 1.5em; /* 2 tingkat lebih besar dari default p (1em) */
    }}
    h4 {{
        font-size: 1.25em; /* 1 tingkat lebih besar dari default p (1em) */
    }}
    /* Penyesuaian khusus untuk sub-sub-kategori agar tidak terlalu besar */
    .stMarkdown h3 + h4 {{ /* Jika h4 mengikuti h3 */
        font-size: 1.2em; /* Sedikit lebih kecil dari h4 biasa */
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
    with os.path.dirname(file_path):
        pass # Pastikan direktori ada (untuk Streamlit Cloud biasanya sudah ada)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Fungsi untuk Menampilkan Catatan ---
def display_section(title, items, level=0):
    """Fungsi pembantu untuk menampilkan bagian dengan bullet points."""
    # Menggunakan header yang berbeda berdasarkan level untuk kontrol ukuran font
    if level == 0:
        st.subheader(title) # Default subheader
    elif level == 1:
        st.markdown(f"#### {title}") # Satu tingkat lebih kecil
    elif level == 2:
        st.markdown(f"##### {title}") # Dua tingkat lebih kecil

    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, dict):
        for key, value in items.items():
            if isinstance(value, (list, dict)):
                st.markdown(f"- **{key}**:")
                # Rekursif untuk sub-sub-kategori
                display_section("", value, level=level + 1)
            else:
                st.markdown(f"- **{key}**: {value}")
    else:
        st.markdown(f"- {items}") # Menggunakan markdown untuk konsistensi

def display_notes_data(notes_data_to_display):
    """Menampilkan data catatan yang sudah ada dalam format rapi."""
    st.title("📝 Catatan Happy Pet & Pengetahuan Umum")

    for category, content in notes_data_to_display.items():
        st.header(f"📍 {category}")
        if isinstance(content, dict):
            for sub_category, items in content.items():
                display_section(f"**{sub_category}**", items, level=1) # Sub-kategori
        elif isinstance(content, list):
            display_section(f"**{category}**", content, level=0) # Jika kategori langsung list
        else:
            st.markdown(f"- {content}") # Jika kategori langsung string

# --- Fungsi untuk Mengelola Catatan Default ---
def edit_default_notes_page():
    st.title("⚙️ Edit Catatan Default Happy Pet")
    st.warning("Halaman ini ditujukan untuk mengedit catatan default. Perubahan di sini akan mempengaruhi semua pengguna.")

    default_notes = load_json_data(DEFAULT_NOTES_FILE)

    if not default_notes:
        st.error("Tidak dapat memuat catatan default untuk diedit. Pastikan file 'default_notes.json' ada dan formatnya benar.")
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
            if new_category_type == "Daftar Item":
                items = [item.strip() for item in (new_category_content or "").split('\n') if item.strip()]
                default_notes[new_category_name] = items
            elif new_category_type == "Teks Tunggal":
                default_notes[new_category_name] = (new_category_content or "").strip()
            else: # Sub-Kategori (Nested Dictionary)
                default_notes[new_category_name] = {}

            save_json_data(default_notes, DEFAULT_NOTES_FILE)
            st.success(f"Kategori '{new_category_name}' berhasil ditambahkan!")
            st.experimental_rerun()
        else:
            st.warning("Nama kategori tidak boleh kosong.")

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
                        st.success("Sub-kategori berhasil diperbarui!")
                        st.experimental_rerun()
                elif isinstance(current_sub_content, str):
                    edited_str_value = st.text_input(
                        "Edit nilai:",
                        value=current_sub_content,
                        key="edit_default_sub_string_input"
                    )
                    if st.button("Simpan Perubahan Sub-Kategori", key="save_sub_category_string_btn"):
                        default_notes[selected_category][selected_sub_category] = edited_str_value
                        save_json_data(default_notes, DEFAULT_NOTES_FILE)
                        st.success("Sub-kategori berhasil diperbarui!")
                        st.experimental_rerun()
                elif isinstance(current_sub_content, dict):
                    st.info("Untuk mengedit lebih dalam (nested dictionary), Anda perlu memanipulasi JSON secara manual atau ini akan menjadi sangat kompleks.")
                    json_str = st.text_area("Edit JSON Sub-Kategori:", value=json.dumps(current_sub_content, indent=4, ensure_ascii=False), height=200, key="edit_nested_dict_area")
                    try:
                        updated_dict = json.loads(json_str)
                        if st.button("Simpan Perubahan JSON Sub-Kategori", key="save_nested_dict_btn"):
                            default_notes[selected_category][selected_sub_category] = updated_dict
                            save_json_data(default_notes, DEFAULT_NOTES_FILE)
                            st.success("Sub-kategori berhasil diperbarui dari JSON!")
                            st.experimental_rerun()
                    except json.JSONDecodeError:
                        st.error("Format JSON tidak valid.")
            
            st.markdown("---")
            st.subheader("Tambahkan Sub-Kategori Baru")
            new_sub_category_name = st.text_input("Nama Sub-Kategori Baru:", key="new_sub_category_name")
            new_sub_category_type = st.radio("Tipe Konten Sub-Kategori Baru:", ["Teks Tunggal", "Daftar Item"], key="new_sub_category_type")
            new_sub_category_content_input = st.text_area("Isi Sub-Kategori Baru (pisahkan dengan baris baru jika daftar):", height=100, key="new_sub_category_content_input")

            if st.button("Tambah Sub-Kategori Baru", key="add_new_sub_category_button"):
                if new_sub_category_name and selected_category:
                    if new_sub_category_type == "Daftar Item":
                        items = [item.strip() for item in (new_sub_category_content_input or "").split('\n') if item.strip()]
                        default_notes[selected_category][new_sub_category_name] = items
                    else: # Teks Tunggal
                        default_notes[selected_category][new_sub_category_name] = (new_sub_category_content_input or "").strip()
                    
                    save_json_data(default_notes, DEFAULT_NOTES_FILE)
                    st.success(f"Sub-kategori '{new_sub_category_name}' berhasil ditambahkan ke '{selected_category}'!")
                    st.experimental_rerun()
                else:
                    st.warning("Nama sub-kategori dan isi tidak boleh kosong.")

            st.markdown("---")
            st.subheader("Hapus Sub-Kategori")
            sub_category_to_delete = st.selectbox("Pilih Sub-Kategori yang akan dihapus:", [""] + sub_categories, key="delete_default_sub_category_select")
            if sub_category_to_delete and st.button(f"Hapus Sub-Kategori '{sub_category_to_delete}'", key="delete_default_sub_category_button"):
                confirm_sub = st.checkbox(f"Saya yakin ingin menghapus sub-kategori '{sub_category_to_delete}'", key="confirm_delete_default_sub_category")
                if confirm_sub:
                    del default_notes[selected_category][sub_category_to_delete]
                    save_json_data(default_notes, DEFAULT_NOTES_FILE)
                    st.success(f"Sub-kategori '{sub_category_to_delete}' berhasil dihapus.")
                    st.experimental_rerun()
                else:
                    st.info("Centang kotak konfirmasi untuk menghapus.")


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
                st.success("Catatan default berhasil diperbarui!")
                st.experimental_rerun()

        elif isinstance(current_category_content, str):
            edited_str_value = st.text_input(
                "Edit nilai:",
                value=current_category_content,
                key="edit_default_category_string_input"
            )
            if st.button("Simpan Perubahan Kategori", key="save_category_string_btn"):
                default_notes[selected_category] = edited_str_value
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.success("Catatan default berhasil diperbarui!")
                st.experimental_rerun()
        else:
            st.info("Tipe data tidak didukung untuk pengeditan langsung di sini (bukan daftar, teks, atau kamus).")
            st.text_area("Konten JSON mentah (untuk debugging/pengeditan manual):", json.dumps(current_category_content, indent=4, ensure_ascii=False), height=200, disabled=True)


    # --- Hapus Kategori dari Catatan Default ---
    st.markdown("---")
    st.subheader("Hapus Kategori dari Catatan Default")
    category_to_delete = st.selectbox("Pilih Kategori yang akan dihapus:", [""] + categories, key="delete_default_main_category_select")
    if category_to_delete and st.button(f"Hapus Kategori '{category_to_delete}'", key="delete_default_main_category_button"):
        confirm = st.checkbox(f"Saya yakin ingin menghapus kategori '{category_to_delete}'", key="confirm_delete_default_main_category")
        if confirm:
            del default_notes[category_to_delete]
            save_json_data(default_notes, DEFAULT_NOTES_FILE)
            st.success(f"Kategori '{category_to_delete}' berhasil dihapus.")
            st.experimental_rerun()
        else:
            st.info("Centang kotak konfirmasi untuk menghapus.")


# --- Fungsi Utama Aplikasi ---
def main():
    st.sidebar.title("Navigasi")
    page_selection = st.sidebar.radio("Pilih Halaman", ["Lihat Catatan Tersimpan", "Tambah Catatan Baru", "Catatan Default Happy Pet", "Edit Catatan Default"])

    if page_selection == "Catatan Default Happy Pet":
        default_notes = load_json_data(DEFAULT_NOTES_FILE)
        if default_notes:
            display_notes_data(default_notes)
        else:
            st.info("Tidak ada catatan default yang ditemukan atau ada kesalahan saat memuat.")

    elif page_selection == "Tambah Catatan Baru":
        st.title("➕ Tambah Catatan Baru")
        note_title = st.text_input("Judul Catatan")
        note_content = st.text_area("Isi Catatan Anda", height=200)

        if st.button("Simpan Catatan"):
            if note_title and note_content:
                notes = load_json_data(USER_NOTES_FILE)
                if "user_notes" not in notes:
                    notes["user_notes"] = {}
                notes["user_notes"][note_title] = note_content
                save_json_data(notes, USER_NOTES_FILE)
                st.success("Catatan berhasil disimpan!")
                st.write(f"**Judul:** {note_title}")
                st.write(f"**Isi:** {note_content}")
            else:
                st.warning("Judul dan isi catatan tidak boleh kosong.")

    elif page_selection == "Lihat Catatan Tersimpan":
        st.title("📚 Catatan Anda")
        notes = load_json_data(USER_NOTES_FILE)

        if "user_notes" in notes and notes["user_notes"]:
            st.write("Berikut adalah catatan yang Anda simpan:")
            # Tampilan catatan dengan opsi hapus
            for title, content in notes["user_notes"].items():
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.subheader(title)
                    st.write(content)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"Hapus '{title}'", key=f"delete_{title}"):
                        del notes["user_notes"][title]
                        save_json_data(notes, USER_NOTES_FILE)
                        st.experimental_rerun()

            # Bagian untuk mengedit catatan
            st.markdown("---")
            st.subheader("Edit Catatan (Pilih salah satu)")
            selected_note_to_edit = st.selectbox(
                "Pilih catatan untuk diedit:",
                [""] + list(notes["user_notes"].keys()),
                key="select_user_note_to_edit"
            )

            if selected_note_to_edit:
                if 'edited_user_title' not in st.session_state or st.session_state.edited_user_title != selected_note_to_edit:
                    st.session_state.edited_user_title = selected_note_to_edit
                    st.session_state.edited_user_content = notes["user_notes"][selected_note_to_edit]

                new_title = st.text_input("Judul Baru:", value=st.session_state.edited_user_title, key="edit_user_title_input")
                new_content = st.text_area("Isi Baru:", value=st.session_state.edited_user_content, height=200, key="edit_user_content_area")

                if st.button("Update Catatan", key="update_user_note_button"):
                    if new_title and new_content:
                        if new_title != st.session_state.edited_user_title:
                            del notes["user_notes"][st.session_state.edited_user_title]
                        notes["user_notes"][new_title] = new_content
                        save_json_data(notes, USER_NOTES_FILE)
                        st.success("Catatan berhasil diperbarui!")
                        if 'edited_user_title' in st.session_state:
                            del st.session_state.edited_user_title
                        if 'edited_user_content' in st.session_state:
                            del st.session_state.edited_user_content
                        st.experimental_rerun()
                    else:
                        st.warning("Judul dan isi catatan tidak boleh kosong.")
        else:
            st.info("Anda belum memiliki catatan yang disimpan.")

    elif page_selection == "Edit Catatan Default":
        edit_default_notes_page() # Panggil fungsi terpisah untuk halaman edit default

if __name__ == "__main__":
    main()
